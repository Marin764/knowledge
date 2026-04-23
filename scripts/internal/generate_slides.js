const fs = require('fs');
const path = require('path');

const WIKI_DIR = path.join(__dirname, '../wiki');
const EXPORTS_DIR = path.join(__dirname, '../exports');

const TEMPLATE = `---
marp: true
theme: default
paginate: true
backgroundColor: #fff
color: #333
style: |
  section {
    font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
  }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# {{TITLE}}

{{SUBTITLE}}

---

<!-- _header: 目录 -->

## 目录

{{TOC}}

---

{{CONTENT}}

---

<!-- _class: lead -->

# 谢谢

<!-- _footer: 由 Claude Code 生成 | {date} -->
`;

function parseFrontmatter(content) {
  if (!content.startsWith('---')) return { frontmatter: null, body: content };
  
  const parts = content.split('---');
  if (parts.length < 3) return { frontmatter: null, body: content };
  
  const fmText = parts[1];
  const body = parts.slice(2).join('---');
  const frontmatter = {};
  
  const lines = fmText.split('\n');
  for (const line of lines) {
    const colonIdx = line.indexOf(':');
    if (colonIdx > 0) {
      const key = line.slice(0, colonIdx).trim();
      let value = line.slice(colonIdx + 1).trim();
      if (value.startsWith('[') && value.endsWith(']')) {
        value = value.slice(1, -1).split(',').map(v => v.trim());
      }
      frontmatter[key] = value;
    }
  }
  
  return { frontmatter, body };
}

function extractBodySections(content) {
  const sections = [];
  const lines = content.split('\n');
  let currentSection = null;
  let currentContent = [];

  for (const line of lines) {
    if (line.startsWith('## ')) {
      if (currentSection) {
        sections.push({ title: currentSection, content: currentContent.join('\n').trim() });
      }
      currentSection = line.slice(3).trim();
      currentContent = [];
    } else {
      currentContent.push(line);
    }
  }
  if (currentSection) {
    sections.push({ title: currentSection, content: currentContent.join('\n').trim() });
  }
  return sections;
}

function mdToMarp(mdPath, outputPath) {
  try {
    const content = fs.readFileSync(mdPath, 'utf8');
    const { frontmatter, body } = parseFrontmatter(content);
    
    if (!frontmatter || !frontmatter.title) {
      console.log(`⚠️  Skipped: ${mdPath} (no frontmatter)`);
      return false;
    }

    const sections = extractBodySections(body);
    const tocItems = sections.map(s => `- ${s.title}`).join('\n');
    const contentSlides = sections
      .filter(s => s.title && s.content)
      .map(s => `## ${s.title}\n\n${s.content}`)
      .join('\n\n---\n\n');

    let slide = TEMPLATE.replace('{{TITLE}}', frontmatter.title);
    slide = slide.replace('{{SUBTITLE}}', frontmatter.definition || '');
    slide = slide.replace('{{TOC}}', tocItems || '- (内容为空)');
    slide = slide.replace('{{CONTENT}}', contentSlides || '## 内容\n\n(无内容)');
    slide = slide.replace('{date}', new Date().toISOString().split('T')[0]);

    if (!fs.existsSync(EXPORTS_DIR)) fs.mkdirSync(EXPORTS_DIR, { recursive: true });
    fs.writeFileSync(outputPath, slide, 'utf8');
    console.log(`✅ Generated: ${outputPath}`);
    return true;
  } catch (err) {
    console.log(`❌ Error: ${mdPath}`, err.message);
    return false;
  }
}

function main() {
  const args = process.argv.slice(2);
  
  if (!fs.existsSync(EXPORTS_DIR)) fs.mkdirSync(EXPORTS_DIR, { recursive: true });

  if (args.includes('--all') || args.includes('-a')) {
    // Generate for all concepts
    const conceptsDir = path.join(WIKI_DIR, 'concepts');
    if (fs.existsSync(conceptsDir)) {
      fs.readdirSync(conceptsDir).filter(f => f.endsWith('.md')).forEach(file => {
        const outputName = `concept-${path.basename(file, '.md')}.md`;
        mdToMarp(path.join(conceptsDir, file), path.join(EXPORTS_DIR, outputName));
      });
    }
    return;
  }

  const fileArg = args.find(a => a.startsWith('-f=')) || args[args.indexOf('-f') + 1];
  if (fileArg) {
    mdToMarp(fileArg, path.join(EXPORTS_DIR, path.basename(fileArg)));
    return;
  }

  const topicArg = args.find(a => a.startsWith('-t=')) || args[args.indexOf('-t') + 1];
  if (topicArg) {
    const outputFile = path.join(EXPORTS_DIR, `${topicArg.replace(/\s+/g, '-')}.md`);
    let slide = TEMPLATE.replace('{{TITLE}}', topicArg);
    slide = slide.replace('{{SUBTITLE}}', `基于知识库生成 | ${new Date().toISOString().split('T')[0]}`);
    slide = slide.replace('{{TOC}}', '- (请指定具体页面)');
    slide = slide.replace('{{CONTENT}}', '## 示例页面\n\n这是基于 Wiki 内容生成的幻灯片演示。');
    slide = slide.replace('{date}', new Date().toISOString().split('T')[0]);
    fs.writeFileSync(outputFile, slide, 'utf8');
    console.log(`✅ Generated presentation: ${outputFile}`);
    return;
  }

  // Show help
  console.log('📚 知识库幻灯片生成工具\n');
  console.log('用法:');
  console.log('  node generate_slides.js --all          # 为所有概念生成幻灯片');
  console.log('  node generate_slides.js -f path/to/wiki.md  # 生成单个页面');
  console.log('  node generate_slides.js -t "游戏交互设计" # 创建空白模板\n');
  console.log('📁 现有概念页面:');
  const conceptsDir = path.join(WIKI_DIR, 'concepts');
  if (fs.existsSync(conceptsDir)) {
    fs.readdirSync(conceptsDir).filter(f => f.endsWith('.md')).forEach(f => {
      console.log(`  - ${f.replace('.md', '')}`);
    });
  }
}

main();
