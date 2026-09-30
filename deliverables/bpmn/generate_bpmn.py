"""Generate the Bouchara Maison main-process BPMN 2.0 collaboration (vertical swimlanes) with DI."""
import json
from xml.sax.saxutils import escape

LW = 140            # lane width
TW, TH = 118, 58    # task size
GW = 42             # gateway size
EW = 32             # event size
ROW = 80
TOP = 10
HDR = 30            # pool header (vertical pool: band at top)
LHDR = 30           # lane header
Y0 = TOP + HDR + LHDR + 8

X_CUST = 10
X_POOL = X_CUST + LW + 20
LANES = ["PLAT", "ADV", "SC", "CS"]
LX = {"CUST": X_CUST, "PLAT": X_POOL, "ADV": X_POOL + LW, "SC": X_POOL + 2 * LW, "CS": X_POOL + 3 * LW}
X_BB = X_POOL + 4 * LW + 20
BBW, BBH = 124, 50
LX["BB"] = X_BB
NROWS = 36
BOTTOM = Y0 + NROWS * ROW + 6

def cx(lane):
    return LX[lane] + (BBW if lane == "BB" else LW) / 2

def cy(r):
    return Y0 + r * ROW + ROW / 2

N = {}   # id -> dict
def node(i, kind, name, lane, row, proc, **kw):
    w, h = {"task": (TW, TH), "xor": (GW, GW), "and": (GW, GW), "evb": (GW, GW)}.get(kind, (EW, EW))
    x = cx(lane) - w / 2 + kw.get("dx", 0)
    y = cy(row) - h / 2
    N[i] = dict(id=i, kind=kind, name=name, lane=lane, row=row, proc=proc, x=x, y=y, w=w, h=h, **kw)

C, B = "Process_Customer", "Process_Bouchara"
# ---- Customer pool
node("c_start", "msgstart", "Room to refresh", "CUST", 0, C, lpos="r")
node("c_visit", "task", "Visit website or store", "CUST", 1, C)
node("c_g0", "xor", "Use AI room planner?", "CUST", 2, C, lpos="r")
node("c_project", "task", "Create room project (room, budget)", "CUST", 3, C)
node("c_compare", "task", "Compare previews, swap items, order samples", "CUST", 6, C)
node("c_g1", "xor", "Advice or custom item?", "CUST", 7, C, lpos="r")
node("c_store", "task", "Visit store with saved project", "CUST", 9, C)
node("c_confirm", "task", "Confirm basket (online or in store)", "CUST", 15, C)
node("c_pay", "task", "Review summary, choose options, pay", "CUST", 19, C)
node("c_receive", "task", "Receive delivery and installation", "CUST", 29, C)
node("c_survey", "task", "Answer survey or report issue", "CUST", 31, C)
node("c_end", "end", "Room done", "CUST", 32, C, lpos="r")
# ---- Bouchara pool
node("b_start", "msgstart", "Session starts", "PLAT", 1, B, lpos="r")
node("b_gp", "xor", "Project created?", "PLAT", 2, B, lpos="r")
node("b_save", "task", "Save project and project ID", "PLAT", 3, B)
node("b_suggest", "task", "Suggest coordinated room within budget", "PLAT", 4, B)
node("b_render", "task", "Render 3 options in parallel (fast preview first)", "PLAT", 5, B)
node("b_fallback", "task", "Fallback: product photos + advice offer", "PLAT", 6, B)
node("b_xa", "xor", "", "PLAT", 7, B)
node("b_ga", "xor", "Advice requested?", "PLAT", 8, B, lpos="r")
node("a_open", "task", "Open shared project; readiness check", "ADV", 9, B)
node("a_advise", "task", "Advise on materials, sizes, samples", "ADV", 10, B)
node("a_g4", "xor", "Custom item?", "ADV", 11, B, lpos="r")
node("a_validate", "task", "Validate spec with production checklist", "ADV", 12, B)
node("a_confirm", "task", "Confirm selection in shared project", "ADV", 13, B)
node("b_xm", "xor", "", "PLAT", 14, B)
node("b_basket", "msgcatch", "Basket confirmed", "PLAT", 15, B, lpos="r")
node("b_stock", "task", "Check stock and dates for whole room", "PLAT", 16, B)
node("b_g2", "xor", "Room complete?", "PLAT", 17, B, lpos="r")
node("b_subst", "task", "Offer substitute, split delivery or wait", "PLAT", 18, B)
node("b_checkout", "task", "Checkout: lead times, installation, terms", "PLAT", 19, B)
node("b_g3", "xor", "Paid?", "PLAT", 20, B, lpos="r")
node("b_order", "task", "Create order linked to project", "PLAT", 21, B)
node("s_split", "and", "", "SC", 22, B)
node("s_stock", "task", "Pick from stock or drop-ship", "SC", 23, B)
node("s_custom", "task", "Send validated spec; track production", "SC", 24, B)
node("s_join", "and", "", "SC", 25, B)
node("s_book", "task", "Confirm lead time; book delivery slot", "SC", 26, B)
node("s_g5", "xor", "Installation ordered?", "SC", 27, B, lpos="r")
node("s_install", "task", "Book installation on delivery day", "SC", 28, B)
node("s_track", "task", "Track delivery to promised date", "SC", 29, B)
node("s_replan", "task", "Warn customer and re-plan", "SC", 30, B)
node("cs_survey", "task", "Send care guide and survey", "CS", 31, B)
node("cs_g6", "xor", "Issue reported?", "CS", 32, B, lpos="r")
node("cs_after", "task", "After-sales: replace or remake", "CS", 33, B)
node("cs_invite", "task", "Invite to next room project", "CS", 34, B)
node("cs_end", "end", "Room delivered, project open", "CS", 35, B, lpos="l")

