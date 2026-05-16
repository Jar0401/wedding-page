const { chromium } = require('playwright');

(async () => {
  const url = process.argv[2] || 'file:///E:/Desktop/claude/%E6%88%91%E4%BB%AC%E7%9A%84%E6%95%85%E4%BA%8B/love-memories.html';
  const output = process.argv[3] || 'preview.png';

  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1280, height: 800 }
  });

  await page.goto(url, { waitUntil: 'networkidle' });
  await page.screenshot({ path: output, fullPage: true });

  await browser.close();
  console.log(`截图已保存: ${output}`);
})();
