# 项目总记录

## 项目名称

Tabular Foundation Models

## 项目目标

比较 `TabPFN v2`、`TabICL` 等表格基础模型与 `XGBoost`、`LightGBM` 等传统树模型在中小型表格分类数据集上的表现，并分析它们在准确率、运行速度和适用场景上的差异。

从 `2026-04-23` 起，项目策略升级为“双轨推进”：

- `主线轨道`：完成课程项目主体比较结果
- `Big Plus 轨道`：围绕 `TabICL` 做检索式支持集选择改进

当前项目问题：

> We compare tabular foundation models with boosted-tree baselines on small to medium tabular classification datasets, and we further explore whether retrieval-style support-set selection can improve TabICL.

## 项目阶段总览

| 阶段 | 目标 | 状态 | 完成时间 | 主要产出 |
| --- | --- | --- | --- | --- |
| Phase 1 | 明确问题、学习基础概念、搭环境、完成教学实验 | 已完成 | 2026-04-16 | 中文概念 notebook、本地环境、GitHub 仓库 |
| Phase 2 | 加载第一个真实数据集并跑通一个 baseline | 已完成 | 2026-04-22 | Adult baseline notebook、first_result.csv |
| Phase 3 | 主线口径修正与公平性加固 | 已完成 | 2026-04-23 | 统一结果字段、full Adult 受限结果、10k 控制实验、多 seed summary、Phase 3 学习 md |
| Phase 4 | 主线模型与数据集补齐 | 未开始 | - | 待补充 |
| Phase 5 | Big Plus 方法定义与主数据集深挖 | 未开始 | - | 待补充 |
| Phase 6 | Big Plus 次验证与稳健性判断 | 未开始 | - | 待补充 |
| Phase 7 | 结果整合、英文报告与演示转写 | 未开始 | - | 待补充 |

## 当前进度

- 已完成第一阶段
- 已完成第二阶段
- 已完成 Phase 3
- 已完成第一次正式模型对比：`Adult + LightGBM vs TabPFN v2`
- 已补做 `Adult 10k control` 控制实验
- 已将 `src/phase3_adult_compare.py` 升级为默认 `all` 的多 seed 脚本
- 已生成三份第三阶段结果表：
  - `results/phase3_adult_compare.csv`
  - `results/phase3_adult_compare_10k.csv`
  - `results/phase3_adult_compare_summary.csv`
- 已确认 full Adult 结果属于“受限条件结果”
- 已完成 Phase 3 的 `5` 个 seeds 稳定性评估
- 已确认在更公平的 `10,000` 样本控制实验中，`LightGBM` 的 `accuracy_mean = 0.8692 ± 0.0014`
- 已确认 `TabPFN v2` 在同一 `10k control` 设置下的 `accuracy_mean = 0.8614 ± 0.0031`
- 已锁定 Big Plus 主方向为：基于 `TabICL` 的检索式支持集选择改进
- 已新增 Big Plus 正式规划文档：`docs/big_plus_plan.md`
- 已完成当前阶段学习型文档：`notebooks/phase3_fairness_reset.md`
- 已把“每推进一个阶段就写一篇 notebooks 中文 md”升级为硬性规则

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

## Phase 3 完成记录

### 时间

2026-04-22 至 2026-04-23

### 本阶段目标

- 把已有 `Adult + LightGBM + TabPFN v2` 结果重新归位
- 明确“正式主结果”和“受限条件结果”的边界
- 设计并执行一个更公平的 `Adult` 控制实验
- 固定后续主线比较要复用的统一字段
- 用多 seed 稳定性评估把单次结果升级成更稳的阶段结论

### 本阶段完成内容

- 在项目本地 `.venv` 中安装并接入 `tabpfn`
- 新增并统一第三阶段实验脚本：`src/phase3_adult_compare.py`
- 通过 `--scenario` 支持三种入口：
  - `all`
  - `full_adult_limit_override`
  - `adult_control_10k`
- 新增 `--seeds` 参数，默认运行 `42, 43, 44, 45, 46`
- 保留了 full Adult 正式对比结果
- 新增了 `Adult 10k control` 控制实验
- 完成了 `full + 10k control` 的多 seed 稳定性评估
- 统一了第三阶段结果字段、输出格式和汇总方式
- 生成结果文件：
  - `results/phase3_adult_compare.csv`
  - `results/phase3_adult_compare_10k.csv`
  - `results/phase3_adult_compare_summary.csv`
- 更新 `docs/experiment_log.md`
- 更新 `docs/phase_plan.md`
- 更新 `docs/session_handoff.md`
- 更新 `docs/work_log.md`
- 更新 `README.md`
- 完成 `notebooks/phase3_fairness_reset.md`