# boundary timers
BT = {}
def boundary(i, name, host, side="bottom"):
    h = N[host]
    x = h["x"] + h["w"] - EW / 2 - 14 if side == "br" else h["x"] + h["w"] / 2 - EW / 2
    y = h["y"] + h["h"] - EW / 2
    BT[i] = dict(id=i, name=name, host=host, x=x, y=y, w=EW, h=EW, proc=B, lane=h["lane"])
boundary("t_render", "> 10 s", "b_render", "br")
boundary("t_late", "Date at risk", "s_track", "br")

# ---- black boxes (collapsed pools)
BB = {}
def bb(i, name, row):
    BB[i] = dict(id=i, name=name, x=X_BB, y=cy(row) - BBH / 2, w=BBW, h=BBH)
bb("P_bazar", "BazarChic (campaigns)", 0)
bb("P_ai", "AI visualisation provider", 5)
bb("P_pay", "Payment provider", 19)
bb("P_supp", "Product suppliers", 23)
bb("P_manu", "Custom manufacturers", 24)
bb("P_deliv", "Delivery partner", 26)
bb("P_inst", "Installation partner", 28)

ALL = {**N, **BT, **BB}

def L(i): return ALL[i]["x"]
def R(i): return ALL[i]["x"] + ALL[i]["w"]
def T(i): return ALL[i]["y"]
def Bt(i): return ALL[i]["y"] + ALL[i]["h"]
def CX(i): return ALL[i]["x"] + ALL[i]["w"] / 2
def CY(i): return ALL[i]["y"] + ALL[i]["h"] / 2
def lane_of(i): return ALL[i]["lane"]
def mleft(lane): return LX[lane] + 6
def mright(lane): return LX[lane] + LW - 6

SEQ = []  # (id, src, tgt, name, points)
def seq(s, t, how="v", name="", lp=None):
    if how == "v":
        pts = [(CX(s), Bt(s)), (CX(t), T(t))]
    elif how in ("left", "right"):
        m = mleft(lane_of(s)) if how == "left" else mright(lane_of(s))
        sx = L(s) if how == "left" else R(s)
        if ALL[t].get("kind") == "task":   # enter from the top, off-centre, to keep side ports free for messages
            ex = CX(t) + (-36 if how == "left" else 36)
            pts = [(sx, CY(s)), (m, CY(s)), (m, T(t) - 9), (ex, T(t) - 9), (ex, T(t))]
        else:
            tx = L(t) if how == "left" else R(t)
            pts = [(sx, CY(s)), (m, CY(s)), (m, CY(t)), (tx, CY(t))]
    elif how in ("left-up", "right-up"):   # loop back up, entering the target from below
        m = mleft(lane_of(s)) if how == "left-up" else mright(lane_of(s))
        sx = L(s) if how == "left-up" else R(s)
        ex = CX(t) + (-36 if how == "left-up" else 36)
        pts = [(sx, CY(s)), (m, CY(s)), (m, Bt(t) + 7), (ex, Bt(t) + 7), (ex, Bt(t))]
    elif how == "hv":   # horizontal from side, then down into top
        sx = R(s) if CX(t) > CX(s) else L(s)
        pts = [(sx, CY(s)), (CX(t), CY(s)), (CX(t), T(t))]
    elif how == "vh":   # down from bottom, then horizontal into side
        tx = L(t) if CX(t) > CX(s) else R(t)
        pts = [(CX(s), Bt(s)), (CX(s), CY(t)), (tx, CY(t))]
    SEQ.append(dict(id=f"f_{s}_{t}", src=s, tgt=t, name=name, pts=pts, lp=lp, proc=ALL[s]["proc"]))

