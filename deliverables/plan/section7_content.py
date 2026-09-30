"""Text and tables for Section 7, Section 6.3 and Appendix 9.2 (pitch + meta-commentary style)."""
import json

def S7():
    P = []
    n = lambda t: P.append(("N", t, None))
    h = lambda t: P.append(("H2", t, None))
    bl = lambda: P.append(("BL", "", None))
    m = lambda lead, t: P.append(("M", lead + " " + t, lead))
    cap = lambda t: P.append(("C", t, None))
    tab = lambda k: P.append(("T", "", k))

    n("Bouchara Maison will be tested the way a start-up tests a product: a small squad, the company’s own resources, six months with real customers and a clear decision at the end. This section sets out where and when the pilot starts, the work behind it, how long each piece takes, what it costs and how the app keeps improving once customers use it.")
    m("Why a start-up and not a company programme?", "Because the pilot tests a business model, not a delivery plan. The goal is to learn at the lowest cost whether customers buy more, which is what the build-measure-learn loop of a lean start-up is designed for [19]. The squad borrows what Bouchara already has, stores, advisers, suppliers and customer data, instead of rebuilding it; new ventures do best when they partner with the existing business rather than compete with it [20].")
    h("7.1 Where, when and how the pilot starts")
    n("The pilot runs in three stores in the west of France: Nantes, Tours and Vannes.")
    m("Why these three?", "They cover the three market sizes behind the plan: a metro area (Nantes, about 665,000 people), a mid-sized city (Tours, about 304,000) and a small town (Vannes, about 53,000) (Table 21). Results from this mix say something about all 25 stores. All three sit within about 200 km of Nantes, so one delivery and installation partner can serve the whole pilot, which matters because partners, not software, set the pace of the plan (Section 7.3).")
    n("Three similar stores keep trading as usual and act as the control group: Rennes, Orléans and Lorient.")
    m("Why a control group?", "The growth test in Section 4.7 counts only sales that would not have happened anyway. Pairing each pilot store with a store of similar size, Nantes with Rennes (about 483,000), Tours with Orléans (about 300,000) and Vannes with Lorient (about 57,000), separates the effect of the service from seasons, sales periods and local events.")
    n("Work starts on 2 November 2026. Customers get the app and website in April 2027, and the go/no-go decision is taken on 27 September 2027.")
    m("Why these dates?", "Five months is what the partners and product data need (Section 7.3). An April launch keeps the start clear of the January winter sales, which French law fixes as a four-week period from the second Wednesday of January [23]; heavy discounting would distort the purchase data and cut across the one-price rule in Section 4.6. Six months of trading ends in September, so the decision lands before the Christmas peak and a successful service can be extended into it. The summer sales fall inside the pilot, but they affect pilot and control stores alike.")
    n("Customers use a Bouchara Maison app and the same service on the website, configured on a partner’s room-planning platform in about a week.")
    m("Why configure rather than build?", "Room planners and AI visualisation already exist as configurable platforms (Section 3.2). Configuring one takes days; building one would take months and money the test does not need. The real work is connecting the app to product records, stock, checkout and the partners, which is why integration and testing get six weeks against one week for the app itself (Table 18).")
    n("A flat squad of six people from Bouchara’s own teams runs the pilot, with a store champion in each pilot store (Section 6.3).")
    m("Why flat?", "A six-month test needs decisions in days, not in monthly committees. With no layers between the people doing the work and the decisions, the squad sets priorities in one backlog and adjusts every two weeks; the responsibilities in Table 13 still name who is accountable for each activity [21].")
    n("Before launch, every partner signs up to measurable commitments. Each one maps to a KPI in Table 14, so a partner that slips shows up on the weekly dashboard.")
    bl()
    cap("Table 16: Partner commitments in the pilot contracts")
    tab(16)
    m("Why write KPIs into contracts?", "In the process map every partner is a black box (Figure 1): Bouchara cannot manage what happens inside it, only what goes in and what must come back. Service levels are the only lever, and tying them to the pilot KPIs aligns each partner with the customer’s experience.")
    h("7.2 Work breakdown structure")
    n("The pilot breaks down into seven work packages and 27 tasks (Table 17). Each task has one owner and one deliverable, and together the deliverables are the pre-conditions of the process in Section 6.1.")
    m("Why a deliverable-based breakdown?", "Listing outcomes rather than activities makes the plan checkable: when every deliverable exists, the pilot can launch, and nothing is left without an owner [25].")
    bl()
    cap("Table 17: Work breakdown structure of the pilot")
    tab(17)
    h("7.3 Dependencies and time estimates")
    n("The critical path runs through product data, not software. Checking 120 product records takes eight weeks and gates the integration of the app; the platform contract runs alongside with one week to spare, and the manufacturer and delivery contracts with two and four. The app itself takes one week (Table 18).")
    m("How were the durations estimated?", "From the work content and typical lead times: about two hours per product record for a part-time merchandiser, plus supplier replies; four weeks for a platform tender over the Christmas break and two to agree service levels; eight weeks to onboard manufacturers and an installer network, including test orders; ten weeks to build safety stock, our estimate of supplier lead times for home textiles. Staff representatives have one month to give their opinion on a consultation [24], which is why the adviser credit rule follows it. Quotations in discovery confirm or replace each estimate.")
    n("The plan has almost no slack before launch, and we accept that.")
    m("Why accept it?", "Adding slack would push the decision into the Christmas peak. The risk is handled differently: the longest tasks all start the week of Gate 1, and the two-week soft launch with staff and invited customers absorbs a late partner before the public launch on 12 April.")
    bl()
    cap("Table 18: Dependencies and time estimates (week of 2 November 2026 = week 0)")
    tab(18)
    h("7.4 Pilot schedule")
    n("Figure 2 puts the plan on one page: 47 weeks from kick-off to the go/no-go decision, three funding gates and two checkpoints.")
    cap("Figure 2: Pilot schedule from kick-off to the go/no-go decision (critical path outlined)")
    P.append(("I", "", None))
    h("7.5 Budget and staged funding")
    n("The pilot needs about €143,000 in cash, excluding VAT (Table 19). The people come from Bouchara’s own teams.")
    m("Why is it this low?", "The app is configured on a partner platform rather than built, and the squad is staffed from existing teams, so salaries are an opportunity cost rather than new cash. That time is still worth about €170,000 over eleven months and is shown so the sponsor sees the full cost of the test.")
    bl()
    cap("Table 19: Pilot budget by work package, excluding VAT")
    tab(19)
    n("The money is released at three gates: about €5,000 for discovery on 2 November, €72,000 for the build on 14 December once requirements are clear, and €66,000 at launch readiness on 29 March, including the stock reserve.")
    m("Why stage the money?", "Each gate arrives with new facts: requirements, partner quotes, a tested service. Committing in steps limits the loss if a fact turns out badly; the most Bouchara can lose before a customer sees the service is €77,000.")
    n("The service covers its running costs at about 104 extra orders a month, roughly one extra room order per pilot store per day.")
    m("How is that calculated?", "Recurring costs are about €14,500 a month: €6,000 in cash plus the squad lead and data analyst. With an average room order of about €300, a 55% gross margin and about €25 of variable service cost, each extra order contributes about €140, and €14,500 ÷ €140 ≈ 104. Order value and margin are assumptions to replace with Bouchara’s figures in discovery; K15 tracks the real number from the first month.")
    h("7.6 Building the app: product backlog and sprints")
    n("Once live, the app improves in two-week sprints from one ordered backlog owned by the squad lead. Table 20 shows the first version: each item serves a KPI, and nothing enters a sprint without one.")
    m("Why sprints and a single backlog?", "Short fixed cycles, each ending in a review, turn the weekly dashboard into decisions quickly, and one backlog owner stops competing requests from stores, merchandising and partners from stalling the team [22]. An item is done only when it works end to end with the partner involved and its KPI appears on the dashboard.")
    bl()
    cap("Table 20: Product backlog for the pilot")
    tab(20)
    m("Why prioritise this way?", "The launch version holds only what the process in Figure 1 cannot work without. Everything else waits for evidence: the Could items enter only if checkpoint 1 shows the core is working.")
    h("7.7 Checkpoints and what happens next")
    n("At month 3 (28 June 2027) the squad reports whether the process works: planner use, preview speed, room completeness and hand-off quality. At month 6 (27 September 2027) the sponsor decides whether to extend, adjust or stop.")
    m("Why agree the stop criteria now?", "Deciding them after the results arrive invites moving the goalposts. The criteria are the targets in Table 14: if contribution per session is not at least 10% higher than in the control stores and there is no credible route to covering fixed costs, the pilot stops, open orders are delivered and after-sales honoured.")
    n("If the pilot passes, a first wave adds seven stores in the west and centre, including the three control stores, before the Christmas peak; the rest follow in 2028, each wave once the previous one covers its fixed costs for three consecutive months.")
    m("Why the west first?", "The delivery and installation partner, sample suppliers and trained champions are already there, so the first wave reuses the pilot’s contracts instead of starting new ones.")
    return P

