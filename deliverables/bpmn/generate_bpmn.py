"""Bouchara Maison main process: BPMN 2.0 collaboration, horizontal swimlanes (flow left to right) with DI.
Two halves joined by link events so the render can be stacked in two bands on one landscape page."""
import json
from xml.sax.saxutils import escape

TW, TH = 100, 58     # task
GW, EW = 40, 30     # gateway, event
CT, CG = 112, 58    # column widths: task column, gateway/event column
X0 = 70             # content start (after pool + lane label strips)
TOP = 10

# ---- columns (name, kind) : band 1 then band 2
COLS = [("c1", "g"), ("c2", "t"), ("c3", "g"), ("c4", "t"), ("c5", "t"), ("c6", "t"), ("c7", "t"), ("c7b", "g"),
        ("c8", "g"), ("c9", "t"), ("c10", "t"), ("c11", "g"), ("c12", "t"), ("c13", "t"), ("c14", "g"), ("c15", "t"),
        ("c16", "g"), ("c17", "t"), ("c18", "g"),
        ("d0", "g"), ("d1", "t"), ("d2", "g"), ("d3", "t"), ("d4", "g"), ("d5", "t"), ("d6", "t"), ("d7", "g"),
        ("d8", "t"), ("d9", "g"), ("d10", "t"), ("d11", "t"), ("d12", "t"), ("d13", "t"), ("d14", "g"), ("d15", "t"),
        ("d16", "t"), ("d17", "g")]
CX = {}
x = X0 + 8
for name, k in COLS:
    w = CT if k == "t" else CG
    CX[name] = x + w / 2
    x += w
WIDTH_CONTENT = x + 8
SPLIT_X = (CX["c18"] + CX["d0"]) / 2          # where the render is cut into two bands

# ---- lanes (y, height, sub-row centres relative to lane top)
LANE = {}
y = TOP
LANE["CUST"] = dict(y=y, h=100, sub=[52]); y += 100 + 14
POOL_Y = y
for ln, h, subs in (("PLAT", 124, [42, 98]), ("ADV", 86, [42]), ("SC", 136, [42, 102]), ("CS", 96, [42])):
    LANE[ln] = dict(y=y, h=h, sub=subs); y += h
POOL_H = y - POOL_Y
y += 14
BB_Y, BBH, BBW = y, 50, 104
HEIGHT = BB_Y + BBH + 10

def cy(lane, sub=0): return LANE[lane]["y"] + LANE[lane]["sub"][sub]
def mtop(lane): return LANE[lane]["y"] + 8
def mbot(lane): return LANE[lane]["y"] + LANE[lane]["h"] - 8

N = {}
def node(i, kind, name, lane, col, proc, sub=0, **kw):
    w, h = {"task": (TW, TH), "xor": (GW, GW), "and": (GW, GW)}.get(kind, (EW, EW))
    N[i] = dict(id=i, kind=kind, name=name, lane=lane, col=col, sub=sub, proc=proc,
                x=CX[col] - w / 2, y=cy(lane, sub) - h / 2, w=w, h=h, **kw)

