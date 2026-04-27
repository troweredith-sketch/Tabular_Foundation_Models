"""Phase 5 experiment: train-size scalability comparison."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

import phase4_mainline_compare as phase4

DEFAULT_TRAIN_SIZE_LABELS = ["512", "2048", "8192", "10000", "full"]
DETAIL_OUTPUT_FILENAME = "phase5_scalability_compare.csv"
SUMMARY_OUTPUT_FILENAME = "phase5_scalability_compare_summary.csv"

DETAIL_COLUMN_ORDER = [
    "dataset",
    "train_size_label",
    "train_size",
    "seed",
    "split",
    "model",
    "metric",
    "accuracy",
    "balanced_accuracy",
    "macro_f1",
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
    "train_size_label",
    "model",
    "n_runs",
    "seeds",
    "train_size_min",
    "train_size_max",
    "accuracy_mean",
    "accuracy_std",
    "accuracy_min",
    "accuracy_max",
    "balanced_accuracy_mean",
    "balanced_accuracy_std",
    "balanced_accuracy_min",
    "balanced_accuracy_max",
    "macro_f1_mean",
    "macro_f1_std",
    "macro_f1_min",
    "macro_f1_max",
    "fit_seconds_median",
    "predict_seconds_median",
    "total_seconds_median",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run Phase 5 train-size scalability comparisons across Adult and "
            "Bank Marketing with the fixed Phase 4 model set."
        ),
    )
    parser.add_argument(
        "--datasets",
        nargs="+",
        default=[phase4.ALL_TOKEN],
        choices=[phase4.ALL_TOKEN, *phase4.DATASET_CONFIGS.keys()],
        help="Datasets to run. Default: all.",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=[phase4.ALL_TOKEN],
        choices=[phase4.ALL_TOKEN, *phase4.MODEL_DISPLAY_NAMES.keys()],
        help="Models to run. Default: all four Phase 4 models.",
    )
    parser.add_argument(
        "--train-sizes",
        nargs="+",
        default=DEFAULT_TRAIN_SIZE_LABELS,
        help=(
            "Train-size labels to run. Use positive integers or 'full'. "
            "Default: 512 2048 8192 10000 full."
        ),
    )
    parser.add_argument(
        "--seeds",
        nargs="+",
        type=int,
        default=phase4.DEFAULT_SEEDS,
        help="Random seeds used for repeated stratified splits. Default: 42 43 44 45 46.",
    )
    return parser.parse_args()


def normalize_train_size_labels(values: list[str]) -> list[str]:
    normalized: list[str] = []
    if phase4.ALL_TOKEN in values:
        values = DEFAULT_TRAIN_SIZE_LABELS

    for value in values:
        label = value.lower()
        if label == phase4.ALL_TOKEN:
            continue
        if label == "full":
            normalized.append(label)
            continue
        try:
            train_size = int(label)
        except ValueError as exc:
            raise ValueError(
                f"Unsupported train-size label: {value}. Use positive integers or 'full'."
            ) from exc
        if train_size <= 0:
            raise ValueError(f"Train size must be positive, got: {value}.")
        normalized.append(str(train_size))

    if not normalized:
        raise ValueError("At least one train-size label is required.")
    return normalized


def make_train_subset(
    X_train_full: pd.DataFrame,
    y_train_full: pd.Series,
    *,
    train_size_label: str,
    seed: int,
) -> tuple[pd.DataFrame, pd.Series, int]:
    if train_size_label == "full":
        return X_train_full, y_train_full, len(X_train_full)

    train_size = int(train_size_label)
    if train_size > len(X_train_full):
        raise ValueError(
            f"Requested train_size={train_size} exceeds available train rows={len(X_train_full)}."
        )

    X_train_small, _, y_train_small, _ = train_test_split(
        X_train_full,
        y_train_full,
        train_size=train_size,
        random_state=seed,
        stratify=y_train_full,
    )
    return X_train_small, y_train_small, train_size


def build_split_name(
    dataset_key: str,
    train_size_label: str,
    seed: int,
    actual_train_size: int,
) -> str:
    dataset_prefix = dataset_key.replace("-", "_")
    if train_size_label == "full":
        return f"{dataset_prefix}_fixed_test_seed{seed}_full_train"
    return f"{dataset_prefix}_fixed_test_seed{seed}_train{actual_train_size}"


def build_scalability_notes(
    train_size_label: str,
    model_key: str,
    *,
    actual_train_size: int,
) -> str:
    if train_size_label == "full":
        if model_key == "tabpfn_v2":
            return (
                "Phase 5 scalability full-train row; used ignore_pretraining_limits=True "
                "because train size exceeds the official 10,000-sample support, so this "
                "is a constrained result."
            )
        if model_key == "tabicl":
            return (
                "Phase 5 scalability full-train row; uses TabICLClassifier with the "
                f"official {phase4.TABICL_CHECKPOINT_VERSION} checkpoint."
            )
        return "Phase 5 scalability full-train row with the fixed Phase 4 baseline settings."

    if model_key == "tabpfn_v2":
        return (
            f"Phase 5 scalability train-size row; seed-specific stratified train subset "
            f"with train_size={actual_train_size}; trained within TabPFN support range."
        )
    if model_key == "tabicl":
        return (
            f"Phase 5 scalability train-size row; seed-specific stratified train subset "
            f"with train_size={actual_train_size}; uses the official "
            f"{phase4.TABICL_CHECKPOINT_VERSION} checkpoint."
        )
    return (
        f"Phase 5 scalability train-size row with train_size={actual_train_size} "
        "and the fixed Phase 4 baseline settings."
    )


def run_models_for_train_size(
    dataset_key: str,
    model_keys: list[str],
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    numeric_cols: list[str],
    categorical_cols: list[str],
    *,
    train_size_label: str,
    seed: int,
    actual_train_size: int,
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    ignore_pretraining_limits = actual_train_size > phase4.CONTROL_TRAIN_SIZE

    for model_key in model_keys:
        notes = build_scalability_notes(
            train_size_label,
            model_key,
            actual_train_size=actual_train_size,
        )

        if model_key == "lightgbm":
            result = phase4.run_lightgbm(
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
        elif model_key == "xgboost":
            result = phase4.run_xgboost(
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
        elif model_key == "tabpfn_v2":
            result = phase4.run_tabpfn_v2(
                dataset_key,
                X_train,
                X_test,
                y_train,
                y_test,
                numeric_cols,
                categorical_cols,
                seed=seed,
                ignore_pretraining_limits=ignore_pretraining_limits,
                notes=notes,
            )
        elif model_key == "tabicl":
            result = phase4.run_tabicl(
                dataset_key,
                X_train,
                X_test,
                y_train,
                y_test,
                seed=seed,
                notes=notes,
            )
        else:
            raise ValueError(f"Unsupported model key: {model_key}")

        results.append(result)

    return results


def run_single_dataset_train_size_seed(
    dataset_key: str,
    train_size_label: str,
    seed: int,
    model_keys: list[str],
    X: pd.DataFrame,
    y: pd.Series,
    *,
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
    X_train, y_train, actual_train_size = make_train_subset(
        X_train_full,
        y_train_full,
        train_size_label=train_size_label,
        seed=seed,
    )

    common_fields = {
        "dataset": dataset_key,
        "train_size_label": train_size_label,
        "train_size": actual_train_size,
        "seed": seed,
        "split": build_split_name(dataset_key, train_size_label, seed, actual_train_size),
        "test_size": len(X_test),
        "n_samples_total": len(X),
        "n_features_raw": X.shape[1],
        "n_numeric_features": len(numeric_cols),
        "n_categorical_features": len(categorical_cols),
        "random_state": seed,
        "test_size_ratio": phase4.TEST_SIZE,
        "data_cache": phase4.format_project_path(cache_path),
    }

    model_results = run_models_for_train_size(
        dataset_key,
        model_keys,
        X_train,
        X_test,
        y_train,
        y_test,
        numeric_cols,
        categorical_cols,
        train_size_label=train_size_label,
        seed=seed,
        actual_train_size=actual_train_size,
    )
    return [{**common_fields, **result} for result in model_results]


def build_summary(detail_df: pd.DataFrame) -> pd.DataFrame:
    if detail_df.empty:
        return pd.DataFrame(columns=SUMMARY_COLUMN_ORDER)

    summary_df = (
        detail_df.groupby(["dataset", "train_size_label", "model"], as_index=False)
        .agg(
            n_runs=("seed", "nunique"),
            seeds=("seed", lambda values: ",".join(str(seed) for seed in sorted(set(values)))),
            train_size_min=("train_size", "min"),
            train_size_max=("train_size", "max"),
            accuracy_mean=("accuracy", "mean"),
            accuracy_std=("accuracy", "std"),
            accuracy_min=("accuracy", "min"),
            accuracy_max=("accuracy", "max"),
            balanced_accuracy_mean=("balanced_accuracy", "mean"),
            balanced_accuracy_std=("balanced_accuracy", "std"),
            balanced_accuracy_min=("balanced_accuracy", "min"),
            balanced_accuracy_max=("balanced_accuracy", "max"),
            macro_f1_mean=("macro_f1", "mean"),
            macro_f1_std=("macro_f1", "std"),
            macro_f1_min=("macro_f1", "min"),
            macro_f1_max=("macro_f1", "max"),
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
        "accuracy_min",
        "accuracy_max",
        "balanced_accuracy_mean",
        "balanced_accuracy_std",
        "balanced_accuracy_min",
        "balanced_accuracy_max",
        "macro_f1_mean",
        "macro_f1_std",
        "macro_f1_min",
        "macro_f1_max",
        "fit_seconds_median",
        "predict_seconds_median",
        "total_seconds_median",
    ]
    for column in numeric_columns:
        summary_df[column] = summary_df[column].round(4)

    return summary_df[SUMMARY_COLUMN_ORDER]


def save_outputs(project_root: Path, detail_records: list[dict[str, object]]) -> tuple[Path, Path]:
    detail_df = pd.DataFrame(detail_records)
    if detail_df.empty:
        detail_df = pd.DataFrame(columns=DETAIL_COLUMN_ORDER)
    else:
        detail_df = detail_df[DETAIL_COLUMN_ORDER]

    detail_path = project_root / "results" / DETAIL_OUTPUT_FILENAME
    detail_df.to_csv(detail_path, index=False)

    summary_df = build_summary(detail_df)
    summary_path = project_root / "results" / SUMMARY_OUTPUT_FILENAME
    summary_df.to_csv(summary_path, index=False)
    return detail_path, summary_path


def main() -> None:
    args = parse_args()
    project_root = phase4.resolve_project_root()
    dataset_keys = phase4.normalize_choice_list(args.datasets, phase4.DEFAULT_DATASETS)
    model_keys = phase4.normalize_choice_list(args.models, phase4.DEFAULT_MODELS)
    train_size_labels = normalize_train_size_labels(args.train_sizes)

    if "tabicl" in model_keys:
        checkpoint_path = phase4.ensure_tabicl_checkpoint_available()
        print(f"TabICL checkpoint ready: {checkpoint_path}")
        print()

    detail_records: list[dict[str, object]] = []

    for dataset_key in dataset_keys:
        X, y, cache_path = phase4.load_dataset(project_root, dataset_key)
        categorical_cols, numeric_cols = phase4.get_feature_groups(X)

        print(f"Dataset: {dataset_key}")
        print(f"Loaded data from: {cache_path}")
        print(f"Samples: {len(X)}, raw features: {X.shape[1]}")
        print(f"Categorical features: {len(categorical_cols)}, numeric features: {len(numeric_cols)}")
        print(f"Train sizes: {', '.join(train_size_labels)}")
        print(f"Models: {', '.join(phase4.MODEL_DISPLAY_NAMES[key] for key in model_keys)}")
        print(f"Seeds: {', '.join(str(seed) for seed in args.seeds)}")
        print()

        for train_size_label in train_size_labels:
            for seed in args.seeds:
                print(f"[{dataset_key} | train_size={train_size_label}] Running seed {seed}")
                run_results = run_single_dataset_train_size_seed(
                    dataset_key,
                    train_size_label,
                    seed,
                    model_keys,
                    X,
                    y,
                    cache_path=cache_path,
                    numeric_cols=numeric_cols,
                    categorical_cols=categorical_cols,
                )
                detail_records.extend(run_results)

                for result in run_results:
                    print(
                        {
                            "dataset": result["dataset"],
                            "train_size_label": result["train_size_label"],
                            "train_size": result["train_size"],
                            "seed": result["seed"],
                            "model": result["model"],
                            "accuracy": result["accuracy"],
                            "balanced_accuracy": result["balanced_accuracy"],
                            "macro_f1": result["macro_f1"],
                            "fit_seconds": result["fit_seconds"],
                            "predict_seconds": result["predict_seconds"],
                            "device": result["device"],
                        }
                    )

                detail_path, summary_path = save_outputs(project_root, detail_records)
                print(f"Intermediate detail saved to: {detail_path}")
                print(f"Intermediate summary saved to: {summary_path}")
                print()

    detail_path, summary_path = save_outputs(project_root, detail_records)
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