def S63():
    P = []
    n = lambda t: P.append(("N", t, None))
    bl = lambda: P.append(("BL", "", None))
    m = lambda lead, t: P.append(("M", lead + " " + t, lead))
    n("Bouchara Maison is run by a flat squad set up like a start-up inside the company. Six people come from Bouchara’s own teams: a squad lead (the pilot lead in Table 13 and Figure 1) who owns the budget, backlog and KPIs, a digital lead, a merchandiser, a supply chain coordinator, a customer service lead and a data analyst. A store champion in each pilot store connects the squad with the advisers. There are no management layers inside the squad: priorities sit in one backlog, and decisions are taken in the weekly review rather than escalated.")
    m("Why flat and not functional or matrix?", "Of the four structures in the framework (functional, divisional, flatarchy and matrix), a functional set-up leaves nobody owning the journey across online, store and supply chain, and a matrix sends every decision through two reporting lines. A flat squad trades hierarchy for speed, which suits a six-month test run by a small team. Its known weakness, unclear accountability, is covered by Table 13, which still names one accountable owner per activity [20][21].")
    n("The squad borrows rather than hires. Advisers stay in their stores and their managers keep line responsibility; the squad books their time and credits them for online orders they helped close. The takeover retained 184 employees [1], so store managers confirm appointment capacity and training cover before launch, and staff representatives are consulted on the new routines (Section 7.2).")
    m("Why borrow?", "The stores, advisers and supplier relationships are what make the service hard to copy. Rebuilding them in a separate unit would cost more and cut the link that makes the model work [20].")
    bl()
    return P

