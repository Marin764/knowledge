# ADR 014: 停用 AI 单控件透明层并收束到 Atlas 主产物

- Status: accepted
- Date: 2026-04-27

## Context

在引入 `generated/singles/` 之后，项目一度尝试把 AI 重建拼板继续拆成单控件透明 PNG，并将其作为可能的后续设计资源层。但这条路线在实践中暴露出几个明确问题：

1. 透明背景处理对复杂底板、信息板和弹窗框体的质量不稳定；
2. 单控件透明文件对当前目标帮助有限，无法保留页面上下文、尺寸比例和组合语法；
3. 用户已明确当前目标不是“直接复用到设计产线的单素材”，而是“给 AI 查看和使用的 UI 图谱参考”；
4. 继续维护 `generated/singles/` 会带来额外目录噪音、脚本负担和索引维护成本。

与此同时，真实截图裁切图 `crops/` 已经成为 `recognized-ui-elements-atlas` 的直接来源，验证了“真实裁切 + atlas 汇总”才是当前主链路。

## Decision

从当前主流程中正式停用 AI 单控件透明导出层：

- 不再继续维护 `assets/star_rail_controls/generated/singles/`；
- 不再继续维护面向该层的 `scripts/images/extract_generated_controls.ps1`；
- 移除依赖单控件透明层的 `generated-ui-elements-atlas-v1` 及其 manifest；
- 保留 `generated/` 下的重建拼板与日志，作为历史试验归档，而不是主参考层；
- 将 `atlas/` 明确为唯一的 AI 主参考产物层；
- 将 `crops/` 明确为 atlas 的真实来源层。

## Consequences

正面影响：

- `star_rail_controls/` 结构更清晰，主路径变成 `star_rail_ui -> manifests -> crops/review -> atlas`；
- 避免继续在低收益的透明导出上投入时间；
- atlas 的来源关系更干净，便于后续持续扩充和解释。

代价与限制：

- 失去了一层可单独浏览的 AI 单控件中间结果；
- 若未来重新需要设计师可直接拖用的素材层，需要重新定义一条独立导出流程；
- 历史 ADR 012 进入 `superseded` 状态，但相关实验产物仍保留在日志中以供追溯。
