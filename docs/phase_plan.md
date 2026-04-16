# 项目阶段计划（修订版）

这份文档基于你提供的 `初步阶段计划.md` 整理而成，并做了两类增强：

1. 标注当前完成状态，避免每次重新判断做到哪一步
2. 在每个阶段里补上“应更新哪些记录”，方便长期回顾和展示

## 项目约束

- 最终交付：英文报告 + 15 分钟演示
- 截止时间：2026-05-04
- 当前定位：机器学习初学者，边学边做
- 当前项目范围：先做中小型表格分类任务
- 当前计划比较模型：`TabPFN v2`、`TabICL`、`XGBoost`、`LightGBM`
- 当前计划数据集：`Adult`、`Bank Marketing`、`Credit-G`

## 阶段总览

| 阶段 | 时间 | 核心目标 | 当前状态 |
| --- | --- | --- | --- |
| 第 1 阶段 | 4月16日-4月18日 | 明确问题、学基础概念、搭环境 | 已完成 |
| 第 2 阶段 | 4月19日-4月21日 | 跑通第一个 baseline | 已完成 |
| 第 3 阶段 | 4月22日-4月24日 | 接入 TabPFN v2 并做第一次正式对比 | 下一步 |
| 第 4 阶段 | 4月25日-4月27日 | 接入 TabICL 并扩展到 3 个数据集 | 未开始 |
| 第 5 阶段 | 4月28日-5月1日 | 做一个分析型扩展实验 | 未开始 |
| 第 6 阶段 | 5月2日-5月3日 | 写英文报告并做演示稿 | 未开始 |
| 第 7 阶段 | 5月4日 | 总检查与正式讲解 | 未开始 |

## 第 1 阶段：4月16日-4月18日

### 目标

- 明确项目问题，并写一句自己的版本
- 学会 6 个基础概念：`classification`、`train/test split`、`accuracy`、`overfitting`、`categorical features`、`missing values`
- 读项目说明文档并写中文笔记
- 选定模型和初步数据集
- 安装实验环境，确保本地能跑 Python、Jupyter 和基础包

### 完成情况

已完成。

### 已有产出

- `notebooks/phase1_concepts_demo.ipynb`
- 本地 `.venv`
- GitHub 公开仓库
- 项目记录体系

### 完成标准

你能用自己的话解释项目要做什么，并把目录搭好。

### 阶段结束后应更新

- `docs/project_record.md`
- `docs/work_log.md`
- `docs/session_handoff.md`

## 第 2 阶段：4月19日-4月21日

### 目标

- 先只做 baseline，不碰 foundation model
- 选 1 个数据集，完成数据读取
- 检查目标列、特征类型、缺失值情况
- 完成一次最基础预处理
- 跑通 `XGBoost` 或 `LightGBM` 至少一个模型
- 记录 `accuracy` 和运行时间
- 把结果写进 `results/first_result.csv` 或 notebook 表格里

### 为什么这个阶段很关键

这个阶段的核心不是“分数多高”，而是拥有第一条完整实验链路。只要这条链路跑通，后面换模型、换数据集都会顺很多。

### 完成情况

已完成。

### 已有产出

- `notebooks/phase2_adult_baseline.ipynb`
- `results/first_result.csv`
- `docs/experiment_log.md` 中的正式 baseline 记录

### 完成标准

你已经有第一条完整实验链路，不再只是“会看论文”。

### 阶段结束后应更新

- `docs/project_record.md`
- `docs/work_log.md`
- `docs/experiment_log.md`
- `docs/session_handoff.md`

## 第 3 阶段：4月22日-4月24日

### 目标

- 接入 `TabPFN v2`
- 在同一个数据集上和 baseline 做第一次正式对比
- 统一评估方式，确保不同模型的测试集一致
- 记录安装难度、内存占用、速度和输入格式要求
- 做第一张正式结果表

### 完成标准

你有一张能放进报告的结果表，至少包含 2 个模型。

### 阶段结束后应更新

- `docs/project_record.md`
- `docs/work_log.md`
- `docs/experiment_log.md`
- `results/` 中的结果表或图
- `docs/session_handoff.md`

## 第 4 阶段：4月25日-4月27日

### 目标

- 接入 `TabICL`
- 把实验扩展到第 2 个和第 3 个数据集
- 对每个数据集都跑：`TabPFN v2`、`TabICL`、`XGBoost`、`LightGBM`
- 统一保存结果，字段至少包括：`dataset`、`model`、`accuracy`、`runtime`、`n_samples`
- 开始写实验观察笔记：谁更准、谁更快、谁更容易跑通

### 完成标准

你手里已经有项目主体结果，不会到最后几天才第一次出表。

### 阶段结束后应更新

- `docs/project_record.md`
- `docs/work_log.md`
- `docs/experiment_log.md`
- `docs/session_handoff.md`

## 第 5 阶段：4月28日-5月1日

### 目标

- 只做一个分析型扩展实验：`dataset size sensitivity`
- 选 1-2 个数据集，采样成不同规模：`500`、`2000`、`full`
- 比较不同模型在不同样本量下的准确率变化
- 画至少 1 张图：横轴是数据规模，纵轴是 `accuracy`
- 写出 3-5 条实验观察

### 完成标准

你不只是“跑模型”，而是真的做了分析。

### 阶段结束后应更新

- `docs/project_record.md`
- `docs/work_log.md`
- `docs/experiment_log.md`
- `docs/session_handoff.md`
- `results/` 中的图和表

## 第 6 阶段：5月2日-5月3日

### 目标

- 开始写英文报告
- 报告结构固定为：`Introduction`、`Related Models`、`Datasets`、`Experimental Setup`、`Results`、`Discussion`、`Conclusion`
- 每一节先写中文要点，再翻成简单英文
- 报告里至少要有：1 张结果总表、1 张分析图、1 段对模型优缺点的讨论
- 做 15 分钟演示稿，建议 8-10 页
- 演示顺序固定为：题目背景 -> 模型简介 -> 数据集 -> 实验设计 -> 结果 -> 分析 -> 结论

### 完成标准

报告有完整初稿，PPT 可以从头讲到尾。

### 阶段结束后应更新

- `docs/project_record.md`
- `docs/work_log.md`
- `docs/session_handoff.md`
- `report/`
- `slides/`

## 第 7 阶段：5月4日

### 目标

- 通读英文报告，修正语言和图表标题
- 检查所有结果数字是否一致
- 按 15 分钟完整讲一遍
- 准备 3 个可能会被问到的问题：
  - 为什么选这些数据集
  - 为什么用 `accuracy`
  - 为什么要和 `XGBoost`、`LightGBM` 比

### 完成标准

你能顺畅讲完，不依赖临场发挥。

### 阶段结束后应更新

- `docs/project_record.md`
- `docs/work_log.md`
- `docs/session_handoff.md`

## 当前最优先动作

你已经完成第 1 阶段，所以当前默认下一步是：

1. 接入 `TabPFN v2`
2. 在 Adult 数据集上保持测试集一致
3. 和 LightGBM baseline 做第一次正式对比
4. 记录准确率、运行时间和使用难度
5. 整理第一张正式结果表

## 使用建议

如果新开对话，不想让 AI 重新猜项目背景，先让它按顺序阅读：

1. `docs/session_handoff.md`
2. `docs/phase_plan.md`
3. `docs/project_record.md`
