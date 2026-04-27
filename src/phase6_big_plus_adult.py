"""Phase 6 Big Plus experiment: TabICL support-set selection on Adult."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import phase4_mainline_compare as phase4

DATASET_KEY = "adult"
MODEL_KEY = "tabicl"
ALL_TOKEN = "all"
FULL_CONTEXT = "full_context"
RANDOM_SUBSET = "random_subset"
BALANCED_RANDOM_SUBSET = "balanced_random_subset"
BALANCED_PROTOTYPE_RETRIEVAL = "balanced_prototype_retrieval"
DEFAULT_STRATEGIES = [
    FULL_CONTEXT,
    RANDOM_SUBSET,
    BALANCED_RANDOM_SUBSET,
    BALANCED_PROTOTYPE_RETRIEVAL,
]
DEFAULT_BUDGETS = [512]
DEFAULT_SEEDS = [42]
FINAL_BUDGETS = [512, 2048, 8192]
FINAL_SEEDS = [42, 43, 44]
DETAIL_OUTPUT_FILENAME = "phase6_big_plus_adult.csv"
SUMMARY_OUTPUT_FILENAME = "phase6_big_plus_adult_summary.csv"
STRATEGY_DISPLAY_NAMES = {
    FULL_CONTEXT: "Full Context",
    RANDOM_SUBSET: "Random Subset",
    BALANCED_RANDOM_SUBSET: "Balanced Random Subset",
    BALANCED_PROTOTYPE_RETRIEVAL: "Balanced Prototype Retrieval",
}

DETAIL_COLUMN_ORDER = [
    "dataset",
    "seed",
    "split",
    "strategy",
    "strategy_display",
    "budget",
    "requested_budget",
    "actual_support_size",
    "support_class_counts",
    "model",
    "metric",
    "accuracy",
    "balanced_accuracy",
    "macro_f1",
    "fit_seconds",
    "predict_seconds",
    "total_seconds",
    "selection_seconds",
    "end_to_end_seconds",
    "device",
    "full_train_size",
    "test_size",
    "n_samples_total",
    "n_features_raw",
    "n_numeric_features",
    "n_categorical_features",
    "n_features_after_preprocessing",
    "retrieval_n_features_after_encoding",
    "random_state",
    "test_size_ratio",
    "data_cache",
    "input_representation",
    "selection_method",
    "notes",
]

SUMMARY_COLUMN_ORDER = [
    "dataset",
    "strategy",
    "strategy_display",
    "budget",
    "model",
    "n_runs",
    "seeds",
    "requested_budget",
    "requested_budget_min",
    "requested_budget_max",
    "actual_support_size",
    "actual_support_size_min",
    "actual_support_size_max",
    "support_class_counts",
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
    "selection_seconds_median",
    "end_to_end_seconds_median",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run Phase 6 Adult-only TabICL support-set selection experiments. "
            "Default arguments run the smoke preset: all strategies, budget 512, seed 42, "
            "saved under results/smoke/."
        ),
    )
    parser.add_argument(
        "--preset",
        choices=["smoke", "final"],
        default="smoke",
        help=(
            "Preset for default budgets, seeds, and output directory. "
            "Use --preset final to reproduce the committed Phase 6 result files."
        ),
    )
    parser.add_argument(
        "--strategies",
        nargs="+",
        default=[ALL_TOKEN],
        choices=[ALL_TOKEN, *DEFAULT_STRATEGIES],
        help="Support-set strategies to run. Default: all four strategies.",
    )
    parser.add_argument(
        "--budgets",
        nargs="+",
        type=int,
        default=None,
        help=(
            "Support-set budgets for budget-limited strategies. "
            "Default: 512 for smoke, 512 2048 8192 for final."
        ),
    )
    parser.add_argument(
        "--seeds",
        nargs="+",
        type=int,
        default=None,
        help=(
            "Random seeds used for repeated stratified splits. "
            "Default: 42 for smoke, 42 43 44 for final."
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help=(
            "Directory for CSV outputs. Relative paths are resolved from project root. "
            "Default: results/smoke for smoke, results for final."
        ),
    )
    return parser.parse_args()


def normalize_strategies(values: list[str]) -> list[str]:
    if ALL_TOKEN in values:
        return DEFAULT_STRATEGIES
    return values


def normalize_budgets(values: list[int]) -> list[int]:
    budgets = sorted(set(values))
    if not budgets:
        raise ValueError("At least one budget is required.")
    invalid = [budget for budget in budgets if budget <= 0]
    if invalid:
        raise ValueError(f"Budgets must be positive integers, got: {invalid}.")
    return budgets


def resolve_preset_defaults(args: argparse.Namespace) -> tuple[list[int], list[int], Path]:
    budgets = args.budgets
    seeds = args.seeds
    output_dir = args.output_dir

    if args.preset == "final":
        if budgets is None:
            budgets = FINAL_BUDGETS
        if seeds is None:
            seeds = FINAL_SEEDS
        if output_dir is None:
            output_dir = Path("results")
    else:
        if budgets is None:
            budgets = DEFAULT_BUDGETS
        if seeds is None:
            seeds = DEFAULT_SEEDS
        if output_dir is None:
            output_dir = Path("results") / "smoke"

    return normalize_budgets(budgets), sorted(set(seeds)), output_dir


def class_counts_json(y: pd.Series) -> str:
    counts = y.value_counts()
    ordered = {str(label): int(counts[label]) for label in sorted(counts.index, key=str)}
    return json.dumps(ordered, sort_keys=True, ensure_ascii=True)


def sorted_labels(y: pd.Series) -> list[Any]:
    return sorted(pd.unique(y), key=str)


def allocate_class_quotas(y: pd.Series, requested_budget: int) -> dict[Any, int]:
    labels = sorted_labels(y)
    if not labels:
        raise ValueError("Cannot allocate class quotas for an empty support pool.")

    effective_budget = min(requested_budget, len(y))
    counts = {label: int((y == label).sum()) for label in labels}
    base = effective_budget // len(labels)
    quotas = {label: min(base, counts[label]) for label in labels}
    remaining = effective_budget - sum(quotas.values())

    while remaining > 0:
        candidates = [label for label in labels if quotas[label] < counts[label]]
        if not candidates:
            break

        total_candidate_count = sum(counts[label] for label in candidates)
        floor_additions: dict[Any, int] = {}
        fractional_parts: list[tuple[float, int, str, Any]] = []

        for label in candidates:
            capacity = counts[label] - quotas[label]
            raw_share = remaining * counts[label] / total_candidate_count
            floor_add = min(int(np.floor(raw_share)), capacity)
            floor_additions[label] = floor_add
            fractional_parts.append((raw_share - floor_add, counts[label], str(label), label))

        floor_total = sum(floor_additions.values())
        if floor_total > 0:
            for label, addition in floor_additions.items():
                quotas[label] += addition
            remaining -= floor_total

        fractional_parts.sort(key=lambda item: (-item[0], -item[1], item[2]))
        for _, _, _, label in fractional_parts:
            if remaining <= 0:
                break
            if quotas[label] >= counts[label]:
                continue
            quotas[label] += 1
            remaining -= 1

    return quotas


def selected_positions_to_support(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    selected_positions: np.ndarray,
) -> tuple[pd.DataFrame, pd.Series]:
    selected_positions = np.array(sorted(int(position) for position in selected_positions))
    return X_train.iloc[selected_positions].copy(), y_train.iloc[selected_positions].copy()


def select_random_subset(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    *,
    budget: int,
    seed: int,
) -> tuple[pd.DataFrame, pd.Series]:
    actual_budget = min(budget, len(X_train))
    rng = np.random.default_rng(seed)
    selected_positions = rng.choice(len(X_train), size=actual_budget, replace=False)
    return selected_positions_to_support(X_train, y_train, selected_positions)


def select_balanced_random_subset(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    *,
    budget: int,
    seed: int,
) -> tuple[pd.DataFrame, pd.Series]:
    rng = np.random.default_rng(seed)
    quotas = allocate_class_quotas(y_train, budget)
    selected_positions: list[int] = []

    for label in sorted(quotas, key=str):
        label_positions = np.flatnonzero((y_train == label).to_numpy())
        quota = quotas[label]
        if quota <= 0:
            continue
        sampled_positions = rng.choice(label_positions, size=quota, replace=False)
        selected_positions.extend(int(position) for position in sampled_positions)

    return selected_positions_to_support(X_train, y_train, np.array(selected_positions))


def build_retrieval_preprocessor(
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
                        ("scaler", StandardScaler()),
                    ]
                ),
                numeric_cols,
            ),
            (
                "cat",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
                    ]
                ),
                categorical_cols,
            ),
        ]
    )
    return preprocessor


def select_balanced_prototype_retrieval(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    numeric_cols: list[str],
    categorical_cols: list[str],
    *,
    budget: int,
) -> tuple[pd.DataFrame, pd.Series, int]:
    quotas = allocate_class_quotas(y_train, budget)
    retrieval_preprocessor = build_retrieval_preprocessor(numeric_cols, categorical_cols)
    retrieval_matrix = retrieval_preprocessor.fit_transform(X_train)
    retrieval_matrix = np.asarray(retrieval_matrix, dtype=np.float64)
    selected_positions: list[int] = []

    for label in sorted(quotas, key=str):
        quota = quotas[label]
        if quota <= 0:
            continue

        label_positions = np.flatnonzero((y_train == label).to_numpy())
        label_vectors = retrieval_matrix[label_positions]
        class_center = label_vectors.mean(axis=0)
        distances = np.linalg.norm(label_vectors - class_center, axis=1)
        order = np.lexsort((label_positions, distances))
        selected_positions.extend(int(position) for position in label_positions[order[:quota]])

    X_support, y_support = selected_positions_to_support(
        X_train,
        y_train,
        np.array(selected_positions),
    )
    return X_support, y_support, retrieval_matrix.shape[1]


def build_split_name(seed: int) -> str:
    return f"adult_fixed_test_seed{seed}_phase6_support_selection"


def build_notes(strategy: str, budget_label: str, actual_support_size: int) -> str:
    base = (
        "Phase 6 Big Plus Adult TabICL support-set selection row; "
        f"strategy={STRATEGY_DISPLAY_NAMES[strategy]}."
    )
    if strategy == FULL_CONTEXT:
        return (
            f"{base} Full Context uses the complete seed-specific training split "
            f"as a budget-independent reference with support_size={actual_support_size}."
        )
    if strategy == RANDOM_SUBSET:
        return (
            f"{base} Random Subset samples budget={budget_label} examples without replacement "
            "from the training split using the experiment seed."
        )
    if strategy == BALANCED_RANDOM_SUBSET:
        return (
            f"{base} Balanced Random Subset uses the frozen class quota rule, then samples "
            f"within each class for budget={budget_label} using the experiment seed."
        )
    return (
        f"{base} Balanced Prototype Retrieval uses train-only median/mode imputation, "
        "numeric standardization, one-hot categorical encoding, Euclidean distance to "
        f"class centers, and the frozen class quota rule for budget={budget_label}."
    )


def make_support_set(
    strategy: str,
    budget: int | None,
    X_train_full: pd.DataFrame,
    y_train_full: pd.Series,
    numeric_cols: list[str],
    categorical_cols: list[str],
    *,
    seed: int,
) -> tuple[pd.DataFrame, pd.Series, str, int, int, int | None]:
    if strategy == FULL_CONTEXT:
        return (
            X_train_full.copy(),
            y_train_full.copy(),
            "full",
            len(X_train_full),
            len(X_train_full),
            None,
        )

    if budget is None:
        raise ValueError(f"Strategy {strategy} requires an integer budget.")

    if strategy == RANDOM_SUBSET:
        X_support, y_support = select_random_subset(
            X_train_full,
            y_train_full,
            budget=budget,
            seed=seed,
        )
        return X_support, y_support, str(budget), budget, len(y_support), None

    if strategy == BALANCED_RANDOM_SUBSET:
        X_support, y_support = select_balanced_random_subset(
            X_train_full,
            y_train_full,
            budget=budget,
            seed=seed,
        )
        return X_support, y_support, str(budget), budget, len(y_support), None

    if strategy == BALANCED_PROTOTYPE_RETRIEVAL:
        X_support, y_support, retrieval_feature_count = select_balanced_prototype_retrieval(
            X_train_full,
            y_train_full,
            numeric_cols,
            categorical_cols,
            budget=budget,
        )
        return X_support, y_support, str(budget), budget, len(y_support), retrieval_feature_count

    raise ValueError(f"Unsupported strategy: {strategy}")


def run_strategy(
    strategy: str,
    budget: int | None,
    X_train_full: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train_full: pd.Series,
    y_test: pd.Series,
    numeric_cols: list[str],
    categorical_cols: list[str],
    *,
    seed: int,
) -> dict[str, object]:
    selection_start = time.perf_counter()
    (
        X_support,
        y_support,
        budget_label,
        requested_budget,
        actual_support_size,
        retrieval_feature_count,
    ) = make_support_set(
        strategy,
        budget,
        X_train_full,
        y_train_full,
        numeric_cols,
        categorical_cols,
        seed=seed,
    )
    selection_seconds = time.perf_counter() - selection_start

    notes = build_notes(strategy, budget_label, actual_support_size)
    result = phase4.run_tabicl(
        DATASET_KEY,
        X_support,
        X_test,
        y_support,
        y_test,
        seed=seed,
        notes=notes,
    )

    return {
        "strategy": strategy,
        "strategy_display": STRATEGY_DISPLAY_NAMES[strategy],
        "budget": budget_label,
        "requested_budget": requested_budget,
        "actual_support_size": actual_support_size,
        "support_class_counts": class_counts_json(y_support),
        "retrieval_n_features_after_encoding": retrieval_feature_count,
        "selection_method": strategy,
        "selection_seconds": round(selection_seconds, 4),
        "end_to_end_seconds": round(selection_seconds + float(result["total_seconds"]), 4),
        **result,
    }


def run_seed(
    X: pd.DataFrame,
    y: pd.Series,
    strategies: list[str],
    budgets: list[int],
    *,
    seed: int,
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

    common_fields = {
        "dataset": DATASET_KEY,
        "seed": seed,
        "split": build_split_name(seed),
        "full_train_size": len(X_train_full),
        "test_size": len(X_test),
        "n_samples_total": len(X),
        "n_features_raw": X.shape[1],
        "n_numeric_features": len(numeric_cols),
        "n_categorical_features": len(categorical_cols),
        "random_state": seed,
        "test_size_ratio": phase4.TEST_SIZE,
        "data_cache": phase4.format_project_path(cache_path),
    }

    seed_results: list[dict[str, object]] = []

    if FULL_CONTEXT in strategies:
        result = run_strategy(
            FULL_CONTEXT,
            None,
            X_train_full,
            X_test,
            y_train_full,
            y_test,
            numeric_cols,
            categorical_cols,
            seed=seed,
        )
        seed_results.append({**common_fields, **result})

    budget_strategies = [strategy for strategy in strategies if strategy != FULL_CONTEXT]
    for budget in budgets:
        for strategy in budget_strategies:
            result = run_strategy(
                strategy,
                budget,
                X_train_full,
                X_test,
                y_train_full,
                y_test,
                numeric_cols,
                categorical_cols,
                seed=seed,
            )
            seed_results.append({**common_fields, **result})

    return seed_results


def build_summary(detail_df: pd.DataFrame) -> pd.DataFrame:
    if detail_df.empty:
        return pd.DataFrame(columns=SUMMARY_COLUMN_ORDER)

    summary_df = (
        detail_df.groupby(["dataset", "strategy", "strategy_display", "budget", "model"], as_index=False)
        .agg(
            n_runs=("seed", "nunique"),
            seeds=("seed", lambda values: ",".join(str(seed) for seed in sorted(set(values)))),
            requested_budget=("requested_budget", "first"),
            requested_budget_min=("requested_budget", "min"),
            requested_budget_max=("requested_budget", "max"),
            actual_support_size=("actual_support_size", "first"),
            actual_support_size_min=("actual_support_size", "min"),
            actual_support_size_max=("actual_support_size", "max"),
            support_class_counts=(
                "support_class_counts",
                lambda values: "; ".join(sorted(set(str(value) for value in values))),
            ),
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
            selection_seconds_median=("selection_seconds", "median"),
            end_to_end_seconds_median=("end_to_end_seconds", "median"),
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
        "selection_seconds_median",
        "end_to_end_seconds_median",
    ]
    for column in numeric_columns:
        summary_df[column] = summary_df[column].round(4)

    return summary_df[SUMMARY_COLUMN_ORDER]


def resolve_output_dir(project_root: Path, output_dir: Path) -> Path:
    if output_dir.is_absolute():
        resolved = output_dir
    else:
        resolved = project_root / output_dir
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def save_outputs(
    project_root: Path,
    detail_records: list[dict[str, object]],
    output_dir: Path,
) -> tuple[Path, Path]:
    detail_df = pd.DataFrame(detail_records)
    if detail_df.empty:
        detail_df = pd.DataFrame(columns=DETAIL_COLUMN_ORDER)
    else:
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
            "strategy": result["strategy"],
            "budget": result["budget"],
            "requested_budget": result["requested_budget"],
            "actual_support_size": result["actual_support_size"],
            "support_class_counts": result["support_class_counts"],
            "accuracy": result["accuracy"],
            "balanced_accuracy": result["balanced_accuracy"],
            "macro_f1": result["macro_f1"],
            "fit_seconds": result["fit_seconds"],
            "predict_seconds": result["predict_seconds"],
            "selection_seconds": result["selection_seconds"],
            "end_to_end_seconds": result["end_to_end_seconds"],
            "device": result["device"],
        }
    )


def main() -> None:
    args = parse_args()
    project_root = phase4.resolve_project_root()
    strategies = normalize_strategies(args.strategies)
    budgets, seeds, output_dir = resolve_preset_defaults(args)

    checkpoint_path = phase4.ensure_tabicl_checkpoint_available()
    print(f"TabICL checkpoint ready: {checkpoint_path}")
    print()

    X, y, cache_path = phase4.load_dataset(project_root, DATASET_KEY)
    categorical_cols, numeric_cols = phase4.get_feature_groups(X)

    print(f"Dataset: {DATASET_KEY}")
    print(f"Loaded data from: {cache_path}")
    print(f"Samples: {len(X)}, raw features: {X.shape[1]}")
    print(f"Categorical features: {len(categorical_cols)}, numeric features: {len(numeric_cols)}")
    print(f"Strategies: {', '.join(strategies)}")
    print(f"Budgets: {', '.join(str(budget) for budget in budgets)}")
    print(f"Seeds: {', '.join(str(seed) for seed in seeds)}")
    print(f"Preset: {args.preset}")
    print(f"Output directory: {resolve_output_dir(project_root, output_dir)}")
    print()

    detail_records: list[dict[str, object]] = []
    for seed in seeds:
        print(f"[adult | phase6_support_selection] Running seed {seed}")
        run_results = run_seed(
            X,
            y,
            strategies,
            budgets,
            seed=seed,
            cache_path=cache_path,
            numeric_cols=numeric_cols,
            categorical_cols=categorical_cols,
        )
        detail_records.extend(run_results)

        for result in run_results:
            print_run_result(result)

        detail_path, summary_path = save_outputs(project_root, detail_records, output_dir)
        print(f"Intermediate detail saved to: {detail_path}")
        print(f"Intermediate summary saved to: {summary_path}")
        print()

    detail_path, summary_path = save_outputs(project_root, detail_records, output_dir)
    print(f"Saved detail results to: {detail_path}")
    print(f"Saved summary results to: {summary_path}")
    print()
    print(f"Detail schema: {', '.join(DETAIL_COLUMN_ORDER)}")
    print(f"Summary schema: {', '.join(SUMMARY_COLUMN_ORDER)}")

    summary_df = pd.read_csv(summary_path)
    if summary_df.empty:
        print("Summary is empty because no runs were executed.")
    else:
        print()
        print(summary_df)


if __name__ == "__main__":
    main()
