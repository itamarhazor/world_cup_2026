import csv
import re
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams

# ── rankings from leaderboard ─────────────────────────────────────────────────
RANKINGS = {
    "יוסי": 1, "אילן": 2, "אמיתי": 2, "ברק": 2, "דרור": 2, "הקוף": 2,
    "אלעד": 7, "ChatGPT": 8, "שלו": 9, "אברגל": 10,
    "Grok": 11, "גיא": 11, "יאיר": 11,
    "אוחיון": 14, "משה": 14, "קדמי": 14,
    "Claude": 17, "Gemini": 17, "ליחי": 17,
    "אבי": 20, "אבישי": 20, "יונתן": 20,
    "אביבה": 23, "המתחכם": 23,
    "אביתר": 25, "יואב": 25, "ליעד": 25, "ניסן": 25, "שלומי": 25,
    "אריה": 30, "בןמשה": 30,
    "עוזיה": 32,
    "איתמר": 33, "גיל": 33,
}

PARTICIPANTS = [
    "גיא","יואב","ליעד","אלעד","אביבה","עוזיה","אריה","משה","בןמשה","שלו",
    "אבי","ליחי","קדמי","שלומי","אמיתי","יוסי","אבישי","אברגל","גיל","אוחיון",
    "אילן","ניסן","יונתן","ברק","דרור","יאיר","איתמר","אביתר",
    "הקוף","המתחכם","Gemini","Claude","Grok","ChatGPT",
]
AI_NAMES = {"Gemini", "Claude", "Grok", "ChatGPT"}

# ── draw counts ───────────────────────────────────────────────────────────────
with open("World_Cup_Bets.csv", encoding="utf-8") as f:
    rows = list(csv.reader(f))

draw_counts: dict[str, int] = {}
for i, name in enumerate(PARTICIPANTS):
    col = 2 + i * 2
    draws = 0
    for row in rows[9:114]:
        if not row[0].startswith("מ"):
            continue
        bet = row[col] if col < len(row) else ""
        m = re.match(r"^\s*(\d+)\s*-\s*(\d+)\s*$", bet)
        if m and m.group(1) == m.group(2):
            draws += 1
    draw_counts[name] = draws

# ── build paired vectors ───────────────────────────────────────────────────────
names, draws_v, rank_v = [], [], []
for name in PARTICIPANTS:
    if name in RANKINGS:
        names.append(name)
        draws_v.append(draw_counts[name])
        rank_v.append(RANKINGS[name])

n = len(names)

# ── statistics ────────────────────────────────────────────────────────────────
def mean(v): return sum(v) / len(v)
def std(v):
    m = mean(v)
    return math.sqrt(sum((x - m) ** 2 for x in v) / len(v))
def pearson(x, y):
    mx, my = mean(x), mean(y)
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    den = math.sqrt(sum((xi - mx)**2 for xi in x) * sum((yi - my)**2 for yi in y))
    return num / den if den else 0

def spearman(x, y):
    def rank_vec(v):
        sorted_v = sorted(enumerate(v), key=lambda t: t[1])
        r = [0.0] * len(v)
        i = 0
        while i < len(sorted_v):
            j = i
            while j < len(sorted_v) - 1 and sorted_v[j+1][1] == sorted_v[j][1]:
                j += 1
            avg_rank = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[sorted_v[k][0]] = avg_rank
            i = j + 1
        return r
    rx, ry = rank_vec(x), rank_vec(y)
    return pearson(rx, ry)

def t_stat(r, n):
    if abs(r) == 1: return float("inf")
    return r * math.sqrt(n - 2) / math.sqrt(1 - r**2)

r_p  = pearson(draws_v, rank_v)
r_s  = spearman(draws_v, rank_v)
t_p  = t_stat(r_p, n)
t_s  = t_stat(r_s, n)

# simple OLS line for scatter
mx, my = mean(draws_v), mean(rank_v)
slope = sum((x - mx)*(y - my) for x,y in zip(draws_v, rank_v)) / sum((x-mx)**2 for x in draws_v)
intercept = my - slope * mx

