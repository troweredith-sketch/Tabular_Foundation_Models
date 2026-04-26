"""Create Phase 6 Adult Big Plus analysis figures from existing result CSVs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DETAIL_PATH = PROJECT_ROOT / "results" / "phase6_big_plus_adult.csv"
SUMMARY_PATH = PROJECT_ROOT / "results" / "phase6_big_plus_adult_summary.csv"
OUTPUT_DIR = PROJECT_ROOT / "results" / "figures"

BUDGET_LIMITED_STRATEGIES = [
    "random_subset",
    "balanced_random_subset",
    "balanced_prototype_retrieval",
]
FULL_CONTEXT = "full_context"
STRATEGY_LABELS = {
    "full_context": "Full Context",
    "random_subset": "Random Subset",
    "balanced_random_subset": "Balanced Random Subset",
    "balanced_prototype_retrieval": "Balanced Prototype Retrieval",
}
STRATEGY_STYLES = {
    "random_subset": {"color": "#0072b2", "marker": "o"},
    "balanced_random_subset": {"color": "#009e73", "marker": "s"},
    "balanced_prototype_retrieval": {"color": "#d55e00", "marker": "^"},
    "full_context": {"color": "#4d4d4d", "marker": None},
}

METRIC_FIGURES = [
    {
        "column": "accuracy_mean",
        "std_column": "accuracy_std",
        "ylabel": "Accuracy (mean over seeds)",
        "title": "Adult Phase 6: Accuracy vs Support Budget",
        "filename": "phase6_big_plus_adult_accuracy",
    },
    {
        "column": "balanced_accuracy_mean",
        "std_column": "balanced_accuracy_std",
        "ylabel": "Balanced accuracy (mean over seeds)",
        "title": "Adult Phase 6: Balanced Accuracy vs Support Budget",
        "filename": "phase6_big_plus_adult_balanced_accuracy",
    },
    {
        "column": "macro_f1_mean",
        "std_column": "macro_f1_std",
        "ylabel": "Macro-F1 (mean over seeds)",
        "title": "Adult Phase 6: Macro-F1 vs Support Budget",
        "filename": "phase6_big_plus_adult_macro_f1",
    },
]


def load_results() -> tuple[pd.DataFrame, pd.DataFrame, list[int]]:
    """Load and validate the completed Phase 6 Adult result tables."""
    if not DETAIL_PATH.exists():
        raise FileNotFoundError(f"Missing input file: {DETAIL_PATH}")
    if not SUMMARY_PATH.exists():
        raise FileNotFoundError(f"Missing input file: {SUMMARY_PATH}")

    detail_df = pd.read_csv(DETAIL_PATH)
    summary_df = pd.read_csv(SUMMARY_PATH)
    required_detail = {
        "seed",
        "strategy",
        "budget",
        "requested_budget",
        "actual_support_size",
        "support_class_counts",
        "accuracy",
        "balanced_accuracy",
        "macro_f1",
        "total_seconds",
    }
    required_summary = {
        "strategy",
        "strategy_display",
        "budget",
        "n_runs",
        "requested_budget",
        "actual_support_size",
        "support_class_counts",
        "accuracy_mean",
        "accuracy_std",
        "balanced_accuracy_mean",
        "balanced_accuracy_std",
        "macro_f1_mean",
        "macro_f1_std",
        "total_seconds_median",
    }
    missing_detail = sorted(required_detail.difference(detail_df.columns))
    missing_summary = sorted(required_summary.difference(summary_df.columns))
    if missing_detail:
        raise ValueError(f"Missing detail columns: {missing_detail}")
    if missing_summary:
        raise ValueError(f"Missing summary columns: {missing_summary}")
    if len(detail_df) != 30:
        raise ValueError(f"Expected 30 detail rows, found {len(detail_df)}")
    if len(summary_df) != 10:
        raise ValueError(f"Expected 10 summary rows, found {len(summary_df)}")

    budget_limited = detail_df[detail_df["strategy"] != FULL_CONTEXT].copy()
    consistency = (
        budget_limited.groupby(["budget", "seed"])["requested_budget"]
        .nunique()
        .reset_index(name="n_unique_requested_budget")
    )
    if not (consistency["n_unique_requested_budget"] == 1).all():
        raise ValueError("Budget-limited requested_budget is inconsistent within budget/seed groups")

    budgets = sorted(int(value) for value in budget_limited["budget"].unique())
    expected_groups = {
        (strategy, str(budget))
        for strategy in BUDGET_LIMITED_STRATEGIES
        for budget in budgets
    }
    observed_groups = set(
        zip(
            budget_limited["strategy"].astype(str),
            budget_limited["budget"].astype(str),
            strict=True,
        )
    )
    missing_groups = sorted(expected_groups.difference(observed_groups))
    if missing_groups:
        raise ValueError(f"Missing strategy/budget groups: {missing_groups}")

    return detail_df, summary_df, budgets


def save_figure(fig: plt.Figure, output_stem: str) -> list[Path]:
    """Save one figure as PNG and PDF."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = [
        OUTPUT_DIR / f"{output_stem}.png",
        OUTPUT_DIR / f"{output_stem}.pdf",
    ]
    fig.savefig(outputs[0], dpi=220, bbox_inches="tight")
    fig.savefig(outputs[1], bbox_inches="tight")
    plt.close(fig)
    return outputs


