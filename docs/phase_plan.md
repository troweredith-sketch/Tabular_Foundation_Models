# 项目阶段计划（硬要求优先版）

这份文档是当前项目的主规划文档。
从 `2026-04-24` 起，项目路线从“主线比较 + 直接进入 Big Plus”调整为：

1. 先补齐课程原始要求中的硬指标和分析闭环
2. 再做 `TabICL` 的检索式支持集选择 Big Plus
3. 最后集中整理英文报告、图表和 15 分钟演示

这次调整不是推翻 Phase 1-4，而是把已经完成的主线结果补成更稳、更符合原始要求的课程项目。

## 项目约束

- 最终交付：英文报告 + 15 分钟演示
- 截止时间：`2026-05-04`
- 当前定位：机器学习初学者，边学边做
- 当前任务类型：只做表格分类，不扩展到回归或 survival analysis
- 当前主线模型范围：`TabPFN v2`、`TabICL`、`LightGBM`、`XGBoost`
- 当前数据集策略：
  - 主线数据集：`Adult`、`Bank Marketing`
  - Big Plus 主深挖：`Adult`
  - Big Plus 次验证：`Bank Marketing`
  - 备用：`Credit-G`
- 当前 Big Plus 方向：基于 `TabICL` 的检索式支持集选择改进

## 当前总判断

项目方向正确，不需要换题，也不需要新增模型或任务类型。

当前已完成的 Phase 1-4 已经支撑起课程项目主体：两个 tabular foundation models、两个树模型 baseline、两个 OpenML 表格分类数据集、多 seed 结果表和运行时间记录都已经具备。

Phase 4 单独还不能直接视为最终主线闭环，原因是：

- 原始要求明确需要 scalability across different dataset sizes，而 Phase 4 只有 `control_10k` 和 `full_train_reference` 两档
- Phase 4 原始主指标只有 `accuracy`，对 `Bank Marketing` 这类不平衡数据集不够充分
- 当前 runtime 是 practical mixed-device timing，树模型在 CPU，foundation models 可能在 GPU，报告中必须解释清楚
- 当前 split 表述容易让人误以为跨 seeds 共用同一个测试集；实际应写成 repeated stratified splits
- 当前树模型是 fixed strong baselines，不是 tuned SOTA baselines
- 当前数据集是 OpenML datasets，不能包装成 TALENT 或 TabArena 实验

截至 2026-04-27，Phase 5 已补齐额外分类指标、完整 train-size scalability、主线图表、英文报告骨架和 15 分钟展示骨架。主线已经可以独立支撑课程报告。Phase 6 已完成 `TabICL` 支持集选择 Big Plus 方法冻结、Adult 主实验、结果图表和报告材料化。当前不启动 Phase 7，优先继续最终报告正文、caption、表格和展示材料整理。

## 双轨原则

### 主线轨道

- 目标是完成课程项目必须有的模型比较、指标、scalability 和 pros/cons 分析
- 主线必须能独立成稿，即使 Big Plus 结果一般或来不及完成，项目仍然成立
- 主线结论必须克制：只说明在当前固定 baseline、当前数据集和当前实验口径下观察到的结果

### Big Plus 轨道

- 目标是在主线稳住后提出一个小而实的方法性贡献
- 当前固定主题：`TabICL` 的支持集选择策略
- Big Plus 不替代主线，也不能威胁最终报告和展示交付

## 阶段总览

