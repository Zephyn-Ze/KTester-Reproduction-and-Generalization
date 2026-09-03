# KTester generation quality intervention experiment

## 结论

这次配对实验确认：**repair prompt/context 质量是 Run3 与 Table 2 差距的真实、可干预原因，但单靠 prompt 不能解释或消除全部差距。**

- B 相比 A，在完全相同的初始生成测试上，把 CPR 从 66.67% 提升到 100.00%（+33.33 pp）。
- 按 KTester 当前过滤口径，EPR 从 17.65% 提升到 61.54%（+43.89 pp）；按原始 JUnit，提升为 5.88% → 38.46%（+32.58 pp）。
- B 的 correct instruction/branch coverage 分别比 A 高 11.67/12.00 pp。
- C 再注入 focal source 后，correct instruction/branch coverage 达到 48.67/47.67%，但 `Verifier` 的错误 oracle 仍未修复；模型五轮都无视源码对 `@` 返回 true 的事实，坚持外部规范先验。
- `commons-codec` 的 production resources 存在于 `src/main/resources`，却不在本地 `target/classes`。补齐资源使 `Rule_pattern` 的 full instruction/branch coverage 从 0/0 恢复为 100/92%，但 raw passed 与 correct coverage 仍为 0。因此这是 full coverage 的环境原因，不是本例 EPR/correct coverage 低的原因。

## 实验控制

- 项目：jdom2、commons-codec。
- 案例：`XPathHelper_getSingleStep`、`Verifier_isXMLPublicIDCharacter`、`Rule_pattern`。
- 模型：`openai/gpt-4o-mini-2024-07-18`，temperature=0.5，FIX_TRIES=5。
- A：当前 prompt + 当前 repair。
- B：明确失败诊断、禁止虚构 API/修改或 shadow production、要求依据源码/契约构造 oracle。
- C：B + 将 focal class source 明确放入 repair context。
- 初始生成只运行一次；A/B 的 294 个已复制 prompt/context/response/test-class 文件 SHA-256 全部一致。C 的 3 个初始 test class 也逐项匹配该 manifest。
- 每组产生 15 个 repair response（3 cases × 5 tries）。

## 组会主表：补齐 production resources 后

| 组 | CPR | KTester EPR | Raw JUnit EPR | IC | BC | Correct IC | Correct BC |
|---|---:|---:|---:|---:|---:|---:|---:|
| A current repair | 66.67 | 17.65 | 5.88 | 65.67 | 61.67 | 32.33 | 31.00 |
| B enhanced repair | 100.00 | 61.54 | 38.46 | 77.33 | 73.67 | 44.00 | 43.00 |
| C enhanced + focal source | 100.00 | 66.67 | 46.67 | 82.00 | 78.33 | 48.67 | 47.67 |

所有数值均为所选 3 个高贡献失败案例的单次配对实验百分比，不能外推为 111-case 全量结果。

## 原始本地 target/classes（资源缺失）

| 组 | CPR | KTester EPR | Raw JUnit EPR | IC | BC | Correct IC | Correct BC |
|---|---:|---:|---:|---:|---:|---:|---:|
| A current repair | 66.67 | 17.65 | 5.88 | 32.33 | 31.00 | 32.33 | 31.00 |
| B enhanced repair | 100.00 | 61.54 | 38.46 | 44.00 | 43.00 | 44.00 | 43.00 |
| C enhanced + focal source | 100.00 | 66.67 | 46.67 | 48.67 | 47.67 | 48.67 | 47.67 |

## 逐案例因果结果

| 案例 | A | B | C | 已验证结论 |
|---|---|---|---|---|
| XPathHelper | compile fail，9 tests | compile pass，raw 4/5，IC/BC 35/36 | compile pass，raw 6/7，IC/BC 49/50 | 增强错误诊断和源码上下文能修复 private/API hallucination，并增加有效 focal coverage |
| Verifier | raw 1/3，IC/BC 97/93 | 与 A 相同 | 与 A 相同 | 上下文和 prompt 都不足以压过模型的错误规范先验；不是 shadow class，本轮测试调用了真实 focal method |
| Rule_pattern | compile pass，raw 0/5 | compile pass，raw 0/5 | compile pass，raw 0/5 | 补资源后 full IC/BC=100/92，但 assertions 仍全失败，故 correct IC/BC=0 |

## 与 Table 2 的关系

Table 2 为 100 / 76.41 / 63.94 / 55.46 / 55.52 / 47.21；Run3 为 90.09 / 53.74 / 49.90 / 44.85 / 40.79 / 36.09。

在所选最差案例上，B/C 的 CPR 已到 100%；B 的 correct IC 44.00% 仍低于 Table 2 11.52 pp，C 缩小到 6.85 pp；B 的 correct BC 43.00% 低 4.21 pp，C 为 47.67%，接近 Table 2。该方向与全量差距一致，但样本是有意选择的高贡献失败案例，不能声称已经把全量 Run3 修到 Table 2。

可以用于组会的严谨判断是：

1. **显著成立**：当前 repair prompt/context 是可复现的因果因素，能同时改善 CPR、EPR 和 correct coverage。
2. **仍未闭合**：错误 oracle 在 15 次（A/B/C 各 5 次）repair 中始终未改正；模型/provider 行为仍是剩余差距候选。
3. **环境差异成立但作用有限**：缺失 resources 可大幅压低 full coverage，但本例不提升 EPR 或 correct coverage。
4. **artifact provenance 不是本轮原因**：所有实验 final 都由开源 `max(passrate)` 选择逻辑产生；A/B/C 的 Verifier 都回选 temp0，XPathHelper 分别选择 A temp5、B temp3、C temp3。

## 推荐复现实验设置

- Java 17；正式执行前确保 Maven resources 已进入运行 classpath/`target/classes`。
- 保持 model string、temperature=0.5、FIX_TRIES=5，同时保存请求级 effective provider/model metadata；当前 KTester 只保存 response content，无法证明 OpenRouter 实际后端快照。
- 合并 B 的增强 repair prompt 和 C 的 focal source context，但不要宣称它已解决 oracle 问题。
- 同时报告 raw JUnit EPR 与 KTester filtered EPR。本样本中 A/B/C 的 filtered EPR 分别比 raw 高 11.77/23.08/20.00 pp。
- 下一次扩展应做 12–15 个分层案例，而不是立即跑 111：覆盖 compile/API、wrong oracle、timeout、zero focal coverage 四类；至少 3 个随机重复。

## 安全迁移

候选补丁只涉及 `code/procedure/post_process.py` 与 `code/templates/post_process.j2`。原始 KTester 当前是 dirty worktree，因此本实验没有自动迁移；应先在新副本执行 `git apply --check migration_candidate.patch`，再运行单案例预检。资源补齐属于构建步骤，不应把 128 个资源文件手工提交到源码补丁。