# customer flow
seq("c_start", "c_visit"); seq("c_visit", "c_g0"); seq("c_g0", "c_project", name="Yes")
seq("c_g0", "c_confirm", "left", name="No")
seq("c_project", "c_compare"); seq("c_compare", "c_g1")
seq("c_g1", "c_store", name="Yes"); seq("c_g1", "c_confirm", "right", name="No")
seq("c_store", "c_confirm"); seq("c_confirm", "c_pay"); seq("c_pay", "c_receive")
seq("c_receive", "c_survey"); seq("c_survey", "c_end")
# bouchara flow
seq("b_start", "b_gp"); seq("b_gp", "b_save", name="Yes"); seq("b_gp", "b_xa", "right", name="No")
seq("b_save", "b_suggest"); seq("b_suggest", "b_render")
seq("b_render", "b_xa", "left")
SEQ.append(dict(id="f_t_render_b_fallback", src="t_render", tgt="b_fallback", name="", lp=None, proc=B, pts=[(CX("t_render"), Bt("t_render")), (CX("t_render"), T("b_fallback"))]))
seq("b_fallback", "b_xa")
seq("b_xa", "b_ga")
seq("b_ga", "a_open", "hv", name="Yes"); seq("b_ga", "b_xm", name="No")
seq("a_open", "a_advise"); seq("a_advise", "a_g4")
seq("a_g4", "a_validate", name="Yes"); seq("a_g4", "a_confirm", "right", name="No")
seq("a_validate", "a_confirm"); seq("a_confirm", "b_xm", "vh")
seq("b_xm", "b_basket"); seq("b_basket", "b_stock"); seq("b_stock", "b_g2")
seq("b_g2", "b_subst", name="No"); seq("b_g2", "b_checkout", "right", name="Yes")
seq("b_subst", "b_checkout"); seq("b_checkout", "b_g3")
seq("b_g3", "b_order", name="Yes"); seq("b_g3", "b_checkout", "left-up", name="No")
seq("b_order", "s_split", "hv")
seq("s_split", "s_stock"); seq("s_split", "s_custom", "right")
seq("s_stock", "s_join", "left"); seq("s_custom", "s_join")
seq("s_join", "s_book"); seq("s_book", "s_g5")
seq("s_g5", "s_install", name="Yes"); seq("s_g5", "s_track", "right", name="No")
seq("s_install", "s_track"); SEQ.append(dict(id="f_t_late_s_replan", src="t_late", tgt="s_replan", name="", lp=None, proc=B, pts=[(CX("t_late"), Bt("t_late")), (CX("t_late"), T("s_replan"))]))
seq("s_replan", "s_track", "left-up")
seq("s_track", "cs_survey", "hv")
seq("cs_survey", "cs_g6"); seq("cs_g6", "cs_after", name="Yes"); seq("cs_g6", "cs_invite", "right", name="No")
seq("cs_after", "cs_invite"); seq("cs_invite", "cs_end")

MSG = []
def msg(s, t, dy=0, via=None):
    """horizontal message between shapes at (roughly) same row; if rows differ: horizontal at source row then vertical."""
    sy = CY(s) + dy
    if abs(CY(s) - CY(t)) < 1:
        if CX(t) > CX(s): pts = [(R(s), sy), (L(t), sy)]
        else: pts = [(L(s), sy), (R(t), sy)]
    else:
        sx = R(s) if CX(t) > CX(s) else L(s)
        tx = CX(t) + (via or 0)
        pts = [(sx, sy), (tx, sy), (tx, T(t) if CY(t) > CY(s) else Bt(t))]
    MSG.append(dict(id=f"m_{s}_{t}", src=s, tgt=t, pts=pts))

