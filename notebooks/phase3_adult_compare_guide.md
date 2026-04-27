> Final source of truth: use report/report_draft.md, results/*.csv, and report/submission_manifest.md for the submitted results. This file may include historical planning or work-log context.

# 第三阶段操作指南

这份文档是给你在 Phase 3 里快速上手脚本和结果文件用的。

说明：

- 这是一份 Phase 3 的过程性操作指南
- 最终阶段结论以 `notebooks/phase3_fairness_reset.md` 和 `docs/experiment_log.md` 为准
- 现在脚本默认已经会同时跑 `full Adult` 和 `10k control`
- 如果你只想跑某一个场景，可以用 `--scenario`

它回答 4 个问题：

1. 现在第三阶段脚本到底会做什么
2. 为什么你之前直接运行时只看到了 full Adult
3. 现在应该怎样运行脚本
4. 跑完后应该看哪些结果文件

---

## 1. 现在第三阶段脚本会做什么

当前脚本是：

- `src/phase3_adult_compare.py`

它现在支持三种入口：

- `--scenario all`
- `--scenario full_adult_limit_override`
- `--scenario adult_control_10k`

默认行为是：

```bash
source .venv/bin/activate
python3 src/phase3_adult_compare.py
```

这条命令会自动执行：

- `full_adult_limit_override`
- `adult_control_10k`

并默认使用：

- `seeds = 42 43 44 45 46`

也就是说，现在直接运行脚本，不再只是跑一组结果，而是会做：

- `5 seeds × 2 scenarios × 2 models`

---

## 2. 为什么你之前直接运行时只看到了 full Adult

因为旧版脚本里：

- `--scenario` 的默认值是 `full_adult_limit_override`

所以你不带参数执行时，脚本只会跑：

- full Adult

而不会自动跑：

- `adult_control_10k`

这不是你操作错了，而是脚本默认值当时就是这样设置的。

现在这个问题已经修好：

- 默认值改成了 `all`

所以直接运行就会同时看到两个场景。

---

## 3. 现在应该怎样运行脚本

### 方式 1：跑完整 Phase 3

这是最推荐的方式：

```bash
source .venv/bin/activate
python3 src/phase3_adult_compare.py
```

适合场景：

- 你想直接复现当前 Phase 3 的完整最终结果
- 你想同时拿到明细表和 summary

### 方式 2：只跑 `10k control`

```bash
source .venv/bin/activate
python3 src/phase3_adult_compare.py --scenario adult_control_10k
```

适合场景：

- 你只想复查主证据
- 你不想再等 full Adult 的长时间推理

### 方式 3：只跑 full Adult

```bash
source .venv/bin/activate
python3 src/phase3_adult_compare.py --scenario full_adult_limit_override
```

适合场景：

- 你只想查看受限条件结果
- 你想确认 `ignore_pretraining_limits=True` 这条路径是否还能正常工作

### 方式 4：只跑一个或几个 seeds

如果你只想快速 smoke test，可以这样：

```bash
source .venv/bin/activate
python3 src/phase3_adult_compare.py --scenario adult_control_10k --seeds 42
```

适合场景：

- 快速验证环境
- 快速复查 `seed=42` 锚点结果

---

## 4. 跑完后应该看哪些结果文件

### 1. `results/phase3_adult_compare.csv`

这是：

- `full_adult_limit_override`
- 多 seed 行级明细表

你可以在里面看到：

- 每个 seed
- 每个模型
- `accuracy`
- `fit_seconds`
- `predict_seconds`
- `train_size`
- `notes`

### 2. `results/phase3_adult_compare_10k.csv`

这是：

- `adult_control_10k`
- 多 seed 行级明细表

这是 Phase 3 更重要的主结果文件，因为它对应更公平的比较场景。

### 3. `results/phase3_adult_compare_summary.csv`

这是当前 Phase 3 最值得优先看的文件。

它会把前两个明细表按：

- `scenario`
- `model`

做汇总，并输出：

- `n_runs`
- `accuracy_mean`
- `accuracy_std`
- `accuracy_min`
- `accuracy_max`
- `fit_seconds_median`
- `predict_seconds_median`

如果你要写报告或做答辩，Phase 3 最终应优先引用这个 summary，而不是只引用某一次 run。

---

## 5. 现在第三阶段最重要的理解

如果你只记一件事，请记这句：

> 第三阶段不是“让 TabPFN 跑起来”就结束了，而是要把 single run 升级成有控制实验、还有多 seed 汇总的更稳结论。

所以当前 Phase 3 的证据结构是：

1. `seed=42` 锚点结果  
   作用：快速复现、快速检查脚本
2. `10k control`  
   作用：更公平的主证据
3. 多 seed summary  
   作用：最终阶段结论

---

## 6. 如果你现在只想快速确认仓库状态

推荐直接按这个顺序读：

1. `results/phase3_adult_compare_summary.csv`
2. `docs/experiment_log.md` 的实验 005
3. `notebooks/phase3_fairness_reset.md`

这样你会最快知道：

- 哪个模型现在更稳
- Phase 3 为什么算真的完成
- 这一步给 Phase 4 铺了什么路
