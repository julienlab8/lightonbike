// Exporte les PNG du logo (fond transparent) depuis les SVG, avec Chromium.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const dir = path.join(__dirname, '..', 'livrables', 'logo');
(async () => {
  const b = await chromium.launch();
  for (const name of ['light-on-bike-blanc-orange', 'light-on-bike-noir-orange']) {
    const svg = fs.readFileSync(path.join(dir, name + '.svg'), 'utf8');
    for (const w of [2000, 800]) {
      const h = Math.round(w * 940 / 1670);
      const p = await b.newPage({ viewport: { width: w, height: h } });
      await p.setContent('<style>html,body{margin:0;background:transparent}svg{display:block;width:' + w + 'px;height:' + h + 'px}</style>' + svg);
      await p.screenshot({ path: path.join(dir, name + '-' + w + 'px.png'), omitBackground: true });
      await p.close();
    }
  }
  await b.close();
})();