def plot_metric(summary_df: pd.DataFrame, budgets: list[int], spec: dict[str, str]) -> list[Path]:
    """Plot one performance metric against support budget."""
    column = spec["column"]
    std_column = spec["std_column"]
    fig, axis = plt.subplots(figsize=(7.8, 4.8))
    x_positions = list(range(len(budgets)))
    x_labels = [str(budget) for budget in budgets]

    full_value = float(summary_df.loc[summary_df["strategy"] == FULL_CONTEXT, column].iloc[0])
    full_label = f"{STRATEGY_LABELS[FULL_CONTEXT]} ({full_value:.4f})"
    axis.axhline(
        full_value,
        color=STRATEGY_STYLES[FULL_CONTEXT]["color"],
        linewidth=2.0,
        linestyle="--",
        label=full_label,
    )

    for strategy in BUDGET_LIMITED_STRATEGIES:
        strategy_df = (
            summary_df[summary_df["strategy"] == strategy]
            .assign(budget_numeric=lambda df: df["budget"].astype(int))
            .set_index("budget_numeric")
            .reindex(budgets)
        )
        style = STRATEGY_STYLES[strategy]
        axis.errorbar(
            x_positions,
            strategy_df[column],
            yerr=strategy_df[std_column],
            label=STRATEGY_LABELS[strategy],
            color=style["color"],
            marker=style["marker"],
            linewidth=2.2,
            markersize=6,
            capsize=3,
        )

    axis.set_title(spec["title"], fontsize=13, weight="bold")
    axis.set_xlabel("Support budget")
    axis.set_ylabel(spec["ylabel"])
    axis.set_xticks(x_positions)
    axis.set_xticklabels(x_labels)
    axis.grid(True, axis="both", alpha=0.28)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.legend(frameon=False, fontsize=9)
    fig.text(
        0.5,
        0.01,
        "Budget-limited points show mean +/- one standard deviation over seeds 42, 43, 44.",
        ha="center",
        fontsize=8.5,
        color="#444444",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    return save_figure(fig, spec["filename"])


def plot_runtime(summary_df: pd.DataFrame, budgets: list[int]) -> list[Path]:
    """Plot median runtime by strategy and budget with full context as a reference."""
    fig, axis = plt.subplots(figsize=(8.2, 4.8))
    x_positions = list(range(len(budgets)))
    width = 0.24
    offsets = [-width, 0.0, width]

    for offset, strategy in zip(offsets, BUDGET_LIMITED_STRATEGIES, strict=True):
        strategy_df = (
            summary_df[summary_df["strategy"] == strategy]
            .assign(budget_numeric=lambda df: df["budget"].astype(int))
            .set_index("budget_numeric")
            .reindex(budgets)
        )
        style = STRATEGY_STYLES[strategy]
        axis.bar(
            [position + offset for position in x_positions],
            strategy_df["total_seconds_median"],
            width=width,
            label=STRATEGY_LABELS[strategy],
            color=style["color"],
            alpha=0.86,
        )

    full_runtime = float(
        summary_df.loc[summary_df["strategy"] == FULL_CONTEXT, "total_seconds_median"].iloc[0]
    )
    axis.axhline(
        full_runtime,
        color=STRATEGY_STYLES[FULL_CONTEXT]["color"],
        linewidth=2.0,
        linestyle="--",
        label=f"{STRATEGY_LABELS[FULL_CONTEXT]} ({full_runtime:.1f}s)",
    )

    axis.set_title("Adult Phase 6: Median Runtime by Support Budget", fontsize=13, weight="bold")
    axis.set_xlabel("Support budget")
    axis.set_ylabel("Median total runtime (seconds, log scale)")
    axis.set_xticks(x_positions)
    axis.set_xticklabels([str(budget) for budget in budgets])
    axis.set_yscale("log")
    axis.grid(True, axis="y", alpha=0.28)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.legend(frameon=False, fontsize=9, ncol=2)
    fig.tight_layout()
    return save_figure(fig, "phase6_big_plus_adult_total_seconds_median")


def compute_bpr_delta(detail_df: pd.DataFrame, budgets: list[int]) -> pd.DataFrame:
    """Compute mean BPR deltas against the two budget-limited baselines."""
    metrics = ["accuracy", "balanced_accuracy", "macro_f1"]
    budget_limited = detail_df[detail_df["strategy"] != FULL_CONTEXT]
    wide = budget_limited.pivot_table(
        index=["budget", "seed"],
        columns="strategy",
        values=metrics,
    )

    rows: list[dict[str, object]] = []
    for budget in budgets:
        budget_df = wide.loc[str(budget)]
        for metric in metrics:
            bpr = budget_df[(metric, "balanced_prototype_retrieval")]
            for comparator in ["random_subset", "balanced_random_subset"]:
                delta = bpr - budget_df[(metric, comparator)]
                rows.append(
                    {
                        "budget": budget,
                        "metric": metric,
                        "comparator": comparator,
                        "delta_mean": float(delta.mean()),
                    }
                )
    return pd.DataFrame(rows)


def plot_bpr_delta(detail_df: pd.DataFrame, budgets: list[int]) -> list[Path]:
    """Plot BPR mean deltas against Random and Balanced Random baselines."""
    delta_df = compute_bpr_delta(detail_df, budgets)
    metric_labels = {
        "accuracy": "Accuracy",
        "balanced_accuracy": "Balanced accuracy",
        "macro_f1": "Macro-F1",
    }
    comparator_labels = {
        "random_subset": "BPR - Random",
        "balanced_random_subset": "BPR - Balanced Random",
    }
    comparator_colors = {
        "random_subset": "#cc79a7",
        "balanced_random_subset": "#e69f00",
    }

    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.2), sharey=True)
    x_positions = list(range(len(budgets)))
    width = 0.34

    for axis, metric in zip(axes, metric_labels, strict=True):
        metric_df = delta_df[delta_df["metric"] == metric]
        for offset, comparator in zip([-width / 2, width / 2], comparator_labels, strict=True):
            values = (
                metric_df[metric_df["comparator"] == comparator]
                .set_index("budget")
                .reindex(budgets)["delta_mean"]
            )
            axis.bar(
                [position + offset for position in x_positions],
                values,
                width=width,
                label=comparator_labels[comparator],
                color=comparator_colors[comparator],
                alpha=0.86,
            )
        axis.axhline(0.0, color="#333333", linewidth=1.0)
        axis.set_title(metric_labels[metric], fontsize=11.5, weight="bold")
        axis.set_xticks(x_positions)
        axis.set_xticklabels([str(budget) for budget in budgets])
        axis.set_xlabel("Support budget")
        axis.grid(True, axis="y", alpha=0.26)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)

    axes[0].set_ylabel("Mean delta over seeds")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False)
    fig.suptitle("Adult Phase 6: Balanced Prototype Retrieval Delta", fontsize=13, weight="bold")
    fig.tight_layout(rect=(0, 0.08, 1, 0.93))
    return save_figure(fig, "phase6_big_plus_adult_bpr_delta")


def main() -> None:
    detail_df, summary_df, budgets = load_results()
    output_paths: list[Path] = []
    for spec in METRIC_FIGURES:
        output_paths.extend(plot_metric(summary_df, budgets, spec))
    output_paths.extend(plot_runtime(summary_df, budgets))
    output_paths.extend(plot_bpr_delta(detail_df, budgets))

    print("Generated Phase 6 Adult figures:")
    for path in output_paths:
        print(f"- {path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
