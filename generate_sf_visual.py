import csv
import re
from collections import defaultdict

def parse_teams(bet):
    m = re.search(r'\s+\d+-\d+\s+', bet.strip())
    if not m:
        return None
    team1 = bet[:m.start()].strip()
    team2 = bet[m.end():].strip()
    if not team1 or not team2:
        return None
    return tuple(sorted([team1, team2]))

with open('World_Cup_Bets.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]
participant_cols = list(range(2, len(header), 2))
participant_names = [header[i] for i in participant_cols]

EXCLUDE = {'הקוף'}
AI_ENGINES = {'Gemini', 'Claude', 'Grok', 'ChatGPT'}

sf_bets = {}  # name -> {101: (teamA, teamB), 102: (teamC, teamD)}
for row in rows:
    event = row[0].strip()
    for match_num in [101, 102]:
        if event.startswith(f'מ{match_num}'):
            for i, col in enumerate(participant_cols):
                name = participant_names[i]
                if name in EXCLUDE:
                    continue
                if col < len(row) and row[col].strip():
                    parsed = parse_teams(row[col].strip())
                    if parsed:
                        sf_bets.setdefault(name, {})[match_num] = parsed

# Build combination key per person: frozenset of both matchups
combo_groups = defaultdict(list)
for name, games in sf_bets.items():
    if 101 not in games or 102 not in games:
        continue
    m101 = games[101]
    m102 = games[102]
    key = (m101, m102)  # ordered: SF1 then SF2
    combo_groups[key].append(name)

sorted_combos = sorted(combo_groups.items(), key=lambda x: -len(x[1]))

# Build HTML
combo_cards = ''
for (m101, m102), names in sorted_combos:
    count = len(names)
    sf1_label = f'{m101[0]} נגד {m101[1]}'
    sf2_label = f'{m102[0]} נגד {m102[1]}'
    chips = ''.join(
        f'<span class="chip ai">{n}</span>' if n in AI_ENGINES
        else f'<span class="chip human">{n}</span>'
        for n in names
    )
    combo_cards += f'''
    <div class="combo-card">
      <div class="combo-header">
        <div class="matchups">
          <div class="matchup-line"><span class="sf-tag">חצי א׳</span><span class="teams-text">{sf1_label}</span></div>
          <div class="matchup-line"><span class="sf-tag">חצי ב׳</span><span class="teams-text">{sf2_label}</span></div>
        </div>
        <div class="count-badge">{count}</div>
      </div>
      <div class="chip-row">{chips}</div>
    </div>'''

html = f'''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>חצי גמר — ניחושי 4 הקבוצות</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: #0f1923;
    font-family: 'Segoe UI', Arial, sans-serif;
    padding: 36px 16px 56px;
    min-height: 100vh;
  }}
  h1 {{
    text-align: center;
    color: #e2e8f0;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
  }}
  h1 span {{ color: #4a9eff; }}
  .subtitle {{
    text-align: center;
    font-size: 12px;
    color: #4a7a9b;
    margin-bottom: 28px;
  }}
  .legend {{
    display: flex;
    justify-content: center;
    gap: 18px;
    margin-bottom: 24px;
    font-size: 12px;
    color: #7a9bb5;
  }}
  .legend-item {{ display: flex; align-items: center; gap: 6px; }}
  .legend-dot {{ width: 10px; height: 10px; border-radius: 50%; }}
  .dot-human {{ background: #4a7a9b; }}
  .dot-ai {{ background: #4ade80; }}

  .grid {{
    display: flex;
    flex-direction: column;
    gap: 14px;
    max-width: 560px;
    margin: 0 auto;
  }}
  .combo-card {{
    background: #1a2632;
    border: 1px solid #263a50;
    border-radius: 14px;
    padding: 16px 18px 14px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.3);
  }}
  .combo-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
    gap: 12px;
  }}
  .matchups {{
    display: flex;
    flex-direction: column;
    gap: 5px;
  }}
  .matchup-line {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .sf-tag {{
    font-size: 10px;
    font-weight: 700;
    color: #4a9eff;
    background: rgba(74,158,255,0.12);
    border-radius: 6px;
    padding: 2px 7px;
    letter-spacing: 0.5px;
    flex-shrink: 0;
  }}
  .teams-text {{
    font-size: 15px;
    font-weight: 700;
    color: #c8d8e8;
  }}
  .count-badge {{
    font-size: 22px;
    font-weight: 800;
    color: #4a9eff;
    min-width: 36px;
    text-align: center;
    flex-shrink: 0;
  }}
  .chip-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
  }}
  .chip {{
    border-radius: 14px;
    padding: 3px 11px;
    font-size: 12px;
    font-weight: 500;
  }}
  .chip.human {{
    background: #162233;
    border: 1px solid #263a50;
    color: #9ab8d0;
  }}
  .chip.ai {{
    background: #1a2a1a;
    border: 1px solid #2a5a2a;
    color: #4ade80;
  }}
</style>
</head>
<body>
  <h1>⚽ חצי גמר 2026 — <span>ניחושי 4 הקבוצות</span></h1>
  <div class="subtitle">מי ניחש אותה הקומבינציה?</div>
  <div class="legend">
    <div class="legend-item"><div class="legend-dot dot-human"></div> משתתפים</div>
    <div class="legend-item"><div class="legend-dot dot-ai"></div> מנועי AI</div>
  </div>
  <div class="grid">
    {combo_cards}
  </div>
</body>
</html>'''

output_path = 'visuals/cards/sf_predictions.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'נוצר: {output_path}')
for (m101, m102), names in sorted_combos:
    print(f'  {m101[0]}+{m101[1]} / {m102[0]}+{m102[1]}: {len(names)} → {", ".join(names)}')
