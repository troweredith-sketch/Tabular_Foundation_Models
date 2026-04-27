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


if __name__ == "__main__":
    unittest.main()
