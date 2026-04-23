# 项目记忆卡

这是一张给后续对话快速续接用的超短记忆卡。

如果新开对话，默认先让 AI 阅读这份文件，再决定是否继续读 `docs/phase_plan.md`、`docs/project_record.md` 和 `docs/big_plus_plan.md`。

## 项目身份

- 项目主题：Tabular Foundation Models
- 项目类型：机器学习课程项目
- 最终交付：英文报告 + 15 分钟演示
- 截止时间：`2026-05-04`
- 当前学习方式：边学习边实验
- 当前推进方式：`双轨推进`

## 用户画像

- 机器学习基础：几乎零基础
- 编程基础：会基本 Python，会一点 numpy、pandas、postgresql
- 算力：普通笔记本，必要时可考虑云服务器
- 目标风格：学习成长型，但愿意挑战 Big Plus
- 可投入时间：每周约 10 小时

## 当前项目范围

- 只做分类任务
- 主线模型：`TabPFN v2`、`TabICL`、`LightGBM`、`XGBoost`
- 数据集策略：
  - 主深挖：`Adult`
  - 次验证：`Bank Marketing`
  - 备用：`Credit-G`
- 当前 Big Plus 方向：基于 `TabICL` 的检索式支持集选择改进
- 当前重点指标：`accuracy`、`runtime`、`context budget sensitivity`

## 当前进度

- 第 1 阶段已完成
- 第 2 阶段已完成
- 第 3 阶段已完成
- 第 4 阶段已完成
- 已完成第一个真实数据集实验：`Adult + LightGBM baseline`
- 已完成第一次正式对比：`Adult + LightGBM vs TabPFN v2`
- 已完成 `Adult 10k control` 控制实验
- 已将 `src/phase3_adult_compare.py` 升级为默认 `all` 的多 seed 脚本
- 已完成 `seeds = 42, 43, 44, 45, 46` 的 Phase 3 稳定性评估
- 已生成 `results/phase3_adult_compare_summary.csv`
- 已确认 full Adult 结果需要作为“受限条件结果”呈现
- 已确认在 `10,000` 样本控制实验中，`LightGBM accuracy_mean = 0.8692 ± 0.0014`
- 已确认在同一 `10k control` 设置下，`TabPFN v2 accuracy_mean = 0.8614 ± 0.0031`
- 已完成路线升级：从单线比较改为“主线比较 + Big Plus 检索改进”
- 已新增 Big Plus 正式规划文档：`docs/big_plus_plan.md`
- 已完成当前阶段学习型文档：`notebooks/phase3_fairness_reset.md`
- 已在项目本地 `.venv` 中正式接入 `tabicl==2.1.0`
- 已新增统一主线脚本：`src/phase4_mainline_compare.py`
- 已完成 `Adult + Bank Marketing` 的四模型双场景主线比较
- 已生成：
  - `results/phase4_mainline_compare.csv`
  - `results/phase4_mainline_compare_summary.csv`
- 已确认在 `Adult control_10k` 中：
  - `XGBoost accuracy_mean = 0.8698 ± 0.0022`
  - `LightGBM accuracy_mean = 0.8692 ± 0.0014`
  - `TabICL accuracy_mean = 0.8681 ± 0.0026`
  - `TabPFN v2 accuracy_mean = 0.8614 ± 0.0031`
- 已确认在 `Bank Marketing control_10k` 中：
  - `TabICL accuracy_mean = 0.9093 ± 0.0021`
  - `TabPFN v2 accuracy_mean = 0.9093 ± 0.0013`
  - `LightGBM accuracy_mean = 0.9044 ± 0.0014`
  - `XGBoost accuracy_mean = 0.9040 ± 0.0016`
- 已确认 `TabICL` 在 `Bank Marketing` 上达到与 `TabPFN v2` 相当或略优的准确率，但预测速度明显更快
- 已完成当前阶段学习型文档：`notebooks/phase4_mainline_completion.md`

## 必读文件

1. `docs/session_handoff.md`
2. `docs/phase_plan.md`
3. `docs/project_record.md`
4. `docs/big_plus_plan.md`
5. `docs/experiment_log.md`
6. 当前阶段对应的 `notebooks/phaseX_*.md`

## 高优先级原则

