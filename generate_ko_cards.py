import csv
import os
import re

DAY_MAP = {
    'Sun': "יום א'", 'Mon': "יום ב'", 'Tue': "יום ג'",
    'Wed': "יום ד'", 'Thu': "יום ה'", 'Fri': "יום ו'", 'Sat': 'שבת',
}

STAGE_LABELS = {
    range(73, 89): 'שלב ה-32',
    range(89, 97): 'שלב ה-16',
    range(97, 101): 'רבע גמר',
    range(101, 103): 'חצי גמר',
    range(103, 104): 'משחק שלישי',
    range(104, 105): 'גמר',
}

def get_stage_label(match_num):
    for r, label in STAGE_LABELS.items():
        if match_num in r:
            return label
    return 'נוקאאוט'

# Parse schedule.txt → per-match metadata + day groups (knockout matches only, >= 73)
match_meta = {}
day_matches = {}
day_order = []

with open('schedule.txt', 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) < 5:
            continue
        try:
            match_num = int(parts[4].strip())
        except ValueError:
            continue
        if match_num < 73:
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

day_options = []
for dl in day_order:
    first_match = sorted(day_matches[dl])[0][1]
    day_options.append((dl, f"match_{str(first_match).zfill(2)}.html"))


def time_key(t):
    h, m = t.split(':')
    return int(h) * 60 + int(m)


def build_nav(match_num, chrono_nums):
    idx = chrono_nums.index(match_num)
    prev_num = chrono_nums[idx - 1] if idx > 0 else None
    next_num = chrono_nums[idx + 1] if idx < len(chrono_nums) - 1 else None

    meta = match_meta.get(match_num, {})
    date_label = meta.get('date_label', '')
    chrono = [m for _, m in sorted(day_matches.get(date_label, []), key=lambda x: time_key(x[0]))]
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


def parse_ko_bet(bet):
    """Parse 'TeamA X-Y TeamB' format.
    In RTL Hebrew, the first number (X) belongs to the RIGHT team (TeamB visually),
    and the second number (Y) belongs to the LEFT team (TeamA visually, which is the
    first team written and appears on the right in RTL — i.e. the 'home' side).
    So we return h_goals=Y (group 2), a_goals=X (group 1).
    """
    m = re.search(r'\s+(\d+)-(\d+)\s+', bet.strip())
    if not m:
        return None
    team1 = bet[:m.start()].strip()
    team2 = bet[m.end():].strip()
    if not team1 or not team2:
        return None
    return team1, int(m.group(2)), int(m.group(1)), team2


with open('visuals/templates/ko_card_template.html', 'r', encoding='utf-8') as f:
    template = f.read()

