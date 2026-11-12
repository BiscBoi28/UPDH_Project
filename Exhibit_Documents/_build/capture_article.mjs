// Capture a live news article as a clean image: loads the page in headless Chrome,
// removes site chrome (menus, ads, cookie banners, related links) and screenshots
// only the article element.
// Usage: node capture_article.mjs <url> <out.png> [articleSelector] [extraRemoveSelectors]
import { spawn } from "node:child_process";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const [url, out, artSel = "", extraRemove = ""] = process.argv.slice(2);
const port = 9300 + Math.floor(Math.random() * 500);
const prof = mkdtempSync(join(tmpdir(), "cap-"));
const chrome = spawn("google-chrome", ["--headless=new", "--no-sandbox", `--remote-debugging-port=${port}`,
  `--user-data-dir=${prof}`, "--window-size=1100,1400", "--hide-scrollbars", "--disable-gpu",
  "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
  "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let ver;
for (let i = 0; i < 50 && !ver; i++) { try { ver = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json(); } catch { await sleep(200); } }
const tabs = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
const ws = new WebSocket(tabs.find((t) => t.type === "page").webSocketDebuggerUrl);
await new Promise((r) => (ws.onopen = r));
let id = 0; const pend = new Map();
ws.onmessage = (m) => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); } };
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });

await send("Page.enable");
await send("Emulation.setDeviceMetricsOverride", { width: 1100, height: 1400, deviceScaleFactor: 2, mobile: false });
await send("Page.navigate", { url });
await sleep(12000);
// scroll through to trigger lazy-loaded images
await send("Runtime.evaluate", { expression: "(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,250));}scrollTo(0,0);})()", awaitPromise: true });
await sleep(2500);
const js = `(() => {
  const pick = () => {
    const h1 = document.querySelector('h1'); if (!h1) return null;
    const total = [...document.querySelectorAll('p')].filter(p => p.innerText.trim().length > 80).length;
    let e = h1;
    while (e.parentElement) { e = e.parentElement; const k = [...e.querySelectorAll('p')].filter(p => p.innerText.trim().length > 80).length; if (k >= Math.max(3, total * 0.6)) return e; }
    return null; };
  const art = ${artSel ? `document.querySelector(${JSON.stringify(artSel)})` : "null"} || pick() || document.querySelector('main') || document.body;
  // outside the article: hide everything that is not an ancestor of it
  let n = art; while (n && n.parentElement) { [...n.parentElement.children].forEach(c => { if (c !== n) c.style.display = 'none'; }); n = n.parentElement; }
  // inside the article: remove only obvious clutter
  const inner = ['iframe','[class*="advert" i]','[id*="google_ads" i]','[class*="newsletter" i]','[class*="taboola" i]','[class*="outbrain" i]','[class*="related" i]','[class*="more-on" i]','[class*="recirc" i]','[aria-label*="advert" i]'${extraRemove ? "," + extraRemove.split("|").map((s) => JSON.stringify(s)).join(",") : ""}];
  inner.forEach(s => art.querySelectorAll(s).forEach(e => e.remove()));
  // promo boxes, found by their wording: remove the largest enclosing block that is still small
  const phrases = ['Advertisement','Get instant alerts','Add Al Jazeera on Google','STARPICKS','Already a subscriber','Follow us on our official',
    'IS THIS ARTICLE USEFUL','REPORT A MISTAKE','Keep up with','Sign up','Subscribe'];
  const walker = document.createTreeWalker(art, NodeFilter.SHOW_TEXT);
  const hits = []; while (walker.nextNode()) { const t = walker.currentNode.textContent.trim(); if (phrases.some(p => t.toLowerCase().startsWith(p.toLowerCase()))) hits.push(walker.currentNode.parentElement); }
  hits.forEach(el => { let b = el; while (b.parentElement && b.parentElement !== art && b.parentElement.innerText.length < 700 && !b.parentElement.querySelector('h1')) b = b.parentElement; if (art.contains(b) && b !== art) b.remove(); });
  // empty boxes (ad slots): no text, no images, but taking up space
  [...art.querySelectorAll('div,section,aside,figure')].reverse().forEach(e => { if (!e.innerText.trim() && !e.querySelector('img,picture,svg,video') && e.getBoundingClientRect().height > 40) e.remove(); });
  document.querySelectorAll('*').forEach(e => { const cs = getComputedStyle(e); if ((cs.position === 'fixed' || cs.position === 'sticky') && !e.contains(art)) e.style.display='none'; });
  document.documentElement.style.overflow = 'visible'; document.body.style.overflow = 'visible';
  window.scrollTo(0, 0);
  const r = art.getBoundingClientRect();
  return JSON.stringify({ x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height, title: document.title });
})()`;
const res = await send("Runtime.evaluate", { expression: js, returnByValue: true });
const box = JSON.parse(res.result.result.value);
console.log(JSON.stringify(box));
await sleep(1500);
const shot = await send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true,
  clip: { x: box.x, y: box.y, width: box.w, height: Math.min(box.h, 12000), scale: 1 } });
writeFileSync(out, Buffer.from(shot.result.data, "base64"));
ws.close(); chrome.kill();
process.exit(0);
