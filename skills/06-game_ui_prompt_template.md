# Skill: 游戏 UI 生成提示模板

> **触发方式**：当用户要求生成游戏界面 Prompt、界面图、生图说明包、HTML/Figma 界面 Brief，或明确要求“不要网页味 / dashboard 味”时，必须加载本 Skill。
>
> **输出目标**：生成一份可直接驱动图片模型、网页版 AI、HTML 原型或 Figma 执行的高约束 Prompt / Brief。

---

## 1. 角色与定位

你是一名**游戏 UI Prompt 编译器**。  
你的职责不是自己发明界面结构，而是把**已经生成好的设计规范 + UI 资源图谱 + 风格偏好**翻译成可执行的生成指令。

这条 Skill 必须与**生成后的设计规范文档**配合使用，优先读取：

- `exports/*交互设计规范*.md`

如果当前系统还没有正式规范，才退回：

- `wiki/analysis/*`

**原则**：没有结构规范时，不直接靠感觉写大段风格词；先吃规范，再写 Prompt。

---

## 2. 红线

- **先读规范，再写 Prompt**：优先读取对应 `exports/*交互设计规范*.md`；没有正式规范时，再退回 `wiki/analysis/`。
- **先锁游戏媒介**：必须先声明“这是游戏 UI / 16:9 / HUD 布局”，不能让模型自由理解。
- **先阻断网页味**：必须显式禁止 dashboard、landing page、浏览器导航、响应式网页流、营销专题页。
- **先问风格偏好，再细化 Prompt**：如果同一系统存在多种可行风格，且用户没指定，必须先询问偏好。
- **高价值内容不能降级**：皮肤、大奖、核心奖励、关键进度必须保留主视觉或高权重槽位。
- **原型模式必须单页互斥**：可交互原型中，同一时刻只允许一个主页面显示；`modal/overlay` 才允许叠加。
- **禁止显示规范元信息**：界面里不能出现 `page.*`、`region.*`、`CTA`、分析备注、浏览器 UI。
- **触控热区与安全区必须可执行**：Prompt 中必须能落到“最小点击尺寸、相邻间距、安全区和画布基线”这几个层面，不能只写“注意适配”。

---

## 3. 先读什么

生成前按以下顺序取上下文：

1. 目标系统的 `exports/*交互设计规范*.md`
2. 对应 `wiki/analysis/*` 页面
3. 对应 `assets/*_controls/atlas/*.png`
4. 需要时再补 `assets/*_ui/` 原图

---

## 4. 输出模式

| mode | 用途 | 输出重点 |
|---|---|---|
| `visual_game_ui` | 生图模型出界面图 | 游戏感、构图、层级、状态、主视觉 |
| `wireframe_interactive_html` | 灰白线框可交互原型 | 页面结构、切换关系、可点击对象、占位符 |
| `figma_brief` | Figma 拼界面 | 单帧构图、组件层级、面板关系 |
| `web_ai_handoff_pack` | 上传到网页版 AI | 附件清单、阅读顺序、规范摘要、最终生图 Prompt |

默认规则：

- 用户提“灰白线框 / 可点击 / 先做结构” -> `wireframe_interactive_html`
- 用户提“上传到网页版 AI / 给新的 AI 看 / 规范和 atlas 一起用” -> `web_ai_handoff_pack`
- 其他界面生图默认 -> `visual_game_ui`

---

## 5. 风格偏好规则

如果一个系统有明显的**多分支界面风格**，在用户没有指定时，必须先询问偏好，而不是直接默认。

### 5.1 通用风格分支

风格分支不应写死为某个系统专属模板，而应根据**设计规范和分析页**提炼 2 到 4 个候选方向。常用分支包括：

1. **总览分发型**
   适合功能入口较多、需要模块总览和分发的系统。

2. **进度聚焦型**
   适合强调阶段进度、里程碑、任务追赶路径的系统。

3. **奖励展示型**
   适合把皮肤、礼包、大奖、高价值钩子作为主视觉重点的系统。

4. **叙事沉浸型**
   适合强调角色引导、剧情氛围、拟物场景或情绪召回的系统。

### 5.2 提问格式

如果用户没指定风格，用一句简短中文直接问，并把当前系统可用的 2 到 4 个风格分支列出来：

`这次你更想要总览分发型、进度聚焦型，还是奖励展示型？`

如果用户已明确偏好，就不要重复问。

---

## 6. Prompt 骨架

无论输出到哪种媒介，Prompt 都按这个顺序写：

1. **媒介声明**
2. **模式声明**
3. **反网页化禁止项**
4. **16:9 / HUD 构图**
5. **页面目标**
6. **核心区域**
7. **关键组件与状态**
8. **风格分支说明**
9. **占位符规则**
10. **按媒介补充约束**

---

## 7. 必写字段

