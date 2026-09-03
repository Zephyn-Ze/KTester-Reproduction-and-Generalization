# KTester Run3 与论文 Table 2 差异根因审计

原始审计日期：2026-08-22

公开长版整理日期：2026-09-03

审计方式：只读检查现有源码、配置、日志、生成测试、修复记录、JaCoCo 报告、论文 PDF 与作者发布的五轮 RQ1 产物。未修改 KTester 源码，未重跑生成/覆盖率，未覆盖任何评价产物。

本文件是逐证据长版分析。它保留完整的指标口径、项目与案例贡献、失败分类、配置审计、证据强度和后续实验结果；本机绝对路径已删除。没有进入 GitHub 的底层日志或官方压缩包被明确标为 `local-only evidence`，避免把“报告中引用过”误写成“仓库中可以直接下载”。

## 1. 结论摘要

Run3 的六个暂定汇总值已由源摘要确认：CPR 90.09%、EPR 53.74%、Instruction Coverage 49.90%、Branch Coverage 44.85%、Correct Instruction Coverage 40.79%、Correct Branch Coverage 36.09%。源文件是 [`../results/run3_111_focal_methods.json`](../results/run3_111_focal_methods.json)，汇总字段位于 1073–1078 行。

最重要的发现有四个：

1. 作者发布的五轮 KTester-gpt4o 摘要按顶层六个字段求平均，**恰好**得到 Table 2 的 100 / 76.41 / 63.94 / 55.46 / 55.52 / 47.21。这说明 Run3 的六个数与 Table 2 在“实际运算口径”上基本可直接比较；差距不是因为拿错了基线表。
2. 论文名称与实际运算不一致：Table 2 的 LC/LCP 实际是 JaCoCo **instruction** coverage，不是 line coverage；EPR 实际是测试方法级通过率，不是论文文字容易让人理解的测试类级通过率。Run3 的真实“整类全部通过”只有 9/111 = 8.11%，不是 53.74%。
3. 覆盖率差距的直接原因是 Run3 生成/修复后的测试质量明显较差。官方第 1 轮初始编译错误为 35/111，Run3 为 73/111；官方五轮最终均为 111/111 编译，Run3 最终仍有 11 个编译失败。Run3 在所有六项非平凡指标上都低于官方五轮的最低值，不属于官方五轮内的普通波动。
4. 不能把差距唯一归因于某一个外部因素。Run3 明确通过 OpenRouter 调用 `openai/gpt-4o-mini-2024-07-18`；论文和仓库模板指向 `gpt-4o-mini`/OpenAI 默认端点，但作者产物没有保存可核验的请求清单、解析后的服务商、模型响应元数据或精确运行 commit。最稳妥的结论是：**近因已证实为生成与修复结果退化；“OpenRouter/模型服务漂移、随机性、代码版本组合”是高可信候选解释，但尚不能单独定责。**

## 2. 证据清单与产物边界

### 2.1 论文与官方发布证据

