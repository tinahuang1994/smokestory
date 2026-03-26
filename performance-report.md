# SmokeStory API — Performance & Reliability Audit Report

**Date:** 2026-03-20
**API Base URL:** https://smokestory.onrender.com
**Hosting:** Render free tier (auto-sleep after 15 min inactivity)

---

## TEST 1 — Sequential Response Times

| Endpoint | Measured Time | Threshold | Result |
|---|---|---|---|
| `GET /health` (cold) | **4.314s** | >1s = Critical | ❌ FAIL |
| `GET /health` (warm) | **1.076s** | >1s = Critical | ❌ FAIL (marginal) |
| `GET /map/pm25/06/20250109` | **2.730s** | >5s = Important, >10s = Critical | ✅ PASS |
| `GET /map/smoke/20250109` | **1.642s** | >5s = Important, >10s = Critical | ✅ PASS |
| `GET /map/fires/20250109` | **2.201s** | >5s = Important, >10s = Critical | ✅ PASS |
| `GET /county/06/Los%20Angeles/20250109` | **13.426s** | >15s = Important, >20s = Critical | ✅ PASS (marginal) |

### Observations
- **Map endpoints** (`/map/*`) are well within acceptable range at ~1.6–2.7s. Good performance.
- **County endpoint** at 13.4s is close to the Important threshold of 15s. Any increase due to cold starts, AI latency, or data growth could push it into the warning zone.
- **Health endpoint** is unexpectedly slow — see Cold Start findings below.

---

## TEST 2 — Concurrent Requests (3 simultaneous map calls)

| Request | Sequential Time | Concurrent Time | Delta |
|---|---|---|---|
| `/map/pm25/06/20250109` | 2.730s | **3.933s** | +1.203s (+44%) |
| `/map/smoke/20250109` | 1.642s | **1.573s** | −0.069s (within variance) |
| `/map/fires/20250109` | 2.201s | **2.253s** | +0.052s (within variance) |

**Overall: ✅ PASS**

The server handles concurrent map requests well. The PM25 endpoint showed a ~44% increase under concurrency, but absolute time remained well under any threshold. Smoke and Fire endpoints showed negligible difference. The server (likely single-threaded Python/FastAPI with async I/O) degrades gracefully under light concurrent load.

---

## TEST 3 — Cold Start Time

| Request | Time | State |
|---|---|---|
| `/health` (first request of session) | 4.314s | Cold (Render waking up) |
| `/health` (second request) | 1.076s | Warm |
| **Cold start overhead** | **~3.2s** | — |

**Result: ⚠️ NOTABLE**

The Render free tier sleeps after 15 minutes of inactivity. The cold start adds approximately **3–4 seconds** to every endpoint on first hit after sleep. This means:
- A real user opening the app after a period of inactivity will experience noticeable lag.
- The county endpoint cold-start time would be estimated at **~16–17s**, which would breach the Important threshold.
- The `/health` endpoint is **still slow at 1.076s even warm** — suggesting it may be doing actual work (data check?) rather than just returning `{"status":"ok"}`.

---

## TEST 4 — Error Handling

### Test 4a — Invalid county name
```
GET /county/06/FakeCounty/20250109
HTTP 404
Body: {"detail":"County 'FakeCounty' not found"}
```
**✅ PASS** — Returns 404, JSON-formatted, clear message.

---

### Test 4b — Out-of-range historical date (1999-01-01)
```
GET /county/06/Los%20Angeles/19990101
HTTP 200
Body: {
  "pm25_mean": null,
  "smoke_density": null,
  "has_smoke": false,
  "narrative": "Clear skies greet Los Angeles County residents as they welcome the new millennium..."
}
```
**❌ FAIL — Hallucinated narrative returned for date outside data range**

The API returns HTTP 200 with null data fields but then calls Claude to generate a narrative anyway. The result is a **fabricated, confident-sounding narrative** with no actual data backing it. This is a data integrity and trust issue: users may believe the AI-generated text is grounded in real measurements from 1999 when it is not.

**Expected behavior:** Return 400/422 with a message like `"No data available before [earliest_date]"`, or if 200 is returned, the narrative should clearly state no data exists for this date rather than hallucinating.

---

### Test 4c — Future date (2099-12-31)
```
GET /map/pm25/06/20991231
HTTP 200
Body: GeoJSON FeatureCollection with pm25_mean: null for all counties
```
**❌ FAIL — Future dates silently return empty data**

The API returns HTTP 200 with a structurally valid but entirely empty GeoJSON response. There is no indication to the client that the date is invalid. A future date like 2099 is clearly erroneous input that should be rejected.

**Expected behavior:** Return 400/422 with a message like `"Date must not be in the future"`.

---

## Summary Table

| Test | Result | Severity |
|---|---|---|
| `/health` response time (cold) | ❌ FAIL — 4.314s | Critical |
| `/health` response time (warm) | ❌ FAIL — 1.076s | Important |
| `/map/*` response times | ✅ PASS — 1.6–2.7s | — |
| `/county/*` response time | ✅ PASS — 13.4s (marginal) | — |
| Concurrent map requests | ✅ PASS — minimal degradation | — |
| Cold start overhead | ⚠️ Notable — ~3.2s | Important |
| Invalid county → 404 | ✅ PASS | — |
| Historical date with no data | ❌ FAIL — hallucinated narrative | Critical |
| Future date validation | ❌ FAIL — silently returns empty | Important |

---

## Recommendations

### High Priority

1. **Fix date validation on all endpoints.**
   Add input guards to reject dates before the earliest available data date (e.g., `< 2017-01-01`) and after today with a clear 400/422 error. This prevents both hallucinated narratives and empty data being silently served.

2. **Guard the narrative against null data.**
   In the county endpoint, if `pm25_mean is None` AND the date is outside a known data range, skip the Claude narrative call entirely or return a fixed message: `"No air quality data is available for this date."` This avoids fabricated content and also saves Claude API credits.

3. **Fix or optimize the `/health` endpoint.**
   At 1.076s warm, `/health` is too slow for a liveness probe. It should return in under 100ms. If it performs a DB or cache check, move that to a separate `/ready` endpoint. The `/health` endpoint should just return `200 OK` instantly.

### Medium Priority

4. **Render free tier cold start warning.**
   Consider adding a client-side loading state or wake-up ping on app load to minimize the cold start impact on user experience. Alternatively, use a cron job or uptime monitor to keep the server warm during expected usage hours.

5. **County endpoint — track if latency grows with data.**
   At 13.4s warm (close to the 15s Important threshold), monitor this endpoint as data volume grows. If it slows further, investigate whether the county data query and Claude API call can be parallelized or whether county summaries can be cached with a TTL.

6. **Add `Cache-Control` headers to map endpoints.**
   Historical map data is immutable. Adding `Cache-Control: public, max-age=86400` would allow CDN/browser caching and dramatically reduce repeat request times.

### Low Priority

7. **Structured error response format.**
   Some endpoints return `{"detail": "..."}` (FastAPI default) while others might vary. Standardize all error responses to a consistent shape, e.g., `{"error": true, "message": "...", "code": "COUNTY_NOT_FOUND"}` for easier client handling.
