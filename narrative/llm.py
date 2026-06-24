"""Shared LLM client for SmokeStory.

Migrated 2026-06-22 from Anthropic Claude (claude-sonnet-4) to DeepSeek
(`deepseek-chat`) because the Anthropic account ran out of credit. DeepSeek
exposes an OpenAI-compatible chat-completions endpoint, so we call it with a
plain `requests` POST — no SDK needed.

Both narrative generation (`narrative/generator.py`) and the /chat assistant
(`api/main.py`) go through `complete()` so there is a single place to change
the model or provider.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"


class LLMError(RuntimeError):
    """Raised when the LLM call cannot be completed."""


def complete(prompt: str, max_tokens: int = 450, temperature: float = 1.0) -> str:
    """Send a single-user-message completion request to DeepSeek and return text.

    Raises LLMError on missing key, HTTP error (incl. 402 insufficient balance),
    or a malformed response, so callers fail loudly rather than returning junk.
    """
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise LLMError("DEEPSEEK_API_KEY is not set")

    try:
        resp = requests.post(
            DEEPSEEK_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=60,
        )
    except requests.RequestException as e:
        raise LLMError(f"DeepSeek request failed: {e}") from e

    if resp.status_code == 402:
        raise LLMError("DeepSeek account has insufficient balance (HTTP 402)")
    if not resp.ok:
        raise LLMError(f"DeepSeek API error {resp.status_code}: {resp.text[:300]}")

    try:
        return resp.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError, ValueError) as e:
        raise LLMError(f"Unexpected DeepSeek response: {resp.text[:300]}") from e
