# Tabular Foundation Models

**Language / 语言**: [English](#english) | [中文](#zh)

<a id="english"></a>

## English

[Switch to 中文](#zh)

Course project repository for comparing tabular foundation models with boosted-tree baselines on small-to-medium tabular classification tasks.

### Current Status

The project is submission-ready with documented limitations.

Final deliverables:

- Official English report: `report/final_report.pdf`
- Chinese study/reference report: `report/final_report_zh_study.pdf`
- Submission manifest: `report/submission_manifest.md`

The official submission file is `report/final_report.pdf`. The Chinese PDF is for learning, review, and presentation preparation.

### Project Question

> We compare tabular foundation models with boosted-tree baselines on small-to-medium tabular classification datasets, and we further explore whether support-set selection can improve TabICL.

The project focuses on classification only. Regression and survival analysis are out of scope.

### Models

Mainline models:

- LightGBM
- XGBoost
- TabPFN v2
- TabICL

Big Plus extension:

- TabICL support-set selection on Adult

### Datasets

Main datasets:

- Adult
- Bank Marketing

Early exploration also considered Credit-G, but the final report focuses on Adult and Bank Marketing.

### Experiment Scope

The final report covers:

- Mainline comparison of LightGBM, XGBoost, TabPFN v2, and TabICL.
- Phase 5 train-size scalability analysis over `512`, `2048`, `8192`, `10000`, and `full`.
- Phase 6 Big Plus negative ablation on TabICL support-set selection for Adult.

Phase 7 was not started.

### Key Results

Mainline findings:

- On Adult, boosted-tree baselines remain strongest overall.
- On Bank Marketing, foundation models are more competitive, especially TabICL on imbalance-aware metrics.
- Tree models are much faster than the foundation models.
- TabICL is substantially faster than TabPFN v2 in this local setup.

Phase 6 Big Plus finding:

- Budget-limited support sets substantially reduce TabICL runtime.
- The frozen Balanced Prototype Retrieval strategy does not outperform Random Subset or Balanced Random Subset.
- The Phase 6 result should be treated as a useful negative ablation, not as a successful new method.

### Repository Layout

- `report/`: final reports, source Markdown, and submission manifest.
- `results/`: CSV results and generated figures.
- `results/figures/`: PNG/PDF figures used by the report.
- `src/`: experiment and figure-generation scripts.
- `notebooks/`: learning notes and phase summaries.
- `docs/`: project logs, phase plans, and handoff notes.
- `slides/`: presentation outline drafts.
- `data/`: local data directory.

### Final Report Files

- `report/final_report.pdf`: official English report for submission.
- `report/report_draft.md`: English source Markdown.
- `report/final_report_zh_study.pdf`: Chinese study/reference report.
- `report/report_draft_zh.md`: Chinese source Markdown.
- `report/submission_manifest.md`: handoff checklist with report, figure, and CSV paths.

### Key Result Files

- `results/phase4_mainline_compare.csv`
- `results/phase4_mainline_compare_summary.csv`
- `results/phase5_scalability_compare.csv`
- `results/phase5_scalability_compare_summary.csv`
- `results/phase6_big_plus_adult.csv`
- `results/phase6_big_plus_adult_summary.csv`
- `results/missingness_robustness_adult.csv`
- `results/missingness_robustness_adult_summary.csv`

### Main Figures

- `results/figures/phase5_scalability_accuracy.png`
- `results/figures/phase5_scalability_balanced_accuracy.png`
- `results/figures/phase5_scalability_macro_f1.png`
- `results/figures/phase5_scalability_total_seconds_median.png`
- `results/figures/phase6_big_plus_adult_bpr_delta.png`

Supporting Phase 6 figures are also available in `results/figures/`.

### Environment

Recommended environment: WSL Ubuntu with a project-local virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-reproduce.txt
```

Dependency files:

- `requirements-basic.txt`: minimal install list for the project scripts.
- `requirements-reproduce.txt`: pinned core environment for reproducing the submitted artifacts and rendering reports.
- `requirements-lock.txt`: key package snapshot used for the submitted experiments.
- `requirements-freeze.txt`: full transitive environment snapshot from the project `.venv`.

The submitted final runs used Python 3.12.3 in WSL Ubuntu, CPU tree models, and CUDA-backed foundation-model runs on an NVIDIA GeForce RTX 4060 Laptop GPU. CPU-only environments can still run the lightweight unit tests and some smoke paths, but full foundation-model reproduction may be much slower or unavailable without compatible CUDA packages and downloaded checkpoints.

### Quick Verification

Use the project-local virtual environment and run:

```bash
source .venv/bin/activate
python -m unittest discover -s tests
python3 src/render_reports.py
```

The first command runs lightweight regression and artifact checks. The second regenerates `report/report_draft.pdf`, `report/final_report.pdf`, `report/report_draft_zh.pdf`, and `report/final_report_zh_study.pdf` from the Markdown sources.

### Reproducing Main Artifacts

The final CSV and figures are already committed. To rerun experiments from scratch, use the scripts below only when intentionally reproducing results.

Mainline comparison:

```bash
source .venv/bin/activate
python3 src/phase4_mainline_compare.py
```

Phase 5 scalability comparison:

```bash
python3 src/phase5_scalability_compare.py
python3 src/phase5_make_mainline_figures.py
```

Phase 6 Big Plus Adult experiment:

```bash
python3 src/phase6_big_plus_adult.py --preset final
python3 src/phase6_make_big_plus_figures.py
```

The default `phase6_big_plus_adult.py` command now runs a smoke preset and writes to
`results/smoke/`; use `--preset final` to reproduce the final Phase 6 CSV files.
The smoke preset is intended for CPU-friendly workflow checks. The final preset is the committed experiment grid and may require CUDA-capable foundation-model execution.

Supplemental Adult missingness robustness check:

```bash
python3 src/missingness_robustness_adult.py --train-size 2048 --seeds 42 --missing-rates 0 0.1 0.3
```

These commands can be expensive. They are not needed just to inspect the final report.

### Documentation Handoff

For project context, read:

1. `report/submission_manifest.md`
2. `docs/session_handoff.md`
3. `docs/project_record.md`
4. `docs/phase_plan.md`
5. `docs/big_plus_plan.md`
6. `notebooks/phase6_big_plus_adult.md`

The handoff notes explicitly record that Phase 7 was not started and that the Phase 6 frozen method definition was preserved. Later review fixes added a supplemental Adult missingness check and safer Phase 6 smoke/final presets.

[Back to top](#tabular-foundation-models) | [Switch to 中文](#zh)

---

<a id="zh"></a>

## 中文

[切换到 English](#english)

这是一个课程项目仓库，用来比较表格基础模型和 boosted-tree baseline 在中小型表格分类任务上的表现。

### 当前状态

项目已经进入带有明确限制说明的 submission-ready 状态。

最终交付文件：

- 英文正式报告：`report/final_report.pdf`
- 中文学习/复习版报告：`report/final_report_zh_study.pdf`
- 提交清单：`report/submission_manifest.md`

正式提交文件建议使用 `report/final_report.pdf`。中文 PDF 主要用于自己学习、复习和答辩准备。

### 项目问题

> 我们比较 tabular foundation models 与 boosted-tree baselines 在中小型表格分类数据集上的表现，并进一步探索 support-set selection 是否能改善 TabICL。

本项目只关注分类任务。Regression 和 survival analysis 不在本项目范围内。

### 模型

主线模型：

- LightGBM
- XGBoost
- TabPFN v2
- TabICL

Big Plus 扩展：

- Adult 上的 TabICL 支持集选择

### 数据集

主线数据集：

- Adult
- Bank Marketing

早期探索也考虑过 Credit-G，但最终报告聚焦 Adult 和 Bank Marketing。

### 实验范围

最终报告覆盖：

- LightGBM、XGBoost、TabPFN v2 和 TabICL 的主线比较。
- Phase 5 train-size scalability 分析，训练规模包括 `512`、`2048`、`8192`、`10000` 和 `full`。
- Phase 6 Big Plus：Adult 上的 TabICL 支持集选择 negative ablation。

Phase 7 没有启动。

### 关键结果

主线发现：

- Adult 上 boosted-tree baseline 整体仍然最强。
- Bank Marketing 上 foundation models 更有竞争力，尤其是 TabICL 在 imbalance-aware metrics 上表现更好。
- 树模型比 foundation models 快得多。
- 在本地设置中，TabICL 明显快于 TabPFN v2。

Phase 6 Big Plus 发现：

- 预算受限支持集可以显著降低 TabICL runtime。
- 冻结版 Balanced Prototype Retrieval 没有超过 Random Subset 或 Balanced Random Subset。
- Phase 6 应解释为有价值的 negative ablation，而不是成功的新方法。

### 仓库结构

- `report/`：最终报告、源 Markdown 和提交清单。
- `results/`：CSV 结果和生成图表。
- `results/figures/`：报告中使用的 PNG/PDF 图表。
- `src/`：实验脚本和图表生成脚本。
- `notebooks/`：学习笔记和阶段总结。
- `docs/`：项目日志、阶段计划和 handoff 文档。
- `slides/`：展示提纲草稿。
- `data/`：本地数据目录。

### 最终报告文件

- `report/final_report.pdf`：英文正式提交报告。
- `report/report_draft.md`：英文报告源 Markdown。
- `report/final_report_zh_study.pdf`：中文学习/复习版报告。
- `report/report_draft_zh.md`：中文报告源 Markdown。
- `report/submission_manifest.md`：包含报告、图表和 CSV 路径的提交清单。

### 关键结果文件

- `results/phase4_mainline_compare.csv`
- `results/phase4_mainline_compare_summary.csv`
- `results/phase5_scalability_compare.csv`
- `results/phase5_scalability_compare_summary.csv`
- `results/phase6_big_plus_adult.csv`
- `results/phase6_big_plus_adult_summary.csv`
- `results/missingness_robustness_adult.csv`
- `results/missingness_robustness_adult_summary.csv`

### 主要图表

- `results/figures/phase5_scalability_accuracy.png`
- `results/figures/phase5_scalability_balanced_accuracy.png`
- `results/figures/phase5_scalability_macro_f1.png`
- `results/figures/phase5_scalability_total_seconds_median.png`
- `results/figures/phase6_big_plus_adult_bpr_delta.png`

Phase 6 的补充图表也在 `results/figures/` 中。

### 本地环境

推荐在 WSL Ubuntu 中使用项目本地虚拟环境。

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-reproduce.txt
```

依赖文件说明：

- `requirements-basic.txt`：项目脚本的最小安装列表。
- `requirements-reproduce.txt`：用于复现提交 artifacts 和渲染报告的核心 pinned 环境。
- `requirements-lock.txt`：提交实验使用的关键包版本快照。
- `requirements-freeze.txt`：从项目 `.venv` 导出的完整传递依赖环境快照。

提交版最终实验使用 WSL Ubuntu 中的 Python 3.12.3，树模型在 CPU 上运行，foundation-model 运行使用 NVIDIA GeForce RTX 4060 Laptop GPU 上的 CUDA。CPU-only 环境仍可运行轻量单元测试和部分 smoke 路径，但如果没有兼容 CUDA 包和已下载 checkpoint，完整 foundation-model 复现可能会非常慢或不可用。

### 快速验证

使用项目本地虚拟环境运行：

```bash
source .venv/bin/activate
python -m unittest discover -s tests
python3 src/render_reports.py
```

第一条命令运行轻量 regression 和 artifact 检查。第二条命令会从 Markdown 源文件重新生成 `report/report_draft.pdf`、`report/final_report.pdf`、`report/report_draft_zh.pdf` 和 `report/final_report_zh_study.pdf`。

### 复现主要产物

最终 CSV 和图表已经提交。如果确实需要从头复现实验，可以使用下面的脚本。只是查看最终报告时不需要运行这些命令。

主线比较：

```bash
source .venv/bin/activate
python3 src/phase4_mainline_compare.py
```

Phase 5 scalability 比较：

```bash
python3 src/phase5_scalability_compare.py
python3 src/phase5_make_mainline_figures.py
```

Phase 6 Big Plus Adult 实验：

```bash
python3 src/phase6_big_plus_adult.py --preset final
python3 src/phase6_make_big_plus_figures.py
```

`phase6_big_plus_adult.py` 的默认无参数命令现在只运行 smoke preset，并写入
`results/smoke/`；要复现最终 Phase 6 CSV，请显式使用 `--preset final`。
Smoke preset 主要用于 CPU 友好的工作流检查；final preset 对应已提交实验网格，可能需要可用的 CUDA foundation-model 运行环境。

补充 Adult missingness robustness 检查：

```bash
python3 src/missingness_robustness_adult.py --train-size 2048 --seeds 42 --missing-rates 0 0.1 0.3
```

这些命令可能比较耗时。仅查看最终报告不需要重新运行实验。

### 文档 Handoff

如果需要快速接续项目上下文，建议阅读：

1. `report/submission_manifest.md`
2. `docs/session_handoff.md`
3. `docs/project_record.md`
4. `docs/phase_plan.md`
5. `docs/big_plus_plan.md`
6. `notebooks/phase6_big_plus_adult.md`

Handoff 文档明确记录：Phase 7 没有启动，并且 Phase 6 冻结方法定义保持不变。后续 review 修复增加了补充 Adult missingness 检查，以及更安全的 Phase 6 smoke/final presets。

[回到顶部](#tabular-foundation-models) | [切换到 English](#english)
