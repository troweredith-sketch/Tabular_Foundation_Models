# 中小型表格分类任务上表格基础模型与 Boosted-Tree Baseline 的比较

> 学习用中文版本。本文保持英文报告的实验结论、数字、图表引用和方法口径不变，只把正文改写成便于理解的中文表述。正式提交仍建议以英文版为准。

## 摘要

本项目在两个 OpenML 表格分类数据集 Adult 和 Bank Marketing 上，比较了两个表格基础模型 TabPFN v2、TabICL，以及两个强 boosted-tree baseline：LightGBM 和 XGBoost。评估采用 repeated stratified splits，并报告 accuracy、balanced accuracy、macro-F1 和实际运行时间。主线结果显示，boosted-tree baseline 在 Adult 上仍然最强，而基础模型，尤其是 TabICL，在 Bank Marketing 上更有竞争力。运行时间结果显示出明显的实际成本差距：树模型快得多，TabICL 明显快于 TabPFN v2，并且基础模型的运行时间会随着训练集规模增大而上升。

作为 Big Plus 扩展，本项目还在 Adult 上研究了 TabICL 的支持集选择。实验把三个预算受限的支持集策略与 full-context 参考结果进行比较。冻结版本的 balanced prototype retrieval 策略没有超过 random subset 或 balanced random subset，但预算受限支持集显著降低了 TabICL fit+predict 的模型侧运行时间。因此，Big Plus 结果更适合被解释为一个有价值的负结果 ablation：支持集压缩在实践上有用，但当前基于类别中心的 prototype retrieval 规则不是一种能提升预测表现的方法。

## 引言

表格数据仍然是应用机器学习中的核心数据类型，常见于金融、营销、医疗和运营等场景。Boosted-tree 方法至今仍是表格预测任务中的强默认选择；与此同时，tabular foundation models 希望通过更广泛的复用能力和更少的任务特定建模工作，成为新的候选方案。本项目关注一个实际问题：在受控的本地实验中，表格基础模型什么时候看起来优于 boosted-tree baseline？这种优势又需要付出多少运行成本？

本项目主线范围是中小型表格数据集上的分类任务。回归和生存分析不在本项目范围内。主线比较包括四个模型：LightGBM、XGBoost、TabPFN v2 和 TabICL。主要数据集是 Adult 和 Bank Marketing。报告关注三个预测指标，也就是 accuracy、balanced accuracy 和 macro-F1，同时也关注 runtime。

项目还包含一个围绕 TabICL 的小型 Big Plus 扩展。因为 TabICL 会把支持样本作为上下文使用，所以支持集选择是一个相对独立、范围清楚的方法扩展方向，可以用来研究更好的上下文构造是否能改善指标和运行时间之间的 tradeoff。这个扩展与主线比较分开处理，这样即使 Big Plus 方法没有提升性能，主线报告仍然是有效的。

本项目的研究问题包括：

- 在 Adult 和 Bank Marketing 上，哪一类模型表现最好？
- 随着 train size 增大，accuracy、balanced accuracy 和 macro-F1 如何变化？
- 实际运行时间如何随 train size 扩展？
- TabICL 是否适合作为一个小型方法扩展的基础模型目标？
- TabICL 支持集选择能否改善指标和运行时间之间的 tradeoff？

## 相关工作与背景

Boosted-tree 模型广泛用于表格学习，因为它们能较好处理异构特征、训练速度快，并且通常在有限调参下也有很强表现。本项目中，LightGBM 和 XGBoost 被用作 fixed strong baselines，而不是经过大量调参的 state-of-the-art baselines。它们提供了实际比较基准，用来判断基础模型是否值得付出额外成本。

表格基础模型的目标是在不同表格预测任务之间复用学习到的结构。TabPFN v2 是一种面向表格预测的 prior-data-fitted model。TabICL 则以 in-context learning 的方式组织表格预测，因此支持样本的选择尤其重要。本项目把这些基础模型当作本地可用的实际工具来评估，而不是把它们当作外部 benchmark suite 上的冠军模型来讨论。

Accuracy 容易理解，但它可能掩盖少数类表现。这个问题在 Bank Marketing 上尤其重要，因为类别不平衡会让单看 accuracy 变得不充分。因此，报告加入 balanced accuracy 和 macro-F1 作为补充指标。Runtime 也是评估的一部分，因为一个模型即使准确，如果太慢，在实际中也可能很难使用。

