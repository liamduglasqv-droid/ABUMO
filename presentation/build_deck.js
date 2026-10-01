// Novaris AI Portal — stakeholder analysis deck
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");
const { applyTheme } = require(process.env.SKILL_DIR + "/scripts/apply_theme.js");

const OUT = process.argv[2] || "deck.pptx";

const THEME = {
  name: "Novaris",
  headFontFace: "Arial",
  bodyFontFace: "Arial",
  colors: {
    dk1: "1A1A1A", lt1: "FFFFFF", dk2: "5F5F5F", lt2: "EFEFEF",
    accent1: "D7263D", // brand red (template arrows) + "against"
    accent2: "2E9E5B", // green = for
    accent3: "9A9A9A", // grey = torn / neutral
    accent4: "C9C9C9", // faded
    accent5: "FBE4E7", // red tint (FOCUS quadrant)
    accent6: "E6F4EC", // green tint
    hlink: "D7263D", folHlink: "8E1A2A",
  },
};
const HEX = THEME.colors;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Novaris AI Portal — Stakeholder analysis";
pres.author = "Anna Li";
const C = pres.SchemeColor;

// ---------- icons ----------
async function icon(Comp, color, size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + color, size: String(size) }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// ---------- layouts ----------
const W = 13.333, H = 7.5;
pres.defineSlideMaster({
  title: "TITLE_DARK",
  background: { color: HEX.dk1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.3, w: 11.5, h: 1.9, fontSize: 40, bold: true, color: C.background1, valign: "bottom", align: "left", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.45, w: 11.5, h: 1.2, fontSize: 18, color: C.accent4, valign: "top", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: HEX.lt1 },
  objects: [
    { placeholder: { options: { name: "tag", type: "body", x: 0.6, y: 0.3, w: 8, h: 0.3, fontSize: 11, bold: true, color: C.accent1, charSpacing: 2, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.6, w: 12.1, h: 0.8, fontSize: 26, bold: true, color: C.text1, valign: "top", align: "left", margin: 0 }, text: "" } },
    { text: { text: "Novaris AI Portal  ·  Stakeholder analysis  ·  Anna Li", options: { x: 0.6, y: 7.08, w: 7, h: 0.25, fontSize: 9, color: C.accent3, margin: 0 } } },
  ],
  slideNumber: { x: 12.3, y: 7.08, w: 0.45, h: 0.25, fontSize: 9, color: C.accent3, align: "right" },
});

const SEC = ["1 · Context & axes", "2 · The map", "3 · Moving the critical few", "Backup"];
const TAG = ["01  CONTEXT & AXES", "02  THE MAP", "03  MOVING THE CRITICAL FEW", "BACKUP"];
SEC.forEach((s) => {}); // sections added before first slide of each

function content(sec, title) {
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: SEC[sec] });
  s.addText(TAG[sec], { placeholder: "tag" });
  s.addText(title, { placeholder: "title" });
  return s;
}

// ---------- map ----------
// r = readiness 0-10 (x), e = adaptation effort 0-10 (y)
const SH = {
  elodie:   { name: "Élodie Martin", sub: "Academic Dean", r: 3.3, e: 8.1, lab: "b" },
  faculty:  { name: "Restrictive faculty", sub: "& programme directors", r: 1.25, e: 6.9, lab: "b" },
  laura:    { name: "Laura Bianchi", sub: "People & Faculty", r: 3.6, e: 6.4, lab: "b" },
  aisha:    { name: "Aisha Khan", sub: "CIO", r: 6.4, e: 8.0, lab: "b" },
  rafael:   { name: "Rafael Mendes", sub: "Intl. campuses", r: 8.7, e: 7.6, lab: "b" },
  legal:    { name: "Legal / DPO", sub: "", r: 6.6, e: 6.2, lab: "b" },
  library:  { name: "Library", sub: "", r: 8.7, e: 5.9, lab: "b" },
  profai:   { name: "Pro-AI faculty", sub: "", r: 6.3, e: 4.3, lab: "b" },
  marc:     { name: "Marc Lefèvre", sub: "Sponsor", r: 8.6, e: 4.3, lab: "b" },
  tio:      { name: "Transformation Office", sub: "", r: 6.3, e: 2.6, lab: "b" },
  claire:   { name: "Claire Moreau", sub: "President & Dean", r: 8.1, e: 2.9, lab: "b" },
  students: { name: "Students", sub: "", r: 9.5, e: 1.6, lab: "l" },
  sophie:   { name: "Sophie Bernard", sub: "CFO", r: 3.7, e: 2.8, lab: "b" },
  board:    { name: "Board of Governors", sub: "", r: 1.5, e: 2.6, lab: "b" },
  publish:  { name: "Publishers", sub: "& case providers", r: 1.25, e: 4.3, lab: "b" },
  reps:     { name: "Employee reps", sub: "works council", r: 3.5, e: 4.3, lab: "b" },
  partners: { name: "Corporate partners", sub: "", r: 4.3, e: 1.3, lab: "l" },
};

const MAP = { x: 1.25, y: 1.6, w: 7.5, h: 4.95 };
const P = (r, e, m = MAP) => ({ x: m.x + (r / 10) * m.w, y: m.y + (1 - e / 10) * m.h });

const QUAD = {
  tl: { t: "FOCUS HERE", s: "Must change a lot · not equipped" },
  tr: { t: "EQUIP", s: "Willing · need tools & clarity" },
  bl: { t: "INFORM", s: "Don't invest · don't surprise" },
  br: { t: "ALLIES", s: "Use them to move the focus group" },
};