| 字段 | 作用 |
|---|---|
| `medium` | 图片 / HTML / Figma / 网页版 AI |
| `output_mode` | 四种模式之一 |
| `system_type` | 回归 / 战令 / 签到等 |
| `style_branch` | 内容总览型 / 进度清晰型 / 奖励强化型 |
| `canvas_ratio` | 默认 `16:9`，横屏优先，但不强制锁死方向 |
| `layout_mode` | HUD 布局语法 |
| `primary_focus` | 主视觉焦点 |
| `state_set` | `claimable / claimed / locked / active / protected` 等 |
| `anti_web_rules` | 反网页约束 |
| `placeholder_rules` | 无素材时的占位规则 |
| `touch_target_min` | 最小触控热区 |
| `target_spacing_min` | 相邻可点击目标最小间距 |
| `safe_area_rules` | 安全区 / 刘海 / 手势区约束 |
| `canvas_size` | 出图画布尺寸基线 |
| `adaptation_rules` | 横竖屏与边缘避让规则 |

如果是 `web_ai_handoff_pack`，还必须加：

| 字段 | 作用 |
|---|---|
| `attachment_bundle` | 要上传哪些文件 |
| `reference_read_order` | 先看什么后看什么 |
| `spec_digest` | 规范摘要 |
| `asset_anchor_rules` | atlas 和原图怎么用 |

---

## 8. 基础触控与适配约束

### 8.1 官方最小值

以下数值优先作为 Prompt 中的最小约束：