C, B = "Process_Customer", "Process_Bouchara"
# customer
node("c_start", "msgstart", "Room to refresh", "CUST", "c1", C)
node("c_visit", "task", "Visit website or store", "CUST", "c2", C)
node("c_g0", "xor", "Use AI planner?", "CUST", "c3", C)
node("c_project", "task", "Create room project (room, budget)", "CUST", "c4", C)
node("c_compare", "task", "Compare previews, swap items", "CUST", "c6", C)
node("c_g1", "xor", "Advice or custom item?", "CUST", "c8", C)
node("c_store", "task", "Visit store with saved project", "CUST", "c9", C)
node("c_confirm", "task", "Confirm basket (online or in store)", "CUST", "c14", C)
node("c_linkC", "linkthrow", "C", "CUST", "c18", C)
node("c_linkC2", "linkcatch", "C", "CUST", "d0", C)
node("c_pay", "task", "Review summary and pay", "CUST", "d1", C)
node("c_receive", "task", "Receive delivery and installation", "CUST", "d11", C)
node("c_survey", "task", "Answer survey or report issue", "CUST", "d13", C)
node("c_end", "end", "Room done", "CUST", "d14", C)
# bouchara
node("b_start", "msgstart", "Session starts", "PLAT", "c2", B)
node("b_gp", "xor", "Project created?", "PLAT", "c3", B)
node("b_save", "task", "Save project and project ID", "PLAT", "c4", B)
node("b_suggest", "task", "Suggest room within budget", "PLAT", "c5", B)
node("b_render", "task", "Render 3 options in parallel", "PLAT", "c6", B)
node("b_fallback", "task", "Fallback: photos + advice offer", "PLAT", "c7", B, sub=1)
node("b_xa", "xor", "", "PLAT", "c7b", B)
node("b_ga", "xor", "Advice requested?", "PLAT", "c8", B)
node("a_open", "task", "Open project; readiness check", "ADV", "c9", B)
node("a_advise", "task", "Advise on materials and sizes", "ADV", "c10", B)
node("a_g4", "xor", "Custom item?", "ADV", "c11", B)
node("a_validate", "task", "Validate spec vs production checklist", "ADV", "c12", B)
node("a_confirm", "task", "Confirm selection in shared project", "ADV", "c13", B)
node("b_basket", "msgcatch", "Basket confirmed", "PLAT", "c14", B)
node("b_stock", "task", "Check stock and dates for whole room", "PLAT", "c15", B)
node("b_g2", "xor", "Room complete?", "PLAT", "c16", B)
node("b_subst", "task", "Offer substitute, split or wait", "PLAT", "c17", B, sub=1)
node("b_linkA", "linkthrow", "A", "PLAT", "c18", B)
node("b_linkA2", "linkcatch", "A", "PLAT", "d0", B)
node("b_checkout", "task", "Checkout: lead times and add-ons", "PLAT", "d1", B)
node("b_g3", "xor", "Paid?", "PLAT", "d2", B)
node("b_order", "task", "Create order linked to project", "PLAT", "d3", B)
node("s_split", "and", "", "SC", "d4", B)
node("s_stock", "task", "Pick from stock or drop-ship", "SC", "d5", B)
node("s_custom", "task", "Send validated spec; track production", "SC", "d6", B, sub=1)
node("s_join", "and", "", "SC", "d7", B)
node("s_book", "task", "Confirm lead time; book delivery slot", "SC", "d8", B)
node("s_g5", "xor", "Installation ordered?", "SC", "d9", B)
node("s_install", "task", "Book installation on delivery day", "SC", "d10", B)
node("s_track", "task", "Track delivery to promised date", "SC", "d11", B)
node("s_replan", "task", "Warn customer and re-plan", "SC", "d12", B, sub=1)
node("cs_survey", "task", "Send care guide and survey", "CS", "d13", B)
node("cs_g6", "xor", "Issue reported?", "CS", "d14", B)
node("cs_after", "task", "After-sales: replace or remake", "CS", "d15", B)
node("cs_invite", "task", "Invite to next room project", "CS", "d16", B)
node("cs_end", "end", "Room delivered, project open", "CS", "d17", B)

BT = {}
def boundary(i, name, host):
    h = N[host]
    BT[i] = dict(id=i, name=name, host=host, x=h["x"] + h["w"] - EW - 6, y=h["y"] + h["h"] - EW / 2, w=EW, h=EW,
                 proc=B, lane=h["lane"])
boundary("t_render", "> 10 s", "b_render")
boundary("t_late", "Date at risk", "s_track")

BB = {}
def bb(i, name, col):
    BB[i] = dict(id=i, name=name, x=CX[col] - BBW / 2, y=BB_Y, w=BBW, h=BBH)
bb("P_bazar", "BazarChic (campaigns)", "c1")
bb("P_ai", "AI visualisation provider", "c6")
bb("P_pay", "Payment provider", "d1")
bb("P_supp", "Product suppliers", "d5")
bb("P_manu", "Custom manufacturers", "d6")
bb("P_deliv", "Delivery partner", "d8")
bb("P_inst", "Installation partner", "d10")

ALL = {**N, **BT, **BB}
L = lambda i: ALL[i]["x"]; R = lambda i: ALL[i]["x"] + ALL[i]["w"]
T = lambda i: ALL[i]["y"]; Bo = lambda i: ALL[i]["y"] + ALL[i]["h"]
X = lambda i: ALL[i]["x"] + ALL[i]["w"] / 2; Y = lambda i: ALL[i]["y"] + ALL[i]["h"] / 2

