import csv
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams

# ── data ──────────────────────────────────────────────────────────────────────
PARTICIPANTS = [
    "גיא","יואב","ליעד","אלעד","אביבה","עוזיה","אריה","משה","בןמשה","שלו",
    "אבי","ליחי","קדמי","שלומי","אמיתי","יוסי","אבישי","אברגל","גיל","אוחיון",
    "אילן","ניסן","יונתן","ברק","דרור","יאיר","איתמר","אביתר",
    "הקוף","המתחכם",
    "Gemini","Claude","Grok","ChatGPT",
]
AI_NAMES = {"Gemini", "Claude", "Grok", "ChatGPT"}

# Group stage: rows 10–114 (1-indexed) → 0-indexed 9–113
GS_START, GS_END = 9, 114

def is_draw(bet: str) -> bool:
    m = re.match(r"^\s*(\d+)\s*-\s*(\d+)\s*$", bet)
    return bool(m) and m.group(1) == m.group(2)

with open("World_Cup_Bets.csv", encoding="utf-8") as f:
    rows = list(csv.reader(f))

draw_counts: dict[str, int] = {}
match_counts: dict[str, int] = {}

for i, name in enumerate(PARTICIPANTS):
    col = 2 + i * 2
    draws = 0
    matches = 0
    for row in rows[GS_START:GS_END]:
        if not row[0].startswith("מ"):   # skip header / separator rows
            continue
        bet = row[col] if col < len(row) else ""
        m = re.match(r"^\s*(\d+)\s*-\s*(\d+)\s*$", bet)
        if m:
            matches += 1
            if m.group(1) == m.group(2):
                draws += 1
    draw_counts[name] = draws
    match_counts[name] = matches

# sort descending by draws, then name
ranked = sorted(PARTICIPANTS, key=lambda n: (-draw_counts[n], n))

# ── plot ──────────────────────────────────────────────────────────────────────
rcParams["font.family"] = "Arial"          # good Unicode coverage
FIG_W, BAR_H = 14, 0.55
N = len(ranked)
fig, ax = plt.subplots(figsize=(FIG_W, N * BAR_H + 2.5))

HUMAN_COLOR = "#3B82F6"    # blue
AI_COLOR    = "#F59E0B"    # amber
AXIS_BG     = "#0F172A"    # dark navy
BAR_BG      = "#1E293B"    # slightly lighter

fig.patch.set_facecolor(AXIS_BG)
ax.set_facecolor(AXIS_BG)

max_draws = max(draw_counts.values()) if draw_counts else 1

for rank, name in enumerate(ranked):
    y = N - rank - 1
    count = draw_counts[name]
    color = AI_COLOR if name in AI_NAMES else HUMAN_COLOR

    # background track
    ax.barh(y, 72, left=0, color=BAR_BG, height=0.75, zorder=1)
    # actual bar
    ax.barh(y, count, left=0, color=color, height=0.75, alpha=0.9, zorder=2)

    # rank badge
    ax.text(-1.2, y, f"#{rank+1}", ha="right", va="center",
            fontsize=9, color="#94A3B8", fontweight="bold")

    # name (RTL-friendly: just right-align on left side)
    ax.text(-2.5, y, name, ha="right", va="center",
            fontsize=11, color="white", fontweight="bold")

    # count label inside / just outside bar
    label_x = count + 0.4 if count < 68 else count - 0.4
    ha = "left" if count < 68 else "right"
    ax.text(label_x, y, str(count), ha=ha, va="center",
            fontsize=11, color="white", fontweight="bold")

# x-axis style
ax.set_xlim(-14, 75)
ax.set_ylim(-0.8, N - 0.2)
ax.set_xticks(range(0, 73, 6))
ax.tick_params(axis="x", colors="#64748B", labelsize=9)
ax.tick_params(axis="y", left=False, labelleft=False)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.xaxis.grid(True, color="#334155", linewidth=0.5, zorder=0)
ax.set_axisbelow(True)

# legend
human_patch = mpatches.Patch(color=HUMAN_COLOR, label="משתתפים")
ai_patch    = mpatches.Patch(color=AI_COLOR,    label="מנועי AI")
ax.legend(handles=[human_patch, ai_patch], loc="lower right",
          facecolor=BAR_BG, edgecolor="none", labelcolor="white", fontsize=10)

# title
fig.text(0.5, 0.985, "כמה תיקו הימר כל משתתף? — שלב הבתים (72 משחקים)",
         ha="center", va="top", fontsize=15, color="white", fontweight="bold")
fig.text(0.5, 0.965, "מיון יורד לפי מספר תיקו",
         ha="center", va="top", fontsize=10, color="#94A3B8")

plt.tight_layout(rect=[0, 0, 1, 0.96])
out = "visuals/draw_ranking.png"
plt.savefig(out, dpi=160, bbox_inches="tight", facecolor=AXIS_BG)
print(f"Saved → {out}")