function drawFrame(s, opt = {}) {
  const m = MAP;
  s.addShape(pres.shapes.RECTANGLE, { x: m.x, y: m.y, w: m.w, h: m.h, fill: { color: C.background2 }, line: { type: "none" }, objectName: "Map panel" });
  if (opt.focusTint !== false)
    s.addShape(pres.shapes.RECTANGLE, { x: m.x, y: m.y, w: m.w / 2, h: m.h / 2, fill: { color: C.accent5 }, line: { type: "none" }, objectName: "Focus quadrant" });
  // dividers
  s.addShape(pres.shapes.LINE, { x: m.x + m.w / 2, y: m.y + 0.2, w: 0, h: m.h - 0.4, line: { color: C.accent4, width: 1 } });
  s.addShape(pres.shapes.LINE, { x: m.x + 0.2, y: m.y + m.h / 2, w: m.w - 0.4, h: 0, line: { color: C.accent4, width: 1 } });
  // quadrant labels in outer corners
  const qw = 2.6, pad = 0.15;
  const ql = (k, x, y, align) => {
    const isFocus = k === "tl";
    s.addText([
      { text: QUAD[k].t, options: { bold: true, fontSize: 12, color: C.text1, breakLine: true } },
      { text: QUAD[k].s, options: { italic: true, fontSize: 10, color: isFocus ? C.accent1 : C.text2 } },
    ], { x, y, w: qw, h: 0.5, align, valign: "top", margin: 0, isTextBox: true, objectName: "Quadrant " + QUAD[k].t });
  };
  ql("tl", m.x + pad, m.y + pad, "left");
  ql("tr", m.x + m.w - pad - qw, m.y + pad, "right");
  ql("bl", m.x + pad, m.y + m.h - pad - 0.5, "left");
  ql("br", m.x + m.w - pad - qw, m.y + m.h - pad - 0.5, "right");

  // red axes like the template
  const ax = m.x - 0.18, ay = m.y + m.h + 0.18;
  s.addShape(pres.shapes.LINE, { x: ax, y: m.y - 0.15, w: 0, h: ay - (m.y - 0.15), line: { color: C.accent1, width: 4, beginArrowType: "triangle" }, objectName: "Y axis" });
  s.addShape(pres.shapes.LINE, { x: ax, y: ay, w: m.x + m.w + 0.2 - ax, h: 0, line: { color: C.accent1, width: 4, endArrowType: "triangle" }, objectName: "X axis" });
  // axis labels
  s.addText("Readiness", { x: m.x + m.w / 2 - 1.5, y: ay + 0.08, w: 3, h: 0.3, align: "center", bold: true, fontSize: 13, color: C.text1, margin: 0, isTextBox: true });
  s.addText("Low", { x: m.x + 0.3, y: ay + 0.08, w: 1, h: 0.3, fontSize: 10, color: C.text2, margin: 0, isTextBox: true });
  s.addText("High", { x: m.x + m.w - 1.3, y: ay + 0.08, w: 1, h: 0.3, align: "right", fontSize: 10, color: C.text2, margin: 0, isTextBox: true });
  s.addText("Adaptation effort", { x: ax - 0.45 - 1.5, y: m.y + m.h / 2 - 0.15, w: 3, h: 0.3, align: "center", bold: true, fontSize: 13, color: C.text1, rotate: 270, margin: 0, isTextBox: true });
  s.addText("Low", { x: ax - 0.45 - 0.5, y: m.y + m.h - 0.6, w: 1, h: 0.3, align: "center", fontSize: 10, color: C.text2, rotate: 270, margin: 0, isTextBox: true });
  s.addText("High", { x: ax - 0.45 - 0.5, y: m.y + 0.3, w: 1, h: 0.3, align: "center", fontSize: 10, color: C.text2, rotate: 270, margin: 0, isTextBox: true });
}

function drawNode(s, key, o = {}) {
  const d = SH[key];
  const p = P(d.r, d.e);
  const rad = o.big ? 0.15 : 0.1;
  s.addShape(pres.shapes.OVAL, {
    x: p.x - rad, y: p.y - rad, w: rad * 2, h: rad * 2,
    fill: { color: o.fill || C.text1 },
    line: o.ring ? { color: C.text1, width: 2.25 } : { type: "none" },
    objectName: "Dot " + d.name,
  });
  const lw = 1.55, lh = d.sub ? 0.42 : 0.24;
  const txtColor = o.textColor || C.text1;
  const runs = [{ text: d.name, options: { bold: true, italic: true, fontSize: 11, color: txtColor, breakLine: !!d.sub } }];
  if (d.sub) runs.push({ text: d.sub, options: { fontSize: 9, color: o.textColor || C.text2 } });
  let box;
  const lab = o.lab || d.lab;
  if (lab === "r") box = { x: p.x + rad + 0.08, y: p.y - lh / 2, w: lw, h: lh, align: "left", valign: "middle" };
  else if (lab === "l") box = { x: p.x - rad - 0.08 - lw, y: p.y - lh / 2, w: lw, h: lh, align: "right", valign: "middle" };
  else box = { x: p.x - lw / 2, y: p.y + rad + 0.03, w: lw, h: lh, align: "center", valign: "top" };
  const opts = { ...box, margin: 0, isTextBox: true, objectName: "Label " + d.name };
  if (o.halo) {
    // tight backdrop so influence lines pass behind the label
    const tw = Math.max(d.name.length * 0.078, d.sub.length * 0.06) + 0.12;
    opts.fill = { color: d.r < 5 && d.e > 5 ? C.accent5 : C.background2 };
    if (lab === "b") opts.x = p.x - tw / 2; else if (lab === "l") opts.x = p.x - rad - 0.08 - tw;
    opts.w = tw;
  }
  s.addText(runs, opts);
  if (o.badge) {
    s.addShape(pres.shapes.OVAL, { x: p.x + rad - 0.02, y: p.y - rad - 0.26, w: 0.28, h: 0.28, fill: { color: C.accent1 }, line: { color: C.background1, width: 1.5 } });
    s.addText(String(o.badge), { x: p.x + rad - 0.02, y: p.y - rad - 0.26, w: 0.28, h: 0.28, fontSize: 10, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true });
  }
}

