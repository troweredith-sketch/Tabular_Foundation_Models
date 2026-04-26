# 项目记忆卡

这是一张给后续对话快速续接用的短记忆卡。
如果新开对话，默认先读这份文件，再读 `docs/phase_plan.md`、`docs/project_record.md` 和 `docs/big_plus_plan.md`。

## 项目身份

- 项目主题：Tabular Foundation Models
- 项目类型：机器学习课程项目
- 最终交付：英文报告 + 15 分钟演示
- 截止时间：`2026-05-04`
- 当前学习方式：边学习边实验
- 当前推进方式：硬要求优先，再做 Big Plus
- 报告/PPT 骨架类交付偏好：默认中英各一份，英文用于最终交付，中文作为理解和复盘参照

## 当前项目范围

- 只做表格分类任务
- 主线模型：`TabPFN v2`、`TabICL`、`LightGBM`、`XGBoost`
- 主线数据集：`Adult`、`Bank Marketing`
- 备用数据集：`Credit-G`
- Big Plus 方向：基于 `TabICL` 的检索式支持集选择改进
- 不新增模型、不扩展到 regression 或 survival analysis

## 当前进度

- Phase 1 已完成：明确问题、学习基础概念、搭环境
- Phase 2 已完成：跑通 `Adult + LightGBM` baseline
- Phase 3 已完成：完成 `Adult` 上的公平性修正、`10k control` 和多 seed 稳定性评估
- Phase 4 已完成：完成 `Adult + Bank Marketing`、四模型、双场景、五 seeds 的主线比较
- Phase 5 已完成：已补齐主线 `balanced_accuracy`、`macro_f1`、完整 train-size scalability、主线图表、英文报告骨架和 15 分钟 PPT 骨架
- Phase 6 已完成：`TabICL` 支持集选择 Big Plus 方法冻结、Adult 主实验、图表和报告材料化
- Phase 6 脚本已实现，smoke test 和完整 Adult 主实验均已完成
- Phase 7 未开始，当前不建议启动；下一步应继续报告正文、caption、表格和展示材料整理

## 已有核心结果

- `Adult control_10k`：
  - `XGBoost accuracy_mean = 0.8698 ± 0.0022`
  - `LightGBM balanced_accuracy_mean = 0.7934`，`macro_f1_mean = 0.8097`
  - `TabICL balanced_accuracy_mean = 0.7909`，`macro_f1_mean = 0.8077`
  - `TabPFN v2 balanced_accuracy_mean = 0.7789`，`macro_f1_mean = 0.7966`
- `Bank Marketing control_10k`：
  - `TabICL accuracy_mean = 0.9093 ± 0.0021`，`balanced_accuracy_mean = 0.7397`，`macro_f1_mean = 0.7606`
  - `TabPFN v2 accuracy_mean = 0.9093 ± 0.0013`，`balanced_accuracy_mean = 0.7215`，`macro_f1_mean = 0.7504`
  - `LightGBM accuracy_mean = 0.9044 ± 0.0014`
  - `XGBoost accuracy_mean = 0.9040 ± 0.0016`
- Phase 5 train-size scalability：
  - 完整 detail CSV 共 `200` 行，summary CSV 共 `40` 行
  - 覆盖 `Adult`、`Bank Marketing`，train sizes 为 `512`, `2048`, `8192`, `10000`, `full`，seeds 为 `42,43,44,45,46`
  - `Adult` 上树模型从 `512` 到 `full` 的 `macro_f1` 增幅最大，`TabPFN v2` runtime 增幅最大
  - `Bank Marketing` 上所有模型随 train size 增大在 `balanced_accuracy` / `macro_f1` 上提升明显，`TabICL` 与 `TabPFN v2` 指标整体更强
- Phase 5 图表和骨架：
  - 已生成 `results/figures/phase5_scalability_accuracy.*`
  - 已生成 `results/figures/phase5_scalability_balanced_accuracy.*`
  - 已生成 `results/figures/phase5_scalability_macro_f1.*`
  - 已生成 `results/figures/phase5_scalability_total_seconds_median.*`
  - 已创建英文版 `report/outline.md` 和 `slides/outline.md`
  - 已创建中文版参照 `report/outline_zh.md` 和 `slides/outline_zh.md`
- `TabICL` 在两个数据集上都明显快于 `TabPFN v2`，因此仍是 Big Plus 的合适入口
- Phase 6 方法冻结：
  - 已创建 `notebooks/phase6_big_plus_adult.md`
  - 已新增 `src/phase6_big_plus_adult.py`
  - 已冻结四种策略：`Full Context`、`Random Subset`、`Balanced Random Subset`、`Balanced Prototype Retrieval`
  - `Balanced Prototype Retrieval` 固定使用训练 split 构造检索空间：数值特征 median 填补 + 标准化，类别特征 most frequent 填补 + one-hot
  - 距离度量固定为欧氏距离，类内选择最接近类别中心的样本
  - 类别配额先按类别平衡分配，剩余预算按训练集类别规模比例补齐；类别样本不足时全部保留并重分配剩余预算
  - 不使用测试标签、测试特征或测试分布
  - 预算固定为 `512`、`2048`、`8192`，seeds 固定为 `42`、`43`、`44`