msg("P_bazar", "c_start")
msg("c_visit", "b_start")
msg("c_project", "b_save")
msg("b_render", "P_ai", dy=-9); msg("P_ai", "b_render", dy=9)
msg("b_render", "c_compare", dy=13)
msg("c_store", "a_open")
msg("c_confirm", "b_basket")
msg("b_checkout", "c_pay", dy=-8); msg("c_pay", "b_checkout", dy=8)
msg("b_checkout", "P_pay", dy=-9); msg("P_pay", "b_checkout", dy=9)
msg("s_stock", "P_supp")
msg("s_custom", "P_manu", dy=-9); msg("P_manu", "s_custom", dy=9)
msg("s_book", "P_deliv", dy=-9); msg("P_deliv", "s_book", dy=9)
msg("s_install", "P_inst")
msg("s_track", "c_receive")
msg("cs_survey", "c_survey", dy=-8); msg("c_survey", "cs_survey", dy=8)

# ------------------------------------------------------------------ XML
def a(s): return escape(s, {'"': "&quot;"})
out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" '
       'xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" '
       'id="Defs_BoucharaMaison" targetNamespace="http://bouchara-maison/bpmn" exporter="python" exporterVersion="1">']
out.append('<bpmn:collaboration id="Collab">')
out.append(f'<bpmn:participant id="P_customer" name="Customer" processRef="{C}" />')
out.append(f'<bpmn:participant id="P_bouchara" name="Bouchara Maison" processRef="{B}" />')
for b in BB.values():
    out.append(f'<bpmn:participant id="{b["id"]}" name="{a(b["name"])}" />')
for m in MSG:
    out.append(f'<bpmn:messageFlow id="{m["id"]}" sourceRef="{m["src"]}" targetRef="{m["tgt"]}" />')
out.append('</bpmn:collaboration>')

TAG = {"task": "task", "xor": "exclusiveGateway", "and": "parallelGateway", "start": "startEvent", "msgstart": "startEvent",
       "end": "endEvent", "msgcatch": "intermediateCatchEvent"}
LANE_NAMES = {"PLAT": "Digital platform", "ADV": "Store advisers", "SC": "Supply chain", "CS": "Customer service"}
for proc in (C, B):
    out.append(f'<bpmn:process id="{proc}" isExecutable="false">')
    if proc == B:
        out.append('<bpmn:laneSet id="LS">')
        for ln in LANES:
            out.append(f'<bpmn:lane id="Lane_{ln}" name="{LANE_NAMES[ln]}">')
            for n in list(N.values()) + list(BT.values()):
                if n["proc"] == B and n["lane"] == ln:
                    out.append(f'<bpmn:flowNodeRef>{n["id"]}</bpmn:flowNodeRef>')
            out.append('</bpmn:lane>')
        out.append('</bpmn:laneSet>')
    for n in N.values():
        if n["proc"] != proc: continue
        tag = TAG[n["kind"]]
        ins = [f'<bpmn:incoming>{f["id"]}</bpmn:incoming>' for f in SEQ if f["tgt"] == n["id"]]
        outs = [f'<bpmn:outgoing>{f["id"]}</bpmn:outgoing>' for f in SEQ if f["src"] == n["id"]]
        body = "".join(ins + outs)
        if n["kind"] in ("msgstart", "msgcatch"): body += f'<bpmn:messageEventDefinition id="med_{n["id"]}" />'
        out.append(f'<bpmn:{tag} id="{n["id"]}" name="{a(n["name"])}">{body}</bpmn:{tag}>')
    for t in BT.values():
        if proc != B: continue
        outs = "".join(f'<bpmn:outgoing>{f["id"]}</bpmn:outgoing>' for f in SEQ if f["src"] == t["id"])
        out.append(f'<bpmn:boundaryEvent id="{t["id"]}" name="{a(t["name"])}" attachedToRef="{t["host"]}" cancelActivity="true">{outs}<bpmn:timerEventDefinition id="ted_{t["id"]}" /></bpmn:boundaryEvent>')
    for f in SEQ:
        if f["proc"] != proc: continue
        nm = f' name="{f["name"]}"' if f["name"] else ""
        out.append(f'<bpmn:sequenceFlow id="{f["id"]}"{nm} sourceRef="{f["src"]}" targetRef="{f["tgt"]}" />')
    out.append('</bpmn:process>')

