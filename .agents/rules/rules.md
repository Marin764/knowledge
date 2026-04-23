# Game Design Wiki - Schema

> 这是整个知识库的"宪法"，定义了 AI 维护者的行为规范和工作流。本知识库以**游戏设计**相关的知识为主，涵盖但不局限于游戏交互设计、关卡设计、系统设计、叙事设计等领域。

## 1. 目录结构规范

```
know/                          # 根目录
├── CLAUDE.md                 # 本文件 - Schema 定义
├── scripts/                  # 工具脚本
│   ├── images/               # 图片处理 (去重/缩放)
│   ├── fetchers/             # 外部抓取 (YouTube 等)
│   ├── internal/             # 内部逻辑 (Lint/Slides)
│   ├── archive/              # [新增] 归档脚本 (备份/环境重建)
│   ├── README.md             # 工具箱说明索引
│   └── wiki.sh               # 便捷命令入口
├── exports/                   # AI 生成的可交付物（幻灯片/图表）
├── wiki/
│   ├── index.md              # 知识库总索引（自动维护）
│   ├── log.md                # 操作日志（纯追加）
│   ├── games/                # 游戏实体页面/枢纽 (e.g., 王者荣耀.md)
│   ├── concepts/             # 交互设计概念 (e.g., hitstop.md)
│   ├── mechanics/            # 具体机制理论 (e.g., 战斗通行证系统.md)
│   ├── analysis/             # [新增] 专项子系统拆解 (e.g., 王者荣耀-战令系统.md)
│   ├── source/               # 来源摘要
│   └── comparisons/           # 跨游戏对比分析
├── raw/                      # 原始资料库（不可变，AI 只读）
│   ├── gdc_vault/            # GDC 演讲/总结
│   ├── articles/             # 博客文章
│   ├── game_manuals/        # 游戏设计文档
│   ├── video_scripts/        # 视频文字稿
│   └── screenshots/          # [新增] 原始截图
├── skills/                   # [新增] AI 技能文件库
│   ├── README.md             # 技能索引与调用规则
│   ├── 01-ui_analysis.md     # UI 截图分析 Skill
│   └── 02-battle_pass_spec.md# 战令系统交互规范生成 Skill
└── assets/                   # 图片/动图/GIF
```

## 2. Frontmatter 规范

每种 wiki 页面都有对应的 YAML frontmatter，格式如下：

### games/ (游戏实体)

```yaml
---
type: game
title: "游戏中文名"
title_en: "Game English Name"
created: 2026-04-13
updated: 2026-04-13
developer: ""
publisher: ""
release_date: ""
genre: [action, rpg, platformer]
platform: [PC, Switch, PS5]
source_count: 1
sources:
  - raw/articles/xxx.md
related_games:
  - wiki/games/塞尔达传说-旷野之息.md
related_concepts:
  - wiki/concepts/hitstop.md
tags: [combat, open-world, exploration]
status: active
confidence: medium
---
```

### concepts/ (交互设计概念)

```yaml
---
type: concept
title: "概念名称"
aliases: [别名1, 别名2]
created: 2026-04-13
updated: 2026-04-13
definition: "一句话定义这个概念"
game_referenced: [游戏名, 游戏名]
source_count: 2
sources:
  - raw/gdc_vault/xxx.md
  - raw/articles/xxx.md
related_concepts:
  - wiki/concepts/xxx.md
tags: [feedback, input, timing, animation]
status: active
confidence: high
---
```

### mechanics/ (机制设计)

```yaml
---
type: mechanics
title: "机制名称"
category: [movement, combat, camera, ui, input]
created: 2026-04-13
updated: 2026-04-13
description: "机制的详细描述"
game_examples: [例子]
implementation_notes: "技术实现要点"
source_count: 1
sources:
  - raw/video_scripts/xxx.md
related_mechanics:
  - wiki/mechanics/xxx.md
tags: []
status: active
---
```

### source/ (来源摘要)

```yaml
---
type: source
title: "来源标题"
author: "作者名"
url: "原始链接"
date: 2026-04-13
format: [article, gdc, video, book]
key_points:
  - "关键要点1"
  - "关键要点2"
game_focus: [游戏名]
concepts_extracted:
  - wiki/concepts/xxx.md
---
```

### ui_specs/ (UI 截图分析)

```yaml
---
type: ui_spec
title: "页面名称"
game: "游戏名"
screen_type: [hud, menu, loading, inventory]
created: 2026-04-21
updated: 2026-04-21
source_image: "raw/screenshots/xxx.png"
components:
  - name: "组件名"
    description: "功能简述"
related_concepts:
  - wiki/concepts/xxx.md
related_mechanics:
  - wiki/mechanics/xxx.md
tags: [layout, alignment, feedback]
status: active
---
```

## 3. 不可变性规则

