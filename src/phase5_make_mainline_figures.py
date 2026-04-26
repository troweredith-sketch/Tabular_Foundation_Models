"""Create Phase 5 mainline scalability figures from existing summary results."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = PROJECT_ROOT / "results" / "phase5_scalability_compare_summary.csv"
OUTPUT_DIR = PROJECT_ROOT / "results" / "figures"

TRAIN_SIZE_ORDER = ["512", "2048", "8192", "10000", "full"]
DATASET_ORDER = ["adult", "bank_marketing"]
DATASET_LABELS = {
    "adult": "Adult",
    "bank_marketing": "Bank Marketing",
}
MODEL_ORDER = ["LightGBM", "XGBoost", "TabICL", "TabPFN v2"]
MODEL_STYLES = {
    "LightGBM": {"color": "#1b9e77", "marker": "o"},
    "XGBoost": {"color": "#d95f02", "marker": "s"},
    "TabICL": {"color": "#7570b3", "marker": "^"},
    "TabPFN v2": {"color": "#e7298a", "marker": "D"},
}

FIGURES = [
    {
        "column": "accuracy_mean",
        "ylabel": "Accuracy (mean)",
        "title": "Train Size vs Accuracy",
        "filename": "phase5_scalability_accuracy",
        "log_y": False,
    },
    {
        "column": "balanced_accuracy_mean",
        "ylabel": "Balanced accuracy (mean)",
        "title": "Train Size vs Balanced Accuracy",
        "filename": "phase5_scalability_balanced_accuracy",
        "log_y": False,
    },
    {
        "column": "macro_f1_mean",
        "ylabel": "Macro-F1 (mean)",
        "title": "Train Size vs Macro-F1",
        "filename": "phase5_scalability_macro_f1",
        "log_y": False,
    },
    {
        "column": "total_seconds_median",
        "ylabel": "Median total runtime (seconds, log scale)",
        "title": "Train Size vs Total Runtime",
        "filename": "phase5_scalability_total_seconds_median",
        "log_y": True,
    },
]


def load_summary() -> pd.DataFrame:
    """Load and validate the Phase 5 scalability summary table."""
    if not SUMMARY_PATH.exists():
        raise FileNotFoundError(f"Missing input file: {SUMMARY_PATH}")

    df = pd.read_csv(SUMMARY_PATH)
    required_columns = {
        "dataset",
        "train_size_label",
        "model",
        *(figure["column"] for figure in FIGURES),
    }
    missing_columns = sorted(required_columns.difference(df.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df = df.copy()
    df["train_size_label"] = df["train_size_label"].astype(str)
    df["train_size_label"] = pd.Categorical(
        df["train_size_label"],
        categories=TRAIN_SIZE_ORDER,
        ordered=True,
    )
    return df.sort_values(["dataset", "train_size_label", "model"])


def plot_figure(df: pd.DataFrame, figure_spec: dict[str, object]) -> list[Path]:
    """Plot one metric as two dataset subplots and save PNG/PDF outputs."""
    column = str(figure_spec["column"])
    output_stem = str(figure_spec["filename"])
    log_y = bool(figure_spec["log_y"])

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4), sharey=not log_y)
    x_positions = list(range(len(TRAIN_SIZE_ORDER)))

    for axis, dataset_key in zip(axes, DATASET_ORDER, strict=True):
        dataset_df = df[df["dataset"] == dataset_key]
        for model in MODEL_ORDER:
            model_df = (
                dataset_df[dataset_df["model"] == model]
                .set_index("train_size_label")
                .reindex(TRAIN_SIZE_ORDER)
            )
            if model_df[column].isna().all():
                continue
            style = MODEL_STYLES[model]
            axis.plot(
                x_positions,
                model_df[column],
                label=model,
                linewidth=2.2,
                markersize=6,
                color=style["color"],
                marker=style["marker"],
            )

        axis.set_title(DATASET_LABELS[dataset_key], fontsize=12, weight="bold")
        axis.set_xticks(x_positions)
        axis.set_xticklabels(TRAIN_SIZE_ORDER)
        axis.set_xlabel("Training set size")
        axis.grid(True, axis="both", alpha=0.28)
        if log_y:
            axis.set_yscale("log")
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)

    axes[0].set_ylabel(str(figure_spec["ylabel"]))
    fig.suptitle(str(figure_spec["title"]), fontsize=14, weight="bold")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="lower center",
        ncol=len(MODEL_ORDER),
        frameon=False,
        bbox_to_anchor=(0.5, -0.02),
    )
    fig.text(
        0.5,
        0.04,
        "Mean metrics and median runtime over seeds 42-46; repeated stratified splits.",
        ha="center",
        fontsize=9,
        color="#444444",
    )
    fig.tight_layout(rect=(0, 0.08, 1, 0.92))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = [
        OUTPUT_DIR / f"{output_stem}.png",
        OUTPUT_DIR / f"{output_stem}.pdf",
    ]
    fig.savefig(outputs[0], dpi=220, bbox_inches="tight")
    fig.savefig(outputs[1], bbox_inches="tight")
    plt.close(fig)
    return outputs


def main() -> None:
    df = load_summary()
    output_paths: list[Path] = []
    for figure_spec in FIGURES:
        output_paths.extend(plot_figure(df, figure_spec))

    print("Generated Phase 5 mainline figures:")
    for path in output_paths:
        print(f"- {path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