| 项目 | 约束值 | 用法 |
|---|---|---|
| iOS 最小点击尺寸 | `44pt × 44pt` | 适用于按钮、tab、icon button 等触控目标 [来源](https://developer.apple.com/design/tips/) |
| Android 最小点击尺寸 | `48dp × 48dp` | 适用于所有可交互目标 [来源](https://support.google.com/accessibility/android/answer/7101858?hl=en) |
| Android 相邻热区最小间距 | `8dp` | 适用于并排按钮、图标按钮、页签 [来源](https://support.google.com/accessibility/android/answer/7101858?hl=en) |
| Web / 泛指针环境最小目标 | `24 × 24 CSS px` | 用作更低保真的底线，不建议作为手游主基准 [来源](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum) |

### 8.2 本知识库默认基线

以下不是平台硬标准，而是当前知识库在出图和原型阶段的默认推荐值：

| 项目 | 默认值 | 说明 |
|---|---|---|
| 高频主 CTA 热区 | `>= 48dp 等效`，优先 `56dp 等效` | 适用于底部主按钮、关键确认按钮 |
| 高频 tab / 侧边入口热区 | `>= 44pt/48dp 等效` | 可见尺寸可略小，但热区不能低于最小值 |
| 相邻点击目标间距 | `>= 8dp 等效` | 密集列表和 icon row 尤其重要 |
| 关键内容与屏幕边缘缓冲 | `>= 16-24dp 等效` | 避免贴边，给手势和误触留空间 |
| 底部高频 CTA 与 Home Indicator 缓冲 | `>= 24dp 等效` | 没有具体 inset 数据时的默认保险值 |

### 8.3 安全区与基础适配规则

- 重要按钮、tab、文本标签、数值和状态信息必须落在安全区内，不能被刘海、挖孔、系统栏遮挡 [Apple 安全区来源](https://developer.apple.com/documentation/uikit/uiview/safearealayoutguide)。
- 允许背景、装饰线、底板延展到边缘，但**触控目标**不要放在系统手势区下方 [Android edge-to-edge 来源](https://developer.android.com/design/ui/mobile/guides/layout-and-content/edge-to-edge)。
- 采用 edge-to-edge 时，关键交互必须根据 window insets / safe area 做回退，不要把主 CTA、拖拽柄、分页切换放到手势抢占区域 [Android insets 来源](https://developer.android.com/develop/ui/views/layout/insets)。
- 视觉尺寸可以小于交互热区，但必须通过内边距或隐形热区补足最小目标尺寸。

### 8.4 出图画布基线

以下为当前知识库用于生图和原型的默认画布尺寸：

| 场景 | 默认画布 |
|---|---|
| 横屏主界面 | `1920 × 1080` |
| 竖屏主界面 | `1080 × 1920` |
| 横屏低成本概念稿 | `1600 × 900` |
| 竖屏低成本概念稿 | `900 × 1600` |

规则：

- 默认仍以 `16:9` 为主，横屏优先。
- 如果系统天然是竖屏手游或规范明确要求竖向主界面，允许切到 `9:16`。
- 同一轮生成中，不要混用横竖两套画布，除非用户明确要做双版本对照。

### 8.5 写进 Prompt 的最小适配句式

如果要把这一组约束写进 Prompt，至少补出类似句子：

```text
All primary interactive targets must meet mobile touch target minimums.
Use touch areas equivalent to at least 44pt on iOS or 48dp on Android, with at least 8dp equivalent spacing between adjacent targets.
Keep critical buttons, tabs, and labels inside the safe area and away from gesture-conflict zones.
Use a 1920x1080 canvas for landscape output by default, or 1080x1920 for portrait-first systems.
```

---

## 9. 各模式最小要求

### 8.1 `visual_game_ui`

必须写明：

- 这是游戏内系统界面，不是网页
- 默认 16:9，横屏优先，但可根据系统需求输出竖屏变体
- HUD 式构图
- 主视觉焦点
- 至少 3 个可见状态
- 明确风格分支

### 8.2 `wireframe_interactive_html`

必须写明：

- 默认 16:9，横屏优先，但可根据系统需求输出竖屏变体
- 灰白线框
- 同时只显示一个主页面
- 左侧 tab 或入口卡可点击切换
- `modal/overlay` 只能在规范明确要求时出现
- 立绘 / 大奖 / banner 用占位框

### 8.3 `figma_brief`

必须写明：

- 单帧 16:9，横屏优先，但允许竖屏变体
- HUD 层级
- 哪些区域用组件拼，哪些区域保留主视觉槽位
- 不按网页 dashboard 拼法组织页面

### 8.4 `web_ai_handoff_pack`

输出必须是一个可直接贴给网页版 AI 的单体说明，包含：

1. 任务说明
2. 附件清单
3. 阅读顺序
4. 规范摘要
5. atlas 使用规则
6. 最终生图 Prompt

---

## 10. 网页版 AI 交接包模板

```text
You are generating a game UI image based on an interaction spec and a UI resource atlas.

Files I am uploading:
1. [spec_file]
2. [atlas_file]
3. [optional_source_files]

How to use them:
- Read the interaction spec first. It defines page structure, regions, component hierarchy, states, and navigation.
- Read the UI atlas second. It teaches you the control vocabulary, framing language, panel shapes, and layout rhythm.
- Use source screenshots only as supporting style evidence.

Important constraints:
- This must look like an in-game system menu, not a webpage.
- Use a fixed 16:9 HUD composition.
- Do not generate dashboard cards, browser UI, marketing banners, article sections, or responsive web layout.
- Preserve the page hierarchy and visible states defined in the spec.
- Use the atlas to learn tabs, buttons, reward panels, and frame language. Do not collage the atlas directly into the output.

Target output:
- [target_page]
- [target_system_type]
- [target_style_branch]
- [target_fidelity]

Mandatory visible states:
- [state_1]
- [state_2]
- [state_3]

Primary focus:
- [primary_focus_1]
- [primary_focus_2]

Final image prompt:
[final_prompt_body]
```

---

## 11. 回归系统补充词

先从设计规范里提炼该系统最适合的风格分支，再写进 Prompt。  
不要把某个系统的固定风格表硬编码成全局规则。

---

## 12. 快速模板

### A. 通用游戏界面生图

```text
Generate a 16:9 game UI screen for a [system_type].
This must look like an in-game system menu, not a webpage.
Use a fixed HUD composition with a top status bar, central main stage, support panels, and strong CTA hierarchy.
Follow the [style_branch] direction.
Show clear [state_set].
Avoid dashboard cards, browser navigation, marketing banners, article layout, and generic web UI patterns.
```

### B. 灰白线框可交互原型

```text
Generate a fixed 16:9 interactive HTML wireframe prototype for a [system_type].
This must look like an in-game system menu, not a webpage.
Keep it grayscale and low-fidelity.
Only one main screen can be active at a time.
Use clickable tabs or entry cards to switch content.
Use labeled placeholder frames for art-heavy areas.
Follow the [style_branch] direction while keeping structure-first output.
```

### C. 网页版 AI 上传包开头

```text
I am uploading an interaction spec and a UI atlas.
Use the interaction spec as the structural source of truth.
Use the atlas as the visual/control language reference.
Read the spec first, then the atlas, then any additional screenshots.
Generate a 16:9 in-game system UI image, not a webpage.
Follow the [style_branch] direction.
```

---

## 13. 执行协议

1. **先判断系统是否已有规范**：优先读取 `exports/*交互设计规范*.md`。
2. **判断是否存在多风格分支**：如果有且用户没指定，先基于设计规范提炼候选风格，再问偏好。
3. **再判断输出模式**：图片、HTML、Figma 还是网页版 AI。
4. **补基础触控与适配约束**：把热区、间距、安全区和画布基线写进 Prompt。
5. **先写反网页约束，再写界面内容**。
6. **先锁结构，再补风格词**。
7. **如果是网页版 AI，必须输出完整交接包，而不是只给一句 Prompt**。

<!-- v1.0: 独立出反网页化的游戏 UI Prompt 模板 -->
<!-- v2.0: 增加 wireframe_interactive_html 模式 -->
<!-- v3.0: 增加 web_ai_handoff_pack 模式 -->
<!-- v4.0: 收束为规范联动、风格分支优先、可同时服务 agent 与网页版 AI 的精简版 Skill -->
<!-- v4.1: 改为依赖生成后的设计规范，16:9 横屏优先但不锁死方向，风格分支改为通用提炼规则 -->
<!-- v4.2: 新增手游触控热区、最小间距、安全区、画布基线与基础适配约束 -->