- **raw/** 目录：只读。AI 不得修改、删除其中的任何文件。
- **assets/** 目录：只读。图片/GIF 仅供引用。
- **wiki/** 目录：AI 全权维护。创建、更新、删除均由 AI 执行。

## 4. 三大核心工作流

### 4.1 摄入 (Ingest)

**触发**：用户说 `ingest <file>` 或 `处理 <file>`

**完整流程**：
1. 读取原始文档 `raw/xxx`
2. **语言处理**：如果原始文档是英文，处理时必须进行翻译，提取和生成的 wiki 内容（包括 source、games、concepts、mechanics）必须全部使用中文。英文原文标题可以在 frontmatter 的 `title_en` 中保留。
3. **单篇处理原则**：无论用户要求处理多少篇文章，AI 都必须**一篇一篇地串行读取和处理**，严禁一次性读取多篇文章，以免超出上下文限制或导致信息混淆。
4. 移动文件到正确分类（`articles/`、`game_manuals/`、`gdc_vault/`、`video_scripts/`）
5. 向用户确认 2-3 个核心要点（摘要 + 关键论断）
4. **完善 tags**：将导入插件生成的通用 `clippings` tag 替换为有意义的标签
   - 根据文档内容提取 2-4 个相关标签
   - 常用标签参考：`game-design`, `ui`, `input`, `feedback`, `platform`, `mobile`, `accessibility`, `typography`, `haptics`, `layout`, `adaptation`
5. 创建 `wiki/source/<source-name>.md`（来源摘要）
6. 更新或创建相关游戏页面 `wiki/games/`
7. 更新或创建相关概念页面 `wiki/concepts/`
8. 更新或创建相关机制页面 `wiki/mechanics/`
9. 检查新旧内容是否有矛盾，标记在页面中
10. 更新 `wiki/index.md`
11. 追加到 `wiki/log.md`
12. 向用户报告：创建/更新了哪些页面、有无矛盾

### 4.2 查询 (Query)

**触发**：用户提问（不以 ingest 开头）

**流程**：
1. 用户提出问题
2. AI 分析需要哪些 wiki 页面来回答
3. 读取相关页面（games/concepts/mechanics）
4. 综合信息，给出带引用的回答
5. **可选**：将回答回填到 wiki 作为新页面（如 comparison）

**格式**：回答可以是纯文本，也可以是：
- Markdown 页面
- 对比表格
- 包含 `---` 分页符的 Marp 幻灯片文件（当用户要求总结时可直接生成，存放在 `exports/` 目录）
- 图表代码

### 4.3 健康检查 (Lint)

**触发**：用户说 `lint` 或 `健康检查`

**检查项**：
- 页面间矛盾（concept 页的新结论是否推翻旧来源）
- 过时内容（数据/版本是否需要更新）
- 孤立页面（无入链的页面）
- Stub 页面（<100 字的占位符）
- 缺失页面（被引用但不存在的 wikilink）
- Frontmatter 不一致（必填字段缺失）
- 未摄入的 raw 文件

**输出**：报告 + 修复建议

### 4.4 UI 分析与模块化存储 (UI Analysis)

**触发**：用户说 `analyze_ui <image>` 或 `分析UI <图片>`

**基础流程**：
1. **预处理**：运行 `python scripts/images/preprocess_images.py` 执行去重与缩放。
2. **视觉逆向工程**：按照“层级、布局、交互、UX、组件抽象”五个维度输出。
3. **枢纽架构 (Hub-and-Spoke)**：
    - **禁止过度堆砌**：核心游戏页面保留概况，具体的系统分析（如战令、商城）应剥离至 `wiki/analysis/` 目录。
    - **双向锚定**：在 Game Hub 页建立链接指向 Analysis 子页，同时在 Analysis 子页链接回母游戏母页。
4. **归档**：保存到 `wiki/analysis/`，并确保不在 `wiki/index.md` 首页过度平铺。

## 5. 索引系统

### wiki/index.md 结构

```markdown
# Game Interaction Design Wiki

Last updated: 2026-04-13 | Pages: X | Sources: X

## Games (X)
- [[games/塞尔达传说-旷野之息]] — 开放世界动作冒险 (2 sources)
- [[games/空洞骑士]] — 2D 魂类平台跳跃 (3 sources)

## Concepts (X)
- [[concepts/hitstop]] — 打击停顿/顿帧 (4 sources)
- [[concepts/coyote-time]] — 土狼时间/跳跃宽容期 (3 sources)

## Mechanics (X)
- [[mechanics/锁定系统]] — 目标锁定机制 (2 sources)
- [[mechanics/镜头跟随]] — 相机跟随算法 (2 sources)

## Source Summaries (X)
- [[source/gdc-2023-action-design]] — GDC 2023 动作设计 (2026-04-02)
```

### wiki/log.md 结构

```markdown
## [2026-04-13] ingest | 游戏交互设计入门文章
- Source: raw/articles/intro-to-game-input.md
- Pages created: source/intro-to-game-input.md, concepts/input-delay.md
- Page updated: games/塞尔达传说-旷野之息.md
- Contradictions: none
```

## 6. 写作风格与卫生约定

- **文件名强制中文**：所有 wiki/ 和 raw/ 文件名必须保存为中文。
- **Wikilink (路径校准)**：
    - **禁止绝对前缀**：在 `wiki/` 目录内部文件互相跳转时，**严禁**使用 `[[wiki/xxx]]` 前缀，以防触发路径解析 Bug 产生 `wiki/wiki/` 幽灵目录。
    - **正确格式**：使用相对于 `wiki/` 根目录的路径，即 `[[目录/文件名.md]]`。
    - **示例**：在 `index.md` 中链接王者，应使用 `[[games/王者荣耀.md]]`。
- **去重原则**：同名称/同实体的词条全库仅保留一个。
- ** Stub 清理**：禁止创建仅含标题的空白笔记。内容不足 20 字的 placeholder 应在 Ingest 阶段直接合并或删除。
- **引用格式**：每个论断必须注明来源 `[来源]`。
- **动图引用**：用 `![描述](assets/xxx.gif)` 格式引用 GIF。

## 7. 特定领域约定

### 游戏交互设计的核心概念分类

1. **输入类 (Input)**：预输入、输入缓冲、输入延迟、取消动画
2. **反馈类 (Feedback)**：Hitstop顿帧、屏幕震动、音效反馈、视觉闪烁
3. **时机类 (Timing)**：土狼时间、跳跃缓冲、攻击前摇、闪避无敌帧
4. **物理类 (Physics)**：摩擦力、跳跃高度、重力曲线、碰撞盒
5. **相机类 (Camera)**：跟随算法、锁定视角、焦点转换、视野控制
6. **UI类 (UI)**：血条交互、血条闪烁时机、提示文字层级

### 交互手感评估维度

- **响应感**：输入到反馈的时间差
- **打击感**：攻击命中时的多感官反馈强度
- **节奏感**：动画节奏与玩家预期的匹配度
- **容错感**：系统对玩家失误的宽容程度
- **重量感**：角色移动/攻击时的惯性体验

## 8. 工具约定

### 8.1 脚本工具

| 脚本 | 用途 | 调用方式 |
|------|------|----------|
| `scripts/internal/lint.js` | 健康检查：死链接、孤立页面、FM 校验 | `node scripts/internal/lint.js` |
| `scripts/internal/generate_slides.js` | Marp 幻灯片生成 | `node scripts/internal/generate_slides.js --all` |
| `scripts/fetchers/youtube.sh` | 抓取 YouTube 字幕并转为 Markdown | `bash scripts/fetchers/youtube.sh <url> [标题]` |
| `scripts/wiki.sh` | 便捷命令入口 (CLI) | `bash scripts/wiki.sh <command>` |
| `scripts/images/preprocess_images.py` | 截图预处理：去重、缩放、压缩 | `python scripts/images/preprocess_images.py` |

**归档原则**：针对特定项目的一次性修复脚本或陈旧脚本存放在 `scripts/archive/`，不列入常用工具表，仅作为环境重建备份。

**Git Hooks**：`.git/hooks/pre-commit` 会在每次 `git commit` 时自动运行 `lint.js`，确保提交内容健康。

**搜索**：当 wiki 页面超过 100 个时，建议使用 qmd 搜索
- **可视化**：需要时用 Mermaid 画概念关系图
- **幻灯片**：需要输出演示时用 Marp 格式

### 8.2 AI 技能库 (Skills)

**目录**：`skills/`

**定义**：Skills 是供 AI 代理人调用的**标准化任务说明文件**。每个 Skill 定义了在特定场景下的分析框架、输出格式、质量检查标准与必须遵循的强约束。

| 技能文件 | 触发场景 | 输出目标 |
|------|------|------|
| `skills/01-ui_analysis.md` | 用户提供游戏 UI 截图 | 五维度分析报告，录入 `wiki/analysis/` |
| `skills/02-game_system_ux_spec.md` | 用户要求生成任意游戏系统交互规范（战令/商城/抽卡/公会等） | 正式规范文档，保存至 `exports/` |

**调用规则**（强制）：
- AI 在执行相关任务前，**必须完整读取对应 Skill 文件**，以 Skill 中的模块结构为输出骨架。
- Skills 中定义"必须覆盖"的内容不可省略。
- 新增 Skill 时，必须同步更新 `skills/README.md` 中的技能索引。

**版本管理**：Skill 文件内容的重大更改须在文件末尾追加变更日志，格式：`<!-- v1.1: 新增了模块 X -->`。

---

*Schema version: 1.7 | Last updated: 2026-04-23*