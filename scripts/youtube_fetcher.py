import argparse
import json
import re
import os
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Configuration
RAW_YOUTUBE_DIR = Path("raw/youtube")

def extract_video_id(url):
    """Extract YouTube video ID from URL."""
    parsed = urlparse(url)
    
    # youtu.be/VIDEO_ID
    if parsed.hostname == 'youtu.be':
        return parsed.path[1:]
    
    # youtube.com/watch?v=VIDEO_ID
    if parsed.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed.path == '/watch':
            return parse_qs(parsed.query)['v'][0]
        # youtube.com/shorts/VIDEO_ID
        elif parsed.path.startswith('/shorts/'):
            return parsed.path.split('/')[2]
            
    return url # Return as-is if it might be an ID already

def format_time(seconds):
    """Convert seconds to MM:SS format."""
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes:02d}:{seconds:02d}"

def fetch_transcript(video_id, languages=['zh-Hans', 'zh-Hant', 'zh-TW', 'zh', 'en']):
    """Fetch transcript using youtube-transcript-api."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api.formatters import TextFormatter
    except ImportError:
        print("❌ 请先安装依赖: pip install youtube-transcript-api")
        return None

    try:
        print(f"🔄 正在尝试获取视频字幕 (ID: {video_id})...")
        
        # Try to get transcript list
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Priority: 1. Manual translation, 2. Auto generated in target language
        try:
            transcript = transcript_list.find_transcript(languages)
        except:
            # Fallback to English, then translate
            try:
                en_transcript = transcript_list.find_transcript(['en'])
                print("🔄 未找到中文，尝试自动翻译为中文...")
                transcript = en_transcript.translate('zh-Hans')
            except:
                # Get whatever is available
                transcript = transcript_list.find_generated_transcript(['en'])
                print("⚠️ 无法翻译，将使用原语言字幕。")

        # Fetch the actual data
        data = transcript.fetch()
        
        # Format as Markdown
        md_lines = []
        md_lines.append(f"## 视频字幕 (来源: {transcript.language})\n")
        
        # Group by sentences/time blocks to make it readable
        current_block = []
        current_time = 0
        
        for entry in data:
            text = entry['text'].replace('\n', ' ').strip()
            if not text:
                continue
                
            # If start of a new minute, add a timestamp marker
            if entry['start'] - current_time > 60 or not current_block:
                if current_block:
                    md_lines.append(f"**[{format_time(current_time)}]** {' '.join(current_block)}")
                current_block = [text]
                current_time = entry['start']
            else:
                current_block.append(text)
                
        # Add the last block
        if current_block:
            md_lines.append(f"**[{format_time(current_time)}]** {' '.join(current_block)}")
            
        return "\n\n".join(md_lines)
        
    except Exception as e:
        print(f"❌ 获取字幕失败: {str(e)}")
        return None

def save_to_raw(video_id, title, content, original_url):
    """Save content to raw/youtube directory."""
    RAW_YOUTUBE_DIR.mkdir(exist_ok=True)
    
    # Clean title for filename
    clean_title = re.sub(r'[\/*?:"<>|]', "", title)
    filename = f"{clean_title}.md"
    filepath = RAW_YOUTUBE_DIR / filename
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    frontmatter = f"""---
type: source
title: "{title}"
url: "{original_url}"
date: {date_str}
format: [video]
status: pending
---

# {title}

"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)
        
    return filepath

def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube video transcript")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--title", "-t", help="Title for the document (default: video ID)")
    
    args = parser.parse_args()
    
    video_id = extract_video_id(args.url)
    print(f"📌 解析到 Video ID: {video_id}")
    
    title = args.title if args.title else f"YouTube_{video_id}"
    
    content = fetch_transcript(video_id)
    
    if content:
        filepath = save_to_raw(video_id, title, content, args.url)
        print(f"\n✅ 成功！文件已保存至: {filepath}")
        print("\n提示: 稍后你可以使用 'ingest' 命令将这个原始文件归档到知识库。")
    else:
        print("\n💡 建议使用备用方案 (yt-dlp):")
        print(f"yt-dlp --write-sub --write-auto-sub --sub-lang zh-Hans,en --skip-download {args.url}")

if __name__ == "__main__":
    main()
