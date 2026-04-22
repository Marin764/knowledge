---
type: concept
title: "UI设计"
title_en: "User Interface Design"
aliases: [用户界面, 视觉设计]
created: 2026-04-21
updated: 2026-04-21
definition: "玩家与游戏进行互动的视觉界面，包括抬头显示器(HUD)、菜单、技能树、弹窗等所有视觉元素。"
game_referenced: [英雄联盟, 堡垒之夜]
source_count: 1
sources:
  - wiki/source/SYWNG-User-Interface-Design.md
related_concepts:
  - wiki/concepts/UX设计.md
  - wiki/concepts/UI动态设计.md
tags: [ui-design, visual-design, HUD]
status: active
confidence: high
---

# UI设计 (User Interface)

> [!NOTE]
> 本概念与 [[concepts/UX设计.md|UX设计]] 及 [[concepts/交互设计.md|交互设计]] 构成游戏开发的三大支柱。

## 定义
游戏中的**用户界面（UI）**是指玩家与游戏交互时所见到的所有视觉元素的集合。UI不仅仅是战斗中的HUD（抬头显示），还包括：
- 等级地图
- 角色选择画面
- 背包/装备界面
- 技能树
- 任务窗口

## 与UX（用户体验）的区别
- **UX设计**解决信息架构：决定信息存储在哪里、玩家以何种流程（Flow）最少操作地获取信息。
- **UI设计**解决视觉呈现：在UX规划的流程基础上，通过颜色、形状、排版和动效，将信息直观、美观地传达给玩家。两者密不可分。

## 视觉设计的核心
UI设计遵从视觉设计的基本原则，核心是**将复杂的信息以直观、简单的方式传达给观众**。

### 1. 适应受众与平台
- PC、主机和手机平台的UI设计有巨大差异（例如《堡垒之夜》的跨平台UI适配）。
- 游戏类型决定UI占比：卡牌游戏和4X策略游戏（如文明系列）90%都是UI，而叙事游戏则可能采用极简UI。

### 2. 生态与一致性
UI需要为整个游戏打造一个统一的生态系统。游戏中使用的：
- **排版 (Typography)**
- **图示 (Iconography)**
- **颜色 (Color)**
- **形状语言 (Shape Language)**
必须有一致的规则（例如红色代表敌对/警告，某种特定形状代表可点击）。

### 3. 布局（Layout）与心理学
布局直接影响玩家读取信息的速度，常利用心理学原则：
- **接近性（Proximity）**：将长条放在敌人名字旁边，玩家大脑会自动将它们关联，理解为"敌人的血条"；将经验值数字放在长条旁边，玩家会理解为经验槽。