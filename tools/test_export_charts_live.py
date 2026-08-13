#!/usr/bin/env python3
import importlib.util
import json
from pathlib import Path
import unittest


SPEC = importlib.util.spec_from_file_location("export_charts", Path(__file__).with_name("export_charts.py"))
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class LiveFallbackParsingTest(unittest.TestCase):
    def test_yahoo_japan_quote(self):
        html = """<div>ポートフォリオに追加 3,006 前日比 +6.5 ( +0.22 % )
        リアルタイム株価 9:11 前日終値 用語 2,999.5 ( 08/12 )
        始値 用語 3,010 ( 09:00 ) 高値 用語 3,020 ( 09:01 )
        安値 用語 2,992.5 ( 09:06 ) 出来高 用語 --- ( --:-- )</div>"""
        quote = MODULE.parse_yahoo_jp_live(html)
        self.assertEqual(quote["close"], 3006.0)
        self.assertEqual(quote["previous_close"], 2999.5)
        self.assertEqual(quote["low"], 2992.5)

    def test_naver_quote(self):
        payload = {"datas": [{"marketStatus": "OPEN", "closePriceRaw": "6878.70",
            "compareToPreviousClosePriceRaw": "299.66", "fluctuationsRatioRaw": "4.55",
            "openPriceRaw": "6773.92", "highPriceRaw": "6895.63", "lowPriceRaw": "6773.92",
            "accumulatedTradingVolumeRaw": "53344000",
            "localTradedAt": "2026-08-13T09:11:28+09:00"}]}
        quote = MODULE.parse_naver_live(payload)
        self.assertEqual(quote["close"], 6878.70)
        self.assertEqual(quote["previous_close"], 6579.04)
        self.assertEqual(quote["time"], "09:11")
        self.assertEqual(quote["volume"], 53344000)


if __name__ == "__main__":
    unittest.main()
