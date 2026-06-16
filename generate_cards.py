import csv
import os
import re

DAY_MAP = {
    'Sun': "יום א'", 'Mon': "יום ב'", 'Tue': "יום ג'",
    'Wed': "יום ד'", 'Thu': "יום ה'", 'Fri': "יום ו'", 'Sat': 'שבת',
}

# Parse schedule.txt → per-match metadata + day groups
match_meta = {}   # match_num -> {date_label, time}
day_matches = {}  # date_label -> [(time, match_num)]  (for chronological ordering)
day_order = []    # date_labels in appearance order

with open('schedule.txt', 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) < 5:
            continue
        try:
            match_num = int(parts[4].strip())
        except ValueError:
            continue
        if match_num > 72:
            continue
        date_raw, time_str = parts[0].strip(), parts[1].strip()
        day_abbr = date_raw.split(',')[0].strip()
        date_part = date_raw.split(',')[1].strip().split('/')
        day_num = date_part[0].lstrip('0')
        month_num = date_part[1].lstrip('0')
        date_label = f"{DAY_MAP.get(day_abbr, day_abbr)}, {day_num}.{month_num}"
        match_meta[match_num] = {'date_label': date_label, 'time': time_str}
        day_matches.setdefault(date_label, []).append((time_str, match_num))
        if date_label not in day_order:
            day_order.append(date_label)

# day_options: (date_label, href_of_first_match_that_day)
day_options = []
for dl in day_order:
    first_match = sorted(day_matches[dl])[0][1]
    day_options.append((dl, f"match_{str(first_match).zfill(2)}.html"))


def build_nav(match_num, sorted_nums):
    idx = sorted_nums.index(match_num)
    prev_num = sorted_nums[idx - 1] if idx > 0 else None
    next_num = sorted_nums[idx + 1] if idx < len(sorted_nums) - 1 else None

    meta = match_meta.get(match_num, {})
    date_label = meta.get('date_label', '')
    chrono = [m for _, m in sorted(day_matches.get(date_label, []))]
    day_pos = chrono.index(match_num) + 1 if match_num in chrono else 1
    day_total = len(chrono)

    prev_tag = (f'<a href="match_{str(prev_num).zfill(2)}.html" class="nav-arrow">קודם ›</a>'
                if prev_num else '<span class="nav-arrow disabled">קודם ›</span>')
    next_tag = (f'<a href="match_{str(next_num).zfill(2)}.html" class="nav-arrow">‹ הבא</a>'
                if next_num else '<span class="nav-arrow disabled">‹ הבא</span>')

    options = ''
    for dl, href in day_options:
        sel = ' selected' if dl == date_label else ''
        options += f'      <option value="{href}"{sel}>{dl}</option>\n'

    return (
        f'<nav class="match-nav">\n'
        f'  {prev_tag}\n'
        f'  <div class="nav-center">\n'
        f'    <select class="date-select" onchange="location.href=this.value">\n'
        f'{options}'
        f'    </select>\n'
        f'    <div class="day-counter">{day_pos} מתוך {day_total} היום</div>\n'
        f'  </div>\n'
        f'  {next_tag}\n'
        f'</nav>'
    )


with open('visuals/templates/match_card_template.html', 'r', encoding='utf-8') as f:
    template = f.read()

with open('World_Cup_Bets.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]
participant_cols = list(range(2, len(header), 2))
participant_names = [header[i] for i in participant_cols]
total_participants = len(participant_names)

os.makedirs('visuals/cards', exist_ok=True)

# First pass: collect all match data (≤72 only)
collected = {}  # match_num -> dict
current_group = ''

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
    match_num = int(m.group(1))
    if match_num > 72:
        continue

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

    collected[match_num] = {
        'group': current_group,
        'home': home_team,
        'away': away_team,
        'bets': bets,
    }

sorted_nums = sorted(collected.keys())

match_count = 0
for match_num in sorted_nums:
    data = collected[match_num]
    home_team = data['home']
    away_team = data['away']
    bets = data['bets']
    current_group = data['group']

    submitted = len(bets)
    missing = total_participants - submitted

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

    meta = match_meta.get(match_num, {})
    date_label = meta.get('date_label', '')
    time_str = meta.get('time', '')
    match_date_str = f'{date_label} &nbsp;&nbsp;|&nbsp;&nbsp; {time_str}' if date_label else ''
    whatsapp_text = f'{date_label}  |  {time_str}  |  {home_team} נגד {away_team}' if date_label else f'{home_team} נגד {away_team}'

    nav_html = build_nav(match_num, sorted_nums)

    html = template
    html = html.replace('{{NAV_BAR}}', nav_html)
    html = html.replace('{{MATCH_DATE}}', match_date_str)
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
    html = html.replace('{{WHATSAPP_TEXT}}', whatsapp_text)

    html = re.sub(
        r'    <!-- REPEAT BLOCK START -->.*?    <!-- REPEAT BLOCK END -->',
        score_rows_html.rstrip('\n'),
        html,
        flags=re.DOTALL
    )

    output_path = f'visuals/cards/match_{str(match_num).zfill(2)}.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    match_count += 1
    print(f'  match_{str(match_num).zfill(2)}.html  {home_team} נגד {away_team}  ({submitted} ניחושים)')

print(f'\nסה"כ נוצרו {match_count} קלפים ב-visuals/cards/')