# DI
out.append('<bpmndi:BPMNDiagram id="Diagram"><bpmndi:BPMNPlane id="Plane" bpmnElement="Collab">')
def shape(el, x, y, w, h, extra="", label=None):
    lab = ""
    if label:
        lx, ly, lw, lh = label
        lab = f'<bpmndi:BPMNLabel><dc:Bounds x="{lx:.0f}" y="{ly:.0f}" width="{lw:.0f}" height="{lh:.0f}" /></bpmndi:BPMNLabel>'
    out.append(f'<bpmndi:BPMNShape id="{el}_di" bpmnElement="{el}"{extra}><dc:Bounds x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" />{lab}</bpmndi:BPMNShape>')
shape("P_customer", X_CUST, TOP, LW, BOTTOM - TOP, ' isHorizontal="false"')
shape("P_bouchara", X_POOL, TOP, 4 * LW, BOTTOM - TOP, ' isHorizontal="false"')
for ln in LANES:
    shape(f"Lane_{ln}", LX[ln], TOP + HDR, LW, BOTTOM - TOP - HDR, ' isHorizontal="false"')
for b in BB.values():
    shape(b["id"], b["x"], b["y"], b["w"], b["h"], ' isHorizontal="true"')
for n in N.values():
    lab = None
    if n["kind"] != "task" and n["name"]:
        lw_ = 62
        if n.get("lpos") == "l":
            lab = (n["x"] - lw_ - 4, n["y"] - 4, lw_, 40)
        else:
            lab = (n["x"] + n["w"] + 4, n["y"] - 6, lw_, 40)
    extra = ' isMarkerVisible="true"' if n["kind"] == "xor" else ""
    shape(n["id"], n["x"], n["y"], n["w"], n["h"], extra, lab)
for t in BT.values():
    shape(t["id"], t["x"], t["y"], t["w"], t["h"], "", (t["x"] + t["w"] + 2, t["y"] + 18, 58, 16))
def edge(eid, pts, label=None):
    wp = "".join(f'<di:waypoint x="{x:.0f}" y="{y:.0f}" />' for x, y in pts)
    lab = ""
    if label:
        lx, ly = label
        lab = f'<bpmndi:BPMNLabel><dc:Bounds x="{lx:.0f}" y="{ly:.0f}" width="22" height="14" /></bpmndi:BPMNLabel>'
    out.append(f'<bpmndi:BPMNEdge id="{eid}_di" bpmnElement="{eid}">{wp}{lab}</bpmndi:BPMNEdge>')
for f in SEQ:
    lab = None
    if f["name"]:
        (x1, y1), (x2, y2) = f["pts"][0], f["pts"][1]
        if abs(x1 - x2) < 1:   # vertical first segment
            lab = (x1 + 4, y1 + 1)
        else:
            lab = (x1 + 3 if x2 > x1 else x1 - 25, y1 + 2)
    edge(f["id"], f["pts"], lab)
for m in MSG:
    edge(m["id"], m["pts"])
out.append('</bpmndi:BPMNPlane></bpmndi:BPMNDiagram></bpmn:definitions>')
open("bouchara_main_process.bpmn", "w").write("\n".join(out))

# overlays meta for renderer
KPI = {"c_g0": "K1", "a_open": "K2", "b_order": "K3 K4", "b_checkout": "K6", "b_render": "K8", "b_stock": "K9",
       "b_suggest": "K10", "s_track": "K11", "s_book": "K11", "a_validate": "K12", "s_custom": "K12", "cs_survey": "K13",
       "a_confirm": "K14", "cs_invite": "K16"}
QC = ["a_open", "a_validate", "b_stock"]
LBL = {n["id"]: (n["name"], n["kind"], n.get("lpos", "r")) for n in N.values() if n["kind"] != "task" and n["name"]}
LBL.update({t["id"]: (t["name"], "timer", "r") for t in BT.values()})
meta = dict(lbl=LBL, kpi=KPI, qc=QC, width=X_BB + BBW + 10, height=BOTTOM + 10,
            lanes={f"Lane_{k}": v for k, v in {"PLAT": "Pilot lead", "ADV": "Store manager", "SC": "Supply chain mgr", "CS": "Customer service mgr"}.items()},
            bbx=X_BB, bbw=BBW, top=TOP, rowy={r: cy(r) for r in range(NROWS)}, row=ROW, y0=Y0, hdr=TOP + HDR + LHDR)
json.dump(meta, open("meta.json", "w"))
print("nodes", len(N), "flows", len(SEQ), "msgs", len(MSG), "size", meta["width"], meta["height"])
