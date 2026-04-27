"""Supplemental Adult missingness robustness experiment."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

import phase4_mainline_compare as phase4

DATASET_KEY = "adult"
DETAIL_OUTPUT_FILENAME = "missingness_robustness_adult.csv"
SUMMARY_OUTPUT_FILENAME = "missingness_robustness_adult_summary.csv"
DEFAULT_MISSING_RATES = [0.0, 0.1, 0.3]
DEFAULT_SEEDS = [42]
DEFAULT_TRAIN_SIZE = 2048

DETAIL_COLUMN_ORDER = [
    "dataset",
    "seed",
    "split",
    "missing_rate",
    "train_size",
    "model",
    "metric",
    "accuracy",
    "balanced_accuracy",
    "macro_f1",
    "accuracy_drop",
    "balanced_accuracy_drop",
    "macro_f1_drop",
    "fit_seconds",
    "predict_seconds",
    "total_seconds",
    "device",
    "test_size",
    "n_samples_total",
    "n_features_raw",
    "n_numeric_features",
    "n_categorical_features",
    "n_features_after_preprocessing",
    "random_state",
    "test_size_ratio",
    "data_cache",
    "input_representation",
    "notes",
]

SUMMARY_COLUMN_ORDER = [
    "dataset",
    "missing_rate",
    "model",
    "n_runs",
    "seeds",
    "train_size_min",
    "train_size_max",
    "accuracy_mean",
    "accuracy_std",
    "accuracy_drop_mean",
    "balanced_accuracy_mean",
    "balanced_accuracy_std",
    "balanced_accuracy_drop_mean",
    "macro_f1_mean",
    "macro_f1_std",
    "macro_f1_drop_mean",
    "fit_seconds_median",
    "predict_seconds_median",
    "total_seconds_median",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run a supplemental Adult missingness robustness check on the fixed Phase 4 model set."
        ),
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=[phase4.ALL_TOKEN],
        choices=[phase4.ALL_TOKEN, *phase4.MODEL_DISPLAY_NAMES.keys()],
        help="Models to run. Default: all four Phase 4 models.",
    )
    parser.add_argument(
        "--missing-rates",
        nargs="+",
        type=float,
        default=DEFAULT_MISSING_RATES,
        help="Cell-level feature missingness rates to inject. Default: 0 0.1 0.3.",
    )
    parser.add_argument(
        "--seeds",
        nargs="+",
        type=int,
        default=DEFAULT_SEEDS,
        help="Random seeds used for repeated stratified splits. Default: 42.",
    )
    parser.add_argument(
        "--train-size",
        type=int,
        default=DEFAULT_TRAIN_SIZE,
        help="Stratified training subset size. Default: 2048.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results"),
        help="Directory for CSV outputs. Relative paths are resolved from project root.",
    )
    return parser.parse_args()


def normalize_missing_rates(values: list[float]) -> list[float]:
    rates = sorted(set(float(value) for value in values))
    if not rates:
        raise ValueError("At least one missing rate is required.")
    invalid = [rate for rate in rates if rate < 0.0 or rate >= 1.0]
    if invalid:
        raise ValueError(f"Missing rates must be in [0, 1), got: {invalid}.")
    if 0.0 not in rates:
        rates.insert(0, 0.0)
    return rates


def resolve_output_dir(project_root: Path, output_dir: Path) -> Path:
    if output_dir.is_absolute():
        resolved = output_dir
    else:
        resolved = project_root / output_dir
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def inject_cell_missingness(
    X: pd.DataFrame,
    *,
    missing_rate: float,
    seed: int,
) -> pd.DataFrame:
    """Inject deterministic cell-level missing values into feature columns only."""
    X_missing = X.copy()
    if missing_rate == 0.0 or X_missing.empty:
        return X_missing

    rng = np.random.default_rng(seed)
    mask = rng.random(X_missing.shape) < missing_rate
    return X_missing.mask(mask, np.nan)


def make_train_subset(
    X_train_full: pd.DataFrame,
    y_train_full: pd.Series,
    *,
    train_size: int,
    seed: int,
) -> tuple[pd.DataFrame, pd.Series]:
    if train_size > len(X_train_full):
        raise ValueError(
            f"Requested train_size={train_size} exceeds available train rows={len(X_train_full)}."
        )

    X_train, _, y_train, _ = train_test_split(
        X_train_full,
        y_train_full,
        train_size=train_size,
        random_state=seed,
        stratify=y_train_full,
    )
    return X_train, y_train


def build_split_name(seed: int, train_size: int, missing_rate: float) -> str:
    rate_label = str(missing_rate).replace(".", "p")
    return f"adult_fixed_test_seed{seed}_train{train_size}_missing{rate_label}"


def build_notes(model_key: str, *, train_size: int, missing_rate: float) -> str:
    return (
        "Supplemental Adult missingness robustness check; "
        f"model={phase4.MODEL_DISPLAY_NAMES[model_key]}, train_size={train_size}, "
        f"cell_missing_rate={missing_rate}. Missing masks are deterministic within each "
        "seed/rate split and are shared across models."
    )


def run_model(
    dataset_key: str,
    model_key: str,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    numeric_cols: list[str],
    categorical_cols: list[str],
    *,
    seed: int,
    train_size: int,
    missing_rate: float,
) -> dict[str, object]:
    notes = build_notes(model_key, train_size=train_size, missing_rate=missing_rate)

    if model_key == "lightgbm":
        return phase4.run_lightgbm(
            dataset_key,
            X_train,
            X_test,
            y_train,
            y_test,
            numeric_cols,
            categorical_cols,
            seed=seed,
            notes=notes,
        )
    if model_key == "xgboost":
        return phase4.run_xgboost(
            dataset_key,
            X_train,
            X_test,
            y_train,
            y_test,
            numeric_cols,
            categorical_cols,
            seed=seed,
            notes=notes,
        )
    if model_key == "tabpfn_v2":
        return phase4.run_tabpfn_v2(
            dataset_key,
            X_train,
            X_test,
            y_train,
            y_test,
            numeric_cols,
            categorical_cols,
            seed=seed,
            ignore_pretraining_limits=False,
            notes=notes,
        )
    if model_key == "tabicl":
        return phase4.run_tabicl(
            dataset_key,
            X_train,
            X_test,
            y_train,
            y_test,
            seed=seed,
            notes=notes,
        )

    raise ValueError(f"Unsupported model key: {model_key}")


def run_seed_missing_rate(
    X: pd.DataFrame,
    y: pd.Series,
    model_keys: list[str],
    *,
    seed: int,
    train_size: int,
    missing_rate: float,
    cache_path: Path,
    numeric_cols: list[str],
    categorical_cols: list[str],
) -> list[dict[str, object]]:
    X_train_full, X_test, y_train_full, y_test = train_test_split(
        X,
        y,
        test_size=phase4.TEST_SIZE,
        random_state=seed,
        stratify=y,
    )
    X_train, y_train = make_train_subset(
        X_train_full,
        y_train_full,
        train_size=train_size,
        seed=seed,
    )

    mask_seed_base = seed * 100_003 + int(round(missing_rate * 10_000))
    X_train_missing = inject_cell_missingness(
        X_train,
        missing_rate=missing_rate,
        seed=mask_seed_base + 17,
    )
    X_test_missing = inject_cell_missingness(
        X_test,
        missing_rate=missing_rate,
        seed=mask_seed_base + 31,
    )

    common_fields = {
        "dataset": DATASET_KEY,
        "seed": seed,
        "split": build_split_name(seed, train_size, missing_rate),
        "missing_rate": missing_rate,
        "train_size": train_size,
        "test_size": len(X_test),
        "n_samples_total": len(X),
        "n_features_raw": X.shape[1],
        "n_numeric_features": len(numeric_cols),
        "n_categorical_features": len(categorical_cols),
        "random_state": seed,
        "test_size_ratio": phase4.TEST_SIZE,
        "data_cache": str(cache_path),
    }

    rows: list[dict[str, object]] = []
    for model_key in model_keys:
        result = run_model(
            DATASET_KEY,
            model_key,
            X_train_missing,
            X_test_missing,
            y_train,
            y_test,
            numeric_cols,
            categorical_cols,
            seed=seed,
            train_size=train_size,
            missing_rate=missing_rate,
        )
        rows.append({**common_fields, **result})
    return rows


def add_baseline_drops(detail_df: pd.DataFrame) -> pd.DataFrame:
    detail_df = detail_df.copy()
    detail_df[["accuracy_drop", "balanced_accuracy_drop", "macro_f1_drop"]] = 0.0
    baseline_df = detail_df[detail_df["missing_rate"] == 0.0]
    baseline_by_run = baseline_df.set_index(["seed", "model"])[
        ["accuracy", "balanced_accuracy", "macro_f1"]
    ]

    for index, row in detail_df.iterrows():
        baseline = baseline_by_run.loc[(row["seed"], row["model"])]
        detail_df.at[index, "accuracy_drop"] = baseline["accuracy"] - row["accuracy"]
        detail_df.at[index, "balanced_accuracy_drop"] = (
            baseline["balanced_accuracy"] - row["balanced_accuracy"]
        )
        detail_df.at[index, "macro_f1_drop"] = baseline["macro_f1"] - row["macro_f1"]

    return detail_df


def build_summary(detail_df: pd.DataFrame) -> pd.DataFrame:
    if detail_df.empty:
        return pd.DataFrame(columns=SUMMARY_COLUMN_ORDER)

    summary_df = (
        detail_df.groupby(["dataset", "missing_rate", "model"], as_index=False)
        .agg(
            n_runs=("seed", "nunique"),
            seeds=("seed", lambda values: ",".join(str(seed) for seed in sorted(set(values)))),
            train_size_min=("train_size", "min"),
            train_size_max=("train_size", "max"),
            accuracy_mean=("accuracy", "mean"),
            accuracy_std=("accuracy", "std"),
            accuracy_drop_mean=("accuracy_drop", "mean"),
            balanced_accuracy_mean=("balanced_accuracy", "mean"),
            balanced_accuracy_std=("balanced_accuracy", "std"),
            balanced_accuracy_drop_mean=("balanced_accuracy_drop", "mean"),
            macro_f1_mean=("macro_f1", "mean"),
            macro_f1_std=("macro_f1", "std"),
            macro_f1_drop_mean=("macro_f1_drop", "mean"),
            fit_seconds_median=("fit_seconds", "median"),
            predict_seconds_median=("predict_seconds", "median"),
            total_seconds_median=("total_seconds", "median"),
        )
    )
    summary_df[["accuracy_std", "balanced_accuracy_std", "macro_f1_std"]] = summary_df[
        ["accuracy_std", "balanced_accuracy_std", "macro_f1_std"]
    ].fillna(0.0)

    numeric_columns = [
        "accuracy_mean",
        "accuracy_std",
        "accuracy_drop_mean",
        "balanced_accuracy_mean",
        "balanced_accuracy_std",
        "balanced_accuracy_drop_mean",
        "macro_f1_mean",
        "macro_f1_std",
        "macro_f1_drop_mean",
        "fit_seconds_median",
        "predict_seconds_median",
        "total_seconds_median",
    ]
    for column in numeric_columns:
        summary_df[column] = summary_df[column].round(4)

    return summary_df[SUMMARY_COLUMN_ORDER]


def save_outputs(
    project_root: Path,
    detail_records: list[dict[str, object]],
    output_dir: Path,
) -> tuple[Path, Path]:
    detail_df = pd.DataFrame(detail_records)
    if detail_df.empty:
        detail_df = pd.DataFrame(columns=DETAIL_COLUMN_ORDER)
    else:
        detail_df = add_baseline_drops(detail_df)
        detail_df = detail_df[DETAIL_COLUMN_ORDER]

    resolved_output_dir = resolve_output_dir(project_root, output_dir)
    detail_path = resolved_output_dir / DETAIL_OUTPUT_FILENAME
    detail_df.to_csv(detail_path, index=False)

    summary_df = build_summary(detail_df)
    summary_path = resolved_output_dir / SUMMARY_OUTPUT_FILENAME
    summary_df.to_csv(summary_path, index=False)
    return detail_path, summary_path


def print_run_result(result: dict[str, object]) -> None:
    print(
        {
            "dataset": result["dataset"],
            "seed": result["seed"],
            "missing_rate": result["missing_rate"],
            "model": result["model"],
            "accuracy": result["accuracy"],
            "balanced_accuracy": result["balanced_accuracy"],
            "macro_f1": result["macro_f1"],
            "fit_seconds": result["fit_seconds"],
            "predict_seconds": result["predict_seconds"],
            "device": result["device"],
        }
    )


def main() -> None:
    args = parse_args()
    project_root = phase4.resolve_project_root()
    model_keys = phase4.normalize_choice_list(args.models, phase4.DEFAULT_MODELS)
    missing_rates = normalize_missing_rates(args.missing_rates)

    if "tabicl" in model_keys:
        checkpoint_path = phase4.ensure_tabicl_checkpoint_available()
        print(f"TabICL checkpoint ready: {checkpoint_path}")
        print()

    X, y, cache_path = phase4.load_dataset(project_root, DATASET_KEY)
    categorical_cols, numeric_cols = phase4.get_feature_groups(X)

    print(f"Dataset: {DATASET_KEY}")
    print(f"Loaded data from: {cache_path}")
    print(f"Samples: {len(X)}, raw features: {X.shape[1]}")
    print(f"Categorical features: {len(categorical_cols)}, numeric features: {len(numeric_cols)}")
    print(f"Models: {', '.join(phase4.MODEL_DISPLAY_NAMES[key] for key in model_keys)}")
    print(f"Train size: {args.train_size}")
    print(f"Missing rates: {', '.join(str(rate) for rate in missing_rates)}")
    print(f"Seeds: {', '.join(str(seed) for seed in args.seeds)}")
    print()

    detail_records: list[dict[str, object]] = []
    for seed in args.seeds:
        for missing_rate in missing_rates:
            print(f"[adult | missing_rate={missing_rate}] Running seed {seed}")
            run_results = run_seed_missing_rate(
                X,
                y,
                model_keys,
                seed=seed,
                train_size=args.train_size,
                missing_rate=missing_rate,
                cache_path=cache_path,
                numeric_cols=numeric_cols,
                categorical_cols=categorical_cols,
            )
            detail_records.extend(run_results)
            for result in run_results:
                print_run_result(result)

            detail_path, summary_path = save_outputs(
                project_root,
                detail_records,
                args.output_dir,
            )
            print(f"Intermediate detail saved to: {detail_path}")
            print(f"Intermediate summary saved to: {summary_path}")
            print()

    detail_path, summary_path = save_outputs(project_root, detail_records, args.output_dir)
    print(f"Saved detail results to: {detail_path}")
    print(f"Saved summary results to: {summary_path}")

    summary_df = pd.read_csv(summary_path)
    if summary_df.empty:
        print("Summary is empty because no runs were executed.")
    else:
        print()
        print(summary_df)


if __name__ == "__main__":
    main()
