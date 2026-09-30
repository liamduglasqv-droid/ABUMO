"""Bouchara Maison pilot plan: WBS, dependencies, forward-pass schedule, tables and Gantt."""
import json, datetime as dt

T0 = dt.date(2026, 11, 2)  # week 0 = Monday 2 Nov 2026
WP = {1: "Set-up and governance", 2: "Discovery", 3: "Partners", 4: "Products and stock",
      5: "App and web", 6: "Stores and people", 7: "Launch and run"}
# id, wp, task, deliverable, owner, preds, weeks, basis
TASKS = [
 ("M0", 0, "Gate 0: discovery funding released", "", "Sponsor", [], 0, ""),
 ("1.1", 1, "Kick-off, squad set-up and pilot charter", "Charter: scope, KPIs, stop criteria", "Squad lead", ["M0"], 1, "One workshop week"),
 ("1.2", 1, "Inform and consult staff representatives (CSE)", "CSE opinion on the new routines", "Squad lead with HR", ["1.1"], 5, "One-month legal opinion period plus preparation"),
 ("2.1", 2, "Customer interviews (12) and adviser workshops", "Validated journey and pain points", "Squad lead", ["1.1"], 3, "Four interviews and one workshop a week"),
 ("2.2", 2, "Requirements from the process map", "Process, data and partner specifications", "Digital lead", ["2.1"], 2, "Derived from Figure 1 and Table 11"),
 ("M1", 0, "Gate 1: build funding released", "", "Sponsor", ["2.2"], 0, ""),
 ("1.3", 1, "KPI definitions, baseline and control stores", "K1-K16 defined; 12-month baseline", "Data analyst", ["2.2"], 3, "Data extraction for six stores"),
 ("3.1", 3, "Select platform and AI partner (tender, 3 quotes)", "Chosen partner", "Digital lead", ["M1"], 4, "Tender over the Christmas break"),
 ("3.2", 3, "Contract platform and AI partner with service levels", "Signed contract with K8 targets", "Squad lead", ["3.1"], 2, "Negotiation and legal review"),
 ("3.3", 3, "Onboard custom manufacturers", "Spec checklist, lead times, remake terms", "Supply chain coordinator", ["M1"], 8, "Test orders with each manufacturer"),
 ("3.4", 3, "Contract delivery and installation partner (west)", "Signed contract with K11 and K6 targets", "Supply chain coordinator", ["M1"], 8, "Tender, contract, installer briefing"),
 ("3.5", 3, "Set up payment provider", "Live payment account", "Digital lead", ["3.2"], 1, "Standard onboarding"),
 ("4.1", 4, "Select the 120 pilot products", "Pilot range list", "Merchandiser", ["2.1"], 2, "Four room needs, best sellers first"),
 ("4.2", 4, "Build and verify 120 product records", "100% checked records (K10)", "Merchandiser", ["4.1"], 8, "About 2 hours per record plus supplier replies"),
 ("4.3", 4, "Write styling rules", "Rules for coordinated suggestions", "Merchandiser", ["4.1"], 4, "Adviser know-how written as rules"),
 ("4.4", 4, "Build safety stock to 98% availability", "Pilot range in stock (K9)", "Supply chain coordinator", ["4.1"], 10, "Estimated supplier lead time"),
 ("4.5", 4, "Sample kits for the three stores", "Fabric and finish samples in store", "Merchandiser", ["3.3"], 4, "Manufacturer samples"),
 ("5.1", 5, "Configure app and web on the partner platform", "Working app and website (MVP)", "Digital lead", ["3.2"], 1, "Configuration, not development"),
 ("5.2", 5, "Integrate records, stock, checkout and partner systems", "Connected end-to-end flow", "Digital lead", ["5.1", "3.5", "4.2"], 4, "About 20 implementation days"),
 ("5.3", 5, "End-to-end tests: standard, custom, mixed, after-sales", "Test report, no blocking defects", "Digital lead", ["5.2", "3.3", "3.4"], 2, "Test script from Figure 1"),
 ("5.4", 5, "KPI dashboard and event tracking", "Weekly dashboard, pilot vs control", "Data analyst", ["5.1", "1.3"], 3, "Events from the backlog"),
 ("6.1", 6, "Adviser credit for assisted online orders", "Agreed credit rule", "Squad lead with HR", ["1.2"], 2, "After CSE opinion"),
 ("6.2", 6, "Train 12 advisers and name store champions", "Trained advisers, 3 champions", "Store champions", ["5.2"], 2, "8 hours per adviser"),
 ("6.3", 6, "Staff dry run in the three stores", "Real orders placed by staff", "Store champions", ["5.3", "6.2", "4.5"], 1, "One week of internal orders"),
 ("M2", 0, "Gate 2: launch readiness", "", "Sponsor", ["6.3", "4.4", "5.4", "6.1", "4.3"], 0, ""),
 ("7.1", 7, "Soft launch: staff and 200 invited customers", "First saved projects and orders", "Squad lead", ["M2"], 2, "Buffer to absorb a late partner"),
 ("7.2", 7, "Public launch and customer invitations", "Service open in app, web and stores", "Squad lead", ["7.1"], 1, "Email to existing customers"),
 ("7.3", 7, "Run the pilot in two-week sprints", "Weekly dashboard, sprint reviews", "Whole squad", ["M2"], 26, "Six months of trading"),
 ("M3", 0, "Checkpoint 1 (month 3)", "", "Sponsor", ["M2"], 13, ""),
 ("M4", 0, "Checkpoint 2: go/no-go", "", "Sponsor", ["7.3"], 0, ""),
]
by = {t[0]: t for t in TASKS}
ES, EF = {}, {}
for t in TASKS:
    tid, wp, name, dl, ow, preds, dur, basis = t
    es = max([EF[p] for p in preds], default=0)
    if tid == "M3": ES[tid] = EF["M2"] + 13; EF[tid] = ES[tid]; continue
    ES[tid], EF[tid] = es, es + dur
# critical path (backward pass)
end = EF["M4"]
LF = {tid: end for tid in by}
for t in reversed(TASKS):
    tid = t[0]
    succ = [s for s in TASKS if tid in s[5]]
    if succ: LF[tid] = min(LF[s[0]] - s[6] for s in succ)
    if tid == "M3": LF[tid] = ES[tid]; LS_fix = True
LS = {tid: LF[tid] - by[tid][6] for tid in by}
CRIT = {tid for tid in by if LS[tid] - ES[tid] == 0 and tid != "M3"}
def d(w): return T0 + dt.timedelta(weeks=w)
def fmt(x): return f"{x.day} {x.strftime('%b')} {x.year % 100:02d}"
out = []
for t in TASKS:
    tid = t[0]
    out.append(dict(id=tid, wp=t[1], name=t[2], deliverable=t[3], owner=t[4], preds=t[5], weeks=t[6], basis=t[7],
                    es=ES[tid], ef=EF[tid], start=fmt(d(ES[tid])), finish=fmt(d(EF[tid]) - dt.timedelta(days=3)) if t[6] else fmt(d(ES[tid])),
                    slack=LS[tid] - ES[tid], crit=tid in CRIT))
json.dump(dict(tasks=out, wp=WP, t0=str(T0)), open("plan.json", "w"), indent=1)
for o in out: print(f'{o["id"]:4} wk{o["es"]:>2}-{o["ef"]:>2} {o["start"]:>10} → {o["finish"]:>10} slack {o["slack"]:>2} {"CRIT" if o["crit"] else ""}  {o["name"]}')