| 阶段 | 时间窗口 | 核心目标 | 当前状态 |
| --- | --- | --- | --- |
| Phase 1 | 4月16日 | 明确问题、学习基础概念、搭环境 | 已完成 |
| Phase 2 | 4月16日-4月22日 | 跑通第一个真实数据集 baseline | 已完成 |
| Phase 3 | 4月23日 | 主线口径修正与公平性加固 | 已完成，但文档表述需补改 |
| Phase 4 | 4月24日-4月28日 | 主线模型与数据集补齐 | 已完成，指标和 scalability 已由 Phase 5 补强 |
| Phase 5 | 4月24日-4月28日 | 主线硬要求闭环与结果补强 | 已完成 |
| Phase 6 | 4月28日-5月1日 | Big Plus 方法冻结、Adult 主实验与结果材料化 | 已完成 Adult 主实验和报告材料整理 |
| Phase 7 | 5月1日-5月2日 | Big Plus 次验证与稳健性判断 | 未开始，当前不启动 |
| Phase 8 | 5月2日-5月4日 | 报告、图表、PPT 和最终提交整理 | 未开始 |

## Phase 1：明确问题、学习基础概念、搭环境

### 完成情况

已完成。

### 已有产出

- `notebooks/phase1_concepts_demo.ipynb`
- 本地 `.venv`
- GitHub 公开仓库
- 项目记录体系

### 阶段意义

这一阶段解决的是“项目能不能开始”的问题，而不是“模型比得赢不赢”的问题。

## Phase 2：跑通第一个真实数据集 baseline

### 完成情况

已完成。

### 已有产出

- `notebooks/phase2_adult_baseline.ipynb`
- `results/first_result.csv`
- `docs/experiment_log.md` 中的正式 baseline 记录

### 阶段意义

这一阶段解决的是“有没有一条完整正式实验链路”的问题。

## Phase 3：主线口径修正与公平性加固

### 完成情况

已完成，但需要补充文档说明。

### 本阶段完成了什么

- 保留了 `Adult + LightGBM vs TabPFN v2` 的 full Adult 正式对比
- 明确这组 full Adult 结果属于“受限条件结果”
- 补做了 `Adult 10k control` 控制实验
- 完成了 `seeds = 42, 43, 44, 45, 46` 的多 seed 稳定性评估
- 统一了第三阶段脚本的结果字段、默认入口和输出方式
- 完成了当前阶段学习型文档：`notebooks/phase3_fairness_reset.md`

### 已完成内容中需要补改的地方

- 多 seed 结果应表述为 repeated stratified splits：每个 seed 内所有模型共享同一个 split，跨 seeds 不是同一个固定测试集
- `fixed test set` 这类表述如果保留，必须限定为“单个 seed 内固定”
- full Adult 中 `TabPFN v2` 超出官方 10,000 样本支持范围，仍必须作为受限条件结果呈现
- Phase 3 的 `accuracy` 结果可以保留，但后续主线闭环需要补更稳的指标

### 阶段产出

- `src/phase3_adult_compare.py`
- `results/phase3_adult_compare.csv`
- `results/phase3_adult_compare_10k.csv`
- `results/phase3_adult_compare_summary.csv`
- `docs/experiment_log.md` 中的实验 003、实验 004 和实验 005
- `notebooks/phase3_fairness_reset.md`

### Phase 3 最终结论

- `10k control` 的多 seed 结果告诉我们：`LightGBM` 以 `0.8692 ± 0.0014` 稳定高于 `TabPFN v2` 的 `0.8614 ± 0.0031`
- full Adult 的多 seed 结果告诉我们：这个方向在受限条件场景下也没有被推翻，但仍必须带限制说明

因此，Phase 3 的方向没有被推翻，只是现在证据更稳了。

## Phase 4：主线模型与数据集补齐

### 完成情况

已完成，但需要补强指标、scalability 和报告口径。

### 本阶段完成了什么

- 在项目本地 `.venv` 中正式接入 `tabicl==2.1.0`
- 将主线实验统一为：
  - 数据集：`Adult`、`Bank Marketing`
  - 模型：`TabPFN v2`、`TabICL`、`LightGBM`、`XGBoost`
  - 场景：`control_10k`、`full_train_reference`
  - seeds：`42, 43, 44, 45, 46`
- 让四个模型全部进入同一张结果表
- 完成 `Adult + Bank Marketing` 的正式多 seed 运行
- 将结果、阶段记录和学习型文档全部同步回仓库