with open('World_Cup_Bets.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]
participant_cols = list(range(2, len(header), 2))
participant_names = [header[i] for i in participant_cols]
total_participants = len(participant_names)

os.makedirs('visuals/cards', exist_ok=True)

# Collect knockout match data from CSV
collected = {}

for row in rows[1:]:
    if not row or not row[0].strip():
        continue
    event = row[0].strip()
    if not (event.startswith('מ') and '|' in event):
        continue
    m = re.match(r'^מ(\d+)', event)
    if not m:
        continue
    match_num = int(m.group(1))
    if match_num < 73:
        continue
    # Only generate cards for matches that are in the schedule
    if match_num not in match_meta:
        continue

    rest = event.split('|', 1)[1].strip()
    parts = rest.split(' - ', 1)
    home_team = parts[0].strip()
    away_team = parts[1].strip() if len(parts) > 1 else ''

    if not home_team or not away_team:
        continue

    bets = []
    for i, col in enumerate(participant_cols):
        if col < len(row):
            bet = row[col].strip()
            if bet:
                bets.append((participant_names[i], bet))

    collected[match_num] = {
        'home': home_team,
        'away': away_team,
        'bets': bets,
    }

sorted_nums = sorted(collected.keys())

# Build chronological order
chrono_nums = []
for dl in day_order:
    for _time, mn in sorted(day_matches[dl], key=lambda x: time_key(x[0])):
        if mn in collected:
            chrono_nums.append(mn)

match_count = 0
for match_num in sorted_nums:
    data = collected[match_num]
    home_team = data['home']
    away_team = data['away']
    bets = data['bets']

    submitted = len(bets)
    home_win = draw = away_win = 0
    # score_counts: score_str -> [(name, is_correct), ...]
    score_counts = {}
    correct_matchup = []
    wrong_matchup = []

    for name, bet in bets:
        parsed = parse_ko_bet(bet)
        if not parsed:
            wrong_matchup.append(name)
            continue
        team1, h_goals, a_goals, team2 = parsed

        is_correct = {team1, team2} == {home_team, away_team}
        if is_correct:
            correct_matchup.append(name)
        else:
            wrong_matchup.append(name)

        # All 34 bets go into both outcome and score distributions
        if h_goals > a_goals:
            home_win += 1
        elif h_goals == a_goals:
            draw += 1
        else:
            away_win += 1

        score_str = f'{h_goals} - {a_goals}'
        score_counts.setdefault(score_str, []).append((name, is_correct))

    # Outcome bars (all bets)
    max_outcome = max(home_win, draw, away_win, 1)
    home_win_pct = round(home_win / max_outcome * 100, 1)
    draw_pct = round(draw / max_outcome * 100, 1)
    away_win_pct = round(away_win / max_outcome * 100, 1)

    # Score distribution — all bets, sorted by count desc
    sorted_scores = sorted(score_counts.items(), key=lambda x: -len(x[1]))
    max_score_count = len(sorted_scores[0][1]) if sorted_scores else 1

    correct_set = set(correct_matchup)

    score_rows_html = ''
    for score, entries in sorted_scores:
        count = len(entries)
        pct = round(count / max_score_count * 100, 1)
        names_html = ', '.join(
            f'<span class="sn-hit">{n}</span>' if ok else f'<span class="sn-miss">{n}</span>'
            for n, ok in entries
        )
        score_rows_html += (
            f'    <div class="score-row">\n'
            f'      <div class="score-badge">{score}</div>\n'
            f'      <div class="score-bar-wrap">\n'
            f'        <div class="score-bar" style="width:{pct}%">{count}</div>\n'
            f'      </div>\n'
            f'    </div>\n'
            f'    <div class="score-names">{names_html}</div>\n'
        )

    # Matchup chips — all 34, green for correct, gray for wrong
    all_chips = ''.join(
        f'<span class="name-chip hit">{n}</span>' for n in correct_matchup
    ) + ''.join(
        f'<span class="name-chip miss">{n}</span>' for n in wrong_matchup
    )
    matchup_html = f'<div class="name-chip-row">{all_chips}</div>' if all_chips else \
        '<div class="matchup-summary" style="color:#4a7a9b">אף אחד לא ניחש נכון את הזוג</div>'

    meta = match_meta.get(match_num, {})
    date_label = meta.get('date_label', '')
    time_str = meta.get('time', '')
    match_date_str = f'{date_label} &nbsp;&nbsp;|&nbsp;&nbsp; {time_str}' if date_label else ''
    whatsapp_text = f'{date_label}  |  {time_str}  |  {home_team} נגד {away_team}' if date_label else f'{home_team} נגד {away_team}'

    nav_html = build_nav(match_num, chrono_nums)
    stage_label = get_stage_label(match_num)

    html = template
    html = html.replace('{{NAV_BAR}}', nav_html)
    html = html.replace('{{MATCH_DATE}}', match_date_str)
    html = html.replace('{{GROUP_LABEL}}', stage_label)
    html = html.replace('{{MATCH_LABEL}}', f'משחק {match_num}')
    html = html.replace('{{HOME_TEAM}}', home_team)
    html = html.replace('{{AWAY_TEAM}}', away_team)
    html = html.replace('{{SUBMITTED_COUNT}}', str(submitted))
    html = html.replace('{{MISSING_COUNT}}', str(total_participants - submitted))
    html = html.replace('{{MATCHUP_CORRECT}}', str(len(correct_matchup)))
    html = html.replace('{{TOTAL_COUNT}}', str(total_participants))
    html = html.replace('{{MATCHUP_NAMES_HTML}}', matchup_html)
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
    print(f'  match_{str(match_num).zfill(2)}.html  {home_team} נגד {away_team}  (✅ {len(correct_matchup)}/{total_participants} ניחשו נכון)')

print(f'\nסה"כ נוצרו {match_count} קלפים ב-visuals/cards/')
