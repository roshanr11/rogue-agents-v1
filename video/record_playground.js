// Records the playground replaying the fake-name demo conversation, for the demo video.
//   node video/record_playground.js        -> video/build/playground.webm
// Steps through by hand, pausing on each verdict so it's readable in the video.
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');

(async () => {
  const root = path.resolve(__dirname, '..');
  const out = path.join(root, 'video', 'build');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const W = 1280, H = 720;
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, recordVideo: { dir: out, size: { width: W, height: H } } });
  const page = await ctx.newPage();
  const t0 = Date.now();
  await page.goto('file://' + path.join(root, 'playground', 'index.html'));
  await page.addStyleTag({ content: 'header{padding-top:10px} .sub{display:none} .feed{max-height:330px}' });
  await page.selectOption('#speed', '0.55');
  await page.evaluate(() => document.activeElement.blur());
  const glide = (sel, block) => page.evaluate(([s, b]) => document.querySelector(s).scrollIntoView({ behavior: 'smooth', block: b }), [sel, block]);
  const key = () => page.keyboard.press('ArrowRight');   // keyboard step: clicking the button would scroll back to it
  const step = async (wait) => { await key(); await page.waitForTimeout(wait); };
  await page.waitForTimeout(600);
  const marks = {};
  // founder + messages
  const nMsgs = await page.evaluate(() => window.SIM_EPISODES.filter(e => e.variant === 'A3').find(e => e.launched && e.actions.length && e.watchdogs.basic.false_quarantines > 0 && e.watchdogs.investigator.rogue_caught).msgs.length);
  for (let i = 0; i <= nMsgs; i++) await step(i === 0 ? 900 : 1100);
  // outreach's email reaches the checkpoint
  marks.checkpoint = Date.now() - t0;
  await key(); await page.waitForTimeout(500);
  await glide('#checkpoint', 'start'); await page.waitForTimeout(2600);
  // end-of-day review
  await key(); await page.waitForTimeout(300);
  await glide('#checkpoint .action:nth-of-type(2)', 'start'); await page.waitForTimeout(2600);
  // results table
  await key(); await page.waitForTimeout(300);
  await glide('#checkpoint table', 'center'); await page.waitForTimeout(2200);
  const total = Date.now() - t0;
  const video = page.video();
  await ctx.close();
  fs.renameSync(await video.path(), path.join(out, 'playground.webm'));
  fs.writeFileSync(path.join(out, 'playground.json'), JSON.stringify({ start_s: 0.5, total_s: total / 1000, marks }));
  console.log('recorded', (total / 1000).toFixed(1), 's');
  await browser.close();
})();
