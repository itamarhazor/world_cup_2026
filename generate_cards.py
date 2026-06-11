import csv
import os
import re

with open('match_card_template.html', 'r', encoding='utf-8') as f:
    template = f.read()

with open('World_Cup_Bets.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]
participant_cols = list(range(2, len(header), 2))
participant_names = [header[i] for i in participant_cols]

os.makedirs('cards', exist_ok=True)

current_group = ''
match_count = 0

for row in rows[1:]:
    if not row or not row[0].strip():
        continue

    event = row[0].strip()

    if event.startswith('בית '):
        current_group = event
        continue

    if not (event.startswith('מ') and '|' in event):
        continue

    m = re.match(r'^מ(\d+)', event)
    if not m:
        continue
    match_num = m.group(1)
    rest = event.split('|', 1)[1].strip()
    parts = rest.split(' - ', 1)
    home_team = parts[0].strip()
    away_team = parts[1].strip() if len(parts) > 1 else ''

    bets = []
    for i, col in enumerate(participant_cols):
        if col < len(row):
            bet = row[col].strip()
            if bet:
                bets.append((participant_names[i], bet))

    submitted = len(bets)
    missing = 35 - submitted

    home_win = draw = away_win = 0
    score_counts = {}

    for name, bet in bets:
        sm = re.match(r'^(\d+)\s*-\s*(\d+)$', bet)
        if not sm:
            continue
        h, a = int(sm.group(1)), int(sm.group(2))
        score_str = f'{h} - {a}'

        if h > a:
            home_win += 1
        elif h == a:
            draw += 1
        else:
            away_win += 1

        score_counts.setdefault(score_str, []).append(name)

    max_outcome = max(home_win, draw, away_win, 1)
    home_win_pct = round(home_win / max_outcome * 100, 1)
    draw_pct = round(draw / max_outcome * 100, 1)
    away_win_pct = round(away_win / max_outcome * 100, 1)

    sorted_scores = sorted(score_counts.items(), key=lambda x: -len(x[1]))
    max_score_count = len(sorted_scores[0][1]) if sorted_scores else 1

    score_rows_html = ''
    for score, names in sorted_scores:
        count = len(names)
        pct = round(count / max_score_count * 100, 1)
        names_str = ', '.join(names)
        score_rows_html += (
            f'    <div class="score-row">\n'
            f'      <div class="score-badge">{score}</div>\n'
            f'      <div class="score-bar-wrap">\n'
            f'        <div class="score-bar" style="width:{pct}%">{count}</div>\n'
            f'      </div>\n'
            f'    </div>\n'
            f'    <div class="score-names">{names_str}</div>\n'
        )

    html = template
    html = html.replace('{{GROUP_LABEL}}', current_group)
    html = html.replace('{{MATCH_LABEL}}', f'משחק {match_num}')
    html = html.replace('{{HOME_TEAM}}', home_team)
    html = html.replace('{{AWAY_TEAM}}', away_team)
    html = html.replace('{{SUBMITTED_COUNT}}', str(submitted))
    html = html.replace('{{MISSING_COUNT}}', str(missing))
    html = html.replace('{{HOME_WIN_COUNT}}', str(home_win))
    html = html.replace('{{HOME_WIN_PCT}}', str(home_win_pct))
    html = html.replace('{{HOME_WIN_ZERO}}', 'zero' if home_win == 0 else '')
    html = html.replace('{{DRAW_COUNT}}', str(draw))
    html = html.replace('{{DRAW_PCT}}', str(draw_pct))
    html = html.replace('{{DRAW_ZERO}}', 'zero' if draw == 0 else '')
    html = html.replace('{{AWAY_WIN_COUNT}}', str(away_win))
    html = html.replace('{{AWAY_WIN_PCT}}', str(away_win_pct))
    html = html.replace('{{AWAY_WIN_ZERO}}', 'zero' if away_win == 0 else '')

    html = re.sub(
        r'    <!-- REPEAT BLOCK START -->.*?    <!-- REPEAT BLOCK END -->',
        score_rows_html.rstrip('\n'),
        html,
        flags=re.DOTALL
    )

    output_path = f'cards/match_{match_num.zfill(2)}.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    match_count += 1
    print(f'  match_{match_num.zfill(2)}.html  {home_team} נגד {away_team}  ({submitted} ניחושים)')

print(f'\nסה"כ נוצרו {match_count} קלפים ב-cards/')
