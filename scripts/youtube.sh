#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Check dependencies
if ! python -c "import youtube_transcript_api" &> /dev/null; then
    echo "📦 正在安装依赖: youtube-transcript-api..."
    pip install youtube-transcript-api
fi

if [ -z "$1" ]; then
    echo "❌ 缺少 YouTube 链接"
    echo "用法: bash scripts/youtube.sh <youtube_url> [文章标题]"
    exit 1
fi

URL="$1"
TITLE="$2"

if [ -n "$TITLE" ]; then
    python scripts/youtube_fetcher.py "$URL" -t "$TITLE"
else
    python scripts/youtube_fetcher.py "$URL"
fi
