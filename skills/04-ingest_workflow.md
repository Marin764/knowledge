# Ingest Workflow (摄入工作流)

> **触发场景**：用户说 `ingest <file>` 或 `处理 <file>` 时。

## 核心流程 (Force Constraints)

1. **单篇处理原则**：严禁一次性读取多篇文章，必须**一篇一篇文章串行读取**。
2. **语言处理**：原始文档如果是英文，生成的 wiki 内容（source, games, concepts）必须全部**翻译为中文**。
3. **标签完善**：将通用 `clippings` 标签替换为具体标签（如 `game-design`, `haptics`, `typography`）。
4. **层级结构**：
   - 创建 `wiki/source/<name>.md`。
   - 更新/创建 `wiki/games/`、`wiki/concepts/`、`wiki/mechanics/`。
5. **冲突检查**：检查新旧内容是否有矛盾，若有则在页面中显著标记。
6. **索引维护**：更新 `wiki/index.md` 并追加日志到 `wiki/log.md`。

## 报告格式
处理完成后向用户报告：
- 创建/更新了哪些页面。
- 提取的核心要点摘要。
- 是否发现内容矛盾。
