import sys
import unittest
from pathlib import Path
import pytest

# tests/ must be in sys.path before tutorials/ so tutorial modules get tests/manifest
# (which points to tests/executables/ rather than tutorials/executables/)
_tests_dir = str(Path(__file__).resolve().parents[1])
_tutorials_dir = str(Path(__file__).resolve().parents[2] / "tutorials")
if _tests_dir not in sys.path:
    sys.path.insert(0, _tests_dir)

import manifest  # cache tests/manifest before tutorial modules are imported
import helpers
from base_sim_test import BaseSimTest

if _tutorials_dir not in sys.path:
    sys.path.append(_tutorials_dir)

import tutorial_1_intro as t1
import tutorial_2_reports as t2
import tutorial_3_interventions as t3
import tutorial_4_seasonality as t4
import tutorial_5_sweep as t5
import tutorial_6_calibration as t6
import tutorial_7_burnin as t7_burnin
import tutorial_7_pickup as t7_pickup


@pytest.mark.tutorial
class TestTutorials(BaseSimTest):

    def test_tutorial_1_intro(self):
        experiment = t1.run_experiment()
        self.assertTrue(experiment.succeeded, "Tutorial 1 experiment failed.")

    def test_tutorial_2_reports(self):
        experiment = t2.run_experiment()
        self.assertTrue(experiment.succeeded, "Tutorial 2 experiment failed.")
        self._assert_reports_and_plots("tutorial_2_results")

    def test_tutorial_3_interventions(self):
        experiment = t3.run_experiment()
        self.assertTrue(experiment.succeeded, "Tutorial 3 experiment failed.")
        self._assert_reports_and_plots("tutorial_3_results")

    def test_tutorial_4_seasonality(self):
        experiment = t4.run_experiment()
        self.assertTrue(experiment.succeeded, "Tutorial 4 experiment failed.")
        self._assert_reports_and_plots("tutorial_4_results")

    def test_tutorial_5_sweep(self):
        experiment = t5.run_experiment()
        self.assertTrue(experiment.succeeded, "Tutorial 5 experiment failed.")
        self._assert_reports_and_plots("tutorial_5_results")

    def test_tutorial_6_calibration(self):
        t6.run_calibration()
        calib_dir = Path("tutorial_6_calibration")
        self.assertTrue(calib_dir.exists(), "tutorial_6_calibration directory not created")
        plots = list(calib_dir.glob("plots/*.png"))
        self.assertGreater(len(plots), 0,
                           "No iteration plots found in tutorial_6_calibration/plots/")

    def test_tutorial_7_serialization(self):
        burnin_exp = t7_burnin.run_experiment()
        self.assertTrue(burnin_exp.succeeded, "Tutorial 7 burnin failed.")
        self._assert_inset_chart_and_plots("tutorial_7_results_burnin")

        t7_pickup.BURNIN_EXP_ID = burnin_exp.id
        pickup_exp = t7_pickup.run_experiment()
        self.assertTrue(pickup_exp.succeeded, "Tutorial 7 pickup failed.")
        self._assert_reports_and_plots("tutorial_7_results_pickup")

    def _assert_reports_and_plots(self, output_path):
        results = Path(output_path)

        # Downloaded report files (nested under exp_uid/sim_uid/output/ by DownloadAnalyzer)
        inset_charts = list(results.rglob("InsetChart.json"))
        self.assertGreater(len(inset_charts), 0,
                           f"InsetChart.json not found under {output_path}")

        summary_reports = list(results.rglob("MalariaSummaryReport_monthly.json"))
        self.assertGreater(len(summary_reports), 0,
                           f"MalariaSummaryReport_monthly.json not found under {output_path}")

        # Plot PNGs saved at the top of the results directory
        pngs = list(results.glob("*.png"))
        self.assertGreater(len(pngs), 0,
                           f"No PNG plots found in {output_path}")

    def _assert_inset_chart_and_plots(self, output_path):
        results = Path(output_path)

        inset_charts = list(results.rglob("InsetChart.json"))
        self.assertGreater(len(inset_charts), 0,
                           f"InsetChart.json not found under {output_path}")

        pngs = list(results.glob("*.png"))
        self.assertGreater(len(pngs), 0,
                           f"No PNG plots found in {output_path}")


if __name__ == '__main__':
    unittest.main()