本项目没有使用 TALENT、TabArena 或其他外部表格 benchmark suite。所有报告结果都来自所选 OpenML 数据集上的本地实验。

## 数据集

本项目使用两个 OpenML 分类数据集。

Adult 是一个二分类收入预测数据集，包含 48,842 个样本、14 个原始特征，其中 6 个是数值特征，8 个是类别特征。它混合了数值列和类别列，并包含缺失值。数据加载器会把 `?`、`NA`、`null` 等常见字符串缺失标记统一规范成 missing values，再进入各模型自己的预处理流程。在主线结果中，Adult 整体上更偏向 boosted-tree baselines，尽管 TabICL 接近最强树模型。

Bank Marketing 是一个类别不平衡更明显的二分类数据集。它可以检验 balanced accuracy 和 macro-F1 是否会给出不同于 accuracy 的结论。这个数据集中的 `unknown` 被保留为观察到的类别取值，而不是被自动当成缺失值。在主线结果中，foundation models 在这个数据集上更有竞争力，并且 TabICL 有最强的不平衡类别相关指标。

实验采用 repeated stratified splits。在每个 seed 内，所有模型共享同一个 train/test split。跨 seeds 时，测试集会变化；因此这些结果是 repeated splits，而不是所有 seeds 复用同一个固定测试集。主线实验使用 seeds 42、43、44、45 和 46。Phase 6 Big Plus Adult 实验使用 seeds 42、43 和 44。

## 方法与模型

LightGBM 被用作快速 boosted-tree baseline。它在 Adult 上表现强，并且在不同 train sizes 下都保持高效率。

XGBoost 被用作第二个 boosted-tree baseline。它同样快速且强，在主线结果中拥有 Adult control-10k 的最高 accuracy，不过并不是每个指标上都最高。

TabPFN v2 被用作 tabular foundation-model baseline。它在一些小训练集规模设置下有竞争力，但比树模型慢，也比 TabICL 慢。Full-train TabPFN v2 行应当被视为 constrained reference results，因为它们超过了主控比较中更干净的 10k support-range 口径。

TabICL 是第二个表格基础模型。它在 Adult 上接近树模型，在 Bank Marketing 的不平衡类别指标上最强。在本地设置中，它也明显快于 TabPFN v2，因此自然成为 Big Plus 支持集选择 ablation 的目标模型。

## 实验设置

主线比较在 Adult 和 Bank Marketing 上评估 LightGBM、XGBoost、TabPFN v2 和 TabICL。实验使用两个主要场景：

- `control_10k`：使用 10,000 个训练样本的受控比较。
- `full_train_reference`：使用完整可用训练 split 的工程参考结果。

Scalability analysis 评估 train sizes 512、2048、8192、10000 和 full。主线均值和标准差基于 seeds 42、43、44、45 和 46 计算。

评估指标包括：

- Accuracy。
- Balanced accuracy。
- Macro-F1。
- Fit seconds、predict seconds 和 total seconds。

Runtime 数值是实际 mixed-device timings。树模型在 CPU 上运行，而 foundation models 可能使用 CUDA。因此，runtime 应被解释为实际本地运行成本，而不是严格的同设备硬件 benchmark。

LightGBM 和 XGBoost 是 fixed strong baselines。它们不是调参后的 state-of-the-art baselines。这个选择使项目聚焦于一个受控课程项目比较，而不是超参数搜索。

作为补充鲁棒性检查，本项目还在 Adult 上做了一个小型 missingness stress test：训练规模固定为 2048，seed 固定为 42，对 feature cells 注入 0%、10% 和 30% 的确定性缺失值，target labels 不变，并且四个模型共享相同的 masked split。这个检查刻意保持轻量，不应被理解为完整的 missing-value 或 categorical-cardinality robustness benchmark。

## 主线结果

Table 1 总结主线模型比较结果。在 Adult 上，boosted-tree models 整体仍然最强。在 `control_10k` 场景中，XGBoost 的 accuracy mean 最高，为 0.8698；LightGBM 的 balanced accuracy 和 macro-F1 最强。TabICL 接近树模型 baseline，但没有明确超过它们。TabPFN v2 在主要指标上较低，并且比树模型和 TabICL 都慢。

