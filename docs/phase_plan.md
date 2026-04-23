# 项目阶段计划（双轨推进版）

这份文档用于替代旧的线性阶段计划。  
从 `2026-04-23` 起，项目不再只按“先比较、后分析”的单线方式推进，而是改为：

- `主线轨道`：完成课程项目必须有的模型比较与结果表
- `Big Plus 轨道`：围绕 `TabICL` 设计并验证一个检索式支持集选择改进

这份新计划有 4 个目的：

1. 让课程主线结果更稳，不会因为加分项失控而拖垮整体交付
2. 让 Big Plus 有清晰的问题定义，而不是临时拼凑
3. 让每个阶段都有明确产出、记录入口和学习沉淀
4. 让后续任何一次新对话都能快速续接当前状态

## 项目约束

- 最终交付：英文报告 + 15 分钟演示
- 截止时间：`2026-05-04`
- 当前定位：机器学习初学者，边学边做
- 当前任务类型：只做表格分类，不扩展到回归
- 当前主线模型范围：`TabPFN v2`、`TabICL`、`LightGBM`、`XGBoost`
- 当前数据集策略：
  - 主深挖：`Adult`
  - 次验证：`Bank Marketing`
  - 备用：`Credit-G`
- 当前 Big Plus 方向：基于 `TabICL` 的检索式支持集选择改进

## 双轨总原则

### 主线轨道

- 目标是完成课程项目主体结果
- 重点是公平比较、统一字段、统一划分、统一口径
- 如果 Big Plus 进度受阻，主线仍然必须能独立成稿

### Big Plus 轨道

- 目标是提出一个比“直接跑现成模型”更进一步的方法性贡献
- 当前固定主题：`TabICL` 的支持集选择策略
- 默认证据结构：`一个主深挖数据集 + 一个次验证数据集`

## 阶段总览

| 阶段 | 时间窗口 | 核心目标 | 当前状态 |
| --- | --- | --- | --- |
| Phase 1 | 4月16日 | 明确问题、学习基础概念、搭环境 | 已完成 |
| Phase 2 | 4月16日-4月22日 | 跑通第一个真实数据集 baseline | 已完成 |
| Phase 3 | 4月23日 | 主线口径修正与公平性加固 | 已完成 |
| Phase 4 | 4月24日-4月28日 | 主线模型与数据集补齐 | 未开始 |
| Phase 5 | 4月28日-5月1日 | Big Plus 方法定义与主数据集深挖 | 未开始 |
| Phase 6 | 5月1日-5月2日 | Big Plus 次验证与稳健性判断 | 未开始 |
| Phase 7 | 5月2日-5月4日 | 结果整合、英文报告与演示转写 | 未开始 |

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

已完成。

### 本阶段完成了什么

- 保留了 `Adult + LightGBM vs TabPFN v2` 的 full Adult 正式对比
- 明确这组 full Adult 结果属于“受限条件结果”
- 补做了 `Adult 10k control` 控制实验
- 完成了 `seeds = 42, 43, 44, 45, 46` 的多 seed 稳定性评估
- 统一了第三阶段脚本的结果字段、默认入口和输出方式
- 完成了当前阶段学习型文档：`notebooks/phase3_fairness_reset.md`

### 本阶段为什么重要

这个阶段的意义，不是再多跑一个模型，而是先判断：

- 当前结果能不能直接作为主结论
- 如果不能，需要补什么控制实验
- 后续主线比较应该沿用什么统一口径

如果不先处理这一步，后面无论接 `TabICL` 还是做 Big Plus，都可能建立在不稳的结论之上。

### 阶段产出

- `src/phase3_adult_compare.py`
- `results/phase3_adult_compare.csv`
- `results/phase3_adult_compare_10k.csv`
- `results/phase3_adult_compare_summary.csv`
- `docs/experiment_log.md` 中的实验 003、实验 004 和实验 005
- `notebooks/phase3_fairness_reset.md`

### 已采用的统一字段

- `dataset`
- `scenario`
- `seed`
- `split`
- `model`
- `metric`
- `accuracy`
- `fit_seconds`
- `predict_seconds`
- `total_seconds`
- `device`
- `train_size`
- `test_size`
- `n_samples_total`
- `n_features_raw`
- `n_numeric_features`
- `n_categorical_features`
- `n_features_after_preprocessing`
- `random_state`
- `test_size_ratio`
- `data_cache`
- `input_representation`
- `notes`

### Phase 3 最终结论

- `10k control` 的多 seed 结果告诉我们：`LightGBM` 以 `0.8692 ± 0.0014` 稳定高于 `TabPFN v2` 的 `0.8614 ± 0.0031`
- full Adult 的多 seed 结果告诉我们：这个方向在受限条件场景下也没有被推翻，但仍必须带限制说明

因此，Phase 3 的方向没有被推翻，只是现在证据更稳了。

### 完成标准

- 已明确记录当前 full Adult 结果的限制条件
- 已固定第三阶段比较字段
- 已补做并记录 `Adult` 控制实验
- 已完成多 seed 稳定性评估并生成 summary 结果表
- 已形成可写进报告的 Phase 3 结论口径

