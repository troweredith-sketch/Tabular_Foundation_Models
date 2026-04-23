"""Phase 3 experiment: compare LightGBM and TabPFN v2 on Adult."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import pandas as pd
import torch
from lightgbm import LGBMClassifier
from sklearn.compose import ColumnTransformer
from sklearn.datasets import fetch_openml
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from tabpfn import TabPFNClassifier
from tabpfn.constants import ModelVersion

TEST_SIZE = 0.2
TARGET_COL = "class"
CONTROL_TRAIN_SIZE = 10_000
CONTROL_TRAIN_SIZE_FALLBACK = 9_500
DEFAULT_SEEDS = [42, 43, 44, 45, 46]
ALL_SCENARIO = "all"
FULL_SCENARIO = "full_adult_limit_override"
CONTROL_SCENARIO = "adult_control_10k"
DETAIL_OUTPUT_FILENAMES = {
    FULL_SCENARIO: "phase3_adult_compare.csv",
    CONTROL_SCENARIO: "phase3_adult_compare_10k.csv",
}
DETAIL_COLUMN_ORDER = [
    "dataset",
    "scenario",
    "seed",
    "split",
    "model",
    "metric",
    "accuracy",
    "fit_seconds",
    "predict_seconds",
    "total_seconds",
    "device",
    "train_size",
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
    "scenario",
    "model",
    "n_runs",
    "seeds",
    "train_size_min",
    "train_size_max",
    "accuracy_mean",
    "accuracy_std",
    "accuracy_min",
    "accuracy_max",
    "fit_seconds_median",
    "predict_seconds_median",
    "total_seconds_median",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run Phase 3 Adult comparisons across one or both scenarios, "
            "optionally over multiple random seeds."
        ),
    )
    parser.add_argument(
        "--scenario",
        choices=[ALL_SCENARIO, FULL_SCENARIO, CONTROL_SCENARIO],
        default=ALL_SCENARIO,
        help="Which Adult comparison scenario to run. Default runs both scenarios.",
    )
    parser.add_argument(
        "--seeds",
        nargs="+",
        type=int,
        default=DEFAULT_SEEDS,
        help=(
            "Random seeds used for repeated train/test splits. "
            "Default: 42 43 44 45 46."
        ),
    )
    return parser.parse_args()


def resolve_project_root() -> Path:
    current = Path.cwd().resolve()
    if (current / "results").exists():
        return current
    if (current.parent / "results").exists():
        return current.parent
    raise FileNotFoundError("Could not find project root that contains results/.")


def load_adult_dataset(project_root: Path) -> tuple[pd.DataFrame, pd.Series, Path]:
    cache_path = project_root / "data" / "raw" / "adult_openml.csv"

    if cache_path.exists():
        adult_df = pd.read_csv(cache_path)
        X = adult_df.drop(columns=[TARGET_COL]).copy()
        y = adult_df[TARGET_COL].copy()
        return X, y, cache_path

    adult = fetch_openml(name="adult", version=2, as_frame=True)
    X = adult.data.copy()
    y = adult.target.copy()

    adult_df = X.copy()
    adult_df[TARGET_COL] = y
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    adult_df.to_csv(cache_path, index=False)

    return X, y, cache_path


def get_feature_groups(X: pd.DataFrame) -> tuple[list[str], list[str]]:
    categorical_cols = X.select_dtypes(
        include=["category", "object", "string"],
    ).columns.tolist()
    numeric_cols = X.select_dtypes(exclude=["category", "object", "string"]).columns.tolist()
    return categorical_cols, numeric_cols


def build_lightgbm_pipeline(
    numeric_cols: list[str],
    categorical_cols: list[str],
    *,
    seed: int,
) -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                    ]
                ),
                numeric_cols,
            ),
            (
                "cat",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        (
                            "onehot",
                            OneHotEncoder(
                                handle_unknown="ignore",
                                sparse_output=False,
                            ),
                        ),
                    ]
                ),
                categorical_cols,
            ),
        ]
    )
    preprocessor.set_output(transform="pandas")

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                LGBMClassifier(
                    random_state=seed,
                    n_estimators=200,
                    learning_rate=0.05,
                    n_jobs=1,
                    verbose=-1,
                ),
            ),
        ]
    )


def build_tabpfn_preprocessor(
    numeric_cols: list[str],
    categorical_cols: list[str],
) -> ColumnTransformer:
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                    ]
                ),
                numeric_cols,
            ),
            (
                "cat",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        (
                            "ordinal",
                            OrdinalEncoder(
                                handle_unknown="use_encoded_value",
                                unknown_value=-1,
                                encoded_missing_value=-1,
                            ),
                        ),
                    ]
                ),
                categorical_cols,
            ),
        ]
    )
    preprocessor.set_output(transform="pandas")
    return preprocessor


def run_lightgbm(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    numeric_cols: list[str],
    categorical_cols: list[str],
    *,
    seed: int,
    notes: str,
) -> dict[str, object]:
    model = build_lightgbm_pipeline(numeric_cols, categorical_cols, seed=seed)

    fit_start = time.perf_counter()
    model.fit(X_train, y_train)
    fit_seconds = time.perf_counter() - fit_start

    predict_start = time.perf_counter()
    y_pred = model.predict(X_test)
    predict_seconds = time.perf_counter() - predict_start

    encoded_feature_count = len(
        model.named_steps["preprocessor"].get_feature_names_out()
    )

    return {
        "dataset": "adult",
        "model": "LightGBM",
        "metric": "accuracy",
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "fit_seconds": round(fit_seconds, 4),
        "predict_seconds": round(predict_seconds, 4),
        "total_seconds": round(fit_seconds + predict_seconds, 4),
        "device": "cpu",
        "n_features_after_preprocessing": encoded_feature_count,
        "input_representation": "median-impute numeric + one-hot categorical",
        "notes": notes,
    }


def create_tabpfn_model(
    categorical_feature_indices: list[int],
    *,
    seed: int,
    ignore_pretraining_limits: bool,
) -> TabPFNClassifier:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = TabPFNClassifier.create_default_for_version(
        version=ModelVersion.V2,
        device=device,
        categorical_features_indices=categorical_feature_indices,
        ignore_pretraining_limits=ignore_pretraining_limits,
        fit_mode="fit_preprocessors",
        memory_saving_mode="auto",
        random_state=seed,
    )
    return model


def run_tabpfn_v2(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    numeric_cols: list[str],
    categorical_cols: list[str],
    *,
    seed: int,
    ignore_pretraining_limits: bool,
    notes: str,
) -> dict[str, object]:
    preprocessor = build_tabpfn_preprocessor(numeric_cols, categorical_cols)
    X_train_prepared = preprocessor.fit_transform(X_train)
    X_test_prepared = preprocessor.transform(X_test)

    categorical_feature_indices = list(
        range(len(numeric_cols), len(numeric_cols) + len(categorical_cols))
    )
    model = create_tabpfn_model(
        categorical_feature_indices,
        seed=seed,
        ignore_pretraining_limits=ignore_pretraining_limits,
    )

    try:
        fit_start = time.perf_counter()
        model.fit(X_train_prepared, y_train)
        fit_seconds = time.perf_counter() - fit_start

        predict_start = time.perf_counter()
        y_pred = model.predict(X_test_prepared)
        predict_seconds = time.perf_counter() - predict_start
    finally:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    return {
        "dataset": "adult",
        "model": "TabPFN v2",
        "metric": "accuracy",
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "fit_seconds": round(fit_seconds, 4),
        "predict_seconds": round(predict_seconds, 4),
        "total_seconds": round(fit_seconds + predict_seconds, 4),
        "device": "cuda" if torch.cuda.is_available() else "cpu",
        "n_features_after_preprocessing": X_train_prepared.shape[1],
        "input_representation": "median-impute numeric + ordinal categorical",
        "notes": notes,
    }


def make_control_subset(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    *,
    seed: int,
    train_size: int,
) -> tuple[pd.DataFrame, pd.Series]:
    X_train_small, _, y_train_small, _ = train_test_split(
        X_train,
        y_train,
        train_size=train_size,
        random_state=seed,
        stratify=y_train,
    )
    return X_train_small, y_train_small


def get_scenarios(scenario_arg: str) -> list[str]:
    if scenario_arg == ALL_SCENARIO:
        return [FULL_SCENARIO, CONTROL_SCENARIO]
    return [scenario_arg]


def build_split_name(scenario: str, seed: int, train_size: int) -> str:
    if scenario == FULL_SCENARIO:
        return f"adult_fixed_test_seed{seed}_full_train"
    return f"adult_fixed_test_seed{seed}_train{train_size}"


def build_notes(
    scenario: str,
    model_name: str,
    *,
    actual_train_size: int,
    fallback_message: str,
) -> str:
    if scenario == FULL_SCENARIO:
        if model_name == "LightGBM":
            return (
                "Baseline pipeline reused from Phase 2 with seed-specific Adult test set; "
                "this full-train row is retained as a constrained Phase 3 comparison."
            )
        return (
            "Seed-specific fixed test set with full Adult training split; "
            "used ignore_pretraining_limits=True because train size exceeds "
            "the official 10,000-sample support, so this is a constrained result."
        )

    if model_name == "LightGBM":
        base_notes = (
            "Fixed test set + train subset within TabPFN support-range comparison; "
            "LightGBM trained on the same seed-specific Adult train subset."
        )
    else:
        base_notes = (
            "Fixed test set + train subset within support range; "
            "trained without ignore_pretraining_limits=True."
        )

    if fallback_message:
        return (
            f"{base_notes} Requested train_size={CONTROL_TRAIN_SIZE} triggered "
            f"TabPFN fallback: {fallback_message} Fallback train_size="
            f"{CONTROL_TRAIN_SIZE_FALLBACK} was used for both models."
        )

    if actual_train_size != CONTROL_TRAIN_SIZE:
        return (
            f"{base_notes} Effective train_size={actual_train_size} was used for "
            "this seed-specific run."
        )

    return base_notes


def run_single_scenario_seed(
    scenario: str,
    seed: int,
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
        test_size=TEST_SIZE,
        random_state=seed,
        stratify=y,
    )

    fallback_message = ""
    actual_train_size = len(X_train_full)
    ignore_pretraining_limits = scenario == FULL_SCENARIO

    if scenario == CONTROL_SCENARIO:
        X_train, y_train = make_control_subset(
            X_train_full,
            y_train_full,
            seed=seed,
            train_size=CONTROL_TRAIN_SIZE,
        )
        actual_train_size = CONTROL_TRAIN_SIZE
        try:
            tabpfn_result = run_tabpfn_v2(
                X_train=X_train,
                X_test=X_test,
                y_train=y_train,
                y_test=y_test,
                numeric_cols=numeric_cols,
                categorical_cols=categorical_cols,
                seed=seed,
                ignore_pretraining_limits=False,
                notes=build_notes(
                    scenario,
                    "TabPFN v2",
                    actual_train_size=actual_train_size,
                    fallback_message="",
                ),
            )
        except ValueError as exc:
            fallback_message = str(exc)
            X_train, y_train = make_control_subset(
                X_train_full,
                y_train_full,
                seed=seed,
                train_size=CONTROL_TRAIN_SIZE_FALLBACK,
            )
            actual_train_size = CONTROL_TRAIN_SIZE_FALLBACK
            tabpfn_result = run_tabpfn_v2(
                X_train=X_train,
                X_test=X_test,
                y_train=y_train,
                y_test=y_test,
                numeric_cols=numeric_cols,
                categorical_cols=categorical_cols,
                seed=seed,
                ignore_pretraining_limits=False,
                notes=build_notes(
                    scenario,
                    "TabPFN v2",
                    actual_train_size=actual_train_size,
                    fallback_message=fallback_message,
                ),
            )
    else:
        X_train = X_train_full
        y_train = y_train_full
        tabpfn_result = run_tabpfn_v2(
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test,
            numeric_cols=numeric_cols,
            categorical_cols=categorical_cols,
            seed=seed,
            ignore_pretraining_limits=ignore_pretraining_limits,
            notes=build_notes(
                scenario,
                "TabPFN v2",
                actual_train_size=actual_train_size,
                fallback_message="",
            ),
        )

    split_name = build_split_name(scenario, seed, actual_train_size)
    common_fields = {
        "dataset": "adult",
        "scenario": scenario,
        "seed": seed,
        "split": split_name,
        "train_size": actual_train_size,
        "test_size": len(X_test),
        "n_samples_total": len(X),
        "n_features_raw": X.shape[1],
        "n_numeric_features": len(numeric_cols),
        "n_categorical_features": len(categorical_cols),
        "random_state": seed,
        "test_size_ratio": TEST_SIZE,
        "data_cache": str(cache_path),
    }
    lightgbm_result = run_lightgbm(
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        numeric_cols=numeric_cols,
        categorical_cols=categorical_cols,
        seed=seed,
        notes=build_notes(
            scenario,
            "LightGBM",
            actual_train_size=actual_train_size,
            fallback_message=fallback_message,
        ),
    )
    tabpfn_result["notes"] = build_notes(
        scenario,
        "TabPFN v2",
        actual_train_size=actual_train_size,
        fallback_message=fallback_message,
    )

    return [
        {**common_fields, **lightgbm_result},
        {**common_fields, **tabpfn_result},
    ]


def run_scenario(
    scenario: str,
    seeds: list[int],
    project_root: Path,
    X: pd.DataFrame,
    y: pd.Series,
    *,
    cache_path: Path,
    numeric_cols: list[str],
    categorical_cols: list[str],
) -> pd.DataFrame:
    print("Phase 3 Adult comparison")
    print(f"Scenario: {scenario}")
    print(f"Seeds: {', '.join(str(seed) for seed in seeds)}")
    print(f"Loaded data from: {cache_path}")
    print(f"Categorical features: {len(categorical_cols)}, numeric features: {len(numeric_cols)}")
    print()

    scenario_results: list[dict[str, object]] = []
    for seed in seeds:
        print(f"[{scenario}] Running seed {seed}")
        run_results = run_single_scenario_seed(
            scenario,
            seed,
            X,
            y,
            cache_path=cache_path,
            numeric_cols=numeric_cols,
            categorical_cols=categorical_cols,
        )
        scenario_results.extend(run_results)
        for result in run_results:
            print(
                {
                    "seed": result["seed"],
                    "model": result["model"],
                    "accuracy": result["accuracy"],
                    "fit_seconds": result["fit_seconds"],
                    "predict_seconds": result["predict_seconds"],
                    "train_size": result["train_size"],
                    "device": result["device"],
                }
            )
        print()

    scenario_df = pd.DataFrame(scenario_results)[DETAIL_COLUMN_ORDER]
    output_path = project_root / "results" / DETAIL_OUTPUT_FILENAMES[scenario]
    scenario_df.to_csv(output_path, index=False)

    print(f"Saved scenario results to: {output_path}")
    print(
        scenario_df[
            ["scenario", "seed", "model", "accuracy", "fit_seconds", "predict_seconds"]
        ]
    )
    print()
    return scenario_df


def load_detail_results(project_root: Path) -> list[pd.DataFrame]:
    frames: list[pd.DataFrame] = []
    for scenario, filename in DETAIL_OUTPUT_FILENAMES.items():
        path = project_root / "results" / filename
        if not path.exists():
            continue
        detail_df = pd.read_csv(path)
        missing_columns = [col for col in DETAIL_COLUMN_ORDER if col not in detail_df.columns]
        if missing_columns:
            print(
                f"Skipping {path} when building summary because it is missing "
                f"columns: {', '.join(missing_columns)}"
            )
            continue
        detail_df = detail_df[DETAIL_COLUMN_ORDER].copy()
        detail_df["scenario"] = scenario
        frames.append(detail_df)
    return frames


def build_summary(detail_frames: list[pd.DataFrame]) -> pd.DataFrame:
    if not detail_frames:
        return pd.DataFrame(columns=SUMMARY_COLUMN_ORDER)

    detail_df = pd.concat(detail_frames, ignore_index=True)
    summary_df = (
        detail_df.groupby(["scenario", "model"], as_index=False)
        .agg(
            n_runs=("seed", "nunique"),
            seeds=("seed", lambda values: ",".join(str(seed) for seed in sorted(set(values)))),
            train_size_min=("train_size", "min"),
            train_size_max=("train_size", "max"),
            accuracy_mean=("accuracy", "mean"),
            accuracy_std=("accuracy", "std"),
            accuracy_min=("accuracy", "min"),
            accuracy_max=("accuracy", "max"),
            fit_seconds_median=("fit_seconds", "median"),
            predict_seconds_median=("predict_seconds", "median"),
            total_seconds_median=("total_seconds", "median"),
        )
    )
    summary_df["accuracy_std"] = summary_df["accuracy_std"].fillna(0.0)

    numeric_columns = [
        "accuracy_mean",
        "accuracy_std",
        "accuracy_min",
        "accuracy_max",
        "fit_seconds_median",
        "predict_seconds_median",
        "total_seconds_median",
    ]
    for column in numeric_columns:
        summary_df[column] = summary_df[column].round(4)

    return summary_df[SUMMARY_COLUMN_ORDER]


def main() -> None:
    args = parse_args()
    project_root = resolve_project_root()
    X, y, cache_path = load_adult_dataset(project_root)
    categorical_cols, numeric_cols = get_feature_groups(X)

    for scenario in get_scenarios(args.scenario):
        run_scenario(
            scenario,
            args.seeds,
            project_root,
            X,
            y,
            cache_path=cache_path,
            numeric_cols=numeric_cols,
            categorical_cols=categorical_cols,
        )

    summary_df = build_summary(load_detail_results(project_root))
    summary_path = project_root / "results" / "phase3_adult_compare_summary.csv"
    summary_df.to_csv(summary_path, index=False)

    print("Saved summary results to:", summary_path)
    if summary_df.empty:
        print("Summary is empty because no detail result files were available.")
    else:
        print()
        print(summary_df)


if __name__ == "__main__":
    main()
