# Tabular Foundation Models

这是一个面向课程项目的学习型仓库，主题是比较表格基础模型与传统树模型在中小型表格分类任务上的表现。

## 当前阶段

目前项目已经完成 Phase 3，接下来准备进入 Phase 4。

已完成的核心内容包括：

- 明确项目问题
- 学习 6 个基础概念
- 搭建本地实验环境
- 完成第一份教学 notebook
- 在 Adult 数据集上跑通第一个 baseline
- 完成第一次正式模型对比：`Adult + LightGBM vs TabPFN v2`
- 完成 `Adult 10k control` 控制实验
- 完成 Phase 3 的多 seed 稳定性评估
- 完成第三阶段的公平性收尾与文档闭环

当前项目问题：

> We compare tabular foundation models with boosted-tree baselines on small to medium tabular classification datasets.

## 计划比较的模型

- TabPFN v2
- TabICL
- XGBoost
- LightGBM

## 初步选择的数据集

- Adult
- Bank Marketing
- Credit-G

## 当前仓库内容

- `notebooks/phase1_concepts_demo.ipynb`：第一阶段中文教学 notebook
- `notebooks/phase2_adult_baseline.ipynb`：第二阶段 Adult 数据集 baseline notebook
- `notebooks/phase3_fairness_reset.md`：第三阶段学习型复盘笔记
- `notebooks/phase3_adult_compare_guide.md`：第三阶段过程性操作指南
- `src/phase3_adult_compare.py`：第三阶段 Adult 双场景对比脚本
- `docs/session_handoff.md`：新开对话时优先读取的项目记忆卡
- `docs/phase_plan.md`：双轨推进阶段计划
- `docs/project_record.md`：项目整体进度与里程碑记录
- `docs/work_log.md`：按时间记录每天/每次推进内容
- `docs/experiment_log.md`：按实验记录数据集、模型、结果与观察
- `docs/big_plus_plan.md`：Big Plus 正式规划文档
- `results/first_result.csv`：第一个正式 baseline 结果
- `results/phase3_adult_compare.csv`：第三阶段 full Adult 多 seed 明细结果
- `results/phase3_adult_compare_10k.csv`：第三阶段 10k control 多 seed 明细结果
- `results/phase3_adult_compare_summary.csv`：第三阶段多 seed 汇总结果
- `src/`：后续实验代码
- `data/`：数据目录
- `results/`：实验结果
- `report/`：英文报告
- `slides/`：演示文稿

## 本地环境

建议在 WSL Ubuntu 中使用项目本地虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-basic.txt
```

## 当前 Phase 3 结论

- `10k control` 的多 seed 结果告诉我们：`LightGBM accuracy_mean = 0.8692 ± 0.0014`，`TabPFN v2 accuracy_mean = 0.8614 ± 0.0031`
- full Adult 的多 seed 结果也保持同一方向，但它仍然属于带限制说明的受限条件结果
- 因此，Phase 3 的方向没有被推翻，而且现在是“seed42 锚点 + 多 seed 汇总”两层证据

## 如何运行 Phase 3 脚本

默认直接运行会同时执行 `full Adult` 和 `10k control` 两个场景，并使用 `seeds = 42 43 44 45 46`：

```bash
source .venv/bin/activate
python3 src/phase3_adult_compare.py
```

如果只想跑单个场景，可以显式指定：

```bash
python3 src/phase3_adult_compare.py --scenario adult_control_10k
python3 src/phase3_adult_compare.py --scenario full_adult_limit_override
```

## 下一步

下一步优先进入 Phase 4：

1. 在 `Adult` 上接入 `TabICL`
2. 把 `XGBoost` 补进统一主线结果表
3. 将主线扩展到 `Bank Marketing`
4. 形成四模型、双数据集的主线比较

## 如何记录项目过程

为了方便后续回顾、展示和写报告，建议每次推进都同步更新下面这些文件：

1. `docs/project_record.md`
   用来维护项目整体阶段、当前状态和关键里程碑。
2. `docs/work_log.md`
   用来记录每次学习、调试、阅读、写代码、搭环境时做了什么。
3. `docs/experiment_log.md`
   用来记录每次实验的设置、结果和观察，后面写报告时会非常有用。
4. `notebooks/phaseX_*.md`
   用来沉淀每个阶段的中文“教学 + 复盘”学习笔记。

## 如何保证后续对话不丢上下文

建议每次和 AI 新开对话时，都先让它阅读下面这些文件：

1. `docs/session_handoff.md`
2. `docs/phase_plan.md`
3. `docs/project_record.md`
4. `docs/big_plus_plan.md`
5. 当前阶段对应的 `notebooks/phaseX_*.md`

如果只想最快续接，优先读 `docs/session_handoff.md`。