### 阶段结束后应更新

- `docs/project_record.md`
- `docs/work_log.md`
- `docs/session_handoff.md`
- `docs/experiment_log.md`
- `notebooks/phase3_fairness_reset.md`

## Phase 4：主线模型与数据集补齐

### 目标

- 在 `Adult` 上正式接入 `TabICL`
- 将 `XGBoost` 纳入统一主线比较
- 将主线扩展到 `Bank Marketing`
- 保持统一划分、统一指标、统一结果表结构

### 主线最终比较范围

- 模型：`TabPFN v2`、`TabICL`、`LightGBM`、`XGBoost`
- 数据集：`Adult`、`Bank Marketing`

### 阶段产出

- 主线总结果表
- 至少两个数据集的统一比较结果
- 对 4 个模型优缺点的初步观察
- 当前阶段学习型文档：`notebooks/phase4_mainline_completion.md`

### 完成标准

- 四个模型都能进入同一主线结果表
- 至少两个数据集能按统一字段输出结果
- 主线本身已经足够支撑课程项目主体部分

### 阶段结束后应更新

- `docs/project_record.md`
- `docs/work_log.md`
- `docs/session_handoff.md`
- `docs/experiment_log.md`
- `notebooks/phase4_mainline_completion.md`

## Phase 5：Big Plus 方法定义与主数据集深挖

### 目标

- 正式提出自己的方法性贡献
- 围绕 `TabICL` 设计支持集选择策略，而不是只比较现成模型
- 在 `Adult` 上做 Big Plus 主深挖

### Big Plus 固定比较策略

- `Full Context`
- `Random Subset`
- `Balanced Random Subset`
- `Balanced Prototype Retrieval`

### 固定实验设置

- 主数据集：`Adult`
- 上下文预算：`512`、`2048`、`8192`
- 随机种子：`42`、`43`、`44`

### 阶段产出

- Big Plus 方法定义
- `Adult` 上的策略对比表
- 准确率与运行时间随上下文预算变化的图
- 失败案例或负面结果分析
- 当前阶段学习型文档：`notebooks/phase5_big_plus_design.md`

### 完成标准

- Big Plus 已经形成清楚的问题定义、方法描述和对照实验结构
- `Adult` 上至少有一轮完整方法对比结果

### 阶段结束后应更新

- `docs/project_record.md`
- `docs/work_log.md`
- `docs/session_handoff.md`
- `docs/experiment_log.md`
- `docs/big_plus_plan.md`
- `notebooks/phase5_big_plus_design.md`

## Phase 6：Big Plus 次验证与稳健性判断

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
- 当前阶段学习型文档：`notebooks/phase6_big_plus_validation.md`

### 完成标准

- 至少完成一个次数据集验证
- 能明确回答 Big Plus 是“有效改进”还是“有价值的负结果”

### 阶段结束后应更新

- `docs/project_record.md`
- `docs/work_log.md`
- `docs/session_handoff.md`
- `docs/experiment_log.md`
- `docs/big_plus_plan.md`
- `notebooks/phase6_big_plus_validation.md`

## Phase 7：结果整合、英文报告与演示转写

### 目标

- 把主线结果和 Big Plus 结果整合成一个完整项目故事
- 固定报告结构与演示结构
- 明确哪些结论可以作为核心结论，哪些需要附限制说明

### 报告结构

- `Introduction`
- `Related Models`
- `Datasets`
- `Experimental Setup`
- `Mainline Results`
- `Big Plus Method and Results`
- `Discussion`
- `Conclusion`

### 演示结构

- 题目背景
- 为什么比较 foundation models
- 主线实验设计
- 主线结果
- Big Plus 动机
- Big Plus 方法
- Big Plus 结果
- 结论与局限

### 阶段产出

- 报告提纲
- PPT 提纲
- 图表与表格清单
- 口头讲解主线
- 当前阶段学习型文档：`notebooks/phase7_report_bridge.md`

### 完成标准

- 报告已经可以从头写到尾
- PPT 已经能支撑 15 分钟完整讲解

### 阶段结束后应更新

- `docs/project_record.md`
- `docs/work_log.md`
- `docs/session_handoff.md`
- `report/`
- `slides/`
- `notebooks/phase7_report_bridge.md`

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

### 作用

- 不是流水账
- 是写给“未来的你”的学习型说明文档
- 后续写报告、做 PPT、复盘项目时都可以直接复用

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

1. 完成 Phase 4 的主线模型与数据集补齐
2. 在 `Adult` 上接入 `TabICL`
3. 把 `XGBoost` 补进统一主线结果表
4. 将主线扩展到 `Bank Marketing`
5. 再进入 Big Plus 方法实验

## 新开对话时推荐阅读顺序

1. `docs/session_handoff.md`
2. `docs/phase_plan.md`
3. `docs/project_record.md`
4. `docs/big_plus_plan.md`
5. 当前阶段对应的 `notebooks/phaseX_*.md`