在 Bank Marketing 上，foundation models 更有竞争力。在 `control_10k` 场景中，TabICL 和 TabPFN v2 的 accuracy mean 同为 0.9093，但 TabICL 在 balanced accuracy 和 macro-F1 上更强。在 `full_train_reference` 场景中，TabICL 拥有最好的 accuracy、balanced accuracy 和 macro-F1。树模型仍然快得多，但它们在这个数据集上的预测指标并不领先。

Table 1 中的 metric columns 是五次 repeated stratified splits 的均值，runtime column 是同一批 seeds 上 total runtime 的中位数。

**表 1. Adult 和 Bank Marketing 上的主线模型比较。**

| 数据集 | 场景 | 模型 | Accuracy | Balanced Accuracy | Macro-F1 | Median Total Seconds |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| Adult | control_10k | LightGBM | 0.8692 | 0.7934 | 0.8097 | 0.3147 |
| Adult | control_10k | TabICL | 0.8681 | 0.7909 | 0.8077 | 5.0990 |
| Adult | control_10k | TabPFN v2 | 0.8614 | 0.7789 | 0.7966 | 13.1286 |
| Adult | control_10k | XGBoost | 0.8698 | 0.7887 | 0.8082 | 0.4186 |
| Adult | full_train_reference | LightGBM | 0.8752 | 0.8013 | 0.8183 | 0.8489 |
| Adult | full_train_reference | TabICL | 0.8707 | 0.7991 | 0.8133 | 29.7518 |
| Adult | full_train_reference | TabPFN v2 | 0.8633 | 0.7778 | 0.7977 | 83.1503 |
| Adult | full_train_reference | XGBoost | 0.8743 | 0.7953 | 0.8150 | 1.2288 |
| Bank Marketing | control_10k | LightGBM | 0.9044 | 0.7092 | 0.7367 | 0.3133 |
| Bank Marketing | control_10k | TabICL | 0.9093 | 0.7397 | 0.7606 | 5.0556 |
| Bank Marketing | control_10k | TabPFN v2 | 0.9093 | 0.7215 | 0.7504 | 13.1897 |
| Bank Marketing | control_10k | XGBoost | 0.9040 | 0.7019 | 0.7315 | 0.3425 |
| Bank Marketing | full_train_reference | LightGBM | 0.9083 | 0.7273 | 0.7524 | 0.7239 |
| Bank Marketing | full_train_reference | TabICL | 0.9119 | 0.7599 | 0.7745 | 20.6253 |
| Bank Marketing | full_train_reference | TabPFN v2 | 0.9110 | 0.7209 | 0.7523 | 80.1081 |
| Bank Marketing | full_train_reference | XGBoost | 0.9083 | 0.7184 | 0.7472 | 0.8925 |

主要解释是 dataset-dependent。Adult 更偏向 boosted trees，而 Bank Marketing 给了 foundation models，尤其是 TabICL，在 imbalance-aware metrics 上更清楚的优势。Runtime column 也说明，foundation-model gains 即使出现，也要比 LightGBM 和 XGBoost 付出明显更高的实际成本。

## Scalability 分析

Scalability analysis 研究当训练集规模从 512 增加到 full training data 时，指标如何变化。Figures 1 到 3 展示了 train-size grid 上的三个预测指标。

![图 1. Train size 与 accuracy 的关系。](../results/figures/phase5_scalability_accuracy.png)

**图 1. Train size 与 accuracy 的关系。** 图中展示 Adult 和 Bank Marketing 上 seeds 42 到 46 的 mean accuracy。更大的训练集通常会提高 accuracy；Adult 上树模型仍然最强，而 Bank Marketing 上 TabICL 变得更有竞争力。图中未画 error bars；标准差可在 summary CSV 中查看。

![图 2. Train size 与 balanced accuracy 的关系。](../results/figures/phase5_scalability_balanced_accuracy.png)

**图 2. Train size 与 balanced accuracy 的关系。** 图中展示 seeds 42 到 46 的 mean balanced accuracy。这个指标突出少数类表现，尤其是在 Bank Marketing 上，TabICL 从更大的 train sizes 中获得的收益比单看 accuracy 更明显。图中未画 error bars；标准差可在 summary CSV 中查看。