- 论文 PDF：[KTester preprint](https://arxiv.org/pdf/2511.14224)。PDF 第 8 页给出 110 个任务、Event-ruler 15 个 MUT、5 次重复、温度 0.5、最多 5 次修复和指标文字定义；第 9 页 Table 2 给出六项结果。
- 官方仓库当前 checkout：[official KTester repository](https://github.com/SYSUSELab/KTester)，HEAD `fce83f1a4b9aa3f1d54598b62027bc17bb585383`。
- 作者发布的五轮 RQ1 结果：
  - `official_evaluation_results/rep_1/summary.json` (local-only evidence)
  - `official_evaluation_results/rep_2/summary-gpt-4o-mini.json` (local-only evidence)
  - `official_evaluation_results/rep_3/summary-gpt-4o-mini.json` (local-only evidence)
  - `official_evaluation_results/rep_4/summary-gpt4o-mini.json` (local-only evidence)
  - `official_evaluation_results/rep_5/summary-gpt-4o-mini.json` (local-only evidence)

这五个摘要都包含 111 个完全相同的任务键，且与 Run3 的 111 个任务键完全一致。因此，论文文字的 110 个任务/15 个 ruler MUT 与官方发布产物本身也不一致；Run3 并不是唯一多跑了一个案例。

### 2.2 Run3 证据

- 源汇总：[`../results/run3_111_focal_methods.json`](../results/run3_111_focal_methods.json)
- 配置：`local_ktester/code/settings.py` (local-only evidence)
- 生成日志：`local_ktester/evaluation/full_run_generation.log` (local-only evidence)
- 覆盖率日志：`local_ktester/evaluation/full_run_coverage2.log` (local-only evidence)
- 每项目最终测试、响应、提示、修复与报告：`local_ktester/evaluation/<project>/...` (local-only evidence)
- 评价实现：`local_ktester/code/evaluations/coverage_test.py` (local-only evidence)、`local_ktester/code/tools/execute_test.py` (local-only evidence)

当前 checkout 不是干净工作树。与 Run3 直接相关的本地修改包括：`coverage_test.py` 的类级 CPR/显式 `execution_passed` 与案例筛选、`execute_test.py` 的 macOS classpath/直接 `cwd` 执行和 JaCoCo HTML parser、`post_process.py` 的 Windows/Unix 路径归一化，以及 JVM classpath 兼容修改。报告比较的是 **Run3 实际使用的工作树**，不是把 HEAD 当作本轮完整代码快照；这些现有修改均未被本次审计改动。

Run3 的当前 `evaluation/` 目录内，提示、响应、修复、最终测试类和 JaCoCo 报告的时间均落在本轮生成/覆盖率窗口内；没有发现旧文件被本轮摘要直接混入。`evaluation_before_full_run/`、`evaluation_mixed_before_full_run/` 和 `experiments/` 是分离目录，未被本轮汇总路径读取。

因此应将本轮称为“使用官方工作流的新实验性 Run3”，而不是作者发布的官方五轮之一。Run3 的 LLM 修复属于官方工作流的一部分，不应与人工修复/A-B 实验混为一谈；但它也不能被标记为历史官方结果。

## 3. Table 2 的实际计算口径

### 3.1 五轮官方摘要精确重现 Table 2

| 指标 | 官方五轮范围 | 五轮顶层字段平均 | Table 2 | Run3 | Run3 相对差距 |
|---|---:|---:|---:|---:|---:|
| CPR | 100.00–100.00 | 100.00 | 100.00 | 90.09 | -9.91 pp |
| EPR | 73.44–79.17 | 76.41 | 76.41 | 53.74 | -22.68 pp |
| Instruction/“LC” | 59.00–70.14 | 63.94 | 63.94 | 49.90 | -14.04 pp |
| BC | 50.45–61.48 | 55.46 | 55.46 | 44.85 | -10.62 pp |
| Correct Instruction/“LCP” | 53.03–59.19 | 55.52 | 55.52 | 40.79 | -14.72 pp |
| BCP | 44.50–50.40 | 47.21 | 47.21 | 36.09 | -11.12 pp |

Run3 除 CPR 外的五项都低于官方五轮最小值；CPR 的官方五轮均为 100%。因此差距不能用“五次随机重复的正常区间”解释。

### 3.2 论文定义、当前实现与官方实际值的差异

| 指标 | 论文第 8 页文字 | 当前 Run3 evaluator | Table 2 的可观察实际口径 | 影响 |
|---|---|---|---|---|
| CPR | 编译成功的测试类百分比 | `compile_num / test_class_num`，见 `coverage_test.py:187–217` | 官方历史 evaluator 曾按测试方法数加权，但五轮均全部编译，因此两者都为 100 | Run3 当前 100/111=90.09%；若用官方历史代码的测试方法分母，则为 964/1111=86.77%，相差 3.32 pp |
| EPR | “无运行错误或断言失败”的百分比，语境指向测试类 | `passed_case_num / test_case_num`，见 `coverage_test.py:198–216` | 官方 Table 2 顶层值也是测试方法级字段 | Run3 的 53.74% 不是整类通过率；原始整类全通过仅 9/111=8.11% |
| LC | focal method 可执行行覆盖率 | `execute_test.py:203–227` 读取 JaCoCo 方法表第 2 列，即 instruction coverage | 官方摘要字段名是 `inst_cov`，五轮平均 63.94 | Table 2 的“LC”实际是 instruction coverage |
| BC | 条件分支覆盖率 | 读取 JaCoCo 第 4 列 branch coverage | 与官方字段一致 | 口径一致 |
| LCP/BCP | 编译且执行成功的测试产生的覆盖率 | 重新只运行被正则识别为通过的方法，生成 `_correct` 报告 | 与官方产物结构一致 | 覆盖率本身可比，但 EPR 还有额外过滤启发式 |
| 聚合 | 论文未明确 micro/macro | 每个任务覆盖率等权平均，缺失/失败任务贡献 0 | 官方摘要也是 111 个任务宏平均 | 项目任务数越多，对总差距贡献越大 |

Run3 JaCoCo HTML 重新按真实 line 列提取后，全测试 line coverage 为 50.92%，passing-test line coverage 为 42.14%；对应 evaluator 报出的 instruction coverage 是 49.90% 和 40.79%。因此 instruction/line 命名错误在 Run3 上约造成 +1.02 pp 和 +1.35 pp 的口径差，**不足以解释 14 pp 左右的主体差距**。

### 3.3 EPR 还有两层数据一致性问题

Run3 覆盖率日志中实际启动 964 个测试方法，原始成功 484 个。11 个无法编译的类内还有 147 个源代码级 `@Test`，随后被 AST 计入分母，使最终分母为 1111。`coverage_test.py:177–181` 还有一个过滤启发式：若全测试覆盖率与仅通过测试覆盖率相同，就把该类的 `passed_cases` 改成 `test_cases`。这使 Run3 的通过数从 484 增至 597，最终得到 597/1111=53.74%。因此 53.74% 是“失败类补零 + 覆盖率相等启发式调整”后的测试方法比率，不是未经处理的 JUnit 比率。

官方发布摘要自身也有顶层/逐项不一致：

- rep_1：632/841 = 75.1486%，与顶层一致。
- rep_2：逐项合计 791/814 = 97.1744%，但顶层写 79.1744%。
- rep_3：576/749 = 76.9025%，与顶层一致。
- rep_4：661/900 = 73.4444%，与顶层一致。
- rep_5：逐项合计 836/1171 = 71.3920%，但顶层写 77.3920%。

五轮逐项比率平均为 78.8124%，顶层字段平均为 76.4124%；Table 2 使用后者。论文第 8 页正文又写 KTester EPR 77.07%，与第 9 页 Table 2 的 76.41% 不一致。不能据此推断人为修改，只能确认：**EPR 的发布数据存在来源不明的顶层字段不一致，精确逐案例归因无法与 22.68 pp 的表格差距完全闭合。**

## 4. 哪些项目驱动覆盖率差距

下表的“贡献”是 `(官方五轮项目均值 - Run3 项目值) × 项目任务数 / 111`，因此各项目贡献之和精确等于四项全局覆盖率差距。

| 项目 | 任务 | Run3 编译 | IC 差距贡献 | BC 差距贡献 | Correct IC 差距贡献 | Correct BC 差距贡献 |
|---|---:|---:|---:|---:|---:|---:|
| jdom2 | 21 | 18/21 | 4.670 pp | 3.908 pp | 4.377 pp | 3.838 pp |
| commons-codec | 18 | 18/18 | 2.504 pp | 1.523 pp | 2.250 pp | 1.550 pp |
| ruler | 16 | 12/16 | 2.283 pp | 1.993 pp | 1.966 pp | 1.499 pp |
| gson | 20 | 18/20 | 1.180 pp | 0.614 pp | 0.641 pp | 0.027 pp |
| batch-processing-gateway | 6 | 6/6 | 0.874 pp | 0.434 pp | 1.667 pp | 1.101 pp |
| commons-cli | 2 | 2/2 | 0.814 pp | 0.668 pp | 0.447 pp | 0.295 pp |
| commons-csv | 6 | 6/6 | 0.607 pp | 0.618 pp | 2.196 pp | 1.894 pp |
| commons-collections | 14 | 13/14 | 0.499 pp | 0.355 pp | 1.009 pp | 0.791 pp |
| windward | 2 | 2/2 | 0.312 pp | 0.276 pp | 0.400 pp | 0.342 pp |
| datafaker | 6 | 5/6 | 0.299 pp | 0.229 pp | -0.231 pp | -0.220 pp |
| **合计** | **111** | **100/111** | **14.043 pp** | **10.618 pp** | **14.723 pp** | **11.117 pp** |

最主要的结构性驱动是：

- jdom2 单独解释约三分之一的四项覆盖率差距，并有 3 个最终编译失败。
- ruler 有 4 个最终编译失败，覆盖率最低；它解释约 1.5–2.3 pp 的各项总差距。
- commons-codec 虽最终全部编译，但多个类执行超时或没有触达 focal method，仍解释 1.5–2.5 pp。
- commons-csv 的全测试覆盖率差距中等，但 passing-test coverage 差距极大，说明主要问题是断言/运行正确性而非路径探索数量。
- datafaker 的正确覆盖率反而略高于官方五轮均值，说明不是所有项目都统一退化。

EPR 的逐项目方向也一致：Run3 相比官方五轮逐项比率均值，commons-cli 16.67% vs 79.04%、commons-csv 23.64% vs 62.13%、jdom2 38.01% vs 73.94%、ruler 42.11% vs 70.76%。但由于 rep_2/rep_5 的顶层 EPR 与逐项合计不一致，这些项目值只能作为定位线索，不能声称与 Table 2 的 22.68 pp 精确加和。

## 5. 哪些案例驱动覆盖率差距

以下是每项全局差距贡献最大的案例。括号内为“Run3 → 官方五轮案例均值；对 111 任务宏平均的贡献”。

### Instruction coverage

1. `Rule_pattern`，commons-codec：0% → 100%（0.901 pp）
2. `Verifier_isXMLPublicIDCharacter`，jdom2：0% → 98.2%（0.885 pp）
3. `Sha2Crypt_sha2Crypt`，commons-codec：0% → 94.6%（0.852 pp）
4. `HelpFormatter_renderOptions`，commons-cli：0% → 90.4%（0.814 pp）
5. `SqlTransformer_handlePrimitivesInArray`，datafaker：0% → 80.0%（0.721 pp）
6. `SubmissionSummary_copyFrom`，batch-processing-gateway：0% → 79.4%（0.715 pp）
7. `CSVParser_createHeaders`，commons-csv：0% → 78.6%（0.708 pp）
8. `DaitchMokotoffSoundex_soundex`，commons-codec：0% → 77.6%（0.699 pp）
9. `MurmurHash3_hash128x64Internal`，commons-codec：0% → 76.0%（0.685 pp）
10. `IteratorUtils_getIterator`，commons-collections：0% → 72.4%（0.652 pp）

### Branch coverage

1. `Verifier_isXMLPublicIDCharacter`：0% → 96.4%（0.868 pp）
2. `Rule_pattern`：0% → 96.2%（0.867 pp）
3. `Sha2Crypt_sha2Crypt`：0% → 87.4%（0.787 pp）
4. `SqlTransformer_handlePrimitivesInArray`：0% → 80.0%（0.721 pp）
5. `IteratorUtils_getIterator`：0% → 76.4%（0.688 pp）
6. `HelpFormatter_renderOptions`：0% → 74.2%（0.668 pp）
7. `AbstractStAXStreamProcessor_printContent`：0% → 68.0%（0.613 pp）
8. `DaitchMokotoffSoundex_soundex`：0% → 64.8%（0.584 pp）

### Correct instruction/branch coverage

- Correct IC 最大贡献：`Verifier_isXMLPublicIDCharacter` 0.861 pp、`Sha2Crypt_sha2Crypt` 0.847 pp、`DaitchMokotoffSoundex_soundex` 0.677 pp、`SubmissionSummary_copyFrom` 0.641 pp、`CSVParser_createHeaders` 0.614 pp。
- Correct BC 最大贡献：`Verifier_isXMLPublicIDCharacter` 0.840 pp、`Sha2Crypt_sha2Crypt` 0.777 pp、`AbstractStAXStreamProcessor_printContent` 0.600 pp、`IteratorUtils_getIterator` 0.598 pp、`SqlTransformer_handlePrimitivesInArray` 0.541 pp、`CSVFormat_toString` 0.514 pp。

这些案例不是统一的“编译失败”模式。部分最终无法编译；部分可编译但超时；部分运行却完全没有触达 focal method；部分全测试覆盖不低但通过测试覆盖接近 0。它们共同说明主体差距来自生成测试的 API 使用、输入选择、断言和修复质量。

## 6. 11 个最终编译失败案例

| 项目/案例 | 最终诊断摘要 | 证据路径 |
|---|---|---|
| commons-collections / `AbstractPatriciaTrie_put` | 泛型擦除造成 name clash，错误 `@Override` | `local_ktester/evaluation/commons-collections/fix/AbstractPatriciaTrie_put/repair_prompt_4.md` (local-only evidence) |
| datafaker / `SqlTransformer_handlePrimitivesInArray` | 调用 private constructor | `local_ktester/evaluation/datafaker/fix/SqlTransformer_handlePrimitivesInArray/repair_prompt_4.md` (local-only evidence) |
| gson / `JsonReader_skipValue` | 未定义变量 `index` | `local_ktester/evaluation/gson/fix/JsonReader_skipValue/repair_prompt_4.md` (local-only evidence) |
| gson / `ReflectiveTypeAdapterFactory_getBoundFields` | 包外访问 package-private `BoundField` | `local_ktester/evaluation/gson/fix/ReflectiveTypeAdapterFactory_getBoundFields/repair_prompt_4.md` (local-only evidence) |
| jdom2 / `WalkerNORMALIZE_analyzeMultiText` | 引用不存在/不可访问的 `MultiText` | `local_ktester/evaluation/jdom2/fix/WalkerNORMALIZE_analyzeMultiText/repair_prompt_4.md` (local-only evidence) |
| jdom2 / `XPathHelper_getSingleStep` | 使用不存在的 API（如 `Filters.processingInstruction`、`Parent.getChildren`） | `local_ktester/evaluation/jdom2/fix/XPathHelper_getSingleStep/repair_prompt_4.md` (local-only evidence) |
| jdom2 / `WalkerTRIM_analyzeMultiText` | 引用不存在/不可访问的 `MultiText` | `local_ktester/evaluation/jdom2/fix/WalkerTRIM_analyzeMultiText/repair_prompt_4.md` (local-only evidence) |
| ruler / `ByteMachine_addEndOfMatch` | 幻觉枚举值 `InputCharacterType.DEFAULT` | `local_ktester/evaluation/ruler/fix/ByteMachine_addEndOfMatch/repair_prompt_4.md` (local-only evidence) |
| ruler / `JsonRuleCompiler_processMatchExpression` | 幻觉 `Patterns` getter | `local_ktester/evaluation/ruler/fix/JsonRuleCompiler_processMatchExpression/repair_prompt_4.md` (local-only evidence) |
| ruler / `Ruler_matches` | `ValuePatterns` constructor 参数类型/顺序错误 | `local_ktester/evaluation/ruler/fix/Ruler_matches/repair_prompt_4.md` (local-only evidence) |
| ruler / `ByteMachine_addRangePattern` | `Range` constructor 参数类型错误 | `local_ktester/evaluation/ruler/fix/ByteMachine_addRangePattern/repair_prompt_4.md` (local-only evidence) |

Run3 有 105 个案例进入修复：首轮反馈中 73 个是编译错误、32 个是执行错误，只有 6 个初始即通过。官方 rep_1 有 102 个案例进入修复：35 个初始编译错误、67 个初始执行错误，9 个初始即通过。也就是说，Run3 在 LLM 初始输出阶段就产生了约两倍的编译问题；经过 5 轮修复后，官方 rep_1 达到 111/111 编译，Run3 仅 100/111。

## 7. 配置、提示、修复与环境审计

### 7.1 Run3 已确认配置

- 模型：`openai/gpt-4o-mini-2024-07-18`
- API：`https://openrouter.ai/api/v1`
- 温度：0.5；`code/tools/llm_api.py:46–52` 确实把温度传入 API
- 项目/案例：`PROJECTS=[]`、`CASES_LIST=[]`，因此运行全部 10 项目、111 案例
- 提示：`condition4case`、`io4case`、`exception4case`、`gencode`，日志第 1 行确认
- 生成方式：case-then-code
- 并发：8
- 修复：最多 5 次，与论文最终版本一致
- 覆盖率：JaCoCo `0.8.13-SNAPSHOT`；JUnit Platform Console `1.9.3`

生成日志第 43–50 行记录模型 ID，第 52 行起记录 OpenRouter 200 响应。HTTP 200 只能证明请求成功，不能证明生成代码质量或模型服务与论文完全等价。

### 7.2 提示与代码版本差异

Run3 当前模板与当前 Git HEAD 的 `code/templates/` 一致。与官方 rep_1 保存的 111 套提示相比，核心 condition/io/exception/gencode 指令语义一致；最明确的模板差异是官方旧模板在初始测试类上有 `@Timeout(600)`，当前模板已去掉。Run3 runner 本身仍有 600 秒进程超时，所以该一行不足以解释覆盖率差距。

上下文文件有排序、换行和抽取完整性差异。代表性案例 `AbstractPatriciaTrie_put` 中，Run3 的调用示例反而比官方 rep_1 多出缺失的方法签名，因此没有证据支持“Run3 上下文更少”这一解释。

2026-02 的代码把多 Java 代码块选择策略从“最长块”改为“第一块”。Run3 的 1067 个实际 LLM 响应中只有 1 个响应含多个完整 Java 块，且第一块就是最长块；该差异未实际改变本轮结果，应排除为主因。

测试案例合并、AST 插入和修复实现自 2025-07 后有修改。rep_4/rep_5 摘要文件的修改时间晚于主要 revision，且仍取得高覆盖和 100% CPR；不过文件时间不能替代运行 commit 清单。现有证据仍不足以表明某一个本地兼容性修改单独造成了本轮退化。

### 7.3 模型/服务可追溯性缺口

论文说所有方法使用 `gpt-4o-mini`、temperature=0.5。当前仓库模板使用 OpenAI 客户端默认端点；Run3 明确使用 OpenRouter 和带日期模型 ID。作者五轮产物未保存 API endpoint、解析后的 provider、请求 ID、response model 字段、seed、system fingerprint 或完整 settings 快照。

此外，Git 历史显示 `temperature=self.temperature` 到 2025-11-11 才进入仓库；rep_1 保存的提示文件时间早于该提交。由于可能存在未提交代码、复制时间变化或后期补产物，不能断言 rep_1 实际用了默认温度；但也无法从发布产物证明五轮都严格使用论文宣称的同一温度和同一代码 commit。这是一个实质可复现性缺口。

### 7.4 Java、Maven 与项目版本

- 当前终端默认 Java/Maven 已漂移到 Java 26 / Maven 3.9.16，但 Run3 生成测试 `.class` 的 major version 为 61，即 Java 17；论文仓库 README 也声明 OpenJDK 17.0.12。因此不能把当前终端的 Java 26 当成本轮实际编译环境。
- Run3 两个主日志没有 Maven 命令；测试类是直接用 `javac` 编译，覆盖率用 JUnit Console/JaCoCo 运行。精确 Maven 版本对本轮六项结果不是直接执行变量，但项目预构建过程未留环境清单。
- 论文 Table 1 写 Event-ruler 1.4.0，而本地 `pom.xml` 写 1.2.1。只读下载并比较官方 1.4.0 sources 后，`Range.java`、`Patterns.java`、`ValuePatterns.java` 与本地完全相同，`InputCharacterType` 在两边都没有 `DEFAULT`；四个 ruler 编译失败所引用的错误 API并不能由 1.2.1→1.4.0 版本差解释。
- 对 92 个同时有官方 rep_1 和 Run3 JaCoCo HTML 的案例比较 focal method 静态计数：branch 总数全部一致；instruction/line 总数差异通常仅 1–4，符合编译器/调试行映射差异，未观察到足以解释 10–15 pp 的控制流版本漂移。

## 8. 排序后的根因判断

### 1. 生成与修复结果质量退化 — 已证实，最高影响

证据：初始编译错误 73 vs 官方 rep_1 的 35；最终 11 个编译失败 vs 官方五轮 0；大量高权重案例覆盖从官方 70–100% 降为 0；Run3 仅 9 个类原始全通过；Sha2Crypt 每轮可运行到 600 秒超时；日志和修复提示显示幻觉 API、错误可见性、错误断言和无效输入。

这是六项差距的直接近因。它解释 CPR、EPR、全覆盖和 passing-only 覆盖同时下降。

### 2. 模型服务/随机输出未与论文环境冻结 — 高可能底层原因，中等归因置信度

证据：Run3 使用 OpenRouter + 日期模型 ID；论文/模板指向 gpt-4o-mini/OpenAI 默认；官方产物没有请求级元数据。官方五轮已有较大随机范围，但 Run3 在所有指标上低于五轮最小值，说明不是典型官方波动。

能确认“生成结果不同”，不能仅凭现有证据确认差异是 OpenRouter 路由、模型快照、服务端变更、随机性还是它们的组合。

### 3. 指标实现与论文名称/分母不一致 — 已证实，显著影响解释，部分影响数值

EPR 的类级/方法级差异极大；CPR 在失败存在时会受类级/方法数加权实现影响；LC/LCP 实为 instruction coverage；EPR 过滤启发式会改变通过数。官方 rep_2/rep_5 顶层 EPR 与逐项合计不一致，导致发布的 76.41 无法严格逐案例复算。

这些问题不能解释 BC 等全部差距，却会让“复现是否接近论文”的判断产生数个百分点甚至数量级的语义偏差。

### 4. 低分集中在 jdom2/ruler/codec/csv 的少数案例 — 已证实，属于差距载体

jdom2、ruler、commons-codec 合计解释 IC 差距 9.46/14.04 pp；commons-csv 额外解释 Correct IC 2.20 pp。优先检查这些项目比全量重跑更有效。

### 5. 论文/产物任务数不一致 — 已证实，低影响

论文写 110/15，数据集、官方五轮和 Run3 都是 111/16，多出的案例是 `MachineComplexityEvaluator_evaluate`。该案例在 Run3 仍有 32%/15% 覆盖，且官方与 Run3 correct coverage 接近；它不是主要负向驱动。单个任务对 111 任务宏平均的理论最大影响不足 0.91 pp。

### 6. Java/Maven/依赖或 Event-ruler 版本 — 现有证据不支持为主因

Run3 实际测试类为 Java 17 字节码，JaCoCo/JUnit 明确；Maven 未进入主评价命令；共同案例 branch 总数一致；ruler 失败 API 在 1.4.0 同样不存在。保留环境清单仍有必要，但不应把它排在模型输出与指标问题之前。

## 9. 最小化后续检查

按成本和判别力排序：

1. **先修正/确认 EPR 数据，不重跑 LLM。** 对官方五个摘要重新从 111 个项目项求和，要求作者确认 rep_2 的 79.1744 与 97.1744、rep_5 的 77.3920 与 71.3920 哪个是原始值，并解释正文 77.07。该检查可直接确定 Table 2 EPR 的可信分母。
2. **索取官方请求清单。** 最少需要五轮各自的 Git commit、`settings.py`、API base URL、实际 response model/provider、temperature、OpenAI SDK 版本、JDK/Maven 和项目构建 commit。没有这些信息，无法把底层原因从“模型/服务/代码组合”进一步拆开。
3. **做 3 个案例的小型端点 A/B，而非全量重跑。** 选择 `Verifier_isXMLPublicIDCharacter`、`Sha2Crypt_sha2Crypt`、`Rule_pattern`；固定官方 rep_1 原提示、同一代码/Java 17、temperature=0.5，分别调用论文端点与 Run3 端点，各重复 3–5 次，隔离保存产物。成功判据是初始编译率、修复后 CPR、执行通过率和 focal coverage，而不是只看 HTTP 200。
4. **在隔离临时工作区编译官方与 Run3 最终测试。** 先选 11 个编译失败案例中的 3 个，将官方 rep_1 最终测试与 Run3 最终测试对同一当前项目字节码进行编译；若官方测试仍全部编译，项目/JDK 偏差基本可排除，生成/修复差异得到更强因果证据。
5. **冻结 evaluator 两种口径。** 同时输出：类级 CPR/EPR、原始方法级 EPR、过滤后方法级 EPR、instruction/branch、line/branch、passing-only 对应值；不要覆盖现有 summary。这样后续运行不会再把论文语义差异与模型性能差异混在一起。

在完成第 1–2 项前，不建议直接全量再跑一次；全量新随机样本无法消除官方 EPR 和运行配置的可追溯性缺口。

## 10. 最终判断

Run3 并非“评价器简单算错导致看起来偏低”。用作者发布五轮摘要的实际 operational semantics 对比，Run3 的覆盖与通过率确实显著更差，且差距集中在可定位的项目和案例。最强证据指向生成/修复结果退化；最合理但尚未完全证实的底层解释是模型服务、随机性和运行代码版本没有被论文产物完整冻结。

同时，Table 2 不能被视为定义完全自洽的金标准：它把 instruction coverage 标成 line coverage，把方法级 EPR 置于测试类级文字定义下，官方 EPR 还有两个顶层/逐项不一致，任务总数也与论文文字不符。后续复现应同时报告“论文标签口径”和“源码实际口径”，并保存请求级与环境级清单。

## 11. 后续受控 repair 实验补强了什么

原始只读审计只能证明“最终生成/修复质量退化是直接近因”，但不能单靠观察性证据证明 repair context 是可干预的因果因素。随后完成的三案例配对实验固定了初始生成测试，并依次比较：

- A：当前 repair；
- B：增强失败诊断、禁止虚构 API、禁止修改或 shadow production code，并要求基于源码/契约构造 oracle；
- C：B 的规则再加 focal class source。

补齐 production resources 后的结果如下：

| 条件 | CPR | KTester-filtered EPR | Raw JUnit EPR | IC | BC | Correct IC | Correct BC |
|---|---:|---:|---:|---:|---:|---:|---:|
| A current repair | 66.67 | 17.65 | 5.88 | 65.67 | 61.67 | 32.33 | 31.00 |
| B enhanced repair | 100.00 | 61.54 | 38.46 | 77.33 | 73.67 | 44.00 | 43.00 |
| C enhanced + focal source | 100.00 | 66.67 | 46.67 | 82.00 | 78.33 | 48.67 | 47.67 |

完整报告见 [`../../repair_analysis/reports/controlled_repair_comparison.md`](../../repair_analysis/reports/controlled_repair_comparison.md)，机器可读结果见 [`../../repair_analysis/results/controlled_repair_metrics.csv`](../../repair_analysis/results/controlled_repair_metrics.csv) 和 [`../../repair_analysis/results/controlled_repair_case_results.csv`](../../repair_analysis/results/controlled_repair_case_results.csv)。

该实验把 repair prompt/context 从“相关性候选”提升为“已验证的可干预因素”：B 相比 A 同时提高 CPR、两种 EPR 和 correct coverage。但它仍然不能说明全量 111 案例会获得相同比例的提升，因为三个案例是有意选择的高贡献失败样本，且错误 oracle 在 `Verifier` 上没有被 A/B/C 修正。

## 12. 三次重复实验如何改变随机性判断

后续又在 12 个分层失败案例上完成三次独立重复。它们覆盖编译失败、API 幻觉、错误 oracle、timeout、runner failure 和低 focal coverage。

| 来源 | CPR | EPR | IC | BC | Correct IC | Correct BC |
|---|---:|---:|---:|---:|---:|---:|
| Run3 selected subset | 66.67 | 7.52 | 6.25 | 5.75 | 2.92 | 3.08 |
| New rep 1 | 75.00 | 32.71 | 40.08 | 33.33 | 35.25 | 27.75 |
| New rep 2 | 66.67 | 31.09 | 46.25 | 43.00 | 41.00 | 37.92 |
| New rep 3 | 83.33 | 38.14 | 48.75 | 39.83 | 35.08 | 25.67 |
| New three-rep mean | 75.00 | 33.98 | 45.03 | 38.72 | 37.11 | 30.44 |
| Official five-rep mean, same 12 cases | 100.00 | 73.90 | 61.20 | 50.80 | 50.47 | 41.40 |

五个案例发生 compile-status flip，五个案例发生 all-pass flip，证明一次 Run3 不能代表稳定期望值。然而即使最好的一次新重复，CPR/EPR 也只有 83.33%/38.14%，仍明显低于同一 12 案例的官方均值 100%/73.90%。因此：

1. 随机性是重要因素；
2. 它能解释 Run3 为什么可能特别差；
3. 它不能单独闭合与官方结果的剩余差距；
4. repair/generation strategy 仍是最强、且已经被配对实验验证的可操作因素。

完整报告见 [`../../repair_analysis/reports/stochasticity_12case_3rep.md`](../../repair_analysis/reports/stochasticity_12case_3rep.md)，逐案例与总体数据位于 [`../../repair_analysis/results/`](../../repair_analysis/results/)。

## 13. Artifact provenance 对结论的限制

官方 artifact 的额外取证发现：555 个官方 final tests 中，438 个与临时 repair candidate 字节完全一致，1 个 Java token 等价，62 个符合 direct initial assembly，18 个符合后续覆盖/assembly 模式，仍有 36 个无法映射。Run3 自身的 111 个 final tests 则形成闭合链：106 个匹配临时候选，5 个匹配直接初始 assembly。

这说明官方发布包不是一个能由单一 commit 和单一写入路径完整解释的历史快照。该 provenance gap 会限制“官方最终文件究竟如何形成”的历史判断，但不会反向造成 Run3 的低分。对应公开摘要见 [`artifact_provenance_findings.md`](artifact_provenance_findings.md)。

## 14. 证据可用性矩阵

| 证据 | 状态 | 用途 |
|---|---|---|
| Run3 111-case summary JSON | 仓库内 | 直接核验 Run3 的逐案例与顶层指标 |
| Table 2 vs Run3 CSV | 仓库内 | 核验六项 headline gap |
| Controlled repair CSV/JSON | 仓库内 | 核验 A/B/C 配对实验结果 |
| 12-case repetition CSV/JSON | 仓库内 | 核验随机范围、逐案例翻转和因素判断 |
| Python five-target artifacts | 仓库内 | 独立的轻量泛化实验，不用于反推 Java Table 2 |
| 论文 PDF | 上游公开 | 核验论文文字定义、任务数和 Table 2 |
| KTester source repository | 上游公开但未随本仓库复制 | 核验公开实现；因上游未提供明确 LICENSE，本仓库不重复发布 |
| 官方五轮 summary 原文件 | local-only evidence | 复算 Table 2 和发现 rep_2/rep_5 EPR 不一致 |
| Run3 完整日志、prompt、repair、Java tests、JaCoCo HTML | local-only evidence | 逐案例根因和时间窗验证；体积大且混有上游材料 |
| 官方完整 evaluation archive | local-only evidence | official final/temp/context provenance；未重复发布 |

“local-only”不表示证据不存在，而表示原始文件仍保存在实验机器上、未进入这个精简公开仓库。本报告对它们给出逻辑名称和用途，不暴露个人目录结构。

## 15. 完整性声明

本文件可以称为“完整的逐证据长版分析报告”，其完整性指：

- 覆盖了从论文指标、官方摘要、Run3 评价实现、项目贡献、案例贡献、失败日志、配置环境，到后续 repair/stochasticity/provenance 实验的整条论证链；
- 对每个主要结论标明了证据来源和置信边界；
- 保留了反例和未解决问题，没有把候选解释写成已证明事实；
- 仓库内可验证的紧凑结果与未上传的底层证据被明确区分。

它不等于“所有原始产物的完整镜像”。后者需要复制数 GB 的第三方项目、官方发布包、生成测试、日志、二进制依赖和无明确许可证的 KTester 源码，既没有必要，也不适合作为公开 GitHub 展示仓库。