SEQ = []
def seq(s, t, pts, name="", lab=None):
    SEQ.append(dict(id=f"f_{s}_{t}", src=s, tgt=t, name=name, pts=pts, lab=lab, proc=ALL[s]["proc"]))
def h(s, t, name=""):
    seq(s, t, [(R(s), Y(s)), (L(t), Y(t))], name, (R(s) + 2, Y(s) - 15) if name else None)
def hv(s, t, name="", dx=0):      # right, then up/down into target
    down = Y(t) > Y(s)
    pts = [(R(s), Y(s)), (X(t) + dx, Y(s)), (X(t) + dx, T(t) if down else Bo(t))]
    seq(s, t, pts, name, (R(s) + 2, Y(s) - 15) if name else None)
def vh(s, t, name="", from_bottom=True):   # down/up from source, then right into target
    sy = Bo(s) if from_bottom else T(s)
    seq(s, t, [(X(s), sy), (X(s), Y(t)), (L(t), Y(t))], name, (X(s) + 4, sy + 1) if name else None)
def via(s, t, yline, name="", dx=0, src_side=None):  # exit top/bottom, run along a margin line, enter top/bottom
    sy = T(s) if yline < Y(s) else Bo(s)
    ty = T(t) if yline < Y(t) else Bo(t)
    seq(s, t, [(X(s), sy), (X(s), yline), (X(t) + dx, yline), (X(t) + dx, ty)], name,
        (X(s) + 4, (sy + yline) / 2 - 7) if name else None)

# customer
h("c_start", "c_visit"); h("c_visit", "c_g0"); h("c_g0", "c_project", "Yes")
via("c_g0", "c_confirm", mbot("CUST"), "No", dx=-24)
h("c_project", "c_compare"); h("c_compare", "c_g1"); h("c_g1", "c_store", "Yes")
via("c_g1", "c_confirm", mtop("CUST"), "No", dx=24)
h("c_store", "c_confirm"); h("c_confirm", "c_linkC"); h("c_linkC2", "c_pay")
h("c_pay", "c_receive"); h("c_receive", "c_survey"); h("c_survey", "c_end")
# bouchara
h("b_start", "b_gp"); h("b_gp", "b_save", "Yes"); via("b_gp", "b_xa", mtop("PLAT"), "No")
h("b_save", "b_suggest"); h("b_suggest", "b_render"); h("b_render", "b_xa")
seq("t_render", "b_fallback", [(X("t_render"), Bo("t_render")), (X("t_render"), Y("b_fallback")), (L("b_fallback"), Y("b_fallback"))])
hv("b_fallback", "b_xa")
h("b_xa", "b_ga")
vh("b_ga", "a_open", "Yes"); h("b_ga", "b_basket", "No")
h("a_open", "a_advise"); h("a_advise", "a_g4"); h("a_g4", "a_validate", "Yes")
via("a_g4", "a_confirm", mbot("ADV"), "No")
h("a_validate", "a_confirm"); hv("a_confirm", "b_basket")
h("b_basket", "b_stock"); h("b_stock", "b_g2")
vh("b_g2", "b_subst", "No"); h("b_g2", "b_linkA", "Yes"); hv("b_subst", "b_linkA")
h("b_linkA2", "b_checkout"); h("b_checkout", "b_g3"); h("b_g3", "b_order", "Yes")
seq("b_g3", "b_checkout", [(X("b_g3"), Bo("b_g3")), (X("b_g3"), cy("PLAT", 1)), (X("b_checkout") - 24, cy("PLAT", 1)),
                           (X("b_checkout") - 24, Bo("b_checkout"))], "No", (X("b_g3") + 4, Bo("b_g3") + 2))
hv("b_order", "s_split")
h("s_split", "s_stock"); vh("s_split", "s_custom")
h("s_stock", "s_join"); hv("s_custom", "s_join")
h("s_join", "s_book"); h("s_book", "s_g5"); h("s_g5", "s_install", "Yes")
seq("s_g5", "s_track", [(X("s_g5"), Bo("s_g5")), (X("s_g5"), cy("SC", 1)), (X("s_track") - 24, cy("SC", 1)),
                        (X("s_track") - 24, Bo("s_track"))], "No", (X("s_g5") + 4, Bo("s_g5") + 2))
