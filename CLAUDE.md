# SmokeStory — Claude Code Rules

## Deployment
- Push to `main` on GitHub triggers automatic Render redeploy
- Always push after changes; confirm with `git push origin main`

## Side Panel Design Rules

### Typography
- **Body font everywhere in the panel: Cormorant Garamond** (`var(--serif)`)
  - Applies to: section labels, body text, step numbers, step text, county names, financial descriptions
- **DM Mono (`var(--mono)`) reserved only for:**
  - Large data figures (e.g. `$36B – $40B`)
  - CTA buttons (e.g. `VIEW FINANCIAL ANALYSIS →`)
- Body text size: `0.98rem`, color: `rgba(226,226,234,0.7)`, line-height: `1.72`
- Section labels: `0.55rem`, uppercase, letter-spacing `0.26em`, amber color at 55% opacity

### Layout
- `welcome-inner` uses `display: flex; flex-direction: column; justify-content: space-between` to fill panel height naturally — no pinned/absolute/sticky elements
- `#welcome-scroll` wraps scrollable content with `flex: 1; overflow-y: auto; display: flex; flex-direction: column`
- "View Financial Analysis" button lives **inside** the Financial Impact section in normal document flow — not as a separate pinned element

### Sections (landing page, date = 20250109)
1. What is this
2. How to explore (3 steps)
3. Most Affected (county row only)
4. Financial Impact (label + figure + description + button)

## Data Accuracy Rules

### Data sources and cadence
- **Active fires**: NASA FIRMS VIIRS SNPP NRT — updates **daily** (satellite passes ~twice/day)
- **Smoke polygons**: NOAA GOES HMS — updates **daily**
- **PM2.5 county layer**: EPA AQS finalized monitoring data — **4–8 week lag**

### "Latest Data" button behavior
- Jumps to today's date
- Fires and smoke will show (near real-time)
- PM2.5 counties will be empty — this is expected and correct
- A banner and a map note explain the EPA lag to users

### Copy principles
- Never claim "real-time" for PM2.5 — it lags 4–8 weeks
- When no fires/smoke detected, show a banner — don't leave the map silently blank
- Be honest about data limitations; turn them into teachable moments
