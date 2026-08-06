#!/usr/bin/env python3
"""Regression checks for the Pages/live-quotes deployment split."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PagesPipelineTest(unittest.TestCase):
    def test_pages_workflow_ignores_quote_only_commits(self) -> None:
        workflow = (ROOT / ".github/workflows/pages.yml").read_text()
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("paths-ignore:", workflow)
        self.assertIn("data/**/charts_*.json", workflow)
        self.assertIn("cancel-in-progress: false", workflow)
        self.assertIn("actions/upload-pages-artifact@v4", workflow)
        self.assertIn("actions/deploy-pages@v4", workflow)

    def test_chart_client_reads_live_data_from_raw_main(self) -> None:
        app = (ROOT / "assets/app.js").read_text()
        self.assertIn("raw.githubusercontent.com/fengjh97/market-daily/main/data", app)
        self.assertIn("fetchChartPayload", app)
        self.assertIn("cache: \"no-store\"", app)

    def test_refresher_stages_only_generated_chart_files(self) -> None:
        refresher = (ROOT / "tools/auto_refresh.sh").read_text()
        self.assertNotIn("git add -A", refresher)
        self.assertIn("CHANGED_FILES", refresher)
        self.assertIn('git add -- "${CHANGED_FILES[@]}"', refresher)


if __name__ == "__main__":
    unittest.main()