function drawLink(s, from, to, strength) {
  const a = P(SH[from].r, SH[from].e), b = P(SH[to].r, SH[to].e);
  const dx = b.x - a.x, dy = b.y - a.y, L = Math.hypot(dx, dy);
  const ux = dx / L, uy = dy / L;
  const x1 = a.x + ux * 0.14, y1 = a.y + uy * 0.14;
  const x2 = b.x - ux * 0.2, y2 = b.y - uy * 0.2;
  const width = { 1: 1.25, 2: 2.75, 3: 4.5 }[strength];
  const bx = Math.min(x1, x2), by = Math.min(y1, y2);
  s.addShape(pres.shapes.CUSTOM_GEOMETRY, {
    x: bx, y: by, w: Math.max(Math.abs(x2 - x1), 0.01), h: Math.max(Math.abs(y2 - y1), 0.01),
    points: [{ x: x1 - bx, y: y1 - by, moveTo: true }, { x: x2 - bx, y: y2 - by }],
    fill: { type: "none" },
    line: { color: C.text2, width, endArrowType: "triangle" },
    objectName: `Influence ${SH[from].name} → ${SH[to].name}`,
  });
}

(async () => {
  const ICO = {
    users: await icon(fa.FaUsers, HEX.lt1),
    bolt: await icon(fa.FaBolt, HEX.lt1),
    question: await icon(fa.FaQuestion, HEX.lt1),
    shield: await icon(fa.FaShieldAlt, HEX.accent1),
    grad: await icon(fa.FaGraduationCap, HEX.lt1),
    chalk: await icon(fa.FaChalkboardTeacher, HEX.lt1),
    userShield: await icon(fa.FaUserShield, HEX.lt1),
    times: await icon(fa.FaTimes, HEX.accent1),
    wrench: await icon(fa.FaTools, HEX.dk2),
    arrow: await icon(fa.FaArrowRight, HEX.accent4),
    check: await icon(fa.FaCheck, HEX.accent2),
  };

  // =============== 1. TITLE ===============
  pres.addSection({ title: SEC[0] });
  let s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: SEC[0] });
  s.addText("Who has to change for Novaris to become an AI school?", { placeholder: "title" });
  s.addText("Stakeholder analysis for the student AI portal  ·  Anna Li  ·  SKEMA Project Management", { placeholder: "body" });
  s.addShape(pres.shapes.OVAL, { x: 0.8, y: 1.5, w: 0.55, h: 0.55, fill: { color: C.accent1 }, line: { type: "none" } });
  s.addImage({ data: ICO.grad, x: 0.92, y: 1.62, w: 0.31, h: 0.31 });
  s.addNotes("~10s. Introduce: we are Anna Li's team, stakeholder analysis for the Novaris student AI portal. One question drives the whole talk: who has to change for this transition to go smoothly?");

  // =============== 2. CONTEXT ===============
  s = content(0, "The project isn't a tool — it's a transition that is already happening");
  const cards = [
    { k: "SITUATION", ic: ICO.users, h: "Students already use AI", b: ["Free public tools, paid subscriptions, employer software", "Faculty rules inconsistent: some encourage, some ban", "The school has no visibility on tools or data"] },
    { k: "COMPLICATION", ic: ICO.bolt, h: "It can't be stopped", b: ["Banning it only pushes use out of sight", "The only choice left: adapt in control, or get dragged along"] },
    { k: "KEY QUESTION", ic: ICO.question, h: "Who has to change the way they work — and are they ready?", b: [] },
  ];
  const cw = 3.75, cg = 0.4, cy = 1.75, ch = 3.6;
  cards.forEach((c, i) => {
    const x = 0.6 + i * (cw + cg);
    const last = i === 2;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: cy, w: cw, h: ch, rectRadius: 0.08, fill: { color: last ? C.text1 : C.background2 }, line: { type: "none" }, objectName: "Card " + c.k });
    s.addShape(pres.shapes.OVAL, { x: x + 0.3, y: cy + 0.3, w: 0.6, h: 0.6, fill: { color: C.accent1 }, line: { type: "none" } });
    s.addImage({ data: c.ic, x: x + 0.45, y: cy + 0.45, w: 0.3, h: 0.3 });
    s.addText(c.k, { x: x + 1.05, y: cy + 0.42, w: 2.5, h: 0.35, fontSize: 11, bold: true, charSpacing: 2, color: last ? C.accent4 : C.text2, margin: 0, isTextBox: true });
    s.addText(c.h, { x: x + 0.3, y: cy + 1.1, w: cw - 0.6, h: last ? 1.6 : 0.8, fontSize: last ? 22 : 18, bold: true, color: last ? C.background1 : C.text1, valign: "top", margin: 0, isTextBox: true });
    if (c.b.length)
      s.addText(c.b.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < c.b.length - 1 } })), { x: x + 0.3, y: cy + 1.75, w: cw - 0.6, h: 1.7, fontSize: 13, color: C.text1, paraSpaceAfter: 6, valign: "top", margin: 0, isTextBox: true });
    if (i < 2) s.addImage({ data: ICO.arrow, x: x + cw + 0.08, y: cy + ch / 2 - 0.12, w: 0.24, h: 0.24 });
  });
  s.addShape(pres.shapes.OVAL, { x: 0.6, y: 5.85, w: 0.55, h: 0.55, fill: { color: C.accent5 }, line: { type: "none" } });
  s.addImage({ data: ICO.shield, x: 0.73, y: 5.98, w: 0.29, h: 0.29 });
  s.addText([
    { text: "So the charter promises ", options: { color: C.text1 } },
    { text: "safer, governed, transparent", options: { bold: true, color: C.accent1 } },
    { text: " AI use — not “risk-free”. No platform can guarantee every prompt, answer or output is legal and accurate.", options: { color: C.text1 } },
  ], { x: 1.35, y: 5.75, w: 11.3, h: 0.75, fontSize: 15, valign: "middle", margin: 0, isTextBox: true });
  s.addNotes("~30s. Students already use AI everywhere: public tools, subscriptions, employer software. Faculty rules are inconsistent and the school sees nothing. We cannot stop it — the only variable is whether Novaris adapts in a controlled way or gets dragged along. So the project is managing a transition, not building a tool. That's also why we reframe Marc's promise: safer, governed, transparent — not risk-free. The key question for stakeholder analysis becomes: who has to change, and are they ready?");

  // =============== 3. WHY THESE AXES ===============
  s = content(0, "Why we map effort and readiness, not power and interest");
  const colW = 5.85, colY = 1.7, colH = 4.95;
  // left: traditional
  const lx = 0.6, rx = 0.6 + colW + 0.43;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: lx, y: colY, w: colW, h: colH, rectRadius: 0.08, fill: { color: C.background2 }, line: { type: "none" }, objectName: "Traditional card" });
  s.addText([
    { text: "TRADITIONAL", options: { fontSize: 11, bold: true, charSpacing: 2, color: C.text2, breakLine: true } },
    { text: "Power × Interest", options: { fontSize: 22, bold: true, color: C.accent3 } },
  ], { x: lx + 0.35, y: colY + 0.3, w: colW - 0.7, h: 0.85, margin: 0, isTextBox: true });
  const why = [
    { h: "Power", t: "Nobody has real power over student AI use — students use it anyway, publishers can't switch off public tools." },
    { h: "Interest", t: "Almost nobody asked for this project. Everyone scores near zero, so the axis separates no one." },
  ];
  why.forEach((w, i) => {
    const y = colY + 1.45 + i * 1.6;
    s.addImage({ data: ICO.times, x: lx + 0.35, y: y + 0.05, w: 0.3, h: 0.3 });
    s.addText([
      { text: w.h, options: { bold: true, fontSize: 15, color: C.text1, breakLine: true } },
      { text: w.t, options: { fontSize: 13, color: C.text2 } },
    ], { x: lx + 0.85, y, w: colW - 1.2, h: 1.3, valign: "top", margin: 0, isTextBox: true });
  });
  // right: ours
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: rx, y: colY, w: colW, h: colH, rectRadius: 0.08, fill: { color: C.background1 }, line: { color: C.accent1, width: 2 }, objectName: "Our axes card" });
  s.addText([
    { text: "OURS — BUILT FOR A TRANSITION", options: { fontSize: 11, bold: true, charSpacing: 2, color: C.accent1, breakLine: true } },
    { text: "Adaptation effort × Readiness", options: { fontSize: 22, bold: true, color: C.text1 } },
  ], { x: rx + 0.35, y: colY + 0.3, w: colW - 0.7, h: 0.85, margin: 0, isTextBox: true });
  const ours = [
    { h: "Adaptation effort  (vertical)", t: "How much of their rules, processes or habits must be rewritten." },
    { h: "Readiness  (horizontal)", t: "Do they know it's coming, can they handle it, do they want to?" },
  ];
  ours.forEach((w, i) => {
    const y = colY + 1.45 + i * 1.6;
    s.addImage({ data: ICO.check, x: rx + 0.35, y: y + 0.05, w: 0.3, h: 0.3 });
    s.addText([
      { text: w.h, options: { bold: true, fontSize: 15, color: C.text1, breakLine: true } },
      { text: w.t, options: { fontSize: 13, color: C.text2 } },
    ], { x: rx + 0.85, y, w: colW - 1.2, h: 1.3, valign: "top", margin: 0, isTextBox: true });
  });
  s.addText("Interest isn't dropped: it stays in the register as a warning flag — high impact + low interest = risk of being blindsided (publishers, regulators, Board).",
    { x: lx + 0.35, y: colY + colH - 1.25, w: colW - 0.7, h: 1.0, fontSize: 11, italic: true, color: C.text2, valign: "bottom", margin: 0, isTextBox: true });
  s.addText("The question becomes: who must change the most, and who is least prepared to?",
    { x: rx + 0.35, y: colY + colH - 1.25, w: colW - 0.7, h: 1.0, fontSize: 13, bold: true, color: C.accent1, valign: "bottom", margin: 0, isTextBox: true });
  s.addNotes("~30s. The classic power/interest grid fails here. Power: nobody controls whether students use AI. Interest: nobody asked for this, so everyone sits at zero. Because the project is a transition, we map adaptation effort — how much each stakeholder must rewrite — against readiness — do they know, can they, do they want to. Interest stays in the register only as a warning flag.");

  // =============== 4. THE MAP ===============
  pres.addSection({ title: SEC[1] });
  s = content(1, "Those who must change the most are the least prepared");
  drawFrame(s);
  Object.keys(SH).forEach((k) => drawNode(s, k));
  // right column: how to read
  const sx = 9.3, sw = 3.45;
  s.addText([
    { text: "HOW TO READ IT", options: { bold: true, fontSize: 11, charSpacing: 2, color: C.text2, breakLine: true } },
    { text: " ", options: { fontSize: 6, breakLine: true } },
    { text: "Up", options: { bold: true, color: C.text1 } },
    { text: " = more of their work has to be rewritten", options: { color: C.text1, breakLine: true } },
    { text: "Right", options: { bold: true, color: C.text1 } },
    { text: " = more aware, able and willing", options: { color: C.text1 } },
  ], { x: sx, y: 1.6, w: sw, h: 1.4, fontSize: 13, valign: "top", margin: 0, isTextBox: true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: sx, y: 3.2, w: sw, h: 2.3, rectRadius: 0.08, fill: { color: C.accent5 }, line: { type: "none" } });
  s.addText([
    { text: "The pattern", options: { bold: true, fontSize: 15, color: C.accent1, breakLine: true } },
    { text: " ", options: { fontSize: 6, breakLine: true } },
    { text: "The top-left is full of academics and HR. The bottom-right is full of leaders and students. The project lives or dies on connecting the two.", options: { fontSize: 13, color: C.text1 } },
  ], { x: sx + 0.25, y: 3.4, w: sw - 0.5, h: 1.95, valign: "top", margin: 0, isTextBox: true });
  s.addText("Positions are our inferences from the case bios — hypotheses to challenge, not facts.",
    { x: sx, y: 5.75, w: sw, h: 0.7, fontSize: 10, italic: true, color: C.text2, valign: "top", margin: 0, isTextBox: true });
  s.addNotes("~40s. Here is everyone, internal and external. Up means more of their work must be rewritten; right means more ready. The pattern jumps out: the top-left — FOCUS HERE — is academics and HR. The bottom-right, our allies, is leadership, the sponsor and students, who have little to change. Bottom-left we simply inform: CFO, Board, publishers, partners. Top-right we equip: IT, legal, international campuses. These positions are our inferences from the bios.");

  // =============== 5. CRITICAL ===============
  s = content(1, "Three stakeholders decide whether the transition is smooth");
  drawFrame(s);
  const crit = ["elodie", "faculty", "laura"];
  Object.keys(SH).forEach((k) => {
    const i = crit.indexOf(k);
    if (i >= 0) drawNode(s, k, { big: true, fill: C.accent1, badge: i + 1 });
    else drawNode(s, k, { fill: C.accent4, textColor: C.accent3 });
  });
  const why3 = [
    { n: 1, h: "Élodie Martin", t: "Must redefine what a grade means when AI is allowed. Owns academic rules for everyone else." },
    { n: 2, h: "Restrictive faculty", t: "Rewrite every syllabus and assessment. Today they ban AI per assignment." },
    { n: 3, h: "Laura Bianchi", t: "Must settle logging and privacy with the works council — post-restructuring." },
  ];
  why3.forEach((w, i) => {
    const y = 1.6 + i * 1.55;
    s.addShape(pres.shapes.OVAL, { x: sx, y: y + 0.02, w: 0.38, h: 0.38, fill: { color: C.accent1 }, line: { type: "none" } });
    s.addText(String(w.n), { x: sx, y: y + 0.02, w: 0.38, h: 0.38, fontSize: 13, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText([
      { text: w.h, options: { bold: true, fontSize: 14, color: C.text1, breakLine: true } },
      { text: w.t, options: { fontSize: 12, color: C.text2 } },
    ], { x: sx + 0.55, y, w: sw - 0.55, h: 1.35, valign: "top", margin: 0, isTextBox: true });
  });
  s.addText("Selection rule: highest effort × lowest readiness. Everyone else is equipped, informed or used as an ally.",
    { x: sx, y: 6.0, w: sw, h: 0.55, fontSize: 10, italic: true, color: C.text2, valign: "top", margin: 0, isTextBox: true });
  s.addNotes("~50s. Our three critical stakeholders are the ones in the top-left: the most to change, the least prepared. 1) Élodie Martin, Academic Dean: assessment and what a grade certifies must be rebuilt, and she sets the rules every faculty member follows. 2) Restrictive faculty and programme directors: they rewrite syllabi and exams, and today they ban AI. 3) Laura Bianchi: any logging of prompts is a monitoring question with the works council, right after a restructuring. Note we did NOT pick the CFO or the CIO: they matter, but the CFO only has to approve a bounded pilot, and the CIO is willing — she needs tools, not persuasion.");

  // =============== 6. INFLUENCE ===============
  pres.addSection({ title: SEC[2] });
  s = content(2, "We move the focus group through peers, not top-down mandates");
  drawFrame(s, { focusTint: true });
  const links = [
    ["profai", "faculty", 3], ["profai", "elodie", 3], ["elodie", "faculty", 3],
    ["students", "elodie", 2],
    ["claire", "elodie", 2], ["claire", "laura", 2],
    ["legal", "laura", 3], ["aisha", "laura", 2],
  ];
  links.forEach(([a, b, w]) => drawLink(s, a, b, w));
  const att = { elodie: C.accent3, faculty: C.accent1, laura: C.accent3, profai: C.accent2, students: C.accent2, claire: C.accent2, legal: C.accent3, aisha: C.accent2 };
  Object.keys(att).forEach((k) => drawNode(s, k, { big: crit.includes(k), ring: crit.includes(k), fill: att[k], halo: true, lab: k === "elodie" ? "r" : undefined }));
  // legend
  s.addText("ATTITUDE", { x: sx, y: 1.6, w: sw, h: 0.3, fontSize: 11, bold: true, charSpacing: 2, color: C.text2, margin: 0, isTextBox: true });
  [["For", C.accent2], ["Torn / neutral", C.accent3], ["Against", C.accent1]].forEach(([t, c], i) => {
    s.addShape(pres.shapes.OVAL, { x: sx, y: 2.03 + i * 0.36, w: 0.2, h: 0.2, fill: { color: c }, line: { type: "none" } });
    s.addText(t, { x: sx + 0.32, y: 1.98 + i * 0.36, w: 2.5, h: 0.3, fontSize: 12, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
  });
  s.addText("INFLUENCE  (arrow = who can move whom)", { x: sx, y: 3.25, w: sw, h: 0.3, fontSize: 11, bold: true, charSpacing: 1, color: C.text2, margin: 0, isTextBox: true });
  [["Strong", 5], ["Medium", 2.75], ["Weak", 1.25]].forEach(([t, wdt], i) => {
    s.addShape(pres.shapes.LINE, { x: sx, y: 3.8 + i * 0.36, w: 0.7, h: 0, line: { color: C.text2, width: wdt, endArrowType: "triangle" } });
    s.addText(t, { x: sx + 0.85, y: 3.65 + i * 0.36, w: 2, h: 0.3, fontSize: 12, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: sx, y: 4.95, w: sw, h: 1.6, rectRadius: 0.08, fill: { color: C.text1 }, line: { type: "none" } });
  s.addText([
    { text: "Pro-AI faculty are our best asset: ", options: { bold: true, color: C.background1 } },
    { text: "they are peers of the people who must change most. Two of three critical stakeholders are torn, not opposed — they can be moved.", options: { color: C.accent4 } },
  ], { x: sx + 0.25, y: 5.1, w: sw - 0.5, h: 1.3, fontSize: 12, valign: "top", margin: 0, isTextBox: true });
  s.addNotes("~40s. Now we clear the map and keep only the critical three and the people who can move them. Colour is attitude. Élodie and Laura are grey — torn, not opposed — which means they are movable. Only restrictive faculty are against. The arrows show the channels: pro-AI faculty are peers of both Élodie and restrictive faculty — the strongest lever we have. Élodie herself then moves restrictive faculty through academic authority. Students push through employability demand. For Laura, the channel is Legal/DPO and the CIO — privacy by design — backed by the Dean. Marc, the sponsor, is deliberately not an arrow: a top-down push from Operations is exactly what academics resist.");

  // =============== 7-9. DEEP DIVES ===============
  const dives = [
    {
      key: "elodie", ic: ICO.grad, att: ["Torn", C.accent3],
      title: "Élodie Martin must rebuild how Novaris grades — and she's torn",
      role: "Academic Dean", why: "Sets the academic rules every programme follows.",
      notReady: ["Assessment assumes unassisted work: take-home essays, computer-based exams", "A school-endorsed tool can look like endorsing AI-written answers", "Protective of academic independence — reads admin-led tech as overreach"],
      work: ["Redefine what a grade certifies when AI is allowed", "Redesign exam and take-home formats across programmes", "Set one disclosure rule faculty can actually enforce"],
      movers: [["Pro-AI faculty", 3, C.accent2], ["Claire Moreau", 2, C.accent2], ["Students", 2, C.accent2]],
      first: "Ask her to chair a faculty co-design group; per-course AI settings (off / with disclosure / encouraged); logs never used to evaluate faculty.",
      notes: "~30s. Élodie is the critical case. Her interest runs both ways: AI literacy is now an employability requirement, and a governed portal beats invisible use — but she must rebuild assessment, and an official tool could look like endorsing AI-written answers. Ambivalence is movability. Solve her assessment worry — give her ownership through a co-design group and per-course rules — and she flips.",
    },
    {
      key: "faculty", ic: ICO.chalk, att: ["Against", C.accent1],
      title: "Restrictive faculty carry the workload but have no tools for it yet",
      role: "& programme directors", why: "Where the change actually happens: in each course.",
      notReady: ["They ban AI per assignment today — no way to check or adapt", "The redesign workload lands on them, with no time or support", "Fear their course content leaks into a portal knowledge base"],
      work: ["Rewrite syllabus and assignment rules course by course", "Redesign assessments to stay valid with AI around", "Teach students how to disclose and cite AI use"],
      movers: [["Pro-AI faculty", 3, C.accent2], ["Élodie Martin", 3, C.accent3], ["Students", 1, C.accent2]],
      first: "Opt-in pilot where they keep an “AI off” switch; peer showcase run by pro-AI colleagues; no course content in a knowledge base in phase 1.",
      notes: "~25s. Restrictive faculty are the only group clearly against. Not because they're anti-change: the workload lands on them, they have no tools, and they fear for their content. We don't mandate — we let them keep an AI-off switch in an opt-in pilot, and let their own colleagues show what works.",
    },
    {
      key: "laura", ic: ICO.userShield, att: ["Torn", C.accent3],
      title: "Laura Bianchi must settle logging before anything goes live",
      role: "Director, People & Faculty Affairs", why: "One monitoring headline can stop the project.",
      notReady: ["Post-restructuring: any “monitoring” story reignites works-council friction", "Logging prompts and outputs can read as surveillance", "No decision yet on whether faculty and staff are in scope"],
      work: ["Define what is logged, kept, and who can see it", "Consult employee representatives before launch", "Update staff policies if faculty and staff use the portal"],
      movers: [["Legal / DPO", 3, C.accent3], ["Aisha Khan", 2, C.accent2], ["Claire Moreau", 2, C.accent2]],
      first: "Bring her in before the logging decision; students-only phase 1; privacy impact assessment with the DPO; written rule that logs never evaluate staff.",
      notes: "~25s. Laura isn't against the portal, but she can't be surprised by it. The logging question is a monitoring question, right after a restructuring. We bring her in before the decision is made, keep phase 1 students-only, and let Legal/DPO and the CIO show privacy by design.",
    },
  ];
  for (const d of dives) {
    s = content(2, d.title);
    const sh = SH[d.key];
    // profile card
    const px = 0.6, py = 1.65, pw = 3.4, ph = 4.95;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: px, y: py, w: pw, h: ph, rectRadius: 0.08, fill: { color: C.background2 }, line: { type: "none" }, objectName: "Profile card" });
    s.addShape(pres.shapes.OVAL, { x: px + 0.3, y: py + 0.3, w: 0.75, h: 0.75, fill: { color: C.accent1 }, line: { type: "none" } });
    s.addImage({ data: d.ic, x: px + 0.48, y: py + 0.48, w: 0.39, h: 0.39 });
    s.addText([
      { text: sh.name === "Restrictive faculty" ? "Restrictive faculty" : sh.name, options: { bold: true, fontSize: 18, color: C.text1, breakLine: true } },
      { text: d.role, options: { fontSize: 11, color: C.text2 } },
    ], { x: px + 0.3, y: py + 1.2, w: pw - 0.6, h: 0.85, valign: "top", margin: 0, isTextBox: true });
    // mini map
    const mm = { x: px + 0.3, y: py + 2.2, w: 1.5, h: 1.2 };
    [["tl", C.accent5], ["tr", C.background1], ["bl", C.background1], ["br", C.background1]].forEach(([q, c]) => {
      const qx = mm.x + (q[1] === "r" ? mm.w / 2 + 0.02 : 0), qy = mm.y + (q[0] === "b" ? mm.h / 2 + 0.02 : 0);
      s.addShape(pres.shapes.RECTANGLE, { x: qx, y: qy, w: mm.w / 2 - 0.02, h: mm.h / 2 - 0.02, fill: { color: c }, line: { type: "none" } });
    });
    const mp = P(sh.r, sh.e, mm);
    s.addShape(pres.shapes.OVAL, { x: mp.x - 0.08, y: mp.y - 0.08, w: 0.16, h: 0.16, fill: { color: d.att[1] }, line: { color: C.text1, width: 1.5 } });
    s.addText([
      { text: "FOCUS", options: { bold: true, fontSize: 11, color: C.accent1, breakLine: true } },
      { text: "High effort", options: { fontSize: 10, color: C.text1, breakLine: true } },
      { text: "Low readiness", options: { fontSize: 10, color: C.text1, breakLine: true } },
      { text: "Attitude: " + d.att[0], options: { fontSize: 10, bold: true, color: d.att[1] === C.accent3 ? C.text2 : d.att[1] } },
    ], { x: mm.x + mm.w + 0.15, y: mm.y, w: 1.4, h: 1.2, valign: "middle", margin: 0, isTextBox: true });
    s.addText(d.why, { x: px + 0.3, y: py + 3.65, w: pw - 0.6, h: 1.1, fontSize: 13, italic: true, color: C.text1, valign: "top", margin: 0, isTextBox: true });

    // two columns
    const cx1 = 4.35, cx2 = 8.6, cwd = 4.15, cyy = 1.65;
    const col = (x, head, ico, items) => {
      s.addImage({ data: ico, x, y: cyy + 0.03, w: 0.28, h: 0.28 });
      s.addText(head, { x: x + 0.42, y: cyy, w: cwd - 0.42, h: 0.35, fontSize: 15, bold: true, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
      s.addText(items.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < items.length - 1 } })),
        { x, y: cyy + 0.5, w: cwd, h: 2.05, fontSize: 13, color: C.text1, paraSpaceAfter: 8, valign: "top", margin: 0, isTextBox: true });
    };
    col(cx1, "Why not ready", ICO.times, d.notReady);
    col(cx2, "Work to do before the switch", ICO.wrench, d.work);
    // movers
    const by = 4.45;
    s.addText("WHO CAN MOVE " + (d.key === "faculty" ? "THEM" : "HER"), { x: cx1, y: by, w: cwd, h: 0.3, fontSize: 11, bold: true, charSpacing: 2, color: C.text2, margin: 0, isTextBox: true });
    d.movers.forEach(([n, st, c], i) => {
      const y = by + 0.45 + i * 0.52;
      s.addShape(pres.shapes.OVAL, { x: cx1, y: y + 0.08, w: 0.22, h: 0.22, fill: { color: c }, line: { type: "none" } });
      s.addText(n, { x: cx1 + 0.35, y, w: 2.1, h: 0.38, fontSize: 13, bold: true, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
      s.addShape(pres.shapes.LINE, { x: cx1 + 2.5, y: y + 0.19, w: 0.8, h: 0, line: { color: C.text2, width: { 1: 1.25, 2: 2.75, 3: 5 }[st], endArrowType: "triangle" } });
      s.addText(["", "weak", "medium", "strong"][st], { x: cx1 + 3.4, y, w: 0.8, h: 0.38, fontSize: 10, color: C.text2, valign: "middle", margin: 0, isTextBox: true });
    });
    // first move
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: cx2, y: by, w: cwd, h: 2.15, rectRadius: 0.08, fill: { color: C.accent5 }, line: { type: "none" }, objectName: "First move" });
    s.addText([
      { text: "OUR FIRST MOVE", options: { fontSize: 11, bold: true, charSpacing: 2, color: C.accent1, breakLine: true } },
      { text: " ", options: { fontSize: 5, breakLine: true } },
      { text: d.first, options: { fontSize: 13, color: C.text1 } },
    ], { x: cx2 + 0.25, y: by + 0.2, w: cwd - 0.5, h: 1.8, valign: "top", margin: 0, isTextBox: true });
    s.addNotes(d.notes);
  }

  // =============== 10. CLOSE ===============
  s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: SEC[2] });
  s.addText("Our job is connecting the two", { placeholder: "title" });
  s.addText("The people who must change the most are the least prepared; the most prepared have the least to change.", { placeholder: "body" });
  const steps = [
    ["1", "Recruit the channel", "Pro-AI faculty and students carry the message to their peers."],
    ["2", "Remove blockers first", "Assessment rules, logging limits, no course content in phase 1."],
    ["3", "Pilot, then re-map", "One-semester Paris pilot; redraw this map at every phase gate."],
  ];
  steps.forEach(([n, h, t], i) => {
    const x = 0.8 + i * 3.95;
    s.addShape(pres.shapes.OVAL, { x, y: 5.75, w: 0.5, h: 0.5, fill: { color: C.accent1 }, line: { type: "none" } });
    s.addText(n, { x, y: 5.75, w: 0.5, h: 0.5, fontSize: 16, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText([
      { text: h, options: { bold: true, fontSize: 14, color: C.background1, breakLine: true } },
      { text: t, options: { fontSize: 11, color: C.accent4 } },
    ], { x: x + 0.65, y: 5.68, w: 3.1, h: 1.0, valign: "top", margin: 0, isTextBox: true });
  });
  s.addNotes("~25s. To close: we can't stop AI adoption, so the project is the transition. The people who must change most are least prepared; the people most prepared have least to change. Our job is connecting the two: recruit pro-AI faculty and students as the channel, remove the focus group's blockers before launch, run a bounded Paris pilot — and redraw this map at every phase, because stakeholder analysis is iterative.");

  // =============== 11. BACKUP REGISTER ===============
  pres.addSection({ title: SEC[3] });
  s = content(3, "Full stakeholder register");
  const hdr = ["Stakeholder", "Int/Ext", "Quadrant", "Attitude", "Interest today", "What has to change"].map((t) => ({ text: t, options: { bold: true, color: C.background1, fill: { color: C.text1 } } }));
  const rows = [
    ["Élodie Martin — Academic Dean", "Int", "FOCUS", "Torn", "Medium", "Assessment model, grade meaning, disclosure rules"],
    ["Restrictive faculty & programme dirs", "Int", "FOCUS", "Against", "Low", "Syllabi, assignment rules, exam formats"],
    ["Laura Bianchi — People & Faculty", "Int", "FOCUS", "Torn", "Low", "Logging/privacy policy, works-council consultation"],
    ["Aisha Khan — CIO", "Int", "EQUIP", "For", "High", "SSO, security, vendor and data classification"],
    ["Rafael Mendes — Intl. campuses", "Int", "EQUIP", "For", "Medium", "Local adaptation for Singapore, São Paulo, Casablanca"],
    ["Legal / DPO", "Int", "EQUIP", "Neutral", "Low", "Privacy impact assessment, vendor contracts"],
    ["Library", "Int", "EQUIP", "Neutral", "Low", "Licence review for content in prompts"],
    ["Marc Lefèvre — Sponsor", "Int", "ALLIES", "For", "High", "Little — owns delivery"],
    ["Claire Moreau — President & Dean", "Int", "ALLIES", "For", "Medium", "Little — strategic backing"],
    ["Pro-AI faculty · Students · Transformation Office", "Int", "ALLIES", "For", "Medium", "Little — already adapted"],
    ["Sophie Bernard — CFO", "Int", "INFORM", "Neutral", "Low", "Approve a bounded pilot with clear economics"],
    ["Employee reps (works council)", "Int", "INFORM", "Neutral", "Low", "Consulted on logging"],
    ["Board · Publishers · Corporate partners · Regulators", "Ext", "INFORM", "Neutral", "Low ⚑", "Not much — but must not be surprised"],
  ];
  s.addTable([hdr, ...rows.map((r) => r.map((t, j) => ({ text: t, options: { bold: j === 0, color: (j === 2 && t === "FOCUS") ? C.accent1 : C.text1 } })))], {
    x: 0.6, y: 1.5, w: 12.1, colW: [3.7, 0.8, 1.1, 1.0, 1.4, 4.1], fontSize: 10, color: C.text1,
    border: { type: "solid", pt: 0.5, color: HEX.accent4 }, fill: { color: C.background1 }, rowH: 0.36, valign: "middle", margin: 0.05,
  });
  s.addText("⚑ high impact + low interest = risk of being blindsided. All ratings are inferences from the case bios.", { x: 0.6, y: 6.7, w: 12, h: 0.3, fontSize: 10, italic: true, color: C.text2, margin: 0, isTextBox: true });
  s.addNotes("Backup only — not presented. Full register with quadrant, attitude, interest flag and the change each stakeholder has to make.");

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})();
