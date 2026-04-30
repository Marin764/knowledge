# ADR 015: 将 assets JSON 元数据收束到 metadata 分层

- Status: accepted
- Date: 2026-04-27

## Context

随着星铁截图裁切链路扩展到全量 29 张页面，`assets/star_rail_controls/` 下累积了多类 JSON：

- 截图级 `manifest-*.json`
- atlas 编排清单
- AI 重建试验日志与队列

这些文件原先分散在根目录、`atlas/` 和 `generated/` 中，导致：

1. `star_rail_controls/` 根目录过于拥挤；
2. `atlas/` 与 `generated/` 同时混有图片主产物和 JSON 元数据；
3. 用户在浏览 `assets/` 时，不容易一眼区分“图片产物”和“控制它们的元数据”。

## Decision

在 `assets/star_rail_controls/` 下新增统一的 `metadata/` 分层：

- `metadata/screens/`
  保存截图级 `manifest-*.json`
- `metadata/atlas/`
  保存 atlas 编排清单
- `metadata/generated/`
  保存 AI 重建试验 manifest、日志与队列

迁移后约定如下：

- `crops/`、`review/`、`atlas/`、`generated/` 主要放图片产物；
- 所有 JSON 元数据优先进入 `metadata/`；
- 脚本继续采用“传入 manifest 路径”的方式，不把固定路径写死在代码里。

## Consequences

正面影响：

- `assets/` 浏览体验更清晰，图片和元数据分层明确；
- `star_rail_controls/` 根目录、`atlas/`、`generated/` 的噪音明显降低；
- 后续继续扩充 JSON 时，不会再次把图片目录堆满。

代价与限制：

- 历史日志和旧对话中提到的旧路径不再是当前物理位置；
- 后续手动运行脚本时，需要传入迁移后的 `metadata/...` 路径；
- 若未来为其他游戏建立同类资源库，建议沿用同样的 `metadata/` 分层。
