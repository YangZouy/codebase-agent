---
name: software-factory-review
description: 按验收标准逐条核对 PR、跑 design 指定的命令、输出 pass/fail/unknown 三态结论与 ≤200 字评论，并按 Blocker/Critical/Major/Minor 分级。只评审，不改任何文件。
version: "1.0.0"
---

## 输入
requirements/ 的 AC（唯一裁判依据）
PR diff
design/ 指定的测试命令
CI 结果 —— 唯一来源是 `gh pr checks <PR号> --repo <repo>` 的输出。
没有记录、或 gate 不是 success，一律按门禁未过处理；自己跑的测试不能替代它。

## 步骤
0. 取门禁结论：`gh pr checks <PR号> --repo <repo>`。
   - gate = success → 继续第 1 步
   - gate = failure / cancelled / 不存在 → PR 评论写「门禁未过」，打 qa:fail，结束，不再核对 AC
   - gate 仍在跑 → 不打任何标签，评论「等待 CI」，结束
1. 逐条取出 AC，建一张核对表，表头固定为 `AC 编号 | 判定 | 证据 | gate`
   （每条 AC 一行，判定先全部标 unknown；gate 列填第 0 步拿到的整体门禁状态，同一 PR 每行一致）。
2. 对每条 AC：读 diff 找实现 → 有测试命令就执行 → 填 pass / fail / unknown。
3. 跑 design 指定命令，记录命令、退出码、关键输出。这份输出是AC级证据，不能替代第0步的gate结论。
4. 越权检查：本 run 是否改过任何文件（`git status` 必须干净）。改了 → 全表强制 fail，理由「越权写入」。
5. 按 base 的分级整理问题清单，只列 Blocker/Critical 的给结论，Major/Minor 附在报告里。
6. 输出 check/qa-<pr号>.md + ≤200 字 PR 评论。
7. 打标签：全 pass → qa:pass；有 Blocker/Critical/fail → qa:fail。

## 评论模板（≤200 字）
结论：pass / fail（Blocker n · Critical m）
- AC1 xxx：pass（证据：文件:行号 / 命令输出行）
- AC2 xxx：fail（证据：…）
- AC3 xxx：unknown（缺：…）
详见 check/qa-<pr>.md

## 边界
- 不改任何文件（含测试文件）—— fail 就写复现步骤打回 developer
- 不合并 PR、不改标签以外的东西
- AC 有歧义回 PM，不自行解释
- 不把静态观察写成"测试通过"

## 验收
每条 AC 都有三态之一；unknown 必须写缺什么；评论 ≤200 字且带证据位置。
`check/qa-<pr号>.md` 必须含 `gh pr checks` 的原始输出行；缺此行视为未完成。

