---
type: concept
title: UI锚点
aliases:
  - Anchor Point
  - 控件定位
created: 2026-04-13
updated: 2026-04-13
definition: 游戏引擎中用于控制UI控件相对屏幕位置的参考点，控件无论屏幕尺寸如何变化，都会保持相对于该锚点的位置关系。
games_referenced:
  - 塞尔达传说
source_count: 1
sources:
  - raw/articles/【游戏交互】手游适配设计.md
related_concepts: [wiki/concepts/动态UI适配.md, wiki/concepts/安全区域适配.md]
tags:
  - ui
  - tech
  - layout
status: active
confidence: high
---

## 核心机制
在游戏引擎的UI系统中，所有UI元素都有一个“锚点”（Anchor）。类似图像处理软件中的中心点，控件的坐标位置即为锚点的位置 [来源: 【游戏交互】手游适配设计.md]。

锚点控制的是控件的**相对位置**。例如：
- 锚定至屏幕左上角：无论屏幕比例是 16:9 还是 19.5:9，UI始终固定在屏幕左上角。
- 锚定至屏幕中心：UI始终居中。

## 适配应用
结合 [[concepts/动态UI适配.md|动态UI适配]] 和 [[concepts/安全区域适配.md|安全区域适配]]：
通过合理设置不同UI模块的锚点（如：血条锚定左上，小地图锚定右上，底部技能栏锚定中下），可以确保在不同设备分辨率下，UI布局框架不会发生错乱崩溃 [来源: 【游戏交互】手游适配设计.md]。
