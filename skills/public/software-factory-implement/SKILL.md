---
name: software-factory-implement
description: 按 design/ 实现代码与测试，产出台规的 PR body 并开 PR。含分支规范、测试取证要求、PR body 模板，以及不落盘的演练模式。
version: "1.0.0"
---

## 输入
design/<issue号>-<slug>.md（实现依据，契约不可偏离）
requirements/<issue号>-<slug>.md（只读，用来核对 AC）
仓库现有代码与测试（新代码必须与既有写法一致）

## 步骤
1. 前置检查（任一不满足就停，不写代码）：
   - Issue 是否带 ready-dev
   - design/ 是否存在
   - AC 与契约是否冲突
2. 分支：`agent/<issue号>-<slug>`，从默认分支最新处拉出。禁止直接推默认分支。
3. 实现：按 T-x 逐条落地，每新增一处逻辑必须配一个测试用例。
    - 复杂度分流：某 T-x 预计改动 >= 3个文件（含新增/删除/重命名）时不要手写，委托ACP：invoke_acp_agent(agent='codex', prompt=<自包含任务>)。
        - prompt里只描述任务本身，禁止出现 /mnt/user-data路径（ACP看不到它）
        - ACP 产出在 /mnt/acp-workspace/（对本 agent 只读），用 ls / read_file 取回
        - 取回后合入当前分支、逐条补测试用例、跑测试取证——这几步仍由本 agent 做。
    - 改动 < 3 个文件、或纯配置/单行修改：直接手写，不走 ACP。
4. 取证：跑测试，保存**命令 + 退出码 + 关键输出行**。
5. 开 PR：`gh pr create`，body 用下面模板。
5b. 等门禁：`timeout 540 gh pr checks <PR号> --watch`。超时后重跑该命令继续等，最多 3 轮。
    gate 不是 success 就自己修、push 到同一分支，禁止在 gate 红的状态下结束 run。
    最终 gate 的 run URL 写进 PR 评论。
6. 补评论：未完成的 T-x 逐条列原因；全完成写「全部任务完成」。

## PR body 模板（六段，缺一段视为未完稿）

## 改了什么
- T-1 <一句话> — 落地文件：`path/to/file.py`
- T-2 …

## 关联
Closes #<issue号>
design: design/<issue号>-<slug>.md

## 怎么验证的
命令：`<实际命令>`
退出码：<0 / 非0>
关键输出：<通过 N 条 / 失败 M 条 的原始行>

## 影响面
- 改了哪些模块：
- 是否改变既有接口行为：是 / 否（是则说明）

## 回滚
<回滚方式，或「纯新增，删文件即回滚」>

## 未完成 / 已知问题
- <T-x 未实现，原因：…> 或「无」

## 边界
- 不改 requirements/、design/ 下任何文件
- 不改 .github/workflows/、.env*、secrets/
- 不 force push、不合并 PR、不打 qa 标签
- 不做超出任务单的顺手重构
- ACP 只负责产出代码改动；建分支、commit、测试取证、gh pr create 一律由本 agent 完成，不交由 ACP。

## 演练模式（实现方法迭代时用）

触发：任务里出现「演练模式」字样。
此时：不改仓库、不建分支、不 push、不建 PR；
只产出 `outputs/pr-body.md`，内容按上面模板填一份**可核对**的草稿，
并在末尾附「本段证据是假设」清单。
目的：不污染真实仓库的前提下，单独验证模板是否符合。

## 验收
- 六段齐全，无占位符残留
- 每个 T-x 在「改了什么」和「未完成」两处之一出现，不允许消失
- 「怎么验证的」有命令和数字，不是「测试通过」