![图 3. Train size 与 macro-F1 的关系。](../results/figures/phase5_scalability_macro_f1.png)

**图 3. Train size 与 macro-F1 的关系。** 图中展示 seeds 42 到 46 的 mean macro-F1。Macro-F1 进一步确认 dataset-dependent pattern：Adult 仍然更有利于 boosted trees，而 Bank Marketing 上 TabICL 拥有最强的 full-train imbalance-aware result。图中未画 error bars；标准差可在 summary CSV 中查看。

在 Adult 上，更大的 train size 通常会提升所有模型，但树模型收益更清楚。LightGBM 的 macro-F1 从 512 examples 下的 0.7513 上升到 full training size 下的 0.8183。TabICL 也有提升，并且仍然接近最强 baselines，但没有超过它们。TabPFN v2 在 Adult 上提升较小，并且仍然低于最强模型。

在 Bank Marketing 上，更大的 train size 会提升所有模型的 balanced accuracy 和 macro-F1。TabICL 达到最强 full-train macro-F1，数值为 0.7745。这个数据集最清楚地说明为什么只看 accuracy 不够：不同模型的 accuracy 可能接近，但 balanced accuracy 和 macro-F1 会有更明显差异。

Table 2 展示了选定的 scalability anchors。该表只保留 512 和 full 设置，使端点变化更容易阅读；Figures 1 到 3 展示完整 train-size curves。

**表 2. 选定 train-size scalability anchors。**

| 数据集 | Train Size | 模型 | Accuracy | Balanced Accuracy | Macro-F1 | Median Total Seconds |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| Adult | 512 | LightGBM | 0.8274 | 0.7403 | 0.7513 | 0.1629 |
| Adult | 512 | TabICL | 0.8426 | 0.7499 | 0.7671 | 3.2788 |
| Adult | 512 | TabPFN v2 | 0.8436 | 0.7468 | 0.7662 | 2.7220 |
| Adult | 512 | XGBoost | 0.8344 | 0.7485 | 0.7605 | 0.1297 |
| Adult | full | LightGBM | 0.8752 | 0.8013 | 0.8183 | 0.8572 |
| Adult | full | TabICL | 0.8707 | 0.7991 | 0.8133 | 22.3303 |
| Adult | full | TabPFN v2 | 0.8633 | 0.7778 | 0.7977 | 84.1770 |
| Adult | full | XGBoost | 0.8743 | 0.7953 | 0.8150 | 1.2079 |
| Bank Marketing | 512 | LightGBM | 0.8880 | 0.6336 | 0.6618 | 0.1872 |
| Bank Marketing | 512 | TabICL | 0.8983 | 0.6458 | 0.6815 | 3.6889 |
| Bank Marketing | 512 | TabPFN v2 | 0.8950 | 0.6246 | 0.6587 | 2.7932 |
| Bank Marketing | 512 | XGBoost | 0.8906 | 0.6405 | 0.6697 | 0.1399 |
| Bank Marketing | full | LightGBM | 0.9083 | 0.7273 | 0.7524 | 0.7195 |
| Bank Marketing | full | TabICL | 0.9119 | 0.7599 | 0.7745 | 20.1147 |
| Bank Marketing | full | TabPFN v2 | 0.9110 | 0.7209 | 0.7523 | 80.3920 |
| Bank Marketing | full | XGBoost | 0.9083 | 0.7184 | 0.7472 | 0.8875 |

端点视角支持两个结论。第一，更多训练数据通常会帮助预测指标。第二，runtime increase 具有明显的 model-dependent 特征：树模型仍然便宜，而 foundation models 会变得昂贵得多。

## Runtime 分析

Runtime 是本项目中非常重要的实际 tradeoff。Figure 4 总结了 train-size grid 上的 median total runtime。

Table 1 和 scalability analysis 来自不同实验输出文件。预测指标在共享 split protocol 下可以直接比较，但 runtime medians 应理解为本地实际计时，不同 rerun 之间可能波动，尤其是使用 GPU 的 foundation-model runs。

![图 4. Train size 与 median total runtime 的关系。](../results/figures/phase5_scalability_total_seconds_median.png)

