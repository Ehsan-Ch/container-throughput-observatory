import unittest
from analysis import ROOT, economy_panel, experiment, paired_summary
from build import render


class AnalysisTests(unittest.TestCase):
    def test_matching_excludes_missing_and_zero_baselines(self):
        rows = [{"values": {2019: 20, 2024: 0}}, {"values": {2019: 0, 2024: 10}},
                {"values": {2019: 50, 2024: None}}, {"values": {2019: None, 2024: 30}}]
        result = paired_summary(rows, 2024)
        self.assertEqual((result["observed"], result["missing"], result["paired"]), (3, 1, 1))
        self.assertEqual(result["combined_change"], -100)
        self.assertEqual(result["median_change"], -100)

    def test_median_economy_and_combined_changes_differ(self):
        rows = [{"values": {2019: 1000, 2024: 1100}}, {"values": {2019: 100, 2024: 150}}]
        result = paired_summary(rows, 2024)
        self.assertEqual(result["median_change"], 30)
        self.assertAlmostEqual(result["combined_change"], 13.636364)

    def test_aggregates_excluded_and_duplicates_rejected(self):
        geography = [{"id": "A", "name": "A", "region": {"id": "X", "value": "Region"}},
                     {"id": "WLD", "name": "World", "region": {"id": "NA", "value": "Aggregates"}}]
        row = {"countryiso3code": "A", "date": 2020, "value": 23,
               "indicator": {"id": "IS.SHP.GOOD.TU"}}
        panel = economy_panel(geography, [row, {**row, "countryiso3code": "WLD", "value": 100}])
        self.assertEqual([r["code"] for r in panel], ["A"])
        self.assertEqual(panel[0]["values"][2020], 23)
        self.assertIsNone(panel[0]["values"][2019])
        with self.assertRaises(ValueError):
            economy_panel(geography, [row, row])

    def test_report_and_committed_page_reproduce(self):
        report = experiment()
        self.assertEqual(len(report["economies"]), 217)
        self.assertEqual(report["coverage"][2024]["observed"], 103)
        self.assertEqual((ROOT / "index.html").read_text(encoding="utf-8"), render())
