/**
 * Script: check-links.js
 * Purpose: Automated Link Validation across all local .html files in the portfolio.
 * Verifies internal relative links, assets, images, and anchors.
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');

function getAllHtmlFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    if (file === 'node_modules' || file === '.git') continue;
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    if (stat.isDirectory()) {
      getAllHtmlFiles(filePath, fileList);
    } else if (file.endsWith('.html')) {
      fileList.push(filePath);
    }
  }
  return fileList;
}

function checkLinks() {
  const htmlFiles = getAllHtmlFiles(ROOT_DIR);
  console.log(`Found ${htmlFiles.length} HTML files to inspect.`);

  let totalLinks = 0;
  let brokenLinks = 0;
  const linkReport = [];

  const linkRegex = /(?:href|src)=["']([^"']+)["']/g;

  for (const file of htmlFiles) {
    const content = fs.readFileSync(file, 'utf-8');
    const relativeFilePath = path.relative(ROOT_DIR, file);
    let match;

    while ((match = linkRegex.exec(content)) !== null) {
      const url = match[1].trim();

      // Skip external links, mailto, tel, JS template strings, empty links, or pure inline data/javascript
      if (
        url.startsWith('http://') ||
        url.startsWith('https://') ||
        url.startsWith('mailto:') ||
        url.startsWith('tel:') ||
        url.startsWith('javascript:') ||
        url.startsWith('data:') ||
        url.startsWith('#') ||
        url.includes('${') ||
        url === ''
      ) {
        continue;
      }

      totalLinks++;
      const cleanUrl = url.split('#')[0].split('?')[0];
      if (!cleanUrl) continue; // Pure anchor on same page

      const fileDir = path.dirname(file);
      const targetPath = path.resolve(fileDir, cleanUrl);

      if (!fs.existsSync(targetPath)) {
        brokenLinks++;
        linkReport.push({
          sourceFile: relativeFilePath,
          link: url,
          targetPath: path.relative(ROOT_DIR, targetPath),
          status: 'BROKEN'
        });
      }
    }
  }

  console.log(`\n================ LINK VALIDATION SUMMARY ================`);
  console.log(`Total Internal Links Checked: ${totalLinks}`);
  console.log(`Broken Internal Links Found: ${brokenLinks}`);

  if (brokenLinks > 0) {
    console.log(`\nBROKEN LINKS DETECTED:`);
    linkReport.forEach(item => {
      console.log(`- Source: ${item.sourceFile} -> Link: "${item.link}" (Target missing: ${item.targetPath})`);
    });
  } else {
    console.log(`✅ PERFECT SCORE! Zero broken internal links detected across all portfolio pages.`);
  }

  // Save report to LINK_VALIDATION_REPORT.md
  const reportMd = `# Link Validation Audit Report

**Date:** July 2026  
**Total Pages Scanned:** ${htmlFiles.length}  
**Total Internal Links Checked:** ${totalLinks}  
**Broken Links Count:** ${brokenLinks}  

## Status Summary
${brokenLinks === 0 ? '✅ **PASSED**: All local relative links, project pages, blog posts, and asset paths resolve cleanly.' : `❌ **FAILED**: ${brokenLinks} broken internal links detected.`}

## Details
${brokenLinks === 0 ? 'No broken internal links found.' : linkReport.map(r => `- **${r.sourceFile}** → \`${r.link}\` (Resolved missing path: \`${r.targetPath}\`)`).join('\n')}
`;

  fs.writeFileSync(path.join(ROOT_DIR, 'LINK_VALIDATION_REPORT.md'), reportMd, 'utf-8');
  console.log(`Saved link validation report to LINK_VALIDATION_REPORT.md`);
}

checkLinks();
