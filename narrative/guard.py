"""Deterministic accuracy guard for generated narratives.

DeepSeek does not reliably honor two of SmokeStory's hard rules from the prompt
alone: (1) no attribution to officials/experts/titles or advisory voice, and
(2) sentence 1 must not name a county other than the subject. This module
detects those violations after generation so the caller can regenerate with a
pointed correction, rather than shipping a fabricated source or geographic bleed.
"""

import re

# Attribution / advisory-voice constructions. These imply a source the data
# does not provide, or use the banned advisory register. "According to the
# Guardian" is allowed (the Guardian context is a real provided source) and is
# excluded below before matching.
_ATTRIBUTION_PATTERNS = [
    r"\bofficials?\b[^.]{0,40}\b(warn|warns|warned|warning|say|said|caution|cautioned|urge|urged|note|noted)\b",
    r"\bauthorities\b[^.]{0,40}\b(warn|warns|warned|warning|say|said|caution|urge|urged)\b",
    r"\b(experts?|scientists?|researchers?|meteorologists?|analysts?|forecasters?)\b[^.]{0,40}\b(say|said|warn|warns|warned|note|noted|found|caution|predict|predicted)\b",
    r"\bfire chief\b",
    r"\b(a|one|the)\s+study\b[^.]{0,40}\b(found|finds|shows|showed|suggests|suggested|warns|warned|indicates|indicated)\b",
    r"\bresidents are (urged|warned|advised)\b",
    r"\bare urged to\b",
    r"\b(warned|warns|warning|cautioned|cautions) that\b",
]

_GUARDIAN_ALLOWED = re.compile(r"according to the guardian|the guardian reports?|the guardian reported", re.I)

_COUNTY_IN_SENTENCE = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+County\b")


def _first_sentence(text):
    # Narratives are a single paragraph; split on the first sentence-ending period
    # followed by a space + capital. Fall back to the whole text.
    m = re.search(r"\.\s+[A-Z]", text)
    return text[: m.start() + 1] if m else text


def check(text, county_name):
    """Return a list of human-readable violations (empty list = passes)."""
    violations = []

    # 1. Attribution / advisory voice — strip the allowed Guardian attribution first
    scrubbed = _GUARDIAN_ALLOWED.sub("", text)
    low = scrubbed.lower()
    for pat in _ATTRIBUTION_PATTERNS:
        m = re.search(pat, low)
        if m:
            violations.append(
                f"attribution/advisory voice: \"{m.group(0).strip()}\" — state context "
                f"as plain fact, attribute nothing to officials/experts/titles"
            )

    # 2. Sentence 1 must not name a county other than the subject
    s1 = _first_sentence(text)
    for m in _COUNTY_IN_SENTENCE.finditer(s1):
        named = m.group(1)
        if named.lower() != county_name.lower():
            violations.append(
                f"sentence 1 names another county: \"{named} County\" — the opener may "
                f"only name a place inside {county_name} County"
            )

    # 3. Sentence 1 must not open with a statewide / out-of-county framing before
    #    reaching the subject county (e.g. "Across California, wildfires... while
    #    {county} County..."). High-precision tokens only, to avoid false positives.
    s1_low = s1.lower()
    county_pos = s1_low.find(county_name.lower())
    lead = s1_low if county_pos == -1 else s1_low[:county_pos]
    for token in ("across california", "across the state", "statewide",
                  "much of the state", "much of california", "throughout california"):
        if token in lead:
            violations.append(
                f"sentence 1 opens with a statewide framing: \"{token}\" — the opener must "
                f"lead with a scene inside {county_name} County, not a statewide setup"
            )
            break

    return violations
