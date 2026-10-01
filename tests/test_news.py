import os
import unittest
from unittest.mock import Mock, patch

import requests

from pipeline.news import NewsAPIError, _query_guardian, get_news_headlines


class GuardianNewsTests(unittest.TestCase):
    def test_missing_key_is_visible(self):
        with patch.dict(os.environ, {"GUARDIAN_API_KEY": ""}):
            with self.assertRaisesRegex(NewsAPIError, "not configured"):
                _query_guardian("California wildfire", "2025-01-08", "2025-01-10")

    def test_upstream_error_is_not_reported_as_empty_news(self):
        response = Mock()
        response.raise_for_status.side_effect = requests.HTTPError("401")
        with patch.dict(os.environ, {"GUARDIAN_API_KEY": "configured-key"}):
            with patch("pipeline.news.requests.get", return_value=response):
                with self.assertRaisesRegex(NewsAPIError, "Guardian request failed"):
                    _query_guardian(
                        "California wildfire",
                        "2025-01-08",
                        "2025-01-10",
                    )

    def test_broad_fallback_keeps_california_wildfire_story(self):
        california_story = {
            "webTitle": "California wildfire smoke reaches nearby towns",
            "webUrl": "https://example.com/california-fire",
            "fields": {
                "headline": "California wildfire smoke reaches nearby towns",
                "trailText": "Firefighters respond as smoke affects air quality.",
            },
        }
        with patch(
            "pipeline.news._query_guardian",
            side_effect=[[], [california_story]],
        ):
            headlines = get_news_headlines("Los Angeles", "20250109")

        self.assertEqual(len(headlines), 1)
        self.assertEqual(headlines[0]["source"], "The Guardian")
        self.assertEqual(headlines[0]["url"], california_story["webUrl"])


if __name__ == "__main__":
    unittest.main()
