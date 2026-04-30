# ADR 020：游戏 UI Prompt Skill 扩展为网页版 AI 交接包

- Status: accepted
- Date: 2026-04-28

## Context

现有 `skills/06-game_ui_prompt_template.md` 已能支持本地 agent 生成游戏 UI Prompt、HTML 线框原型 Prompt 与 Figma Brief，但它主要面向“本地执行者直接消费”。  
当任务转向“把交互规范和 UI 资源图一起上传给网页版 AI”时，原 Skill 缺少：

- 附件清单
- 阅读顺序
- 规范与 atlas 的职责分工
- 自包含交接包模板

这会导致网页版 AI 只看图不看规范，或错误地把 atlas 当成拼贴素材，而不是结构与视觉语言参考。

## Decision

将 `skills/06-game_ui_prompt_template.md` 扩展为双通道 Skill：

1. 继续支持本地 agent 直接生成游戏 UI Prompt、HTML 线框 Prompt 与 Figma Brief。
2. 新增 `web_ai_handoff_pack` 模式，用于输出可直接上传到网页版 AI 的自包含说明包。

新增内容包括：

- 附件清单模板
- 阅读顺序模板
- 规范摘要模板
- atlas 使用规则
- 网页版 AI 最终生图 Prompt 模板

## Consequences

正面影响：

- 同一份 Skill 同时支持本地 agent 和网页版 AI。
- 交互规范与 UI atlas 的分工被明确写死，降低误读。
- 后续生成图片时更容易保持“规范先行、图谱补充”的结构约束。

成本与限制：

- Skill 会更长，执行时需要先判断当前输出模式。
- 若上传材料不完整，仍需要调用者补齐规范或 atlas。

## Follow-up

- 后续可为回归、战令、签到分别沉淀一版 `web_ai_handoff_pack` 实战模板。
