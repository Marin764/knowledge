#!/bin/bash
# Wiki Helper - Easy commands for wiki maintenance

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WIKI_DIR="$SCRIPT_DIR/../wiki"
EXPORTS_DIR="$SCRIPT_DIR/../exports"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

show_help() {
    echo "📚 知识库工具集"
    echo ""
    echo "用法: wiki <command> [options]"
    echo ""
    echo "命令:"
    echo "  lint              运行健康检查"
    echo "  health            同 lint"
    echo "  slides [file]     生成幻灯片 (可选: 指定文件或 --all)"
    echo "  new <type> <name> 创建新页面 (type: concept/game/mechanics)"
    echo "  stats             显示知识库统计"
    echo "  orphan            列出孤立页面"
    echo "  list              列出所有页面"
    echo ""
    echo "示例:"
    echo "  wiki lint"
    echo "  wiki slides --all"
    echo "  wiki new concept 交互延迟"
    echo "  wiki new game 艾尔登法环"
}

cmd_lint() {
    echo -e "${YELLOW}🔍 运行健康检查...${NC}"
    cd "$SCRIPT_DIR/.."
    node scripts/internal/lint.js
}

cmd_stats() {
    echo -e "${YELLOW}📊 知识库统计${NC}"
    cd "$SCRIPT_DIR/.."

    echo ""
    echo "页面统计:"
    echo "  - 游戏 (games):     $(find wiki/games -name "*.md" 2>/dev/null | wc -l)"
    echo "  - 概念 (concepts):   $(find wiki/concepts -name "*.md" 2>/dev/null | wc -l)"
    echo "  - 机制 (mechanics):  $(find wiki/mechanics -name "*.md" 2>/dev/null | wc -l)"
    echo "  - 来源 (sources):    $(find wiki/sources -name "*.md" 2>/dev/null | wc -l)"
    echo ""
    echo "原始资料:"
    echo "  - 文章 (articles):   $(find raw/articles -name "*.md" 2>/dev/null | wc -l)"
    echo "  - 手册 (manuals):    $(find raw/game_manuals -name "*.md" 2>/dev/null | wc -l)"
}

cmd_list() {
    echo -e "${YELLOW}📄 知识库页面列表${NC}"
    echo ""
    echo "=== 游戏 ==="
    ls -1 wiki/games/*.md 2>/dev/null | xargs -I {} basename {} .md | sed 's/^/  /'
    echo ""
    echo "=== 概念 ==="
    ls -1 wiki/concepts/*.md 2>/dev/null | xargs -I {} basename {} .md | sed 's/^/  /'
    echo ""
    echo "=== 机制 ==="
    ls -1 wiki/mechanics/*.md 2>/dev/null | xargs -I {} basename {} .md | sed 's/^/  /'
}

cmd_slides() {
    cd "$SCRIPT_DIR/.."
    if [ "$1" == "--all" ]; then
        echo -e "${YELLOW}🎴 为所有概念生成幻灯片...${NC}"
        node scripts/internal/generate_slides.js --all
    elif [ -n "$1" ]; then
        echo -e "${YELLOW}🎴 生成幻灯片: $1${NC}"
        node scripts/internal/generate_slides.js -f "$1"
    else
        echo -e "${YELLOW}🎴 生成幻灯片 (默认全部)...${NC}"
        node scripts/internal/generate_slides.js --all
    fi
    echo -e "${GREEN}✅ 幻灯片已生成到 exports/ 目录${NC}"
}

cmd_new() {
    local type="$1"
    local name="$2"

    if [ -z "$type" ] || [ -z "$name" ]; then
        echo "❌ 缺少参数"
        echo "用法: wiki new <type> <name>"
        return 1
    fi

    local dir=""
    case "$type" in
        concept) dir="concepts" ;;
        game) dir="games" ;;
        mechanics) dir="mechanics" ;;
        *)
            echo "❌ 未知的类型: $type"
            echo "支持的类型: concept, game, mechanics"
            return 1
            ;;
    esac

    local filename="${name// /-}.md"
    local filepath="wiki/$dir/$filename"
    local today=$(date +%Y-%m-%d)

    if [ -f "$filepath" ]; then
        echo -e "${RED}❌ 文件已存在: $filepath${NC}"
        return 1
    fi

    cat > "$filepath" << EOF
---
type: $type
title: "$name"
created: $today
updated: $today
status: stub
---

## 概述

TODO: 填写页面内容

## 参考资料

- [来源标题](链接)

EOF

    echo -e "${GREEN}✅ 已创建: $filepath${NC}"
}

# Main
case "${1:-}" in
    lint|health)
        cmd_lint
        ;;
    stats)
        cmd_stats
        ;;
    list)
        cmd_list
        ;;
    slides)
        cmd_slides "$2"
        ;;
    new)
        cmd_new "$2" "$3"
        ;;
    -h|--help|help)
        show_help
        ;;
    "")
        show_help
        ;;
    *)
        echo -e "${RED}❌ 未知命令: $1${NC}"
        show_help
        exit 1
        ;;
esac