**图 4. Train size 与 median total runtime 的关系。** 图中展示 seeds 42 到 46 的 median total runtime，并使用 log scale。树模型保持在亚秒到一秒左右的范围；TabICL 更慢，但仍然远快于 TabPFN v2；TabPFN v2 在较大 train sizes 下成为最昂贵的模型。

树模型始终很快。在主线 summary 中，即使使用 full training size，LightGBM 和 XGBoost 也大致保持在亚秒到约一秒的运行时间范围。这使它们成为非常强的 practical baselines。

TabPFN v2 慢得多。在 scalability results 中，full train size 下它在 Adult 上的 median total runtime 约为 84.1770 秒，在 Bank Marketing 上约为 80.3920 秒。这些行是有用的 engineering references，但应结合 support-range caveat 来解释。

TabICL 也比树模型慢，但比 TabPFN v2 快得多。在 scalability results 中，full train size 下 TabICL 在 Adult 上的 median total runtime 约为 22.3303 秒，在 Bank Marketing 上约为 20.1147 秒。这使 TabICL 成为 Big Plus 扩展更合适的目标：它的指标有竞争力，尤其是在 Bank Marketing 上，同时比 TabPFN v2 更实际。

因为这些 timings 是 practical mixed-device timings，所以不应把它们表述为严格的硬件归一化速度比较。它们仍然有助于回答一个课程项目问题：在这个本地设置中，每个模型的实际成本是多少？

## Big Plus：TabICL 支持集选择

Big Plus 扩展聚焦于 Adult 上的 TabICL 支持集选择。动机很直接：因为 TabICL 使用 support examples 作为上下文，所以选择更小或更有代表性的支持集，可能改善效率、性能，或二者兼顾。

Phase 6 实验只使用 Adult，并使用 seeds 42、43 和 44。它比较四种 support-set strategies：

- Full Context：使用完整的 seed-specific training split，作为不受预算限制的参考。
- Random Subset：从训练 split 中无放回均匀抽样指定 budget。
- Balanced Random Subset：先按类别配额分配 support budget，然后在每个类内随机抽样。
- Balanced Prototype Retrieval：使用与 balanced random 相同的类别配额，但在 train-only retrieval space 中选择最接近类别中心的样本。

预算受限支持集大小为 512、2048 和 8192。Full Context 使用 39,073 个 support examples。Balanced Prototype Retrieval 的 retrieval space 只由训练 split 构建。它使用 train-split numeric imputation and scaling、train-split categorical imputation and one-hot encoding，并用到类别中心的 Euclidean distance。方法定义在主要 Adult 实验之前已经冻结，因此结果应被当作 ablation 来评估，而不是被当作 tuned method search。

Figure 5 直接比较 BPR 与两个 budget-fair random baselines。负柱表示 BPR 比对应 comparator 更差。

![图 5. Balanced Prototype Retrieval 相对随机 baseline 的 delta。](../results/figures/phase6_big_plus_adult_bpr_delta.png)

**图 5. Balanced Prototype Retrieval 相对随机 baseline 的 delta。** 图中展示 seeds 42、43 和 44 上的 mean metric deltas。冻结版 BPR 策略相对 Random Subset 和 Balanced Random Subset 大多为负。唯一的正值是在 budget 2048 下，相对 Random Subset 的 balanced-accuracy delta 极小为正。

支持性的 Phase 6 图也可用于查看 metric-by-budget 和 runtime：

- `results/figures/phase6_big_plus_adult_accuracy.png`
- `results/figures/phase6_big_plus_adult_balanced_accuracy.png`
- `results/figures/phase6_big_plus_adult_macro_f1.png`
- `results/figures/phase6_big_plus_adult_total_seconds_median.png`

Table 3 给出对应的 Phase 6 summary values。Metrics 是三个 seeds 的均值，runtime 是支持集已经构造完成之后的 TabICL fit+predict 时间中位数。

**表 3. Phase 6 Adult 支持集选择结果。**