### 已完成内容中需要补改的地方

- 主结果已在 Phase 5 第一轮补齐 `balanced_accuracy` 和 `macro_f1`
- `10k` 与 `full` 两档不足以完整回答不同数据规模下的 scalability；已由 Phase 5 train-size scalability 补齐
- 当前 speed 结果是 practical mixed-device timing；可以比较实际本地运行成本，但不能过度声称是同设备公平速度比较
- 当前树模型 baseline 是固定参数 strong baselines，不是调参后的 SOTA baseline
- `Adult` 和 `Bank Marketing` 是 OpenML 数据集，可以称为常见 benchmark datasets，但不能说成已经使用 TALENT 或 TabArena
- `full_train_reference` 可保留为工程参考线，但最终主结论应优先引用支持范围内或可解释更清楚的结果

### 阶段产出

- `src/phase4_mainline_compare.py`
- `results/phase4_mainline_compare.csv`
- `results/phase4_mainline_compare_summary.csv`
- `notebooks/phase4_mainline_completion.md`

### Phase 4 当前结论

- 在 `Adult control_10k` 中，树模型仍然最强，`XGBoost` 与 `LightGBM` 基本并列领先
- 在 `Bank Marketing` 中，foundation models 开始展现优势，`TabICL` 与 `TabPFN v2` 的准确率整体高于树模型
- `TabICL` 在两个数据集上都明显快于 `TabPFN v2`，因此仍是 Big Plus 的合适入口
- 这些结论成立于当前固定 baseline、当前数据集、当前 split 和当前设备口径下，报告中必须加限制说明

## Phase 5：主线硬要求闭环与结果补强

### 当前定位

这是已经完成的主线闭环阶段。
目标是先让项目完整回应原始要求，再进入 Big Plus。

截至 2026-04-26，三块主线补强已完成：

- `results/phase4_mainline_compare.csv` 已包含 `balanced_accuracy` 和 `macro_f1`
- `results/phase4_mainline_compare_summary.csv` 已包含两类新指标的 `mean/std/min/max`
- 完整主线重跑已覆盖 `2 datasets × 2 scenarios × 5 seeds × 4 models`
- `results/phase5_scalability_compare.csv` 已覆盖 `2 datasets × 5 train sizes × 5 seeds × 4 models = 200` 行 detail 结果
- `results/phase5_scalability_compare_summary.csv` 已覆盖 `2 datasets × 5 train sizes × 4 models = 40` 行 summary 结果
- `results/figures/` 已包含 4 组 size-vs-metric / runtime 图表的 PNG 和 PDF
- `report/outline.md` 已建立英文报告骨架
- `slides/outline.md` 已建立 15 分钟英文展示骨架

### 目标

- 已补齐 `accuracy` 之外的分类指标
- 已补齐不同训练规模下的 scalability 分析
- 修正文档和报告中的实验口径表述
- 建立英文报告和 PPT 的骨架，避免最后交付失控

### 必做任务

- 已在主线结果中新增：
  - `balanced_accuracy`
  - `macro_f1`
- 已完成 train-size grid：
  - `512`
  - `2048`
  - `8192`
  - `10000`
  - `full`
- 已在 `Adult` 和 `Bank Marketing` 上生成 size vs metric / runtime 的结果表
- 修正所有容易误导的 split protocol 表述
- 在文档中加入 runtime caveat：
  - `TabICL` vs `TabPFN v2` 的速度比较相对更可解释
  - foundation models vs tree baselines 是 practical mixed-device timing
- 在文档中加入 baseline caveat：
  - `LightGBM` 和 `XGBoost` 是固定参数 strong baselines，不是 tuned SOTA baselines
- 建立 `report/` 和 `slides/` 的骨架

### 阶段产出

