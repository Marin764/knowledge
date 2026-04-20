const fs = require('fs');
const path = require('path');

const WIKI_DIR = path.join(__dirname, '../wiki');

const REQUIRED_FRONTMATTER = {
  game: ['type', 'title', 'status'],
  concept: ['type', 'title', 'status'],
  mechanics: ['type', 'title', 'status'],
  source: ['type', 'title', 'status']
};

function getAllMdFiles(dir, fileList = []) {
  if (!fs.existsSync(dir)) return fileList;
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const filePath = path.join(dir, file);
    if (fs.statSync(filePath).isDirectory()) {
      getAllMdFiles(filePath, fileList);
    } else if (file.endsWith('.md')) {
      fileList.push(filePath);
    }
  }
  return fileList;
}

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
      // Simple parse for array-like values
      if (value.startsWith('[') && value.endsWith(']')) {
        value = value.slice(1, -1).split(',').map(v => v.trim());
      }
      frontmatter[key] = value;
    }
  }
  
  return { frontmatter, body };
}

function extractWikilinks(content) {
  const links = [];
  const regex = /\[\[(.*?)\]\]/g;
  let match;
  while ((match = regex.exec(content)) !== null) {
    const link = match[1].split('|')[0].trim();
    links.push(link);
  }
  return links;
}

function lint() {
  const files = getAllMdFiles(WIKI_DIR);
  
  // Create relative posix paths for easier comparison
  const filePaths = files.map(f => {
    const rel = path.relative(path.join(__dirname, '..'), f);
    return rel.split(path.sep).join('/');
  });
  
  const fileSet = new Set(filePaths);
  
  const errors = {
    frontmatter_missing: [],
    frontmatter_invalid: [],
    dead_links: [],
    isolated_pages: [],
    stubs: []
  };

  const incomingLinks = {};
  for (const p of filePaths) incomingLinks[p] = 0;
  
  // Exceptions
  incomingLinks['wiki/index.md'] = 1;
  incomingLinks['wiki/log.md'] = 1;

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const pathStr = filePaths[i];
    const content = fs.readFileSync(file, 'utf8');
    
    const { frontmatter, body } = parseFrontmatter(content);
    
    // 1. Frontmatter checks
    if (!['wiki/index.md', 'wiki/log.md'].includes(pathStr)) {
      if (!frontmatter || Object.keys(frontmatter).length === 0) {
        errors.frontmatter_missing.push(pathStr);
      } else {
        const type = frontmatter.type;
        if (!type || !REQUIRED_FRONTMATTER[type]) {
          errors.frontmatter_invalid.push(`${pathStr} (Invalid or missing type: ${type})`);
        } else {
          const missingFields = REQUIRED_FRONTMATTER[type].filter(f => !frontmatter[f]);
          if (missingFields.length > 0) {
            errors.frontmatter_invalid.push(`${pathStr} (Missing: ${missingFields.join(', ')})`);
          }
        }
      }
    }
    
    // 2. Stub checks
    if (!pathStr.startsWith('wiki/source/') && !['wiki/index.md', 'wiki/log.md'].includes(pathStr)) {
      // Very simple word count
      const words = body.replace(/[\n\r]/g, ' ').split(' ').filter(w => w.trim().length > 0);
      if (words.length < 20) {
        errors.stubs.push(`${pathStr} (${words.length} words)`);
      }
    }
    
    // 3. Dead links check
    const links = extractWikilinks(content);
    for (const link of links) {
      const target = link.endsWith('.md') ? link : `${link}.md`;
      
      // Target could be "wiki/games/xxx.md" or "games/xxx.md" or just "xxx.md"
      let found = false;
      let matchedPath = '';
      
      if (fileSet.has(target)) {
        found = true;
        matchedPath = target;
      } else if (fileSet.has(`wiki/${target}`)) {
        found = true;
        matchedPath = `wiki/${target}`;
      } else {
        // Try to find it anywhere
        const basename = path.basename(target);
        for (const p of filePaths) {
          if (path.basename(p) === basename) {
            found = true;
            matchedPath = p;
            break;
          }
        }
      }
      
      if (found) {
        if (incomingLinks[matchedPath] !== undefined) {
          incomingLinks[matchedPath]++;
        }
      } else {
        errors.dead_links.push(`${pathStr} -> ${target}`);
      }
    }
  }
  
  // 4. Isolated pages
  for (const [p, count] of Object.entries(incomingLinks)) {
    if (count === 0 && !['wiki/index.md', 'wiki/log.md'].includes(p)) {
      errors.isolated_pages.push(p);
    }
  }
  
  // Print Report
  console.log('\n' + '='.repeat(50));
  console.log('🧠 WIKI LINT REPORT');
  console.log('='.repeat(50));
  
  const totalErrors = Object.values(errors).reduce((sum, arr) => sum + arr.length, 0);
  
  if (totalErrors === 0) {
    console.log('✅ All checks passed! The wiki is healthy.');
    process.exit(0);
  }
  
  for (const [category, items] of Object.entries(errors)) {
    if (items.length > 0) {
      console.log(`\n❌ ${category.toUpperCase().replace('_', ' ')} (${items.length}):`);
      for (const item of items) {
        console.log(`  - ${item}`);
      }
    }
  }
  
  console.log('\n' + '='.repeat(50));
  process.exit(1);
}

lint();
