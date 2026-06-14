import csv
from collections import defaultdict

CSV_PATH = "World_Cup_Bets.csv"
OUT_DIR = "visuals/group_standings"

GROUPS = {
    "A": (119, 122),
    "B": (126, 129),
    "C": (133, 136),
    "D": (140, 143),
    "E": (147, 150),
    "F": (154, 157),
    "G": (161, 164),
    "H": (168, 171),
    "I": (175, 178),
    "J": (182, 185),
    "K": (189, 192),
    "L": (196, 199),
}

RANK_ICONS = ["🥇", "🥈", "🥉", "4"]

with open(CSV_PATH, encoding="utf-8") as f:
    rows = list(csv.reader(f))

header = rows[0]
participants = [(i, header[i]) for i in range(2, len(header), 2)]


def get_group_data(start_row, end_row):
    """Return list of (participant_name, (p1, p2, p3, p4)) for the group."""
    rank_rows = [rows[r] for r in range(start_row, end_row + 1)]
    result = []
    for col_idx, name in participants:
        combo = tuple(rank_rows[pos][col_idx].strip() for pos in range(4))
        if all(combo):
            result.append((name, combo))
    return result


def build_combinations(group_data):
    """Group participants by their combo, return sorted by count desc."""
    combo_map = defaultdict(list)
    for name, combo in group_data:
        combo_map[combo].append(name)
    return sorted(combo_map.items(), key=lambda x: -len(x[1]))


def generate_html(group_letter, combinations):
    group_name = f"בית {group_letter}"
    total = sum(len(names) for _, names in combinations)

    cards_html = ""
    for combo, names in combinations:
        count = len(names)
        rank_rows_html = ""
        for i, team in enumerate(combo):
            icon = RANK_ICONS[i]
            is_fourth = i == 3
            rank_rows_html += f"""
            <div class="rank-row {'fourth' if is_fourth else ''}">
                <span class="rank-icon">{icon}</span>
                <span class="team-name">{team}</span>
            </div>"""

        chips_html = "".join(
            f'<span class="chip">{n}</span>' for n in names
        )

        cards_html += f"""
        <div class="combo-card">
            <div class="vote-badge">{count} / {total}</div>
            <div class="ranks">{rank_rows_html}
            </div>
            <div class="chips">{chips_html}</div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{group_name} – סדר הבית</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: 'Segoe UI', Arial, sans-serif;
    background: #0d1117;
    color: #e6edf3;
    min-height: 100vh;
    padding: 32px 24px;
    direction: rtl;
  }}

  h1 {{
    text-align: center;
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 8px;
    color: #f0f6fc;
    letter-spacing: 0.5px;
  }}

  .subtitle {{
    text-align: center;
    color: #8b949e;
    font-size: 0.95rem;
    margin-bottom: 36px;
  }}

  .cards-wrapper {{
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
    max-width: 1400px;
    margin: 0 auto;
  }}

  .combo-card {{
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 14px;
    padding: 20px 22px;
    min-width: 200px;
    max-width: 240px;
    flex: 1 1 200px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    transition: border-color 0.2s;
  }}

  .combo-card:first-child {{
    border-color: #d29922;
    box-shadow: 0 0 0 1px #d29922;
  }}

  .vote-badge {{
    background: #21262d;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #58a6ff;
    text-align: center;
    width: fit-content;
    margin: 0 auto;
    direction: ltr;
  }}

  .combo-card:first-child .vote-badge {{
    background: #2d2208;
    color: #e3b341;
  }}

  .ranks {{
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}

  .rank-row {{
    display: flex;
    align-items: center;
    gap: 10px;
    background: #0d1117;
    border-radius: 8px;
    padding: 7px 10px;
  }}


  .rank-icon {{
    font-size: 1.1rem;
    min-width: 22px;
    text-align: center;
  }}

  .team-name {{
    font-size: 0.95rem;
    font-weight: 500;
    line-height: 1.2;
  }}

  .chips {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    border-top: 1px solid #21262d;
    padding-top: 12px;
    justify-content: flex-start;
  }}

  .chip {{
    background: #21262d;
    border-radius: 12px;
    padding: 3px 10px;
    font-size: 0.78rem;
    color: #c9d1d9;
    white-space: nowrap;
  }}
</style>
</head>
<body>
  <h1>⚽ {group_name}</h1>
  <p class="subtitle">תחזיות סיום הבית · {total} משתתפים · {len(combinations)} צירופים שונים</p>
  <div class="cards-wrapper">
    {cards_html}
  </div>
</body>
</html>"""


if __name__ == "__main__":
    import os
    os.makedirs(OUT_DIR, exist_ok=True)
    for letter, (start, end) in GROUPS.items():
        group_data = get_group_data(start, end)
        combos = build_combinations(group_data)
        html = generate_html(letter, combos)
        path = os.path.join(OUT_DIR, f"group_{letter}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Group {letter}: {len(combos)} combinations, {len(group_data)} participants → {path}")