| 策略 | Budget | Accuracy | Balanced Accuracy | Macro-F1 | Median TabICL Fit+Predict Seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| Full Context | full | 0.8722 | 0.7919 | 0.8117 | 45.8005 |
| Random Subset | 512 | 0.8438 | 0.7358 | 0.7592 | 3.4771 |
| Random Subset | 2048 | 0.8573 | 0.7668 | 0.7873 | 2.5291 |
| Random Subset | 8192 | 0.8654 | 0.7874 | 0.8038 | 4.6601 |
| Balanced Random Subset | 512 | 0.7964 | 0.8180 | 0.7610 | 3.4701 |
| Balanced Random Subset | 2048 | 0.8155 | 0.8295 | 0.7792 | 2.5361 |
| Balanced Random Subset | 8192 | 0.8344 | 0.8293 | 0.7941 | 4.6720 |
| Balanced Prototype Retrieval | 512 | 0.7020 | 0.7093 | 0.6588 | 3.2666 |
| Balanced Prototype Retrieval | 2048 | 0.7336 | 0.7684 | 0.7002 | 2.4829 |
| Balanced Prototype Retrieval | 8192 | 0.6437 | 0.7256 | 0.6253 | 4.7904 |

对于冻结的 Balanced Prototype Retrieval 方法来说，这个结果是一个 negative ablation。它没有超过 Random Subset 或 Balanced Random Subset。Balanced Random Subset 在每个 metric 和每个 budget 上都优于 BPR。相对 Random Subset，BPR 只有在 budget 2048 下有一个非常小的 positive balanced-accuracy delta，但 accuracy 和 macro-F1 仍然明显更低。

Runtime 结果仍然有价值，但必须明确它的定义。Phase 6 runtime column 记录的是支持集构造完成之后的 TabICL fit+predict 时间，不包含 BPR 的 preprocessing、class-center 计算和 distance ranking 等 support-set selection overhead。在这个模型侧计时定义下，Full Context 的 median 为 45.8005 秒，而预算受限策略大约在 2.5 到 4.8 秒范围内。因此，support-set compression 可以让 TabICL 模型执行快得多；但如果要声称完整 retrieval system 运行时间收益，还需要把支持集选择开销也计入。

正确结论不是 Big Plus “成功了”。更谨慎的结论是：support-set compression 具有实际价值，而 Balanced Random Subset 是一个很强的 baseline，未来任何 retrieval method 都必须先超过它。

## 补充 Missingness 鲁棒性检查

为了更直接回应 missing-value robustness，本项目增加了一个 Adult-only 小型 stress test。实验使用 train size 2048 和 seed 42，对 train/test 的 feature cells 注入确定性缺失 mask，四个模型使用同一 masked split。Table 4 报告各模型指标，以及相对 0% 注入缺失 baseline 的下降幅度。

**表 4. Adult missingness robustness check，train size 2048，seed 42。**

| Missing Rate | Model | Accuracy | Accuracy Drop | Balanced Accuracy | Balanced Accuracy Drop | Macro-F1 | Macro-F1 Drop |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.0 | LightGBM | 0.8508 | 0.0000 | 0.7692 | 0.0000 | 0.7835 | 0.0000 |
| 0.0 | XGBoost | 0.8603 | 0.0000 | 0.7793 | 0.0000 | 0.7959 | 0.0000 |
| 0.0 | TabPFN v2 | 0.8552 | 0.0000 | 0.7707 | 0.0000 | 0.7876 | 0.0000 |
| 0.0 | TabICL | 0.8556 | 0.0000 | 0.7673 | 0.0000 | 0.7863 | 0.0000 |
| 0.1 | LightGBM | 0.8418 | 0.0089 | 0.7549 | 0.0144 | 0.7695 | 0.0140 |
| 0.1 | XGBoost | 0.8525 | 0.0078 | 0.7663 | 0.0130 | 0.7834 | 0.0125 |
| 0.1 | TabPFN v2 | 0.8525 | 0.0027 | 0.7628 | 0.0079 | 0.7816 | 0.0061 |
| 0.1 | TabICL | 0.8542 | 0.0013 | 0.7616 | 0.0057 | 0.7823 | 0.0040 |
| 0.3 | LightGBM | 0.8255 | 0.0253 | 0.7213 | 0.0480 | 0.7389 | 0.0446 |
| 0.3 | XGBoost | 0.8316 | 0.0287 | 0.7243 | 0.0550 | 0.7447 | 0.0512 |
| 0.3 | TabPFN v2 | 0.8337 | 0.0215 | 0.7227 | 0.0480 | 0.7450 | 0.0426 |
| 0.3 | TabICL | 0.8393 | 0.0163 | 0.7378 | 0.0295 | 0.7581 | 0.0282 |