h("s_install", "s_track")
seq("t_late", "s_replan", [(X("t_late"), Bo("t_late")), (X("t_late"), Y("s_replan")), (L("s_replan"), Y("s_replan"))])
seq("s_replan", "s_track", [(X("s_replan"), T("s_replan")), (X("s_replan"), mtop("SC")), (X("s_track"), mtop("SC")),
                            (X("s_track"), T("s_track"))])
hv("s_track", "cs_survey", dx=-26)
h("cs_survey", "cs_g6"); h("cs_g6", "cs_after", "Yes")
via("cs_g6", "cs_invite", mbot("CS"), "No")
h("cs_after", "cs_invite"); h("cs_invite", "cs_end")

MSG = []
def msg(s, t, dx=0):
    x_ = X(s) + dx
    if Y(t) > Y(s): pts = [(x_, Bo(s)), (x_, T(t))]
    else: pts = [(x_, T(s)), (x_, Bo(t))]
    MSG.append(dict(id=f"m_{s}_{t}", src=s, tgt=t, pts=pts))
msg("P_bazar", "c_start"); msg("c_visit", "b_start"); msg("c_project", "b_save")
msg("b_render", "P_ai", -30); msg("P_ai", "b_render", -16); msg("b_render", "c_compare")
msg("c_store", "a_open"); msg("c_confirm", "b_basket")
msg("b_checkout", "c_pay", -8); msg("c_pay", "b_checkout", 8)
msg("b_checkout", "P_pay", -8); msg("P_pay", "b_checkout", 8)
msg("s_stock", "P_supp"); msg("s_custom", "P_manu", -8); msg("P_manu", "s_custom", 8)
msg("s_book", "P_deliv", -8); msg("P_deliv", "s_book", 8); msg("s_install", "P_inst")
msg("s_track", "c_receive", -20)
msg("cs_survey", "c_survey", 8); msg("c_survey", "cs_survey", 22)

# ---------------------------------------------------------------- XML
def a(s): return escape(s, {'"': "&quot;"})
o = ['<?xml version="1.0" encoding="UTF-8"?>',
     '<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" '
     'xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" '
     'id="Defs_BoucharaMaison" targetNamespace="http://bouchara-maison/bpmn" exporter="python" exporterVersion="2">',
     '<bpmn:collaboration id="Collab">',
     f'<bpmn:participant id="P_customer" name="Customer" processRef="{C}" />',
     f'<bpmn:participant id="P_bouchara" name="Bouchara Maison" processRef="{B}" />']
o += [f'<bpmn:participant id="{b["id"]}" name="{a(b["name"])}" />' for b in BB.values()]
o += [f'<bpmn:messageFlow id="{m["id"]}" sourceRef="{m["src"]}" targetRef="{m["tgt"]}" />' for m in MSG]
o.append('</bpmn:collaboration>')
TAG = {"task": "task", "xor": "exclusiveGateway", "and": "parallelGateway", "msgstart": "startEvent", "end": "endEvent",
       "msgcatch": "intermediateCatchEvent", "linkthrow": "intermediateThrowEvent", "linkcatch": "intermediateCatchEvent"}
LN = {"PLAT": "Digital platform", "ADV": "Store advisers", "SC": "Supply chain", "CS": "Customer service"}
for proc in (C, B):
    o.append(f'<bpmn:process id="{proc}" isExecutable="false">')
    if proc == B:
        o.append('<bpmn:laneSet id="LS">')
        for ln in LN:
            o.append(f'<bpmn:lane id="Lane_{ln}" name="{LN[ln]}">')
            o += [f'<bpmn:flowNodeRef>{n["id"]}</bpmn:flowNodeRef>' for n in list(N.values()) + list(BT.values())
                  if n["proc"] == B and n["lane"] == ln]
            o.append('</bpmn:lane>')
        o.append('</bpmn:laneSet>')
    for n in N.values():
        if n["proc"] != proc: continue
        body = "".join(f'<bpmn:incoming>{f["id"]}</bpmn:incoming>' for f in SEQ if f["tgt"] == n["id"])
        body += "".join(f'<bpmn:outgoing>{f["id"]}</bpmn:outgoing>' for f in SEQ if f["src"] == n["id"])
        if n["kind"] in ("msgstart", "msgcatch"): body += f'<bpmn:messageEventDefinition id="med_{n["id"]}" />'
        if n["kind"] in ("linkthrow", "linkcatch"): body += f'<bpmn:linkEventDefinition id="led_{n["id"]}" name="{n["name"]}" />'
        o.append(f'<bpmn:{TAG[n["kind"]]} id="{n["id"]}" name="{a(n["name"])}">{body}</bpmn:{TAG[n["kind"]]}>')
    if proc == B:
        for t in BT.values():
            outs = "".join(f'<bpmn:outgoing>{f["id"]}</bpmn:outgoing>' for f in SEQ if f["src"] == t["id"])
            o.append(f'<bpmn:boundaryEvent id="{t["id"]}" name="{a(t["name"])}" attachedToRef="{t["host"]}">{outs}'
                     f'<bpmn:timerEventDefinition id="ted_{t["id"]}" /></bpmn:boundaryEvent>')
    for f in SEQ:
        if f["proc"] != proc: continue
        nm = f' name="{f["name"]}"' if f["name"] else ""
        o.append(f'<bpmn:sequenceFlow id="{f["id"]}"{nm} sourceRef="{f["src"]}" targetRef="{f["tgt"]}" />')
    o.append('</bpmn:process>')