- 更新后的主线结果表
- scalability 结果表
- 4 组可用于报告和 PPT 的图表草稿
- 修正后的实验口径说明
- `report/` 英文报告骨架
- `slides/` 演示骨架
- 当前阶段学习型文档：`notebooks/phase5_mainline_requirements_closure.md`

### 完成标准

- 可以明确说明项目已经覆盖原始要求中的 accuracy、inference speed、scalability 和 pros/cons 分析
- 主线即使不依赖 Big Plus，也能独立写成一份完整课程项目报告
- 后续进入 Big Plus 时，不再需要回头大改主线口径

### 阶段结束后应更新

- `docs/project_record.md`
- `docs/work_log.md`
- `docs/session_handoff.md`
- `docs/experiment_log.md`
- `notebooks/phase5_mainline_requirements_closure.md`

## Phase 6：Big Plus 方法冻结与 Adult 主实验

### 当前状态

已完成 Adult 主实验和结果材料化。
截至 `2026-04-27`，Phase 6 已完成方法冻结、Adult 主实验脚本实现、`budget=512, seed=42` smoke test、完整 Adult 主实验、结果图表和报告材料。
正式结论以完整 Adult 主实验为准；smoke test 只保留为历史工程记录。

### 目标

- 正式冻结 Big Plus 方法定义
- 围绕 `TabICL` 设计支持集选择策略，而不是只比较现成模型
- 在 `Adult` 上做 Big Plus 主深挖

### 前置条件

只有 Phase 5 完成后，才进入 Phase 6。
如果 Phase 5 未完成，Big Plus 不应抢占主线硬要求的时间。

### Big Plus 固定比较策略

- `Full Context`
- `Random Subset`
- `Balanced Random Subset`
- `Balanced Prototype Retrieval`

### `Balanced Prototype Retrieval` 必须冻结的细节

- 检索空间只用训练 split 构造
- 数值特征用训练 split 的 median 填补，并用训练 split 的 mean/std 标准化
- 类别特征用训练 split 的 most frequent 值填补，并用训练 split 拟合的 one-hot 编码
- 距离度量固定为欧氏距离
- 每个类别先计算 one-hot + 标准化数值空间里的类别中心，再选取最接近本类别中心的样本
- 类别配额：先按 `floor(B / K)` 做基础平衡分配，剩余预算按训练集类别规模比例补齐
- 类别样本不足时：该类别全部保留，未用完预算重新分配给仍有剩余样本的类别，不重复样本凑数
- 随机 baseline：必须使用相同 budget、相同 seeds、相同 train/test split
- 信息边界：只能使用训练集特征和训练集标签，不能使用测试标签、测试特征或测试分布
- 结果表必须记录 `requested_budget`、`actual_support_size` 和 `support_class_counts`

### 固定实验设置

- 主数据集：`Adult`
- 次验证数据集：`Bank Marketing`，留到未来 Phase 7；当前 Phase 6 closure 没有启动
- 上下文预算：`512`、`2048`、`8192`
- 随机种子：`42`、`43`、`44`
- `Full Context` 使用完整训练 split，作为 budget-independent reference

### 阶段产出

- Big Plus 方法定义
- Adult 主实验设计
- 当前阶段学习型文档：`notebooks/phase6_big_plus_adult.md`
- Phase 6 Adult 实验脚本：`src/phase6_big_plus_adult.py`
- 完整 Adult 主实验结果表：
  - `results/phase6_big_plus_adult.csv`
  - `results/phase6_big_plus_adult_summary.csv`
- `Adult` 上的策略对比表和 BPR delta 分析
- accuracy、balanced accuracy、macro-F1、runtime 和 BPR delta 图
- 负结果分析：冻结版 `Balanced Prototype Retrieval` 未超过强随机 baseline
- 报告材料：
  - `report/phase6_big_plus_results.md`
  - `report/phase6_big_plus_results_zh.md`

### 完成标准

