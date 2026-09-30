// Render the BPMN with bpmn-js in headless Chromium; add accountability and KPI overlays; save full PNG + SVG.
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

(async () => {
  const xml = fs.readFileSync('bouchara_main_process.bpmn', 'utf8');
  const meta = JSON.parse(fs.readFileSync('metah.json', 'utf8'));
  const lib = fs.readFileSync(path.join(__dirname, 'node_modules/bpmn-js/dist/bpmn-viewer.development.js'), 'utf8');
  const css1 = fs.readFileSync(path.join(__dirname, 'node_modules/bpmn-js/dist/assets/diagram-js.css'), 'utf8');
  const css2 = fs.readFileSync(path.join(__dirname, 'node_modules/bpmn-js/dist/assets/bpmn-js.css'), 'utf8');
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage({ viewport: { width: meta.width + 40, height: meta.height + 40 }, deviceScaleFactor: 4 });
  await page.setContent(`<html><head><style>${css1}${css2}
    html,body{margin:0;background:#fff;font-family:Arial,Helvetica,sans-serif}
    #c{width:${meta.width + 20}px;height:${meta.height + 20}px}
    .djs-label{paint-order:stroke;stroke:#fff;stroke-width:3px;stroke-linejoin:round}
    .kpi{background:#2b5aa6;color:#fff;font:bold 10px Arial;padding:1px 4px;border-radius:7px;white-space:nowrap}
    .qc{background:#d9822b;color:#fff;font:bold 10px Arial;padding:1px 4px;border-radius:7px}
    .acc{background:#fff;width:${140 - 4}px;height:26px;font:11px Arial;color:#333;text-align:center;line-height:12px}
    .acc b{font-size:12px;color:#000}
    .gl{font:10.5px Arial;line-height:11.5px;color:#111;text-shadow:0 0 2px #fff,0 0 2px #fff,0 0 3px #fff}
    .accv{transform-origin:top left;height:30px;background:#fff;font:10px Arial;line-height:12px;text-align:center;color:#333;padding-top:3px;box-sizing:border-box}.accv b{font-size:11px;color:#000}
    .bbh{background:#fff;width:${meta.bbw}px;font:bold 12px Arial;text-align:center;color:#000}
  </style></head><body><div id="c"></div><script>${lib}</script></body></html>`);
  const res = await page.evaluate(async ({ xml, meta }) => {
    const viewer = new BpmnJS({ container: '#c', textRenderer: { defaultStyle: { fontSize: 12.5, fontFamily: 'Arial', lineHeight: 1.15 }, externalStyle: { fontSize: 11, fontFamily: 'Arial', lineHeight: 1.1 } } });
    const r = await viewer.importXML(xml);
    const canvas = viewer.get('canvas');
    canvas.viewbox({ x: 0, y: 0, width: meta.width + 20, height: meta.height + 20 });
    const ov = viewer.get('overlays');
    const reg = viewer.get('elementRegistry');
    // colour black boxes and QC tasks
    const gfx = (id) => reg.getGraphics(id);
    ['P_bazar','P_ai','P_pay','P_supp','P_manu','P_deliv','P_inst'].forEach(id => {
      const rect = gfx(id).querySelector('.djs-visual rect'); rect.style.fill = '#3a3a3a'; rect.style.stroke = '#000';
      gfx(id).querySelectorAll('.djs-visual text').forEach(t => { t.style.fill = '#fff'; t.style.stroke = 'none'; t.style.fontWeight = 'bold'; t.style.fontSize = '11px'; });
    });
    meta.qc.forEach(id => { const rect = gfx(id).querySelector('.djs-visual rect'); rect.style.fill = '#fdf0e2'; rect.style.stroke = '#d9822b'; });
    ['P_customer'].forEach(id => { const rect = gfx(id).querySelector('.djs-visual rect'); rect.style.fill = '#f4f8fd'; });
    for (const [id, k] of Object.entries(meta.kpi)) {
      const isG = meta.lbl[id] && meta.lbl[id][1] === 'xor';
      ov.add(id, { position: isG ? { bottom: 2, left: -24 } : { top: -8, left: 4 }, html: `<div class="kpi">${k}</div>` });
    }
    reg.filter(e => e.type === 'label' && e.labelTarget && !e.labelTarget.waypoints).forEach(e => { reg.getGraphics(e).style.display = 'none'; });
    const down = ['c_g1', 'b_gp'];
    for (const [id, [name, kind]] of Object.entries(meta.lbl)) {
      let pos, w = 74, al = 'center';
      if (kind === 'xor' || kind === 'and') pos = down.includes(id) ? { top: 42, left: -17 } : { top: -26, left: -17 };
      else if (kind === 'linkthrow' || kind === 'linkcatch') { continue; }
      else if (kind === 'timer') { pos = { top: 30, left: -10 }; w = 60; al = 'left'; }
      else pos = { top: 32, left: -22 };
      ov.add(id, { position: pos, html: `<div class="gl" style="width:${w}px;text-align:${al}">${name}</div>` });
    }
    // link event letters
    ['c_linkC','c_linkC2','b_linkA','b_linkA2'].forEach(id => ov.add(id, { position: { top: -15, left: 10 }, html: `<div class="gl" style="font-weight:bold">${meta.lbl[id][0]}</div>` }));
    meta.qc.forEach(id => ov.add(id, { position: { bottom: -6, left: 4 }, html: `<div class="qc">Check</div>` }));
    const names = { Lane_PLAT: ['Digital platform', 'A: Pilot lead'], Lane_ADV: ['Store advisers', 'A: Store manager'], Lane_SC: ['Supply chain', 'A: Supply chain mgr'], Lane_CS: ['Customer service', 'A: CS manager'] };
    for (const [id, [nm, acc]] of Object.entries(names)) {
      gfx(id).querySelectorAll('.djs-visual text').forEach(t => t.style.display = 'none');
      const hh = meta.lanes[id.replace('Lane_', '')][1];
      ov.add(id, { position: { top: 0, left: 0 }, html: `<div class="accv" style="width:${hh}px;transform:translateY(${hh}px) rotate(-90deg)"><b>${nm}</b><br>${acc}</div>` });
    }
    return { warnings: r.warnings.map(w => w.message) };
  }, { xml, meta });
  console.log('warnings', JSON.stringify(res.warnings));
  await page.waitForTimeout(300);
  // add header over the black-box column
  await page.evaluate((meta) => {
    const d = document.createElement('div');
    d.style.cssText = `position:absolute;left:12px;top:${meta.bby + meta.bbh}px;width:${meta.bbh}px;height:56px;transform-origin:top left;transform:rotate(-90deg);font:bold 10px Arial;line-height:12px;text-align:center`;
    d.innerHTML = 'Third<br>parties';
    document.body.appendChild(d);
  }, meta);
  const rects = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('.djs-shape, .djs-overlay').forEach(el => {
      if (el.closest('[data-element-id^="Lane_"]') || el.getAttribute('data-element-id') === 'P_customer' || el.getAttribute('data-element-id') === 'P_bouchara') return;
      const r = el.getBoundingClientRect(); if (r.height > 0 && r.height < 200) out.push([r.top, r.bottom]);
    });
    return out;
  });
  require('fs').writeFileSync('rects.json', JSON.stringify(rects));
  await page.screenshot({ path: 'fullh.png', clip: { x: 0, y: 0, width: meta.width + 10, height: meta.height + 5 } });
  await browser.close();
})();
