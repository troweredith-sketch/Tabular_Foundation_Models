> Final source of truth: use report/report_draft.md, results/*.csv, and report/submission_manifest.md for the submitted results. This file may include historical planning or work-log context.

# 项目过程日志

这份文档按时间记录每次学习、调试、写代码和推进项目时做了什么。

建议每次记录都尽量包含：

- 日期
- 花费时间
- 目标
- 实际完成内容
- 遇到的问题
- 解决方式
- 学到的东西
- 下一步

---

## 2026-04-16

### 花费时间

约 1 个工作阶段

### 目标

完成项目第一阶段，建立学习和实验的起点。

### 实际完成内容

- 明确项目问题和研究范围
- 选择第一阶段的学习顺序
- 学习 `classification`、`train/test split`、`accuracy`、`overfitting`、`categorical features`、`missing values`
- 完成一个使用 `breast_cancer` 数据集的教学实验
- 搭建本地 `.venv`
- 安装 `jupyterlab`、`numpy`、`pandas`、`scikit-learn`、`openml`、`xgboost`、`lightgbm`
- 创建中文 notebook：`notebooks/phase1_concepts_demo.ipynb`
- 初始化 Git 仓库并推送到 GitHub
- 建立项目记录体系：`project_record.md`、`work_log.md`、`experiment_log.md`
- 读取并修订外部的初步阶段计划
- 新增项目记忆卡 `session_handoff.md`

### 遇到的问题

- `jupyter` 初始未安装
- `lightgbm` 安装后缺少系统运行库 `libgomp.so.1`
- WSL 里 `gh auth login` 无法自动打开浏览器

### 解决方式

- 在项目虚拟环境中安装 `jupyterlab`
- 安装系统库 `libgomp1`
- 手动打开 GitHub device login 页面完成 `gh` 登录

### 学到的东西

- 训练集和测试集必须区分，不然很难判断泛化能力
- 训练集准确率非常高时，需要警惕过拟合
- 环境搭建过程本身也是项目推进的一部分，值得记录
- 如果把关键信息沉淀到仓库文件里，就不用依赖超长对话记忆

### 下一步

- 进入第二阶段
- 加载第一个真实表格分类数据集
- 跑通一个 baseline 模型
- 每次推进后同步更新记忆卡和日志

---

## 2026-04-16（第二阶段推进）

### 花费时间

约 1 个工作阶段

### 目标

进入第二阶段，在第一个真实表格数据集上跑通 baseline。

### 实际完成内容

- 选定 `Adult` 作为第一个真实数据集
- 从 `OpenML` 成功加载数据
- 检查样本数、特征数、目标分布、类别特征和缺失值
- 确认 `workclass`、`occupation`、`native-country` 存在缺失值
- 确认该数据集有 8 个类别特征、6 个数值特征
- 使用 `LightGBM` 完成第一个 baseline
- 编写 `notebooks/phase2_adult_baseline.ipynb`
- 生成 `results/first_result.csv`
- 更新项目计划、记忆卡和项目记录

### 遇到的问题

- notebook 通过 `nbconvert` 执行时，结果文件保存到错误的相对路径

### 解决方式

- 修改 notebook 中的保存逻辑，让它先判断项目根目录，再写入 `results/first_result.csv`

### 学到的东西

- 第二阶段的重点是建立第一条正式实验链路，而不是立刻追求最高分
- 真实数据集实验前，必须先做列类型、缺失值和目标分布检查
- 相对路径在 notebook 和自动执行环境里可能不一致，需要写得更稳妥

### 下一步

- 进入第三阶段
- 接入 `TabPFN v2`
- 在 Adult 数据集上与 LightGBM 做第一次正式对比

---

## 2026-04-22（第二阶段收尾确认）

### 花费时间

约 1 次阶段复盘

### 目标

确认第二阶段已经完成，并把项目记录正式同步到“进入第三阶段”的状态。

### 实际完成内容

- 复查项目记忆卡和项目总记录
- 确认第二阶段目标已经达成：第一个真实数据集实验和 baseline 已完成
- 将 `project_record.md` 中的阶段状态更新为“Phase 2 已完成，Phase 3 进行中”
- 将第二阶段的正式完成时间同步到当前日期
- 补充工作日志和实验日志中的阶段归属说明

### 遇到的问题

- 文档中之前已经记录“第二阶段已完成”，但缺少“2026-04-22 正式确认收尾”的痕迹

### 解决方式

- 在 `project_record.md` 和 `work_log.md` 中补写阶段收尾确认记录
- 在 `experiment_log.md` 中明确 Adult baseline 是 Phase 2 的官方基线实验

### 学到的东西

- 阶段“实验跑通”和阶段“正式收尾确认”是两件相关但不完全相同的事
- 在项目推进中，阶段状态最好和当前日期保持一致，方便回顾和展示

### 下一步

- 进入第三阶段
- 接入 `TabPFN v2`
- 在 Adult 数据集上与 LightGBM baseline 做第一次正式对比

---

## 2026-04-22（第三阶段启动）

### 花费时间

约 1 个工作阶段

### 目标

正式进入第三阶段，接入 `TabPFN v2`，并在固定 Adult 测试集上与 `LightGBM` 做第一次正式对比。

### 实际完成内容

- 检查并复用第二阶段的 Adult baseline notebook 逻辑
- 在项目本地 `.venv` 中安装 `tabpfn`
- 新增可复现实验脚本：`src/phase3_adult_compare.py`
- 复用 Adult 本地缓存和 `random_state=42` 的固定训练/测试集划分
- 在同一测试集上运行 `LightGBM` 和 `TabPFN v2`
- 生成结果文件：`results/phase3_adult_compare.csv`
- 将第三阶段第一次正式对比的结果同步写回项目记录

### 遇到的问题

- `TabPFN v2` 默认不接受当前 Adult 全量训练集规模
- 报错提示官方支持上限为 `10,000` 个样本，而当前训练集大小是 `39,073`

### 解决方式

- 保持训练/测试集划分不变
- 在 `TabPFN v2` 实验里显式设置 `ignore_pretraining_limits=True`
- 同时把这个限制条件写进脚本说明和实验记录，而不是把它隐藏掉

### 学到的东西

- 第三阶段除了比较准确率，还要记录模型能不能顺利接入、有哪些真实限制
- `TabPFN v2` 在这个任务上不是“装好就直接公平比较”，它对数据规模有明确前提
- 即使有 GPU，实际预测耗时也可能远高于树模型，因此运行成本本身就是结果的一部分

### 下一步

- 做一个训练样本不超过 `10,000` 的 Adult 控制实验
- 判断当前全量 Adult 结果在报告里应该如何表述
- 再决定是否继续扩展到下一数据集或模型

---

## 2026-04-23（路线升级与双轨规划）

### 花费时间

约 1 次规划重构

### 目标

- 判断当前项目方向是否需要修改
- 决定是否挑战 Big Plus
- 把后续阶段、文档同步规则和学习型沉淀规则一次性定清楚

### 实际完成内容

- 重新阅读项目要求，并对照当前仓库进度判断方向是否需要改轨
- 确认项目主方向不变，但推进方式升级为“双轨推进”
- 确定 Big Plus 主方向为：基于 `TabICL` 的检索式支持集选择改进
- 重写 `docs/phase_plan.md`，把当前阶段重定义为“主线口径修正与公平性加固”
- 新增 `docs/big_plus_plan.md`，作为 Big Plus 正式说明文档
- 更新 `docs/project_record.md` 和 `docs/session_handoff.md`
- 新增当前阶段学习型文档：`notebooks/phase3_fairness_reset.md`
- 确认从现在起每推进一个阶段，都要在 `notebooks/` 下新增一篇中文“教学 + 复盘”风格的 `md`

### 遇到的问题

- 原来的阶段计划是单线结构，已经不适合“主线 + Big Plus”并行推进
- 如果直接写未来阶段结果，会让记录看起来像已经完成，和真实状态不一致

### 解决方式

- 保留历史阶段完成记录，不重写真实过去
- 将当前及之后的阶段改成新的双轨结构
- 只为当前已推进的阶段新增正式学习文档，未来阶段先写进路线图，等真正推进时再补对应 `md`

### 学到的东西

- 课程项目一旦开始追求加分项，就必须先把主线和支线分开管理
- 结果的“可运行性”和“可作为主结论的证据强度”必须分开判断
- 如果想让未来的自己继续推进，最有价值的不是堆更多文件，而是让每份文件各司其职

### 下一步

- 完成 Phase 3 的口径修正与统一字段定义
- 设计并执行 `Adult` 控制实验
- 接入 `TabICL`
- 继续推进主线模型与数据集补齐

---

## 2026-04-23（Phase 3 完成）

### 花费时间

约 1 次实验收尾 + 文档同步

### 目标

- 用一个更公平的控制实验把 Phase 3 真正做完
- 统一第三阶段脚本输出字段
- 把实验结论同步写回 `docs/` 和 `notebooks/`

### 实际完成内容

- 将 `src/phase3_adult_compare.py` 轻量重构为单入口双场景脚本
- 新增 `--scenario` 参数，支持：
  - `full_adult_limit_override`
  - `adult_control_10k`
- 统一第三阶段结果字段为固定 schema
- 重新生成 full Adult 受限条件结果
- 新增并运行 `Adult 10k control` 控制实验
- 生成：
  - `results/phase3_adult_compare.csv`
  - `results/phase3_adult_compare_10k.csv`
- 更新 `docs/experiment_log.md`
- 更新 `docs/project_record.md`
- 更新 `docs/session_handoff.md`
- 更新 `docs/phase_plan.md`
- 更新 `README.md`
- 将 `notebooks/phase3_fairness_reset.md` 升级为带真实结果的学习型阶段总结
- 在 `notebooks/phase3_adult_compare_guide.md` 开头补充说明，明确它是过程性指南

### 遇到的问题

- 需要确认 `TabPFN v2` 在 `10,000` 条训练样本时能否不加限制直接运行
- 需要保证控制实验和 full Adult 实验使用同一个测试集

### 解决方式

- 固定 `test_size=0.2`、`random_state=42`、`stratify=y`
- 先切固定测试集，再从原训练集内部抽 `10,000` 条样本做控制实验
- 在 `10,000` 条设置下直接运行成功，没有触发 `9,500` fallback

### 学到的东西

- 公平性修正不是删除旧结果，而是补上能解释旧结果的控制实验
- 控制实验最重要的是“只改一个关键条件”，这里改的是训练样本规模
- 结果字段一旦统一，后面 Phase 4 和写报告都会轻松很多

### 下一步

- 进入 Phase 4
- 在 `Adult` 上接入 `TabICL`
- 把 `XGBoost` 补进统一主线比较
- 将主线扩展到 `Bank Marketing`

---

## 2026-04-23（Phase 3 升级：多 seed 稳定性评估）

### 花费时间

约 1 次脚本重构 + 1 轮完整多 seed 运行 + 文档回填

### 目标

- 把 Phase 3 从“单次结果”升级成“多次运行后的稳定结论”
- 修复 `phase3_adult_compare.py` 直接运行时只执行 full Adult 的问题
- 让脚本默认同时跑 `full Adult` 和 `10k control`

### 实际完成内容

- 将 `src/phase3_adult_compare.py` 的 CLI 改成：
  - `--scenario all`
  - `--scenario full_adult_limit_override`
  - `--scenario adult_control_10k`
- 将默认行为改成直接运行时执行 `all`
- 新增 `--seeds` 参数，默认 `42 43 44 45 46`
- 把结果文件升级为多 seed 行级明细：
  - `results/phase3_adult_compare.csv`
  - `results/phase3_adult_compare_10k.csv`
- 新增汇总文件：
  - `results/phase3_adult_compare_summary.csv`
- 真实运行完成 `5 seeds × 2 scenarios × 2 models`
- 更新 `docs/experiment_log.md`，新增实验 005
- 更新 `docs/project_record.md`
- 更新 `docs/session_handoff.md`
- 更新 `docs/phase_plan.md`
- 更新 `README.md`
- 更新 `notebooks/phase3_fairness_reset.md`
- 更新 `notebooks/phase3_adult_compare_guide.md`

### 遇到的问题

- 旧版脚本默认 `--scenario = full_adult_limit_override`，所以直接运行时只会得到 full Adult 结果
- 单次结果更适合做锚点，不适合直接当最终统计结论
- 如果只重跑一个场景，summary 还需要能够从现有结果文件重新聚合

### 解决方式

- 把默认入口改成 `all`
- 让脚本在每个 seed 上重新做一次 split / subset，而不是机械重复同一条命令
- summary 统一从现有明细文件聚合生成

### 学到的东西

- 对课程项目来说，最有价值的重复实验是“多 seed / 多抽样”，而不是简单重复同一设置
- `accuracy` 更适合报告 `mean ± std`，运行时间更适合报告 `median`
- 一个脚本如果默认行为和文档不一致，很容易让后续自己误判项目状态

### 下一步

- Phase 3 已经可以封箱，后续默认引用 `results/phase3_adult_compare_summary.csv`
- 进入 Phase 4
- 在 `Adult` 上接入 `TabICL`
- 把 `XGBoost` 补进统一主线比较
- 将主线扩展到 `Bank Marketing`

---

## 2026-04-23（Phase 4 主线完成）

### 花费时间

约 1 次统一脚本开发 + 1 轮完整四模型双数据集实验 + 1 轮文档收尾

### 目标

- 正式进入 Phase 4
- 在 `Adult` 上接入 `TabICL`
- 把 `XGBoost` 补进统一主线比较
- 将主线扩展到 `Bank Marketing`
- 形成四模型、双数据集、双场景、五 seeds 的统一主线框架

### 实际完成内容

- 在项目本地 `.venv` 中安装 `tabicl==2.1.0`
- 读取 `tabicl` 本地源码，确认：
  - `TabICLClassifier` 的 sklearn 接口
  - 官方 checkpoint 版本
  - 内部 `TransformToNumerical` 预处理逻辑
- 将 `tabicl` 补入 `requirements-basic.txt`
- 新增统一主线脚本：`src/phase4_mainline_compare.py`
- 让脚本支持：
  - 数据集：`adult`、`bank_marketing`
  - 模型：`lightgbm`、`xgboost`、`tabpfn_v2`、`tabicl`
  - 场景：`control_10k`、`full_train_reference`
  - seeds：默认 `42 43 44 45 46`
- 新增 `Bank Marketing` 本地缓存：`data/raw/bank_marketing_openml.csv`
- 完整运行：
  - `2 datasets × 2 scenarios × 5 seeds × 4 models`
- 生成：
  - `results/phase4_mainline_compare.csv`
  - `results/phase4_mainline_compare_summary.csv`
- 更新：
  - `docs/experiment_log.md`
  - `docs/project_record.md`
  - `docs/work_log.md`
  - `docs/session_handoff.md`
  - `docs/phase_plan.md`
  - `README.md`
- 完成当前阶段学习型文档：`notebooks/phase4_mainline_completion.md`

### 遇到的问题

- 仓库里原本没有 `TabICL` 依赖，也没有现成的 Phase 4 主线脚本骨架
- `TabICL` 第一次运行需要下载官方 checkpoint，如果不先处理，会污染真实计时
- 需要在“不破坏 Phase 3 公平口径”的前提下，同时保留 full-train 参考结果

### 解决方式

- 先在本地环境安装 `tabicl`，再直接阅读包内源码确认真实 API
- 在统一脚本里先预热 `TabICL` checkpoint，再开始正式计时
- 采用双场景统一主表：
  - `control_10k` 作为公平主证据
  - `full_train_reference` 作为工程参考线
- 保持结果字段尽量沿用 Phase 3，只把 `dataset` 加入 summary 分组

### 学到的东西

- 统一脚本不是为了“写得更大”，而是为了后面每个新模型、新数据集都能无痛进入同一口径
- `Adult` 和 `Bank Marketing` 的模型排序并不相同，说明双数据集主线是必要的
- `TabICL` 比 `TabPFN v2` 更像一个“可继续做方法改进”的入口，因为它更快、而且在 `Bank Marketing` 上已经达到很强的准确率
- 报告里应该把“准确率”和“运行成本”一起讲，否则 foundation model 的优劣会被讲偏

### 下一步

- 进入 Phase 5
- 先补齐主线 `balanced_accuracy` 和 `macro_f1`
- 再补 train-size scalability
- Big Plus 顺延到 Phase 6

---

## 2026-04-24（Phase 5 指标补齐完成）

### 花费时间

约 1 次 smoke test + 1 轮完整主线重跑 + 文档同步

### 目标

- 完成 Phase 5 第一块：补齐 `accuracy` 之外的主线分类指标
- 让 Phase 4 主线结果同时包含 `balanced_accuracy` 和 `macro_f1`
- 不改变 Big Plus 方向，不新增模型，不扩展任务类型

### 实际完成内容

- 修改 `src/phase4_mainline_compare.py`
  - 新增 `balanced_accuracy_score`
  - 新增 `f1_score(average="macro")`
  - 四个模型统一写入 `accuracy`、`balanced_accuracy`、`macro_f1`
  - detail CSV 和 summary CSV 都扩展新指标列
- 先完成 smoke test：
  - `python3 src/phase4_mainline_compare.py --datasets adult --scenarios control_10k --seeds 42`
- 之后完整重跑主线：
  - `python3 src/phase4_mainline_compare.py --datasets adult bank_marketing --scenarios control_10k full_train_reference --seeds 42 43 44 45 46`
- 重新生成：
  - `results/phase4_mainline_compare.csv`
  - `results/phase4_mainline_compare_summary.csv`
- 校验结果：
  - detail CSV 共 `80` 行
  - summary CSV 共 `16` 行
  - 每个 summary 组合 `n_runs = 5`
  - seeds 均为 `42,43,44,45,46`
- 更新：
  - `docs/experiment_log.md`
  - `docs/project_record.md`
  - `docs/work_log.md`
  - `docs/session_handoff.md`
  - `docs/phase_plan.md`
  - `notebooks/phase5_mainline_requirements_closure.md`

### 遇到的问题

- 第一次后台启动完整实验时被外层命令超时机制截断，留下了不完整 CSV
- PowerShell 与 WSL 混合执行时，部分 here-doc / 引号写法会被错误解释

### 解决方式

- 改用 detached WSL 进程重新从头跑完整主线
- 用 `/tmp/tfm_phase5_mainline_rerun.log` 监控日志
- 用 CSV 行数和 summary 校验脚本确认最终结果完整

### 学到的东西

- 对不平衡数据集，只看 `accuracy` 容易漏掉重要差异
- 在 `Bank Marketing control_10k` 中，`TabICL` 和 `TabPFN v2` 的 `accuracy_mean` 相同，但 `TabICL` 的 `balanced_accuracy_mean` 和 `macro_f1_mean` 更高
- 长实验最好先做 smoke test，再完整重跑，并保留旧结果备份

### 下一步

- 进入 Phase 5 第二块：train-size scalability
- 默认 size grid：`512`, `2048`, `8192`, `10000`, `full`
- 继续只做当前四个模型和两个数据集，不新增模型、不调参、不进入 Big Plus

---

## 2026-04-24（Phase 5 完整 train-size scalability 完成）

### 花费时间

约 1 次完整长实验 + 校验 + 文档同步

### 目标

- 完成 Phase 5 第二块：train-size scalability
- 用固定模型、固定数据集、固定指标观察不同训练规模下的性能和运行时间变化
- 保持 Big Plus 方向不变，不新增模型、不调参、不扩展任务类型

### 实际完成内容

- 确认 smoke test 状态：
  - `src/phase5_scalability_compare.py` 已存在
  - `results/phase5_scalability_compare.csv` 已存在
  - `results/phase5_scalability_compare_summary.csv` 已存在
  - smoke 覆盖 `Adult + train_size=512 + seed=42 + 四个模型`
- 启动并完成完整 scalability 实验：

```bash
python3 src/phase5_scalability_compare.py \
  --datasets adult bank_marketing \
  --train-sizes 512 2048 8192 10000 full \
  --seeds 42 43 44 45 46
```

- 覆盖并生成：
  - `results/phase5_scalability_compare.csv`
  - `results/phase5_scalability_compare_summary.csv`
- 没有写入 Phase 4 结果文件：
  - `results/phase4_mainline_compare.csv`
  - `results/phase4_mainline_compare_summary.csv`

### 校验结果

- 实验退出码：`0`
- detail CSV：`200` 行
- summary CSV：`40` 行
- 每个 summary 组合：`n_runs = 5`
- seeds：`42,43,44,45,46`
- detail 组合最小/最大行数：`5 / 5`
- duplicate detail rows：`0`
- required detail / summary columns：无缺失

### 主要观察

- `Adult` 上，树模型从 `512` 到 `full` 的 `macro_f1` 增幅最大，尤其 `LightGBM`；`TabPFN v2` 指标提升最小但 runtime 增幅最大。
- `Bank Marketing` 上，所有模型随 train size 增大在 `balanced_accuracy` / `macro_f1` 上提升明显；`TabICL` 和 `TabPFN v2` 指标整体更强。
- runtime 最明显变化来自 foundation models：`TabPFN v2` 从几秒增长到约 `80` 秒量级，`TabICL` 从约 `3` 秒增长到约 `20` 秒量级；树模型仍保持亚秒到约 `1` 秒量级。
- `TabICL` 的 full runtime 明显低于 `TabPFN v2`，这继续支持后续 Big Plus 以 `TabICL` 为入口。

### 遇到的问题

- 上一个对话中完整实验已经启动但尚未收尾，当前对话需要先确认后台进程、日志、CSV 行数和退出码。
- 系统 Python 没有 `pandas`，校验脚本需要进入项目 `.venv` 后运行。

### 解决方式

- 继续监控原后台进程，没有重启实验。
- 用 `/tmp/tfm_phase5_scalability_full.log`、CSV 行数和退出码确认实验完成。
- 用 `.venv` 中的 `python3` 读取 CSV 做完整性校验。

### 学到的东西

- 完整 scalability 最慢部分集中在 `full` train size 下的 `TabPFN v2` 和 `TabICL`。
- 对 `Bank Marketing` 这类不平衡数据集，`balanced_accuracy` 和 `macro_f1` 比单看 `accuracy` 更能体现 train size 增长带来的改进。
- scalability 图表需要同时画 metric 和 runtime，否则容易只看到性能提升而忽略运行成本。

### 下一步

- 进入 Phase 5 的图表/报告骨架整理
- 优先生成 size-vs-metric 和 size-vs-runtime 图表草稿
- 建立英文报告和 PPT 的主线结果结构
- Big Plus 继续顺延到主线图表和报告骨架稳定之后

---

## 2026-04-26（Phase 5 主线图表与报告/PPT 骨架完成）

### 花费时间

约 1 次结果整理 + 文档同步

### 目标

- 完成 Phase 5 第三步：主线图表和报告/PPT 骨架整理
- 只使用已有 Phase 4/5 结果，不重跑实验、不新增模型、不调参、不进入 Big Plus
- 把已完成的主线实验转成可用于英文报告和 15 分钟展示的结构化材料

### 实际完成内容

- 新增可复现画图脚本：`src/phase5_make_mainline_figures.py`
- 从 `results/phase5_scalability_compare_summary.csv` 生成英文图表草稿
- 新建图表输出目录：`results/figures/`
- 生成 4 组 PNG/PDF 图表：
  - `phase5_scalability_accuracy`
  - `phase5_scalability_balanced_accuracy`
  - `phase5_scalability_macro_f1`
  - `phase5_scalability_total_seconds_median`
- 创建英文报告骨架：`report/outline.md`
- 创建 15 分钟英文 PPT 骨架：`slides/outline.md`
- 在报告和 PPT 骨架中写入 Adult、Bank Marketing、train-size scalability、runtime 和四模型优缺点的主线观察
- 明确写入 runtime caveat、split caveat、baseline caveat 和 full-reference caveat

### 本步骤目的

Phase 5 第三步把已完成的主线实验结果整理成可用于英文报告和 15 分钟展示的图表与结构化叙事。

### 遇到的问题

- `report/` 和 `slides/` 目录原本只有 `.gitkeep`，需要新建正式 outline 文件
- 图表需要同时服务英文报告和 PPT，因此必须用清晰英文标题、稳定模型颜色和双数据集 subplot

### 解决方式

- 将画图逻辑做成独立脚本，只读取已有 summary CSV，不改动实验结果
- 每张图都用 `Adult` 与 `Bank Marketing` 两个 subplot，固定 train-size 顺序为 `512`, `2048`, `8192`, `10000`, `full`
- runtime 图使用 log-scale y 轴，让树模型和 foundation models 的时间差异都可读

### 学到的东西

- 主线结果不仅需要 CSV，还需要被压缩成报告和展示能直接使用的叙事结构
- `Bank Marketing` 的结论必须依赖 `balanced_accuracy` 和 `macro_f1`，不能只看 `accuracy`
- runtime 结果可以说明实际使用成本，但必须保留 practical mixed-device timing 的限制说明

### 下一步

- Phase 5 主线已经可以独立支撑课程报告
- 后续已进入 Phase 6，并完成 `TabICL` 支持集选择 Big Plus 方法冻结
- Big Plus 方向保持不变，不新增模型、不扩展到 regression 或 survival analysis

---

## 2026-04-26（补充中文版报告/PPT 骨架）

### 花费时间

约 1 次文档补齐

### 目标

- 给已经创建的英文报告和 PPT 骨架补一份中文版参照
- 记录后续偏好：报告/PPT 骨架类材料默认中英各一份

### 实际完成内容

- 新增中文版报告骨架：`report/outline_zh.md`
- 新增中文版 15 分钟展示骨架：`slides/outline_zh.md`
- 更新 `docs/session_handoff.md`，记录“报告/PPT 骨架类交付默认中英各一份”

### 下一步

- 后续写报告正文、PPT 叙事或阶段性 presentation outline 时，默认同时保留英文交付版和中文参照版。

---

## 2026-04-26（Phase 6 Big Plus 方法冻结）

### 花费时间

约 1 次方法设计 + 文档同步

### 目标

- 进入 Phase 6 第一步：先冻结 `TabICL` 支持集选择 Big Plus 方法
- 不直接启动完整长实验
- 不改变主线范围，不新增模型、不调参、不扩展到 regression 或 survival analysis

### 实际完成内容

- 阅读并对齐 Phase 5 收口、Big Plus 规划、报告/PPT 骨架和当前项目记忆卡
- 新增 Phase 6 学习型文档：`notebooks/phase6_big_plus_adult.md`
- 更新 `docs/big_plus_plan.md`，将 Big Plus 方法冻结为 `v1`
- 同步更新：
  - `docs/phase_plan.md`
  - `docs/project_record.md`
  - `docs/session_handoff.md`
  - `docs/work_log.md`
- 固定四种支持集策略：
  - `Full Context`
  - `Random Subset`
  - `Balanced Random Subset`
  - `Balanced Prototype Retrieval`
- 明确 `Balanced Prototype Retrieval` 的算法细节：
  - 检索空间只由训练 split 构造
  - 数值特征使用训练 split median 填补并按训练 split mean/std 标准化
  - 类别特征使用训练 split most frequent 填补并 one-hot
  - 距离度量固定为欧氏距离
  - 类内选择最接近类别中心的样本
  - 类别配额先平衡，再按训练集类别规模比例补齐
  - 类别样本不足时全部保留并重分配剩余预算
  - 不使用测试标签、测试特征或测试分布
  - 与随机 baseline 使用相同 budgets、seeds 和 train/test splits

### 遇到的问题

- `Full Context` 使用完整训练 split，和 `512/2048/8192` 预算策略不是完全预算公平比较
- `Balanced Prototype Retrieval` 如果只选类别中心样本，可能忽略决策边界附近样本
- one-hot 后的类别维度可能影响欧氏距离

### 解决方式

- 将 `Full Context` 明确写成 budget-independent reference
- 将预算公平比较限定在 `Random Subset`、`Balanced Random Subset` 和 `Balanced Prototype Retrieval` 之间
- 先冻结当前版本，不在实验中临时改成边界检索或距离加权
- 将这些潜在问题写入 Phase 6 风险和后续结果解释口径

### 学到的东西

- Big Plus 的关键不是把方法写复杂，而是让每个对照回答一个清楚问题
- `Balanced Random Subset` 很重要，因为它能区分“类别平衡收益”和“原型检索收益”
- 方法冻结能保护后续实验解释，不会因为看了结果再改规则而失去可信度

### 下一步

- 实现 `src/phase6_big_plus_adult.py`
- 先跑 `Adult + budget 512 + seed 42` smoke test
- smoke test 通过后，再运行完整 Adult 主实验
- 真实实验完成前，不更新 `docs/experiment_log.md` 为 Phase 6 结果

---

## 2026-04-26（Phase 6 脚本实现与 smoke test）

### 花费时间

约 1 次脚本实现 + smoke test + CSV 校验

### 目标

- 实现 `src/phase6_big_plus_adult.py`
- 只做 `Adult + TabICL` 支持集选择实验脚本
- 实现四种已冻结策略
- 先跑 `budget=512, seed=42` smoke test，不启动完整长实验

### 实际完成内容

- 新增 `src/phase6_big_plus_adult.py`
- 实现命令行参数：
  - `--strategies`
  - `--budgets`
  - `--seeds`
- 默认参数设为 smoke-test 友好：
  - all four strategies
  - `budget=512`
  - `seed=42`
- 实现四种支持集策略：
  - `full_context`
  - `random_subset`
  - `balanced_random_subset`
  - `balanced_prototype_retrieval`
- 实现 frozen class quota 分配规则
- 实现 train-only 检索空间：
  - 数值列 median 填补 + 标准化
  - 类别列 most frequent 填补 + one-hot
  - 欧氏距离到类别中心
- 复用 Phase 4 的：
  - Adult 数据加载
  - repeated stratified split
  - TabICL checkpoint 预热
  - TabICL fit/predict
  - `accuracy`、`balanced_accuracy`、`macro_f1`
- 运行语法检查：

```bash
python3 -m py_compile src/phase6_big_plus_adult.py
```

- 运行 smoke test：

```bash
python3 src/phase6_big_plus_adult.py --budgets 512 --seeds 42
```

### 输出文件

- `results/phase6_big_plus_adult.csv`
- `results/phase6_big_plus_adult_summary.csv`

### Smoke test 校验

- detail CSV：`4` 行
- summary CSV：`4` 行
- strategies：
  - `full_context`
  - `random_subset`
  - `balanced_random_subset`
  - `balanced_prototype_retrieval`
- budgets：
  - `512`
  - `full`
- seeds：
  - `42`
- `requested_budget` 无缺失
- `actual_support_size` 无缺失
- `support_class_counts` 无缺失

### Smoke test 观察

- `full_context` 使用完整训练 split：`actual_support_size = 39073`
- 三种预算策略都使用 `requested_budget = 512` 且 `actual_support_size = 512`
- `balanced_random_subset` 和 `balanced_prototype_retrieval` 都得到 `{"<=50K": 256, ">50K": 256}`
- `random_subset` 得到 `{"<=50K": 410, ">50K": 102}`
- `Full Context` 本次运行耗时明显较长，后续完整 Adult 主实验需要显式确认后再启动

### 遇到的问题

- 第一次 CSV 检查命令被 PowerShell/WSL 引号处理影响，检查命令本身失败
- `cut` 读取 CSV 时会被 JSON 字符串中的逗号干扰

### 解决方式

- 改用 PowerShell `Import-Csv` 读取 WSL 路径下的 CSV 做字段完整性检查
- 保留脚本输出本身，不因为检查命令失败重跑实验

### 学到的东西

- `support_class_counts` 这种字段最好用合法 JSON 字符串保存，但检查时要使用 CSV parser，而不是简单 `cut`
- Full-context reference 的工程成本比预算受限策略高很多，后续完整实验需要主动控制节奏
- Smoke test 的价值是验证实现和 schema，不是提前解释方法优劣

### 下一步

- 审查 `src/phase6_big_plus_adult.py` 的 quota 分配、BPR 检索空间和输出列
- 确认后再运行完整 Adult 主实验
- 完整实验完成前，不把 smoke test 写成 Big Plus 正式成功或失败

---

## 2026-04-27（Phase 6 结果整理与论文材料化）

### 花费时间

约 1 次文档整理 + 报告材料同步

### 目标

- 不启动任何新实验
- 不启动 Phase 7
- 不启动 Bank Marketing 次验证
- 不重跑 Phase 4/5
- 把已完成的 Phase 6 Adult 主实验整理成可以写进报告的材料

### 实际完成内容

- 阅读并对齐：
  - `report/outline.md`
  - `report/outline_zh.md`
  - `docs/project_record.md`
  - `docs/experiment_log.md`
  - `docs/work_log.md`
  - `docs/session_handoff.md`
  - `notebooks/phase6_big_plus_adult.md`
- 新增英文 Phase 6 结果材料：
  - `report/phase6_big_plus_results.md`
- 新增中文 Phase 6 结果材料：
  - `report/phase6_big_plus_results_zh.md`
- 更新英文报告 outline：
  - 新增 `Big Plus Support-Set Selection Ablation`
  - 把 Big Plus 从未来 preview 改为已完成的 Adult ablation
  - 明确 BPR 是负结果，不是成功方法
- 更新中文报告 outline：
  - 新增 `Big Plus 支持集选择 Ablation`
  - 写入图表引用、实验设置、结果解释和限制
- 更新 `docs/project_record.md`：
  - Phase 6 状态改为 Adult 主实验已完成并已材料化
  - 下一步改为 Phase 6 论文整理，而不是启动 Phase 7
- 更新 `docs/experiment_log.md`：
  - 新增实验 013，记录 Phase 6 Adult 主实验、结果图表和结论
- 更新 `docs/session_handoff.md`：
  - 记录当前接手者应继续报告正文/caption/table，而不是启动 Phase 7

### 遇到的问题

- 多份文档仍停留在 “Phase 6 完整 Adult 主实验未运行 / 下一步启动长实验” 的旧口径。
- 报告 outline 中 Big Plus 仍是 future preview，需要改成已完成的 ablation。

### 解决方式

- 统一改成当前真实状态：
  - Adult 主实验已完成
  - 图表已生成
  - BPR 冻结版本未超过强随机 baseline
  - Phase 6 是有价值的负结果
- 保留方法冻结，不改算法、不改结果 CSV、不新增实验。

### 学到的东西

- 负结果也可以成为报告亮点，前提是对照组设计清楚。
- `Balanced Random Subset` 是强 baseline；后续任何检索式支持集选择都需要先超过它。
- 对项目交接最重要的是避免旧文档继续诱导下一步启动已完成的实验。

### 下一步

- 继续打磨 Phase 6 报告正文
- 为 5 张 Phase 6 图写正式 caption
- 准备可放进最终报告的英文结果段落和表格
- 暂不启动 Phase 7

---

## 记录模板

### 日期

YYYY-MM-DD

### 花费时间

X 小时

### 目标

- 

### 实际完成内容

- 

### 遇到的问题

- 

### 解决方式

- 

### 学到的东西

- 

### 下一步

- 
