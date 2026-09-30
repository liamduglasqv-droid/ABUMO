import json, datetime as dt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Patch
from matplotlib.lines import Line2D
import matplotlib.dates as mdates

P = json.load(open("plan.json"))
T0 = dt.date.fromisoformat(P["t0"])
COL = {1: "#2a78d6", 2: "#eb6834", 3: "#1baf7a", 4: "#eda100", 5: "#e87ba4", 6: "#008300", 7: "#4a3aa7"}
INK, MUTED, GRID = "#1f1f1e", "#6b6a64", "#e4e3dc"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.2})

tasks = [t for t in P["tasks"] if t["wp"]]
miles = [t for t in P["tasks"] if not t["wp"]]
rows = [("hdr", "Gates and checkpoints", None)]
for wp in range(1, 8):
    rows.append(("hdr", f'{wp}. {P["wp"][str(wp)]}', wp))
    rows += [("task", t, wp) for t in tasks if t["wp"] == wp]
n = len(rows)
fig, ax = plt.subplots(figsize=(10.0, 7.15), dpi=300)
fig.subplots_adjust(left=0.335, right=0.975, top=0.955, bottom=0.085)
d = lambda w: mdates.date2num(T0 + dt.timedelta(weeks=w))
x0, x1 = d(-0.3), d(51.5)
ax.set_xlim(x0, x1); ax.set_ylim(n - 0.4, -0.7)
ax.xaxis.set_major_locator(mdates.MonthLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
ax.xaxis.tick_top(); ax.tick_params(axis="x", length=0, colors=MUTED, labelsize=7)
ax.grid(axis="x", color=GRID, lw=0.6); ax.set_axisbelow(True)
for s in ax.spines.values(): s.set_visible(False)
ax.set_yticks([])
# pilot window shading
ax.axvspan(d(21), d(47), color="#f3f1fb", zorder=0)
ax.text(d(34), n - 0.55, "Pilot open to customers (6 months)", ha="center", va="bottom", color="#4a3aa7", fontsize=7)
for i, (kind, obj, wp) in enumerate(rows):
    if kind == "hdr":
        ax.text(x0 - (x1 - x0) * 0.50, i, obj, ha="left", va="center", fontweight="bold", color=INK, fontsize=7.6, clip_on=False)
        if i: ax.axhline(i - 0.5, color=GRID, lw=0.6)
        continue
    t = obj
    ax.text(x0 - (x1 - x0) * 0.495, i, f'{t["id"]}  {t["name"]}', ha="left", va="center", color=INK, clip_on=False)
    a, b = d(t["es"]), d(t["ef"]) - 0.35
    ax.barh(i, b - a, left=a, height=0.56, color=COL[wp], edgecolor=INK if t["crit"] else COL[wp],
            linewidth=1.3 if t["crit"] else 0, zorder=3)
    ax.text(b + 1.2, i, f'{t["weeks"]} wk', va="center", ha="left", color=MUTED, fontsize=6.5)
# milestones on row 0
for m in miles:
    x = d(m["es"])
    ax.plot([x], [0], marker="D", ms=6.5, color=INK, zorder=4)
    ax.axvline(x, color=INK, lw=0.5, ls=(0, (2, 2)), zorder=1)
lab = {"M0": "Gate 0\n2 Nov", "M1": "Gate 1\n14 Dec", "M2": "Gate 2 · launch\n29 Mar", "M3": "Checkpoint 1\n28 Jun", "M4": "Go/no-go\n27 Sep"}
for m in miles:
    ax.text(d(m["es"]) + 1.5, 0, lab[m["id"]], va="center", ha="left", fontsize=6.4, color=INK, linespacing=0.95,
            bbox=dict(fc="white", ec="none", pad=0.2))
handles = [Patch(fc=COL[w], label=P["wp"][str(w)]) for w in range(1, 8)]
handles += [Patch(fc="white", ec=INK, lw=1.3, label="Critical path"), Line2D([], [], marker="D", color=INK, lw=0, label="Gate / checkpoint")]
fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False, fontsize=6.8, bbox_to_anchor=(0.62, 0.0),
           handlelength=1.2, columnspacing=1.0)
fig.savefig("gantt.png", dpi=300)
print("ok", n)
