"""Phase 4 experiment: unified four-model comparison on Adult and Bank Marketing."""

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
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
from tabicl import TabICLClassifier
from tabpfn import TabPFNClassifier
from tabpfn.constants import ModelVersion
from xgboost import XGBClassifier

TEST_SIZE = 0.2
CONTROL_TRAIN_SIZE = 10_000
CONTROL_TRAIN_SIZE_FALLBACK = 9_500
DEFAULT_SEEDS = [42, 43, 44, 45, 46]
DEFAULT_DATASETS = ["adult", "bank_marketing"]
DEFAULT_MODELS = ["lightgbm", "xgboost", "tabpfn_v2", "tabicl"]
ALL_TOKEN = "all"
CONTROL_SCENARIO = "control_10k"
FULL_SCENARIO = "full_train_reference"
DETAIL_OUTPUT_FILENAME = "phase4_mainline_compare.csv"
SUMMARY_OUTPUT_FILENAME = "phase4_mainline_compare_summary.csv"
TABICL_CHECKPOINT_VERSION = "tabicl-classifier-v2-20260212.ckpt"
MODEL_DISPLAY_NAMES = {
    "lightgbm": "LightGBM",
    "xgboost": "XGBoost",
    "tabpfn_v2": "TabPFN v2",
    "tabicl": "TabICL",
}
DATASET_CONFIGS = {
    "adult": {
        "openml_name": "adult",
        "version": 2,
        "target_col": "class",
        "cache_path": Path("data/raw/adult_openml.csv"),
    },
    "bank_marketing": {
        "openml_name": "bank-marketing",
        "version": 1,
        "target_col": "Class",
        "cache_path": Path("data/raw/bank_marketing_openml.csv"),
    },
}
DETAIL_COLUMN_ORDER = [
    "dataset",
    "scenario",
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
    "dataset",
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
            "Run Phase 4 unified comparisons across Adult and Bank Marketing "
            "with LightGBM, XGBoost, TabPFN v2, and TabICL."
        ),
    )
    parser.add_argument(
        "--datasets",
        nargs="+",
        default=[ALL_TOKEN],
        choices=[ALL_TOKEN, *DATASET_CONFIGS.keys()],
        help="Datasets to run. Default: all.",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=[ALL_TOKEN],
        choices=[ALL_TOKEN, *MODEL_DISPLAY_NAMES.keys()],
        help="Models to run. Default: all four models.",
    )
    parser.add_argument(
        "--scenarios",
        nargs="+",
        default=[ALL_TOKEN],
        choices=[ALL_TOKEN, CONTROL_SCENARIO, FULL_SCENARIO],
        help="Scenarios to run. Default: both control_10k and full_train_reference.",
    )
    parser.add_argument(
        "--seeds",
        nargs="+",
        type=int,
        default=DEFAULT_SEEDS,
        help="Random seeds used for repeated train/test splits. Default: 42 43 44 45 46.",
    )
    return parser.parse_args()


def resolve_project_root() -> Path:
    current = Path.cwd().resolve()
    if (current / "results").exists():
        return current
    if (current.parent / "results").exists():
        return current.parent
    raise FileNotFoundError("Could not find project root that contains results/.")


def normalize_choice_list(values: list[str], defaults: list[str]) -> list[str]:
    if ALL_TOKEN in values:
        return defaults
    return values


def load_dataset(project_root: Path, dataset_key: str) -> tuple[pd.DataFrame, pd.Series, Path]:
    config = DATASET_CONFIGS[dataset_key]
    cache_path = project_root / config["cache_path"]
    target_col = config["target_col"]

    if cache_path.exists():
        dataset_df = pd.read_csv(cache_path)
        X = dataset_df.drop(columns=[target_col]).copy()
        y = dataset_df[target_col].copy()
        return X, y, cache_path

    dataset = fetch_openml(name=config["openml_name"], version=config["version"], as_frame=True)
    X = dataset.data.copy()
    y = dataset.target.copy()

    dataset_df = X.copy()
    dataset_df[target_col] = y
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    dataset_df.to_csv(cache_path, index=False)

    return X, y, cache_path


