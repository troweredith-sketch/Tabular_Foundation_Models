# 项目总记录

## 项目名称

Tabular Foundation Models

## 项目目标

比较 `TabPFN v2`、`TabICL` 等表格基础模型与 `XGBoost`、`LightGBM` 等传统树模型在中小型表格分类数据集上的表现，并分析它们在准确率、运行速度和适用场景上的差异。

当前项目问题：

> We compare tabular foundation models with boosted-tree baselines on small to medium tabular classification datasets.

## 项目阶段总览

| 阶段 | 目标 | 状态 | 完成时间 | 主要产出 |
| --- | --- | --- | --- | --- |
| Phase 1 | 明确问题、学习基础概念、搭环境、完成教学实验 | 已完成 | 2026-04-16 | 中文概念 notebook、本地环境、GitHub 仓库 |
| Phase 2 | 加载第一个真实数据集并跑通一个 baseline | 已完成 | 2026-04-22 | Adult baseline notebook、first_result.csv |
| Phase 3 | 对多个数据集和模型做系统对比 | 进行中 | 2026-04-22 | 待补充 |
| Phase 4 | 分析结果、出图、写英文报告和演示 | 未开始 | - | 待补充 |

## 当前进度

- 已完成第一阶段
- 已完成第二阶段
- 已在 2026-04-22 正式确认第二阶段收尾，开始进入第三阶段
- 已初始化本地 Git 仓库并创建公开 GitHub 仓库
- 已完成第一份中文教学 notebook
- 已完成第一个真实数据集实验：`Adult + LightGBM baseline`
- 已准备好后续实验的基础目录结构
- 已导入并修订初步阶段计划
- 已建立项目记忆卡和协作记录体系

## Phase 1 完成记录

### 时间

2026-04-16

### 本阶段目标

- 明确项目问题
- 学习 6 个机器学习基础概念
- 完成一个用于理解 `accuracy`、`train/test split` 和 `overfitting` 的教学实验
- 搭建本地 Python / Jupyter 环境
- 将当前进度同步到 GitHub

### 本阶段完成内容

- 将项目范围收敛为“中小型表格分类任务上的模型比较”
- 初步选定模型：`TabPFN v2`、`TabICL`、`XGBoost`、`LightGBM`
- 初步选定数据集：`Adult`、`Bank Marketing`、`Credit-G`
- 完成本地 `.venv` 和基础依赖安装
- 编写 `notebooks/phase1_concepts_demo.ipynb`
- 创建公开 GitHub 仓库并完成首次推送

### 本阶段学到的关键点

- 训练集表现好不代表模型泛化好
- `accuracy` 是一个入门友好但不总是充分的指标
- 表格数据里的类别特征和缺失值会影响后续预处理和模型选择
- 把实验过程写下来，会显著降低后面写报告和做 PPT 的难度

### 下一阶段计划

- 选择第一个真实项目数据集
- 看懂数据规模、特征列和目标列
- 先用一个 baseline 模型跑通完整流程

## Phase 2 完成记录

### 时间

2026-04-22（实验首次跑通于 2026-04-16，已在 2026-04-22 正式确认收尾）

### 本阶段目标

- 选择第一个真实数据集
- 完成数据读取
- 检查目标列、特征类型和缺失值
- 完成一次最基础预处理
- 跑通一个 baseline 模型
- 记录 `accuracy` 和运行时间

### 本阶段完成内容

- 选定第一个正式数据集：`Adult`
- 确认该数据集共有 48842 条样本、14 个原始特征
- 检查出 `workclass`、`occupation`、`native-country` 存在缺失值
- 确认存在 8 个类别特征和 6 个数值特征
- 使用 `LightGBM + ColumnTransformer + SimpleImputer + OneHotEncoder` 跑通第一个 baseline
- 生成 `notebooks/phase2_adult_baseline.ipynb`
- 保存第一次正式结果到 `results/first_result.csv`
- 同步更新项目记录体系
- 在 2026-04-22 正式确认第二阶段完成，并将项目状态切换到第三阶段

### 本阶段结果

- 数据集：`Adult`
- 模型：`LightGBM`
- 指标：`accuracy = 0.8751`
- 训练耗时：`0.5361` 秒

### 本阶段学到的关键点

- 真实数据集和教学数据集最大的差别，在于必须先做数据体检
- 类别特征和缺失值会直接决定预处理方案
- baseline 的意义不是“简单”，而是提供后续比较的参照物
- 一旦第一条正式实验链路跑通，后面接入新模型会快很多

### 下一阶段计划

- 接入 `TabPFN v2`
- 在相同 Adult 测试集上与 LightGBM 做第一次正式对比
- 记录模型表现、运行时间和使用难度

## 协作记忆入口

为了避免对话过长后上下文丢失，后续协作默认优先参考以下文件：

1. `docs/session_handoff.md`
2. `docs/phase_plan.md`
3. `docs/project_record.md`
4. `docs/work_log.md`
5. `docs/experiment_log.md`

## 展示时可以强调的亮点

- 这个项目不是只跑代码，而是按阶段逐步学习并构建实验能力
- 第一阶段已经完成从“零散理解”到“有结构地掌握问题、概念、环境和记录方式”的过渡
- 项目过程有完整文档沉淀，后续适合直接转化为报告与展示材料

## 更新规则

建议每完成一个小阶段，就更新以下 4 项：

1. 当前阶段状态
2. 新完成的产出
3. 学到的关键点
4. 下一阶段计划