print(f"n = {n}")
print(f"Pearson r  = {r_p:.4f}  (t = {t_p:.2f})")
print(f"Spearman ρ = {r_s:.4f}  (t = {t_s:.2f})")
print(f"OLS: rank = {slope:.3f} × draws + {intercept:.3f}")

# ── plot ──────────────────────────────────────────────────────────────────────
rcParams["font.family"] = "Arial"
AXIS_BG = "#0F172A"
PANEL_BG = "#1E293B"
HUMAN_C  = "#3B82F6"
AI_C     = "#F59E0B"
LINE_C   = "#EF4444"
GRID_C   = "#334155"

fig, ax = plt.subplots(figsize=(13, 8))
fig.patch.set_facecolor(AXIS_BG)
ax.set_facecolor(PANEL_BG)

# regression line
x_line = [min(draws_v) - 0.5, max(draws_v) + 0.5]
y_line = [slope * x + intercept for x in x_line]
ax.plot(x_line, y_line, color=LINE_C, linewidth=2, linestyle="--",
        alpha=0.7, zorder=2, label="קו מגמה (OLS)")

# scatter points
for name, d, r in zip(names, draws_v, rank_v):
    color = AI_C if name in AI_NAMES else HUMAN_C
    ax.scatter(d, r, color=color, s=90, zorder=3, edgecolors="white",
               linewidths=0.5, alpha=0.92)
    # label – nudge to avoid overlap
    offset_x, offset_y = 0.25, -0.5
    ax.annotate(name, (d, r), (d + offset_x, r + offset_y),
                fontsize=8, color="white", va="center",
                textcoords="data")

# axes
ax.set_xlabel("מספר תיקו מהוימר (מתוך 72)", color="white", fontsize=12, labelpad=8)
ax.set_ylabel("מיקום בטבלה (1 = מקום ראשון)", color="white", fontsize=12, labelpad=8)
ax.tick_params(colors="#94A3B8", labelsize=10)
ax.invert_yaxis()   # rank 1 at top

for spine in ax.spines.values():
    spine.set_color(GRID_C)
ax.xaxis.grid(True, color=GRID_C, linewidth=0.6, zorder=0)
ax.yaxis.grid(True, color=GRID_C, linewidth=0.6, zorder=0)

# annotation box
direction = "חיובית" if r_s > 0 else "שלילית"
strength = "חלשה" if abs(r_s) < 0.2 else ("בינונית" if abs(r_s) < 0.4 else "חזקה")
box_txt = (
    f"Pearson r  = {r_p:+.3f}\n"
    f"Spearman ρ = {r_s:+.3f}\n"
    f"קורלציה {direction} {strength}\n"
    f"n = {n} משתתפים"
)
ax.text(0.02, 0.97, box_txt, transform=ax.transAxes,
        fontsize=10, color="white", va="top", ha="left",
        bbox=dict(boxstyle="round,pad=0.5", facecolor=AXIS_BG, edgecolor=GRID_C, alpha=0.9))

# legend
human_p = mpatches.Patch(color=HUMAN_C, label="משתתפים")
ai_p    = mpatches.Patch(color=AI_C,    label="מנועי AI")
ax.legend(handles=[human_p, ai_p, ax.get_lines()[0]],
          facecolor=AXIS_BG, edgecolor=GRID_C, labelcolor="white", fontsize=10,
          loc="lower right")

fig.text(0.5, 0.97,
         "האם יותר הימורי תיקו = מיקום גבוה יותר?",
         ha="center", va="top", fontsize=15, color="white", fontweight="bold")
fig.text(0.5, 0.942,
         "קורלציה בין מספר תיקו מהוימר לבין מיקום בטבלה — שלב הבתים",
         ha="center", va="top", fontsize=10, color="#94A3B8")

plt.tight_layout(rect=[0, 0, 1, 0.94])
out = "visuals/draw_correlation.png"
plt.savefig(out, dpi=160, bbox_inches="tight", facecolor=AXIS_BG)
print(f"Saved → {out}")