o.append('<bpmndi:BPMNDiagram id="Diagram"><bpmndi:BPMNPlane id="Plane" bpmnElement="Collab">')
def shape(el, x, y, w, h, extra=""):
    o.append(f'<bpmndi:BPMNShape id="{el}_di" bpmnElement="{el}"{extra}><dc:Bounds x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" /></bpmndi:BPMNShape>')
shape("P_customer", 40, LANE["CUST"]["y"], WIDTH_CONTENT - 40, LANE["CUST"]["h"], ' isHorizontal="true"')
shape("P_bouchara", 10, POOL_Y, WIDTH_CONTENT - 10, POOL_H, ' isHorizontal="true"')
for ln in LN:
    shape(f"Lane_{ln}", 40, LANE[ln]["y"], WIDTH_CONTENT - 40, LANE[ln]["h"], ' isHorizontal="true"')
for b in BB.values(): shape(b["id"], b["x"], b["y"], b["w"], b["h"], ' isHorizontal="true"')
for n in N.values(): shape(n["id"], n["x"], n["y"], n["w"], n["h"], ' isMarkerVisible="true"' if n["kind"] == "xor" else "")
for t in BT.values(): shape(t["id"], t["x"], t["y"], t["w"], t["h"])
def edge(eid, pts, lab=None):
    wp = "".join(f'<di:waypoint x="{x:.0f}" y="{y:.0f}" />' for x, y in pts)
    lb = f'<bpmndi:BPMNLabel><dc:Bounds x="{lab[0]:.0f}" y="{lab[1]:.0f}" width="22" height="14" /></bpmndi:BPMNLabel>' if lab else ""
    o.append(f'<bpmndi:BPMNEdge id="{eid}_di" bpmnElement="{eid}">{wp}{lb}</bpmndi:BPMNEdge>')
for f in SEQ: edge(f["id"], f["pts"], f["lab"])
for m in MSG: edge(m["id"], m["pts"])
o.append('</bpmndi:BPMNPlane></bpmndi:BPMNDiagram></bpmn:definitions>')
open("bouchara_main_process.bpmn", "w").write("\n".join(o))

KPI = {"c_g0": "K1", "a_open": "K2", "b_order": "K3 K4", "b_checkout": "K6", "b_render": "K8", "b_stock": "K9",
       "b_suggest": "K10", "s_track": "K11", "s_book": "K11", "a_validate": "K12", "s_custom": "K12", "cs_survey": "K13",
       "a_confirm": "K14", "cs_invite": "K16"}
LBL = {n["id"]: (n["name"], n["kind"]) for n in N.values() if n["kind"] != "task" and n["name"]}
LBL.update({t["id"]: (t["name"], "timer") for t in BT.values()})
meta = dict(kpi=KPI, qc=["a_open", "a_validate", "b_stock"], lbl=LBL, width=WIDTH_CONTENT + 10, height=HEIGHT,
            split=SPLIT_X, lanes={ln: [LANE[ln]["y"], LANE[ln]["h"]] for ln in LANE}, bby=BB_Y, bbh=BBH, pooly=POOL_Y, poolh=POOL_H)
json.dump(meta, open("metah.json", "w"))
print("nodes", len(N), "flows", len(SEQ), "msgs", len(MSG), "size", meta["width"], HEIGHT, "split", SPLIT_X)
