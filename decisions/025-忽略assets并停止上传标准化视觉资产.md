# ADR 025: 忽略 assets 并停止上传标准化视觉资产

## Status

accepted

## Date

2026-04-30

## Context

`assets/` 中包含大量标准化截图、控件裁切、图谱和本地研究素材。它们对本地 AI 分析和生图研究很重要，但体积较大，且不适合作为默认 GitHub 同步内容。

此前 `.gitignore` 已经忽略 `raw/`，但 `assets/` 中已有部分文件被 Git 跟踪，导致上传知识库时仍会携带图片资产。

## Decision

将 `assets/` 加入 `.gitignore`，并把已经被 Git 跟踪的 `assets/` 文件从 Git 索引中移除，仅保留本地文件。

后续 GitHub 只同步知识库文本、规范、脚本和元规则；视觉资产保留在本地工作区。

## Consequences

- GitHub 仓库体积会明显降低。
- 新增或修改的 `assets/` 内容不会被默认提交。
- 文档中仍可引用本地 `assets/` 路径，但远端仓库不再保证这些图片存在。
- 如果未来需要发布一批资产，应使用单独的发布包或重新设计资产同步策略。