def get_feature_groups(X: pd.DataFrame) -> tuple[list[str], list[str]]:
    categorical_cols = X.select_dtypes(
        include=["category", "object", "string", "bool", "boolean"],
    ).columns.tolist()
    numeric_cols = X.select_dtypes(
        exclude=["category", "object", "string", "bool", "boolean"],
    ).columns.tolist()
    return categorical_cols, numeric_cols


def calculate_classification_metrics(y_true: object, y_pred: object) -> dict[str, object]:
    return {
        "metric": "accuracy",
        "accuracy": round(accuracy_score(y_true, y_pred), 4),
        "balanced_accuracy": round(balanced_accuracy_score(y_true, y_pred), 4),
        "macro_f1": round(f1_score(y_true, y_pred, average="macro", zero_division=0), 4),
    }


def build_tree_preprocessor(
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
    return preprocessor


def build_lightgbm_pipeline(
    numeric_cols: list[str],
    categorical_cols: list[str],
    *,
    seed: int,
) -> Pipeline:
    return Pipeline(
        steps=[
            ("preprocessor", build_tree_preprocessor(numeric_cols, categorical_cols)),
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


def build_xgboost_pipeline(
    numeric_cols: list[str],
    categorical_cols: list[str],
    *,
    seed: int,
) -> Pipeline:
    return Pipeline(
        steps=[
            ("preprocessor", build_tree_preprocessor(numeric_cols, categorical_cols)),
            (
                "classifier",
                XGBClassifier(
                    random_state=seed,
                    n_estimators=200,
                    learning_rate=0.05,
                    max_depth=6,
                    n_jobs=1,
                    tree_method="hist",
                    objective="binary:logistic",
                    eval_metric="logloss",
                    verbosity=0,
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


def create_tabpfn_model(
    categorical_feature_indices: list[int],
    *,
    seed: int,
    ignore_pretraining_limits: bool,
) -> TabPFNClassifier:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return TabPFNClassifier.create_default_for_version(
        version=ModelVersion.V2,
        device=device,
        categorical_features_indices=categorical_feature_indices,
        ignore_pretraining_limits=ignore_pretraining_limits,
        fit_mode="fit_preprocessors",
        memory_saving_mode="auto",
        random_state=seed,
    )


def ensure_tabicl_checkpoint_available() -> Path:
    probe = TabICLClassifier(
        checkpoint_version=TABICL_CHECKPOINT_VERSION,
        allow_auto_download=True,
        device="cuda" if torch.cuda.is_available() else "cpu",
        n_jobs=1,
        verbose=False,
    )
    probe._load_model()  # noqa: SLF001 - warming the official checkpoint avoids polluting fit timing.
    model_path = probe.model_path_
    del probe
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return model_path


def create_tabicl_model(*, seed: int) -> TabICLClassifier:
    return TabICLClassifier(
        checkpoint_version=TABICL_CHECKPOINT_VERSION,
        allow_auto_download=True,
        device="cuda" if torch.cuda.is_available() else "cpu",
        batch_size=8,
        kv_cache=False,
        random_state=seed,
        n_jobs=1,
        verbose=False,
    )


def run_lightgbm(
    dataset_key: str,
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

    encoded_feature_count = len(model.named_steps["preprocessor"].get_feature_names_out())

    return {
        "dataset": dataset_key,
        "model": MODEL_DISPLAY_NAMES["lightgbm"],
        **calculate_classification_metrics(y_test, y_pred),
        "fit_seconds": round(fit_seconds, 4),
        "predict_seconds": round(predict_seconds, 4),
        "total_seconds": round(fit_seconds + predict_seconds, 4),
        "device": "cpu",
        "n_features_after_preprocessing": encoded_feature_count,
        "input_representation": "median-impute numeric + one-hot categorical",
        "notes": notes,
    }


def run_xgboost(
    dataset_key: str,
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
    model = build_xgboost_pipeline(numeric_cols, categorical_cols, seed=seed)
    target_encoder = LabelEncoder()
    y_train_encoded = target_encoder.fit_transform(y_train)
    y_test_encoded = target_encoder.transform(y_test)

    fit_start = time.perf_counter()
    model.fit(X_train, y_train_encoded)
    fit_seconds = time.perf_counter() - fit_start

    predict_start = time.perf_counter()
    y_pred_encoded = model.predict(X_test)
    predict_seconds = time.perf_counter() - predict_start

    encoded_feature_count = len(model.named_steps["preprocessor"].get_feature_names_out())

    return {
        "dataset": dataset_key,
        "model": MODEL_DISPLAY_NAMES["xgboost"],
        **calculate_classification_metrics(y_test_encoded, y_pred_encoded),
        "fit_seconds": round(fit_seconds, 4),
        "predict_seconds": round(predict_seconds, 4),
        "total_seconds": round(fit_seconds + predict_seconds, 4),
        "device": "cpu",
        "n_features_after_preprocessing": encoded_feature_count,
        "input_representation": "median-impute numeric + one-hot categorical",
        "notes": notes,
    }


def run_tabpfn_v2(
    dataset_key: str,
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
        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    return {
        "dataset": dataset_key,
        "model": MODEL_DISPLAY_NAMES["tabpfn_v2"],
        **calculate_classification_metrics(y_test, y_pred),
        "fit_seconds": round(fit_seconds, 4),
        "predict_seconds": round(predict_seconds, 4),
        "total_seconds": round(fit_seconds + predict_seconds, 4),
        "device": "cuda" if torch.cuda.is_available() else "cpu",
        "n_features_after_preprocessing": X_train_prepared.shape[1],
        "input_representation": "median-impute numeric + ordinal categorical",
        "notes": notes,
    }


def run_tabicl(
    dataset_key: str,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    *,
    seed: int,
    notes: str,
) -> dict[str, object]:
    model = create_tabicl_model(seed=seed)

    try:
        fit_start = time.perf_counter()
        model.fit(X_train, y_train)
        fit_seconds = time.perf_counter() - fit_start

        predict_start = time.perf_counter()
        y_pred = model.predict(X_test)
        predict_seconds = time.perf_counter() - predict_start

        transformed_train = model.X_encoder_.transform(X_train)
    finally:
        resolved_device = str(getattr(model, "device_", model.device))
        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    return {
        "dataset": dataset_key,
        "model": MODEL_DISPLAY_NAMES["tabicl"],
        **calculate_classification_metrics(y_test, y_pred),
        "fit_seconds": round(fit_seconds, 4),
        "predict_seconds": round(predict_seconds, 4),
        "total_seconds": round(fit_seconds + predict_seconds, 4),
        "device": resolved_device,
        "n_features_after_preprocessing": transformed_train.shape[1],
        "input_representation": (
            "TabICL TransformToNumerical (ordinal categorical + default numeric imputation)"
        ),
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


def build_split_name(dataset_key: str, scenario: str, seed: int, train_size: int) -> str:
    dataset_prefix = dataset_key.replace("-", "_")
    if scenario == FULL_SCENARIO:
        return f"{dataset_prefix}_fixed_test_seed{seed}_full_train"
    return f"{dataset_prefix}_fixed_test_seed{seed}_train{train_size}"


def build_notes(
    scenario: str,
    model_key: str,
    *,
    actual_train_size: int,
    fallback_message: str,
) -> str:
    if scenario == FULL_SCENARIO:
        if model_key == "tabpfn_v2":
            return (
                "Full-train reference row; used ignore_pretraining_limits=True because "
                "train size exceeds the official 10,000-sample support, so this is a "
                "constrained result."
            )
        if model_key == "tabicl":
            return (
                "Full-train reference row; uses TabICLClassifier with the official "
                f"{TABICL_CHECKPOINT_VERSION} checkpoint and internal TransformToNumerical."
            )
        return "Full-train reference row in the unified Phase 4 mainline table."

    if model_key == "tabpfn_v2":
        base_notes = (
            "Fixed test set + seed-specific 10k train subset within TabPFN support range; "
            "trained without ignore_pretraining_limits=True."
        )
    elif model_key == "tabicl":
        base_notes = (
            "Fixed test set + seed-specific 10k train subset; uses TabICLClassifier with "
            f"the official {TABICL_CHECKPOINT_VERSION} checkpoint."
        )
    else:
        base_notes = "Fixed test set + seed-specific 10k train subset in the unified Phase 4 mainline table."

    if fallback_message:
        return (
            f"{base_notes} Requested train_size={CONTROL_TRAIN_SIZE} triggered TabPFN fallback: "
            f"{fallback_message} Fallback train_size={CONTROL_TRAIN_SIZE_FALLBACK} was used for all models."
        )

    if actual_train_size != CONTROL_TRAIN_SIZE:
        return f"{base_notes} Effective train_size={actual_train_size} was used for this run."

    return base_notes


def run_models_for_configuration(
    dataset_key: str,
    model_keys: list[str],
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    numeric_cols: list[str],
    categorical_cols: list[str],
    *,
    scenario: str,
    seed: int,
    actual_train_size: int,
    fallback_message: str,
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []

    for model_key in model_keys:
        notes = build_notes(
            scenario,
            model_key,
            actual_train_size=actual_train_size,
            fallback_message=fallback_message,
        )

        if model_key == "lightgbm":
            result = run_lightgbm(
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
            result = run_xgboost(
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
            result = run_tabpfn_v2(
                dataset_key,
                X_train,
                X_test,
                y_train,
                y_test,
                numeric_cols,
                categorical_cols,
                seed=seed,
                ignore_pretraining_limits=scenario == FULL_SCENARIO,
                notes=notes,
            )
        elif model_key == "tabicl":
            result = run_tabicl(
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


def run_single_dataset_scenario_seed(
    dataset_key: str,
    scenario: str,
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
        test_size=TEST_SIZE,
        random_state=seed,
        stratify=y,
    )

    fallback_message = ""
    actual_train_size = len(X_train_full)

    if scenario == CONTROL_SCENARIO:
        X_train, y_train = make_control_subset(
            X_train_full,
            y_train_full,
            seed=seed,
            train_size=CONTROL_TRAIN_SIZE,
        )
        actual_train_size = CONTROL_TRAIN_SIZE
    else:
        X_train = X_train_full
        y_train = y_train_full

    common_fields = {
        "dataset": dataset_key,
        "scenario": scenario,
        "seed": seed,
        "split": build_split_name(dataset_key, scenario, seed, actual_train_size),
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

    model_results = run_models_for_configuration(
        dataset_key,
        model_keys,
        X_train,
        X_test,
        y_train,
        y_test,
        numeric_cols,
        categorical_cols,
        scenario=scenario,
        seed=seed,
        actual_train_size=actual_train_size,
        fallback_message=fallback_message,
    )

    return [{**common_fields, **result} for result in model_results]


def build_summary(detail_df: pd.DataFrame) -> pd.DataFrame:
    if detail_df.empty:
        return pd.DataFrame(columns=SUMMARY_COLUMN_ORDER)

    summary_df = (
        detail_df.groupby(["dataset", "scenario", "model"], as_index=False)
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
    project_root = resolve_project_root()
    dataset_keys = normalize_choice_list(args.datasets, DEFAULT_DATASETS)
    model_keys = normalize_choice_list(args.models, DEFAULT_MODELS)
    scenarios = normalize_choice_list(args.scenarios, [CONTROL_SCENARIO, FULL_SCENARIO])

    if "tabicl" in model_keys:
        checkpoint_path = ensure_tabicl_checkpoint_available()
        print(f"TabICL checkpoint ready: {checkpoint_path}")
        print()

    detail_records: list[dict[str, object]] = []

    for dataset_key in dataset_keys:
        X, y, cache_path = load_dataset(project_root, dataset_key)
        categorical_cols, numeric_cols = get_feature_groups(X)

        print(f"Dataset: {dataset_key}")
        print(f"Loaded data from: {cache_path}")
        print(f"Samples: {len(X)}, raw features: {X.shape[1]}")
        print(f"Categorical features: {len(categorical_cols)}, numeric features: {len(numeric_cols)}")
        print(f"Scenarios: {', '.join(scenarios)}")
        print(f"Models: {', '.join(MODEL_DISPLAY_NAMES[key] for key in model_keys)}")
        print(f"Seeds: {', '.join(str(seed) for seed in args.seeds)}")
        print()

        for scenario in scenarios:
            for seed in args.seeds:
                print(f"[{dataset_key} | {scenario}] Running seed {seed}")
                run_results = run_single_dataset_scenario_seed(
                    dataset_key,
                    scenario,
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
                            "scenario": result["scenario"],
                            "seed": result["seed"],
                            "model": result["model"],
                            "accuracy": result["accuracy"],
                            "balanced_accuracy": result["balanced_accuracy"],
                            "macro_f1": result["macro_f1"],
                            "fit_seconds": result["fit_seconds"],
                            "predict_seconds": result["predict_seconds"],
                            "train_size": result["train_size"],
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