- 优先帮助用户理解，而不是只给结果
- 主线比较必须先站稳，再推进 Big Plus
- 每推进一个阶段，就同步更新 `docs/` 和 `notebooks/phaseX_*.md`
- 不要让不同文档出现互相冲突的“下一步”

## 当前推荐下一步

1. 在 `Adult` 上正式开始 Phase 5 的 Big Plus 方法实验
2. 先固定 `TabICL` 的 4 种支持集策略，不要反复改问题定义
3. 用 `512 / 2048 / 8192` 上下文预算和 `42 / 43 / 44` 三个 seeds 形成第一轮主数据集结果
4. 保留 Phase 4 主线结果作为 Big Plus 的基础参照，不再回头改主表口径
5. 在 `Adult` 主深挖稳定后，再进入 `Bank Marketing` 次验证

## Phase 4 当前结论

- `Adult` 的公平主证据 `control_10k` 说明：树模型仍然最强，`XGBoost` 和 `LightGBM` 基本并列领先，`TabICL` 已接近但尚未超越，`TabPFN v2` 继续落后
- `Bank Marketing` 的 `control_10k` 和 `full_train_reference` 都说明：foundation model 开始展现优势，`TabICL` 与 `TabPFN v2` 的准确率整体高于树模型
- `TabICL` 在两个数据集上都明显快于 `TabPFN v2`，而在 `Bank Marketing` 上还达到了最强或并列最强的准确率
- 因此，Phase 4 的主线已经足够支撑课程项目主体部分，而 `TabICL` 也已经成为最适合进入 Big Plus 的方法入口

## 阶段学习文档规则

- 从现在起，每推进一个阶段，都要在 `notebooks/` 下新增一篇中文学习型 `md`
- 风格固定为“教学 + 复盘”
- 固定结构：
  1. 阶段目标
  2. 这一阶段做了什么
  3. 关键概念学习
  4. 为什么这样设计
  5. 当前结果说明了什么
  6. 遇到的问题与风险
  7. 下一阶段怎么接

## 常用情景模板

### 1. 新开对话

```text
请先阅读 docs/session_handoff.md、docs/phase_plan.md、docs/project_record.md、docs/big_plus_plan.md、docs/experiment_log.md。
如果当前阶段已有 notebooks/phaseX_*.md，也请一起阅读。
先用 5 条总结当前项目状态，再继续帮助我完成下一步。
```

### 2. 完成一个阶段后更新记录

```text
我刚完成了一个阶段。请先阅读 docs/session_handoff.md 和 docs/project_record.md，
然后把本次进展同步更新到 docs/project_record.md、docs/work_log.md、docs/session_handoff.md，
并补写本阶段对应的 notebooks/phaseX_*.md。
如果有真实实验结果，再同步更新 docs/experiment_log.md。
最后给我一版“当前状态 + 下一步”的简短总结。
```

### 3. 完成一次实验后更新记录

```text
我刚完成了一次实验。请先阅读 docs/session_handoff.md、docs/experiment_log.md、docs/big_plus_plan.md，
把这次实验的设置、结果、观察和下一步写进 docs/experiment_log.md，
并同步补充 docs/work_log.md。
如果这次实验对应一个阶段收尾，也要补写 notebooks/phaseX_*.md。
```

### 4. 需要短交接摘要

```text
请先阅读 docs/session_handoff.md、docs/project_record.md、docs/work_log.md、docs/experiment_log.md、docs/big_plus_plan.md，
然后给我一版短交接摘要，只包含：
1. 当前做到哪一步
2. 最近完成了什么
3. 现在卡在哪里
4. 下一步最优先做什么
```

### 5. 开始今天的工作

```text
请先阅读 docs/session_handoff.md、docs/phase_plan.md、docs/big_plus_plan.md、docs/experiment_log.md，
告诉我今天最适合推进的 1-2 个任务，并说明为什么先做它们。
```

### 6. 写报告或做展示前

```text
请先阅读 docs/session_handoff.md、docs/project_record.md、docs/experiment_log.md、docs/big_plus_plan.md，
基于当前项目进度，帮我整理一版可以直接转成英文报告/PPT 的结构化要点。
```

## 更新规则

如果项目状态发生变化，优先更新以下 4 项：

1. `当前进度`
2. `当前推荐下一步`
3. `阶段学习文档规则`
4. `常用情景模板` 是否需要调整
