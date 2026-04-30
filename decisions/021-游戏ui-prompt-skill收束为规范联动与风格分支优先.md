# ADR 021：游戏 UI Prompt Skill 收束为规范联动与风格分支优先

- Status: accepted
- Date: 2026-04-28

## Context

`skills/06-game_ui_prompt_template.md` 在补入网页版 AI 交接包能力后，已经能覆盖本地 agent 和网页版 AI 两种场景，但正文开始变长，且与 `skills/02-game_system_ux_spec.md` 的分工仍不够显式。

同时，像回归系统这类模块已经出现明显的多风格分支：

- 内容总览型
- 进度清晰型
- 奖励强化型

如果不在生成前先确认偏好，agent 很容易直接默认其中一种风格，导致出图方向偏离用户预期。

## Decision

将 `skills/06-game_ui_prompt_template.md` 收束为更精简的执行卡，并明确三件事：

1. **与 `skills/02-game_system_ux_spec.md` 强绑定**  
   `06` 不负责发明结构，而是负责把 `02` 产出的规范转成 Prompt / Brief / 交接包。

2. **风格分支前置**  
   对存在多种风格方向的系统，若用户未指定，生成前必须先询问偏好。

3. **正文简化**  
   保留四种输出模式，但把 Skill 压缩为更短的结构，避免执行时被冗长模板淹没。

## Consequences

正面影响：

- Skill 与设计规范链路分工更清楚。
- 生成前的风格确认更稳定，减少“默认画偏”的概率。
- 对 agent 和网页版 AI 都更易执行。

成本：

- 对多风格系统，生成前会增加一次必要的偏好确认。

## Follow-up

- 后续可将战令、签到等系统也补成自己的风格分支表。
