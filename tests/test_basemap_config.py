from pathlib import Path
import unittest


INDEX_HTML = Path(__file__).parents[1] / "frontend" / "index.html"


class BasemapConfigTest(unittest.TestCase):
    def test_uses_keyless_openfreemap_basemap(self):
        html = INDEX_HTML.read_text(encoding="utf-8")

        self.assertIn("https://tiles.openfreemap.org/styles/dark", html)
        self.assertIn("@maplibre/maplibre-gl-leaflet@0.1.4", html)
        self.assertIn("styleimagemissing", html)
        self.assertIn("basemapMap.addImage", html)
        self.assertNotIn("cartodb-basemaps", html)
        self.assertNotIn("basemaps.cartocdn.com", html)


if __name__ == "__main__":
    unittest.main()