### 本阶段结果

#### 1. `seed=42` 锚点结果

- full Adult
  - `LightGBM accuracy = 0.8751`
  - `TabPFN v2 accuracy = 0.8650`
- `10k control`
  - `LightGBM accuracy = 0.8684`
  - `TabPFN v2 accuracy = 0.8621`

说明：

- 这两组 `seed=42` 结果保留在正式记录里，作为历史锚点和最容易复现的入口
- `full Adult` 中的 `TabPFN v2` 仍然带有 `ignore_pretraining_limits=True` 的限制说明

#### 2. 多 seed 汇总结果

- `adult_control_10k`
  - `LightGBM accuracy_mean = 0.8692 ± 0.0014`
  - `TabPFN v2 accuracy_mean = 0.8614 ± 0.0031`
  - `LightGBM predict_seconds_median = 0.1217`
  - `TabPFN v2 predict_seconds_median = 22.3014`
- `full_adult_limit_override`
  - `LightGBM accuracy_mean = 0.8752 ± 0.0025`
  - `TabPFN v2 accuracy_mean = 0.8633 ± 0.0023`
  - `LightGBM predict_seconds_median = 0.0914`
  - `TabPFN v2 predict_seconds_median = 171.7491`

说明：

- 多 seed 默认使用 `seeds = 42, 43, 44, 45, 46`
- `10,000` 条训练样本在 5 个 seeds 下都能直接运行，没有触发 `9,500` fallback
- Phase 3 的最终结论优先引用这里的汇总结果，而不是只引用一次 run

### Phase 3 最终结论

- 第一层：`10k control` 的多 seed 结果说明，即使在更公平的支持范围内，`LightGBM` 仍然是 Adult 上更强或更高效的基线
- 第二层：full Adult 的多 seed 结果说明，这个方向在受限条件场景下也没有被推翻

因此，Phase 3 的最终结论不是“`TabPFN` 一定不行”，而是：

> 在当前 Adult 分类任务、当前 `ModelVersion.V2` 和当前实验设置下，`LightGBM` 在 `10k control` 的多 seed 结果中仍是更稳的主线 baseline；full Adult 结果的方向没有被推翻，但仍应作为带限制说明的受限条件结果来呈现。

### 本阶段学到的关键点

- “代码能跑出结果”不等于“结果已经足够作为主结论”
- foundation model 的支持范围、本地可运行性和推理成本本身就是实验结论的一部分
- 控制实验的价值，在于判断已有结论是被修正，还是被强化
- 多次运行里，真正值得重复的是“不同 seed / 不同抽样”，而不是机械重复同一个设置
- 课程项目想同时兼顾完成度和加分项，最稳的方式不是单线冲刺，而是双轨推进

### Phase 4 下一步

- 在 `Adult` 上接入 `TabICL`
- 在统一结果表中补入 `XGBoost`
- 扩展到 `Bank Marketing`

## 2026-04-23（双轨规划确立）

### 目标

- 回答“当前方向是否正确”
- 决定是否挑战 Big Plus
- 如果挑战，必须把规划、阶段顺序和文档同步规则一次性定清楚

### 本次完成内容

- 重新对齐外部项目要求和当前仓库状态
- 确认项目不再只做“现成模型比较”，而是升级为“双轨推进”
- 将 Big Plus 主方向锁定为：`TabICL` 检索式支持集选择改进
- 确定证据结构为：`一个主深挖数据集 + 一个次验证数据集`
- 确认每推进一个阶段，都要在 `notebooks/` 下新增一篇中文学习型 `md`
- 将新的路线图、交接入口和记录规则写回仓库文档

### 为什么这次变更重要

这次不是简单改一条“下一步”，而是重置整个项目的推进逻辑。  
如果没有这次文档重构，后续会同时出现两套不同优先级，导致实验、记录和报告叙事互相打架。

## 协作记忆入口

为了避免对话过长后上下文丢失，后续协作默认优先参考以下文件：

1. `docs/session_handoff.md`
2. `docs/phase_plan.md`
3. `docs/project_record.md`
4. `docs/big_plus_plan.md`
5. 当前阶段对应的 `notebooks/phaseX_*.md`

## 展示时可以强调的亮点

- 项目不是只跑代码，而是按阶段逐步学习并构建实验能力
- 现在不仅有主线比较，还有一个清楚定义的 Big Plus 方法方向
- 项目过程有完整文档沉淀，后续适合直接转化为报告与展示材料

## 更新规则

建议每完成一个小阶段，就更新以下 5 项：

1. 当前阶段状态
2. 新完成的产出
3. 学到的关键点
4. 下一阶段计划
5. 当前阶段对应的 `notebooks/phaseX_*.md`