def S92():
    P = []
    n = lambda t: P.append(("N", t, None))
    bu = lambda t: P.append(("B", t, None))
    n("The €143,000 cash budget in Section 7.5 is built bottom-up from the work breakdown in Table 17 with these assumptions:")
    for t in ["Implementation day rate of €750 (18 days of integration work).",
              "€75 per product record (120 records) and €2,000 of samples per store.",
              "Adviser cover at €35 an hour (12 advisers, 8 hours of training each).",
              "Running costs of €6,000 a month in cash: software and AI €2,500, adviser cover €1,500, campaigns €1,000, product data upkeep €1,000.",
              "Squad time of about €170,000 over eleven months (squad lead full time, other members part time), reassigned from existing roles and not counted as new cash.",
              "Break-even: average room order of €300, 55% gross margin and €25 of variable service cost per order."]:
        bu(t)
    n("All figures are estimates to confirm with quotations and Bouchara’s own data during discovery.")
    return P

TABLES = {
 16: [["Partner", "What they commit to", "KPI"],
      ["Room-planning and AI platform", "App and website configured in one week; first preview within 5 s and full render within 10 s for 90% of requests; at least 98% of renders delivered", "K8"],
      ["Custom manufacturers", "Confirm every validated specification before cutting; a fixed lead-time window per product; remakes at their cost when the error is theirs", "K11, K12"],
      ["Delivery and installation partner (western France)", "Delivery on the date promised at checkout; installation on the same visit; photo proof of completion", "K6, K11"],
      ["Product suppliers", "Replenishment lead times that hold 98% availability on the 120 pilot products", "K9"],
      ["Payment provider", "Real-time payment confirmation at checkout", "K3"]],
 19: [["Work package", "Cash", "Basis"],
      ["1. Set-up and governance", "€1,500", "Charter workshop; documents for staff representatives"],
      ["2. Discovery", "€3,000", "Incentives for 12 customer interviews; adviser workshops"],
      ["3. Partners", "€10,000", "Manufacturer test orders €5,000; installer onboarding €3,000; legal review €2,000"],
      ["4. Products and stock", "€15,000", "120 product records at €75; samples at €2,000 per store"],
      ["5. App and web", "€33,000", "Platform set-up including app and website €15,000; 18 integration days at €750; dashboard €4,500"],
      ["6. Stores and people", "€4,500", "Training cover for 12 advisers, 8 hours each at €35; materials"],
      ["7. Launch and run", "€40,000", "Soft launch and invitations €4,000; six months at €6,000 (software and AI, adviser cover, campaigns, data upkeep)"],
      ["Contingency", "€16,000", "15% of the work packages"],
      ["Safety-stock reserve", "€20,000", "98% availability on the pilot range (K9)"],
      ["Total cash", "€143,000", "Excluding VAT; squad time of about €170,000 comes from existing roles"]],
 20: [["Priority", "Backlog item", "KPI"],
      ["Must (launch)", "Save, share and reopen a room project in the app, on the website and in store", "K1, K2"],
      ["Must (launch)", "Three options rendered in parallel, fast preview first, photo fallback after 10 s", "K8"],
      ["Must (launch)", "Room-level stock and date check with substitute, split delivery or wait date", "K9"],
      ["Must (launch)", "Checkout with lead time per line, installation option and custom terms", "K6, K11"],
      ["Must (launch)", "Adviser view with the custom-specification checklist", "K12, K14"],
      ["Must (launch)", "Event tracking that separates planner and direct shoppers", "K1, K5"],
      ["Should (sprints 1 to 4)", "Sample ordering from the project", "K3"],
      ["Should (sprints 1 to 4)", "Delivery and installation tracking notifications", "K11"],
      ["Should (sprints 1 to 4)", "Post-delivery survey and next-room invitation", "K13, K16"],
      ["Could (after checkpoint 1)", "Room photo upload for AI previews", "K8"],
      ["Could (after checkpoint 1)", "BazarChic campaign landing page", "K1"],
      ["Won’t (in the pilot)", "B2B trade accounts; augmented-reality measuring", "–"]],
}
plan = json.load(open("plan.json"))
WP = plan["wp"]
t17 = [["ID", "Task", "Deliverable", "Owner"]]
t18 = [["ID", "Depends on", "Weeks", "Start", "Finish", "Basis of estimate"]]
for wp in range(1, 8):
    t17.append([str(wp), WP[str(wp)], "", ""])
    for t in plan["tasks"]:
        if t["wp"] == wp:
            t17.append([t["id"], t["name"], t["deliverable"], t["owner"]])
for t in plan["tasks"]:
    preds = ", ".join(t["preds"]) or "–"
    basis = t["basis"].replace("About 20 implementation days", "About 18 implementation days")
    if t["wp"] == 0:
        t18.append([t["id"], preds, "–", t["start"], "–", t["name"]])
    else:
        t18.append([t["id"], preds, str(t["weeks"]), t["start"], t["finish"], basis])
TABLES[17] = t17
TABLES[18] = t18
