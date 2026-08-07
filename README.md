# Governance-Driven Agentic Coding

## 一家 AI Native 公司的治理方式

一种由 Owner 掌舵、由 Agent 执行，并通过授权、留痕、独立挑战、
只读汇报与可审计学习闭环进行治理的软件开发方法。

这套方法关注的不是让更多 AI 同时写代码，而是如何把概率性的、
不完全可靠的模型组织成一个可替换、可追溯、可审查、可学习，
并始终由人类掌握最终责任的生产系统。

## 阅读

- [在线阅读中文版 v1.4](https://qisun2026.github.io/governance-driven-agentic-coding/)
- [下载中文版 PDF v1.4](./Governance-Driven-Agentic-Coding-v1.4.pdf)
- [Read the English edition v1.4 online](https://qisun2026.github.io/governance-driven-agentic-coding/en.html)
- [Download the English PDF v1.4](./Governance-Driven-Agentic-Coding-EN-v1.4.pdf)
- [查看 Change Log 与迁移说明](./CHANGELOG.md)
- [查看许可证与署名说明](./NOTICE.md)

## Practice Kit：直接拿来用

如果你不想先实现一套新 runtime，可以从轻量的
[GDAC Practice Kit](./practice-kit/README.md) 开始：

- Outcome Contract：在工作开始前冻结结果、权限、预算和停止条件；
- Project Closeout：停止一个项目，但不丢失其中可验证的学习；
- Method-Change Re-test：先和现有方法做基线比较，再决定是否升级规则；
- Harness Closeout Case：一个工程通过、产品证据不足，因此停止产品线并
  只保留可复用治理工具的负面案例。

Practice Kit 是非规范性配套材料，不改变 v1.4，也不代表其中的每个字段
都适用于每个任务。

## 当前版本

- 方法版本：v1.4，2026-07-30
- 中文版：v1.4
- 英文版：v1.4

从 v1.4 起，中英文使用同一个方法版本号。此前中文版 v1.2 与英文版
v1.3 保留其历史版本与文件，不追溯改名。

历史 PDF：

- [中文版 v1.2](./Governance-Driven-Agentic-Coding-v1.2.pdf)
- [English v1.3](./Governance-Driven-Agentic-Coding-EN-v1.3.pdf)

## 内容

1. 执行摘要
2. 第一性原理：委托不能等于失控
3. Investor Mandate 与组织宪法
4. 组织结构与权限模型
5. 标准运行循环
6. Organizational Memory：组织记忆
7. 四条信息流
8. 三个只读办公室
9. 一个项目留下五类复利资产
10. Lean 纪律、失效模式与衡量
11. 实践记录：三次治理干预
12. Practice → Evidence：可审计的治理学习闭环
13. 能力声明、结论来源与派生完整性
14. 最低可行实施清单

## 应用组合

该方法正在两条应用线上接受实践检验：

- **RiskFirewall AI — Product Risk Review** — Complex Instruments · Second Line
- **RiskFirewall AI — Risk Control Assurance** — Transactions, Processes & AI Actions · Third Line

`RiskFirewall AI` 是组合品牌，不是第四个仓库，也不证明 live AI execution、
自动决策、生产 firewall、已部署控制系统或两个应用具有相同实现状态。

## 边界

本文总结的是一套正在真实项目中实践和迭代的方法，不将其表述为
已经完成行业验证的标准。

应用项目提供事实、摩擦与证据，但不能自行改写共同方法。未经验证的
hypothesis 不进入 canonical method；未发布的候选不表述为公开版本。
AI 或 Agent 不替 Owner 决定风险偏好、重大原则或不可逆事项。

## 作者标识

Qi Sun · 小红书 `@就很菜` · `veggiedesu`

## 开源许可

除另有说明外，本仓库原创内容由 Qi Sun 以
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)
许可公开。你可以复制、传播和改编，包括商业使用；使用时须合理署名、
链接许可证、注明是否修改，并不得暗示作者为改编内容或其用途背书。

完整法律文本见 [LICENSE](./LICENSE)，推荐署名方式及第三方材料边界见
[NOTICE.md](./NOTICE.md)。

## 文件完整性

发布文件的 SHA-256 记录在 [SHA256SUMS.txt](./SHA256SUMS.txt)。
