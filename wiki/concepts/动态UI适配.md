---
type: concept
title: "动态UI适配"
aliases: [Dynamic UI Scaling, 自适应布局, 响应式界面]
created: 2026-04-13
updated: 2026-04-13
definition: "通过相对约束（而非固定坐标/尺寸）构建UI布局，使界面能够自动适应不同屏幕尺寸、分辨率和系统字体大小等变化。"
games_referenced: []
source_count: 1
sources:
  - raw/articles/小屏幕游戏界面适配.md
related_concepts: [wiki/concepts/最小触控热区.md, wiki/concepts/安全区域适配.md]
tags: [ui, layout, responsive, multi-device]
status: active
confidence: high
---

## 核心设计原则
在多端游戏中，动态UI适配的核心原则是：**避免固定尺寸 UI，使用相对约束和安全区（Safe Area）** [来源: 小屏幕游戏界面适配.md]。

## 具体技术要求
1. **字体适配**：系统字体大小设置会影响游戏内文本的可读性。字体需要使用相对单位（pt/point）而非固定像素，并在用户更改系统字体大小时实时更新 [来源: 小屏幕游戏界面适配.md]。

2. **布局安全区**：在布局阶段需要顾及设备的刘海、圆角、Home Indicator 等物理和系统特性，使用平台提供的安全区 API（如 iOS 的 `safeAreaLayoutGuide`）来定位 UI 元素，而非使用屏幕边缘作为锚点 [来源: 针对游戏设计.md]。

3. **宽高比适配**：游戏菜单和 HUD 需要在各种宽高比（16:9、19.5:9、16:10、4:3 等）下都正确呈现而不遮挡游戏内容。这需要在设计时使用动态布局（Dynamic Layout），而非为每个分辨率单独制作固定布局 [来源: 针对游戏设计.md]。

4. **分辨率独立图形**：优先使用矢量或高清纹理而非固定分辨率的位图，以避免在不同屏幕上出现模糊或像素化 [来源: 针对游戏设计.md]。
