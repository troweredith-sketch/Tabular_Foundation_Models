"""Lightweight regression tests for the review-driven fixes."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import missingness_robustness_adult as missingness  # noqa: E402
import phase4_mainline_compare as phase4  # noqa: E402
import phase6_big_plus_adult as phase6  # noqa: E402


class ReviewFixTests(unittest.TestCase):
    def test_normalize_missing_tokens_preserves_unknown_category(self) -> None:
        frame = pd.DataFrame(
            {
                "category": ["?", " NA ", "unknown", "Private"],
                "numeric": [1, 2, 3, 4],
            }
        )

        normalized = phase4.normalize_missing_tokens(frame)

        self.assertTrue(pd.isna(normalized.loc[0, "category"]))
        self.assertTrue(pd.isna(normalized.loc[1, "category"]))
        self.assertEqual(normalized.loc[2, "category"], "unknown")
        self.assertEqual(normalized.loc[3, "category"], "Private")
        self.assertEqual(normalized["numeric"].tolist(), [1, 2, 3, 4])

    def test_allocate_class_quotas_respects_budget_and_class_capacity(self) -> None:
        y = pd.Series(["major"] * 10 + ["minor"] * 3)

        quotas = phase6.allocate_class_quotas(y, 8)

        self.assertEqual(sum(quotas.values()), 8)
        self.assertLessEqual(quotas["minor"], 3)
        self.assertLessEqual(quotas["major"], 10)
        self.assertEqual(quotas["minor"], 3)

    def test_smoke_preset_defaults_to_safe_output_directory(self) -> None:
        args = type(
            "Args",
            (),
            {
                "preset": "smoke",
                "budgets": None,
                "seeds": None,
                "output_dir": None,
            },
        )()

        budgets, seeds, output_dir = phase6.resolve_preset_defaults(args)

        self.assertEqual(budgets, [512])
        self.assertEqual(seeds, [42])
        self.assertEqual(output_dir, Path("results") / "smoke")

    def test_final_preset_defaults_to_committed_experiment_grid(self) -> None:
        args = type(
            "Args",
            (),
            {
                "preset": "final",
                "budgets": None,
                "seeds": None,
                "output_dir": None,
            },
        )()

        budgets, seeds, output_dir = phase6.resolve_preset_defaults(args)

        self.assertEqual(budgets, [512, 2048, 8192])
        self.assertEqual(seeds, [42, 43, 44])
        self.assertEqual(output_dir, Path("results"))

    def test_inject_cell_missingness_is_deterministic_and_feature_only(self) -> None:
        frame = pd.DataFrame(
            {
                "a": [1.0, 2.0, 3.0],
                "b": ["x", "y", "z"],
            }
        )

        first = missingness.inject_cell_missingness(frame, missing_rate=0.5, seed=123)
        second = missingness.inject_cell_missingness(frame, missing_rate=0.5, seed=123)

        pd.testing.assert_frame_equal(first, second)
        self.assertGreater(int(first.isna().sum().sum()), 0)
        self.assertFalse(frame.isna().any().any())

    def test_zero_missingness_returns_equal_copy(self) -> None:
        frame = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})

        result = missingness.inject_cell_missingness(frame, missing_rate=0.0, seed=99)

        pd.testing.assert_frame_equal(result, frame)
        self.assertIsNot(result, frame)

    def test_format_project_path_returns_repository_relative_cache_path(self) -> None:
        absolute_cache_path = PROJECT_ROOT / "data" / "raw" / "adult_openml.csv"

        formatted = phase4.format_project_path(absolute_cache_path, PROJECT_ROOT)

        self.assertEqual(formatted, "data/raw/adult_openml.csv")

    def test_committed_result_csvs_do_not_expose_author_absolute_cache_paths(self) -> None:
        csv_paths = sorted((PROJECT_ROOT / "results").glob("*.csv"))
        self.assertGreater(len(csv_paths), 0)

        for csv_path in csv_paths:
            frame = pd.read_csv(csv_path)
            if "data_cache" not in frame.columns:
                continue

            with self.subTest(csv=csv_path.name):
                data_cache_values = frame["data_cache"].dropna().astype(str)
                self.assertGreater(len(data_cache_values), 0)
                self.assertFalse(
                    data_cache_values.str.startswith("/home/mr/src/").any(),
                    msg=f"{csv_path} contains an author-machine absolute data_cache path.",
                )
                self.assertTrue(
                    data_cache_values.str.startswith("data/raw/").all(),
                    msg=f"{csv_path} should use repository-relative data_cache paths.",
                )

    def test_key_result_artifacts_have_expected_schema_and_size(self) -> None:
        expectations = {
            "phase4_mainline_compare.csv": {
                "rows": 80,
                "columns": {"dataset", "scenario", "seed", "model", "accuracy", "balanced_accuracy", "macro_f1"},
            },
            "phase5_scalability_compare_summary.csv": {
                "rows": 40,
                "columns": {"dataset", "train_size_label", "model", "accuracy_mean", "total_seconds_median"},
            },
            "phase6_big_plus_adult_summary.csv": {
                "rows": 10,
                "columns": {"strategy", "budget", "accuracy_mean", "selection_seconds_median", "end_to_end_seconds_median"},
            },
            "missingness_robustness_adult_summary.csv": {
                "rows": 12,
                "columns": {"missing_rate", "model", "accuracy_mean", "accuracy_drop_mean"},
            },
        }

        for filename, expectation in expectations.items():
            csv_path = PROJECT_ROOT / "results" / filename
            frame = pd.read_csv(csv_path)

            with self.subTest(csv=filename):
                self.assertEqual(len(frame), expectation["rows"])
                self.assertTrue(expectation["columns"].issubset(frame.columns))

    def test_report_referenced_main_figures_exist(self) -> None:
        figure_names = [
            "phase5_scalability_accuracy.png",
            "phase5_scalability_balanced_accuracy.png",
            "phase5_scalability_macro_f1.png",
            "phase5_scalability_total_seconds_median.png",
            "phase6_big_plus_adult_bpr_delta.png",
        ]

        for figure_name in figure_names:
            figure_path = PROJECT_ROOT / "results" / "figures" / figure_name
            with self.subTest(figure=figure_name):
                self.assertTrue(figure_path.exists())
                self.assertGreater(figure_path.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
