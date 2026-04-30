# ADR 023：游戏 UI Prompt Skill 补入手游热区尺寸与适配约束

- Status: accepted
- Date: 2026-04-29

## Context

`skills/06-game_ui_prompt_template.md` 已经能约束媒介、风格分支、反网页化和网页版 AI 交接包，但对手游界面最关键的**可操作性约束**仍不够明确：

- 触控热区
- 相邻可点击目标间距
- 安全区与手势区避让
- 出图画布尺寸基线
- 横竖屏基础适配

如果缺少这部分，生成出的界面即使风格正确，也可能在点击尺寸、贴边布局或刘海区避让上出现问题。

## Decision

在 `skills/06-game_ui_prompt_template.md` 中新增一组“基础触控与适配约束”，并区分：

1. **官方最小值**
   - Apple：44pt × 44pt
   - Android：48dp × 48dp
   - Android 相邻热区最小间距：8dp
   - WCAG 2.2 指针目标底线：24 × 24 CSS px

2. **知识库默认基线**
   - 高频主 CTA 优先 56dp 等效
   - 关键边缘缓冲与底部 CTA 安全缓冲
   - 横屏/竖屏默认画布尺寸

## Consequences

正面影响：

- 生图 Prompt 不再只约束风格，也开始约束可操作性。
- 线框原型、图片生图、Figma Brief 可以共享同一套基础适配底线。
- 对手游界面尤其常见的误触、贴边、手势冲突问题有更明确的前置约束。

成本：

- Prompt 会增加一小段基础适配说明。
- 对某些极小控件密集界面，可能需要使用“视觉小、热区大”的方式处理。

## Sources

- Apple Design Tips: Hit Targets
- Android Accessibility: Touch target size
- W3C WCAG 2.2 Target Size (Minimum)
- Apple Safe Area Layout Guide
- Android Edge-to-edge / Window Insets
