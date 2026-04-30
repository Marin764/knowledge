# ADR 009：游戏 UI Skill 升级为线框原型优先

- Status: accepted
- Date: 2026-04-24

## Context

现有的两条能力链路存在错位：

1. `skills/02-game_system_ux_spec.md` 已经能输出页面合同、区域合同和组件合同，但对“灰白线框原型”仍缺少专门约束，尤其缺少默认页、页面互斥、单页切换、占位符规则和线框表现红线。
2. `skills/06-game_ui_prompt_template.md` 更擅长约束“不要生成网页味的游戏 UI Prompt”，但对“可交互 HTML 线框原型”缺少单独模式，导致容易把规范元信息、说明文字或多页面内容带进同一画面。
3. 用户当前的核心诉求不是直接生成高保真网页，而是严格按照沉淀过的规范，先生成可点击、可切换、只表达游戏界面结构和信息框架的灰白线框原型。

## Decision

将游戏 UI 生成链路升级为“线框原型优先”的双层结构：

1. `skills/02-game_system_ux_spec.md` 增加 `wireframe_interactive` 模式。
2. 在 `skill 02` 中新增以下原型专属章节：
   - 原型呈现规则
   - 线框布局合同
   - 交互原型合同
   - 占位符规则
   - 线框表现红线
3. `skills/06-game_ui_prompt_template.md` 增加 `wireframe_interactive_html` 模式。
4. 在 `skill 06` 中新增以下约束：
   - 固定 `16:9` 画幅
   - 同一时刻只显示一个主页面
   - 左侧 tab / 主入口卡 / 返回按钮必须可点击
   - 禁止显式露出 `page.* / region.* / CTA` 等规范元信息
   - 角色立绘、大奖、横幅等内容以占位框 + 标签呈现
5. 后续只要用户明确提出“灰白线框”“先做结构”“可交互原型”“不要直接高保真”，默认命中原型模式，而不是视觉稿模式。

## Consequences

### Positive

- 规范层和 Prompt 层都能直接服务于 HTML 线框原型，不再只服务于视觉稿。
- 可以更稳定地生成“像游戏界面一样点击切换”的原型，而不是落回网页文档流。
- 后续验收标准更明确，能直接排查“页面叠层”“不可点击”“规范标签露出”等问题。

### Tradeoffs

- `skill 02` 的结构更重，产出规范时需要多补一层原型约束。
- `skill 06` 不再只是通用 Prompt 模板，而是分化为视觉稿与线框原型两种模式，使用时必须先判断目标模式。

## Follow-up

- 用战令、签到、商城等系统继续回测 `wireframe_interactive` 与 `wireframe_interactive_html` 的稳定性。
- 若后续 HTML 原型仍出现“网页味”或“交互错层”，优先检查 `skill 02` 的页面互斥规则和 `skill 06` 的元信息隐藏规则是否被 Prompt 完整继承。