- 方法冻结完成标准：
  - Big Plus 已经形成清楚的问题定义、方法描述和对照实验结构
  - `notebooks/phase6_big_plus_adult.md` 已记录方法定义、实验设计、预期输出和风险
- Phase 6 完整完成标准：
  - `Adult` 上至少有一轮完整方法对比结果
  - 结果表和图表可以支撑 Big Plus 主实验讨论

## Phase 7：Big Plus 次验证与稳健性判断

### 目标

- 判断 Big Plus 是否只在 `Adult` 上偶然有效
- 在 `Bank Marketing` 上轻量验证最强方法
- 对“泛化性”和“局限性”做出明确判断

### 次验证固定比较对象

- 原始 `TabICL`
- 最强随机策略
- `Balanced Prototype Retrieval`
- 最强树模型 baseline

### 阶段产出

- 次验证结果表
- 对泛化性与局限性的判断
- Big Plus 在报告中的表述口径
- 当前阶段学习型文档：`notebooks/phase7_big_plus_validation.md`

### 完成标准

- 至少完成一个次数据集验证
- 能明确回答 Big Plus 是“有效改进”还是“有价值的负结果”

## Phase 8：报告、图表、PPT 和最终提交整理

### 目标

- 把主线结果和 Big Plus 结果整合成一个完整项目故事
- 固定报告结构与演示结构
- 明确哪些结论可以作为核心结论，哪些需要附限制说明
- 准备最终提交材料

### 报告结构

- `Introduction`
- `Related Models`
- `Datasets`
- `Experimental Setup`
- `Mainline Results`
- `Scalability and Cost Analysis`
- `Big Plus Method and Results`
- `Discussion and Limitations`
- `Conclusion`

### 演示结构

- 题目背景
- 为什么比较 foundation models
- 主线实验设计
- 主线结果
- scalability 与 runtime 观察
- Big Plus 动机
- Big Plus 方法
- Big Plus 结果
- 结论与局限

### 阶段产出

- 英文报告正文
- 15 分钟 PPT
- 图表与表格清单
- 口头讲解主线
- 依赖版本记录
- 当前阶段学习型文档：`notebooks/phase8_final_delivery.md`

### 完成标准

- 报告已经可以从头读到尾
- PPT 已经能支撑 15 分钟完整讲解
- 所有核心结论都有对应结果表或图表支撑

## Notebook Markdown 规则

从现在起，每推进一个阶段，都必须在 `notebooks/` 下新增一篇中文学习型 `md`。

### 命名规则

- `phaseX_主题名.md`

### 写作风格

- 默认中文
- 风格固定为“教学 + 复盘”
- 可以出现英文术语，但必须解释清楚

### 固定结构

每篇 `md` 都按下面的顺序写：

1. `阶段目标`
2. `这一阶段做了什么`
3. `关键概念学习`
4. `为什么这样设计`
5. `当前结果说明了什么`
6. `遇到的问题与风险`
7. `下一阶段怎么接`

## Docs 同步规则

### 只要阶段推进，就同步更新

- `docs/project_record.md`
- `docs/work_log.md`
- `docs/session_handoff.md`

### 只要真实实验完成，就额外更新

- `docs/experiment_log.md`

### 只要总规划、优先级、Big Plus 设计发生变化，就同步更新

- `docs/phase_plan.md`
- `docs/big_plus_plan.md`

## 当前默认优先顺序

1. 继续 Phase 6/Phase 8 交界处的写作整理：英文报告正文、figure captions、结果表和讨论段。
2. 更新 PPT/展示材料中的 Big Plus 页，写成支持集选择 ablation 和负结果。
3. 暂不启动 Phase 7；如未来启动，必须基于新的验证目的，而不是回改 Phase 6 冻结方法。

## 新开对话时推荐阅读顺序

1. `docs/session_handoff.md`
2. `docs/phase_plan.md`
3. `docs/project_record.md`
4. `docs/big_plus_plan.md`
5. 当前阶段对应的 `notebooks/phaseX_*.md`