- Phase 6 smoke test：
  - 命令：`python3 src/phase6_big_plus_adult.py --budgets 512 --seeds 42`
  - 已生成 `results/phase6_big_plus_adult.csv` 和 `results/phase6_big_plus_adult_summary.csv`
  - smoke test 只作为历史工程记录，不作为正式结论
- Phase 6 Adult 主实验：
  - detail CSV：`results/phase6_big_plus_adult.csv`，共 `30` 行
  - summary CSV：`results/phase6_big_plus_adult_summary.csv`，共 `10` 行
  - strategies：`full_context`、`random_subset`、`balanced_random_subset`、`balanced_prototype_retrieval`
  - budgets：`512`、`2048`、`8192`
  - seeds：`42`、`43`、`44`
  - 已确认 `requested_budget`、`actual_support_size`、`support_class_counts` 都被记录且无缺失
  - 三个 budget-limited 策略在同一 `budget/seed` 下 `requested_budget` 一致
- Phase 6 结果图表：
  - `results/figures/phase6_big_plus_adult_accuracy.*`
  - `results/figures/phase6_big_plus_adult_balanced_accuracy.*`
  - `results/figures/phase6_big_plus_adult_macro_f1.*`
  - `results/figures/phase6_big_plus_adult_total_seconds_median.*`
  - `results/figures/phase6_big_plus_adult_bpr_delta.*`
- Phase 6 报告材料：
  - `report/phase6_big_plus_results.md`
  - `report/phase6_big_plus_results_zh.md`
  - `notebooks/phase6_big_plus_adult.md`
- Phase 6 核心结论：
  - `Balanced Prototype Retrieval` 没有优于 `Random Subset` / `Balanced Random Subset`
  - `Balanced Random Subset` 在 balanced accuracy 上最强
  - `Random Subset` 在 accuracy 和 macro-F1 上更稳
  - `Full Context` 效果最好但 runtime 明显更高
  - 这是有价值的负结果，不要为了追分修改冻结方法

## 当前必须保留的口径

- 主线已补齐 `balanced_accuracy`、`macro_f1`、train-size scalability、size-vs-metric / size-vs-runtime 图表和英文报告/PPT 骨架
- 主线目前已经可以独立支撑课程报告
- 当前多 seed 实验应表述为 repeated stratified splits：每个 seed 内模型共享同一 split，跨 seeds 不是同一个固定测试集
- 当前 runtime 是 practical mixed-device timing，树模型在 CPU，foundation models 可能在 GPU
- 当前树模型是 fixed strong baselines，不是 tuned SOTA baselines
- 当前 `Adult` 和 `Bank Marketing` 是 OpenML datasets，不能包装成 TALENT 或 TabArena 实验
- Phase 6 Adult 主实验已经完成，但不要把 Big Plus 写成成功方法
- Phase 6 smoke test 只是历史工程记录；正式结论以 30 行 Adult 主实验为准
- 当前冻结版 `Balanced Prototype Retrieval` 未超过强随机 baseline，应写成负结果 ablation
- `Full Context` 是完整训练 split reference，不是和 `512/2048/8192` 完全预算公平的 baseline

## 当前推荐下一步

1. 继续 Phase 6 论文/报告整理：英文正文段落、figure captions、结果表和讨论段。
2. 把 `report/phase6_big_plus_results.md` 的内容压缩进最终报告正文。
3. 更新 PPT/展示材料中的 Big Plus 页，但暂不启动 Phase 7。

## 必读文件

1. `docs/session_handoff.md`
2. `docs/phase_plan.md`
3. `docs/project_record.md`
4. `docs/big_plus_plan.md`
5. `docs/experiment_log.md`
6. 当前阶段对应的 `notebooks/phaseX_*.md`

## 高优先级原则

- 优先补齐原始要求，不盲目追求复杂模型
- 主线必须能独立成稿，Big Plus 是加分项
- 每推进一个阶段，就同步更新 `docs/` 和 `notebooks/phaseX_*.md`
- 报告/PPT 骨架、展示叙事、最终提纲默认中英各一份
- 不要让不同文档出现互相冲突的“下一步”

## 常用情景模板

### 1. 新开对话

```text
请先阅读 docs/session_handoff.md、docs/phase_plan.md、docs/project_record.md、docs/big_plus_plan.md、docs/experiment_log.md。
如果当前阶段已有 notebooks/phaseX_*.md，也请一起阅读。
先用 5 条总结当前项目状态，再继续帮助我完成下一步。
```

### 2. 开始今天的工作

```text
请先阅读 docs/session_handoff.md、docs/phase_plan.md、docs/experiment_log.md，
告诉我今天最适合推进的 1-2 个任务，并说明为什么先做它们。
```

### 3. 完成一次实验后更新记录

```text
我刚完成了一次实验。请先阅读 docs/session_handoff.md、docs/experiment_log.md、docs/phase_plan.md，
把这次实验的设置、结果、观察和下一步写进 docs/experiment_log.md，
并同步补充 docs/work_log.md、docs/project_record.md 和 docs/session_handoff.md。
```

### 4. 写报告或做展示前

```text
请先阅读 docs/session_handoff.md、docs/project_record.md、docs/experiment_log.md、docs/phase_plan.md，
基于当前项目进度，帮我整理一版可以直接转成英文报告/PPT 的结构化要点。
```