所有模型都会随着注入缺失率升高而下降。在这个单 seed、2048 train-size 设置中，TabICL 在 30% 注入缺失下三个指标的下降幅度最小。但这只是补充 sanity check，不能扩展成系统鲁棒性结论；更完整的 missingness mechanism、categorical-cardinality shift 和更多 benchmark 数据集仍属于未来工作。

## 讨论

结果显示，表格模型表现具有明显 dataset-dependent 特征。Adult 更偏向 boosted-tree baselines，而 Bank Marketing 给 foundation models 更清楚的优势，尤其是在 balanced accuracy 和 macro-F1 被纳入考虑时。

结果也说明为什么 accuracy alone 不够。在 Bank Marketing control-10k 中，TabICL 和 TabPFN v2 的 accuracy 持平，但 TabICL 在 balanced accuracy 和 macro-F1 上更强。这一点很重要，因为 Bank Marketing 比 Adult 更不平衡。

Runtime 会改变实际解释。树模型既强又快。TabPFN v2 在一些设置中有竞争力，但 runtime 高得多。TabICL 提供了更好的 foundation-model tradeoff：它比树模型慢，但远快于 TabPFN v2，并且在 Bank Marketing 的 imbalance-aware metrics 上最强。

Big Plus 结果虽然是负结果，但仍然有用。它说明一个看起来合理的支持集选择规则，也就是 class-center prototype selection，并不会自动优于 random context construction。它也说明 Balanced Random Subset 是一个认真且强的 baseline。未来的 retrieval method 不只需要超过 naive random subset，还需要在相同 budgets 和 splits 下超过 balanced random sampling。

## 局限性

本项目只使用两个主线数据集 Adult 和 Bank Marketing，因此结果不能泛化到所有表格分类任务。

Missingness 鲁棒性检查也刻意保持较小规模：只覆盖 Adult、一个 train size 和一个 seed。它可以作为 injected feature missingness 下的 sanity check，但不是跨 missingness mechanisms、categorical-cardinality shifts 或更多 benchmark suites 的系统研究。

项目只覆盖分类任务。回归和生存分析不在范围内。

LightGBM 和 XGBoost 是 fixed strong baselines，而不是 tuned state-of-the-art baselines。更充分的超参数调优可能改变部分差距。

Runtime 是 practical mixed-device timing。树模型在 CPU 上运行，而 foundation models 可能使用 CUDA。因此，runtime 不应被解释为严格同设备 benchmark。

Repeated stratified split protocol 意味着每个 seed 有不同的测试集。在一个 seed 内，模型共享 split；但跨 seeds 时，评估是 repeated-split evaluation，而不是一个固定 held-out test set。

Full-train TabPFN v2 results 超过了更干净的 10k support-range 设置，应被当作 constrained reference results。

Phase 6 Big Plus ablation 只在 Adult 上进行，并且使用三个 seeds。它不应被解释为所有 retrieval-based support-set selection 都无效。它只说明，在当前设置中，冻结版 balanced prototype retrieval rule 没有超过强随机 baselines。

## 结论

本项目在 Adult 和 Bank Marketing 上比较了 tabular foundation models 和 boosted-tree baselines。主线结果显示，boosted trees 仍然非常强，尤其是在 Adult 和 runtime 上。Foundation models 在 Bank Marketing 上更有竞争力，其中 TabICL 拥有最强的 imbalance-aware metrics。

Train-size scalability 显示，更大的训练集通常会改善指标，但也会增加 runtime，尤其是对 foundation models 而言。Runtime analysis 显示出实际差距：树模型最快，TabICL 远快于 TabPFN v2，而 TabPFN v2 在较大 train sizes 下变得昂贵。

Big Plus 支持集选择实验给出了一个有价值的负结果。预算受限支持集显著降低了 TabICL fit+predict 的模型侧 runtime，但冻结版 balanced prototype retrieval strategy 没有在预测表现上超过 random subset 或 balanced random subset。补充 missingness check 显示四个模型在注入缺失下都会退化，但这个结果仍只是小规模 sanity check。最后的经验是保守的：TabICL 是 Bank Marketing 和实际扩展工作的一个有希望的 foundation-model baseline，但支持集检索方法必须先超过强 random 和 balanced random baselines，才能被称为真正的改进。
