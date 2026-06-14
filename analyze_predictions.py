#!/usr/bin/env python3
"""
World Cup 2026 Prediction Analysis
Reads World_Cup_Bets.csv and generates predictions_analysis.html
"""

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

CSV_PATH = Path(__file__).parent / 'World_Cup_Bets.csv'
OUTPUT_PATH = Path(__file__).parent / 'visuals/analysis/predictions_analysis.html'

AI_ENGINES = {'Gemini', 'Claude', 'Grok', 'ChatGPT'}
FUN_PARTICIPANTS = {'הקוף', 'המתחכם'}
SEMI_SLOT_ROWS = {'קבוצה 1 – חצי גמר', 'קבוצה 2 – חצי גמר', 'קבוצה 3 – חצי גמר', 'קבוצה 4 – חצי גמר'}
QF_SLOT_ROWS = {f'קבוצה {i} – רבע גמר' for i in range(1, 9)}
GROUP_LETTERS = list('ABCDEFGHIJKL')


def load_csv():
    with open(CSV_PATH, encoding='utf-8') as f:
        return list(csv.reader(f))


def get_participants(header):
    return [(header[i].strip(), i) for i in range(2, len(header), 2) if header[i].strip()]


def get_bets(row, participants):
    return {name: row[col].strip() for name, col in participants
            if col < len(row) and row[col].strip()}


def normalize_scorer(name):
    name = name.strip()
    if 'אמבפה' in name:
        return 'אמבפה'
    if 'קיין' in name:
        return 'הארי קיין'
    if 'ויניסיוס' in name:
        return 'ויניסיוס ג׳וניור'
    return name


def parse_final_bet(bet):
    """Parse 'TeamA score-score TeamB' → (team1, team2, winner_or_None)."""
    m = re.match(r'^(.+?)\s+(\d+)-(\d+)\s+(.+)$', bet.strip())
    if m:
        t1, s1, s2, t2 = m.group(1).strip(), int(m.group(2)), int(m.group(3)), m.group(4).strip()
        winner = t1 if s1 > s2 else (t2 if s2 > s1 else None)
        return t1, t2, winner
    return None


def analyze():
    rows = load_csv()
    header = rows[0]
    participants = get_participants(header)

    all_names = [n for n, _ in participants]
    human_names = [n for n in all_names if n not in AI_ENGINES and n not in FUN_PARTICIPANTS]
    ai_names = [n for n in all_names if n in AI_ENGINES]
    fun_names = [n for n in all_names if n in FUN_PARTICIPANTS]

    champion_bets = {}
    scorer_bets = {}
    final_bets = {}
    semi_picks = []   # flat list of all teams predicted to be semifinalists
    qf_picks = []     # flat list of all teams predicted to be quarterfinalists
    second_place_bets = {}
    third_place_bets = {}
    fourth_place_bets = {}
    group_p1 = {g: Counter() for g in GROUP_LETTERS}  # group -> top pick distribution
    group_p2 = {g: Counter() for g in GROUP_LETTERS}
    participant_goals = defaultdict(list)   # name -> list of total goals per game

    for row in rows:
        if not row or not row[0].strip():
            continue
        event = row[0].strip()

        if event == 'אלוף':
            champion_bets = get_bets(row, participants)
        elif event == 'מלך שערים':
            scorer_bets = get_bets(row, participants)
        elif 'מ104' in event:
            final_bets = get_bets(row, participants)
        elif event == 'מקום שני':
            second_place_bets = get_bets(row, participants)
        elif event == 'מקום שלישי':
            third_place_bets = get_bets(row, participants)
        elif event == 'מקום רביעי':
            fourth_place_bets = get_bets(row, participants)
        elif event in SEMI_SLOT_ROWS:
            bets = get_bets(row, participants)
            semi_picks.extend(bets.values())
        elif event in QF_SLOT_ROWS:
            bets = get_bets(row, participants)
            qf_picks.extend(bets.values())
        else:
            # Group stage games for goal-count analysis
            for g in GROUP_LETTERS:
                if event == f'מקום 1 – בית {g}':
                    for name, team in get_bets(row, participants).items():
                        group_p1[g][team] += 1
                elif event == f'מקום 2 – בית {g}':
                    for name, team in get_bets(row, participants).items():
                        group_p2[g][team] += 1

            if '|' in event:
                prefix = event.split('|')[0].replace('מ', '').strip()
                try:
                    num = int(prefix)
                    if 1 <= num <= 72:
                        for name, bet in get_bets(row, participants).items():
                            m = re.search(r'(\d+)\s*[-–]\s*(\d+)', bet)
                            if m:
                                participant_goals[name].append(int(m.group(1)) + int(m.group(2)))
                except ValueError:
                    pass

    scorer_bets_norm = {k: normalize_scorer(v) for k, v in scorer_bets.items()}

    # Champion stats
    champ_counter = Counter(champion_bets.values())
    champ_human_counter = Counter(v for k, v in champion_bets.items() if k in human_names)
    champ_ai = {k: champion_bets.get(k, '–') for k in ai_names}

    # Scorer stats
    scorer_counter = Counter(scorer_bets_norm.values())

    # Final matchup stats
    final_matchup_counter = Counter()
    final_winner_counter = Counter()
    participant_final_winner = {}
    for name, bet in final_bets.items():
        parsed = parse_final_bet(bet)
        if parsed:
            t1, t2, winner = parsed
            matchup = ' נגד '.join(sorted([t1, t2]))
            final_matchup_counter[matchup] += 1
            if winner:
                final_winner_counter[winner] += 1
                participant_final_winner[name] = winner

    # Semi-finalist popularity
    semi_counter = Counter(semi_picks)

    # QF-finalist popularity
    qf_counter = Counter(qf_picks)

    # Contrarians: champion pick chosen by ≤2 participants (from humans only)
    popular_champs = {t for t, c in champ_counter.items() if c >= 3}
    contrarians = [
        (name, champion_bets[name])
        for name in human_names
        if name in champion_bets and champion_bets[name] not in popular_champs
    ]

    # Unique scorer picks (chosen by only 1 person)
    unique_scorers = [
        (name, scorer_bets_norm[name])
        for name in all_names
        if name in scorer_bets_norm and scorer_counter[scorer_bets_norm[name]] == 1
    ]

    submitted_humans = [n for n in human_names if n in champion_bets]
    submitted_fun = [n for n in fun_names if n in champion_bets]
    submitted_non_ai = submitted_humans + submitted_fun

    # Goals-per-game per participant (group stage only)
    goals_ranking = sorted(
        [(name, sum(g) / len(g), len(g)) for name, g in participant_goals.items() if len(g) >= 50],
        key=lambda x: -x[1]
    )

    # Group controversy: per group, % who agree on P1 pick
    group_controversy = []
    for g in GROUP_LETTERS:
        total = sum(group_p1[g].values())
        if total and group_p1[g]:
            top_team, top_count = group_p1[g].most_common(1)[0]
            second = group_p1[g].most_common(2)
            p2_top = group_p2[g].most_common(1)
            group_controversy.append({
                'group': g,
                'p1_team': top_team,
                'p1_pct': round(100 * top_count / total),
                'p2_team': p2_top[0][0] if p2_top else '?',
                'p2_pct': round(100 * p2_top[0][1] / sum(group_p2[g].values())) if p2_top and sum(group_p2[g].values()) else 0,
            })
    group_controversy.sort(key=lambda x: x['p1_pct'])  # most controversial first

    # Podium: runner-up, 3rd, 4th
    second_counter = Counter(second_place_bets.values()).most_common()
    third_counter = Counter(third_place_bets.values()).most_common()
    fourth_counter = Counter(fourth_place_bets.values()).most_common()

    return {
        'total_participants': len(submitted_non_ai),
        'all_names': all_names,
        'human_names': human_names,
        'ai_names': ai_names,
        'submitted_humans': submitted_humans,
        'champion_bets': champion_bets,
        'champ_counter': champ_counter.most_common(),
        'champ_human_counter': champ_human_counter.most_common(),
        'champ_ai': champ_ai,
        'scorer_bets': scorer_bets_norm,
        'scorer_counter': scorer_counter.most_common(),
        'final_bets': final_bets,
        'final_matchup_counter': final_matchup_counter.most_common(8),
        'final_winner_counter': final_winner_counter.most_common(),
        'participant_final_winner': participant_final_winner,
        'semi_counter': semi_counter.most_common(8),
        'qf_counter': qf_counter.most_common(12),
        'contrarians': contrarians,
        'unique_scorers': unique_scorers,
        'goals_ranking': goals_ranking,
        'group_controversy': group_controversy,
        'second_counter': second_counter,
        'third_counter': third_counter,
        'fourth_counter': fourth_counter,
    }


# ── Color palette ────────────────────────────────────────────────────────────

CHART_COLORS = [
    '#4a9eff', '#f5a623', '#7ed321', '#d0021b', '#9b59b6',
    '#1abc9c', '#e74c3c', '#3498db', '#f39c12', '#2ecc71',
    '#e67e22', '#16a085',
]


def color_for(idx):
    return CHART_COLORS[idx % len(CHART_COLORS)]


def champ_color(team):
    palette = {
        'ספרד': '#c60b1e',
        'צרפת': '#002395',
        'ארגנטינה': '#74acdf',
        'ברזיל': '#009c3b',
        'אנגליה': '#cf081f',
        'פורטוגל': '#006600',
        'גרמניה': '#000000',
        'בלגיה': '#ef3340',
        'הולנד': '#ff6600',
    }
    return palette.get(team, '#4a9eff')


# ── HTML generation ──────────────────────────────────────────────────────────

def bar_chart(canvas_id, labels, values, colors, title=''):
    data = {
        'labels': labels,
        'datasets': [{
            'data': values,
            'backgroundColor': colors,
            'borderRadius': 6,
            'borderSkipped': False,
        }]
    }
    opts = {
        'responsive': True,
        'maintainAspectRatio': False,
        'plugins': {
            'legend': {'display': False},
            'tooltip': {'callbacks': {}},
        },
        'scales': {
            'y': {
                'beginAtZero': True,
                'ticks': {'color': '#8a9bb0', 'stepSize': 1},
                'grid': {'color': 'rgba(255,255,255,0.05)'},
            },
            'x': {
                'ticks': {'color': '#c8d8e8', 'font': {'size': 13}},
                'grid': {'display': False},
            },
        },
    }
    return f"""
    new Chart(document.getElementById('{canvas_id}'), {{
        type: 'bar',
        data: {json.dumps(data)},
        options: {json.dumps(opts)}
    }});
"""


def horizontal_bar_chart(canvas_id, labels, values, colors):
    data = {
        'labels': labels,
        'datasets': [{
            'data': values,
            'backgroundColor': colors,
            'borderRadius': 6,
            'borderSkipped': False,
        }]
    }
    opts = {
        'indexAxis': 'y',
        'responsive': True,
        'maintainAspectRatio': False,
        'plugins': {'legend': {'display': False}},
        'scales': {
            'x': {
                'beginAtZero': True,
                'ticks': {'color': '#8a9bb0', 'stepSize': 1},
                'grid': {'color': 'rgba(255,255,255,0.05)'},
            },
            'y': {
                'ticks': {'color': '#c8d8e8', 'font': {'size': 13}},
                'grid': {'display': False},
            },
        },
    }
    return f"""
    new Chart(document.getElementById('{canvas_id}'), {{
        type: 'bar',
        data: {json.dumps(data)},
        options: {json.dumps(opts)}
    }});
"""


def generate_html(d):
    # ── Section 1: Champion ──────────────────────────────────────────────────
    champ_labels = [t for t, _ in d['champ_counter']]
    champ_vals = [c for _, c in d['champ_counter']]
    champ_colors = [champ_color(t) for t in champ_labels]

    # Who picked what (champion detail table rows)
    champ_by_team = {}
    for name, team in d['champion_bets'].items():
        champ_by_team.setdefault(team, []).append(name)

    champ_rows_html = ''
    for team, count in d['champ_counter']:
        pickers = champ_by_team.get(team, [])
        ai_pickers = [n for n in pickers if n in AI_ENGINES]
        human_pickers = [n for n in pickers if n not in AI_ENGINES and n not in FUN_PARTICIPANTS]
        fun_pickers = [n for n in pickers if n in FUN_PARTICIPANTS]
        tag = f'<span class="ai-tag">AI</span>' if ai_pickers else ''
        names_display = ', '.join(human_pickers + fun_pickers + [f'🤖 {n}' for n in ai_pickers])
        champ_rows_html += f"""
        <tr>
          <td class="team-cell">{team}</td>
          <td class="count-cell">{count} {tag}</td>
          <td class="names-cell">{names_display}</td>
        </tr>"""

    # ── Section 2: Top Scorer ────────────────────────────────────────────────
    scorer_labels = [s for s, _ in d['scorer_counter']]
    scorer_vals = [c for _, c in d['scorer_counter']]
    scorer_colors = [color_for(i) for i in range(len(scorer_labels))]

    scorer_rows_html = ''
    scorer_by_player = {}
    for name, player in d['scorer_bets'].items():
        scorer_by_player.setdefault(player, []).append(name)
    for player, count in d['scorer_counter']:
        pickers = scorer_by_player.get(player, [])
        ai_pickers = [n for n in pickers if n in AI_ENGINES]
        human_pickers = [n for n in pickers if n not in AI_ENGINES and n not in FUN_PARTICIPANTS]
        fun_pickers = [n for n in pickers if n in FUN_PARTICIPANTS]
        tag = f'<span class="ai-tag">AI</span>' if ai_pickers else ''
        names_display = ', '.join(human_pickers + fun_pickers + [f'🤖 {n}' for n in ai_pickers])
        scorer_rows_html += f"""
        <tr>
          <td class="team-cell">{player}</td>
          <td class="count-cell">{count} {tag}</td>
          <td class="names-cell">{names_display}</td>
        </tr>"""

    # ── Section 3: Final Matchups ────────────────────────────────────────────
    final_labels = [m for m, _ in d['final_matchup_counter']]
    final_vals = [c for _, c in d['final_matchup_counter']]
    final_colors = [color_for(i) for i in range(len(final_labels))]

    # ── Section 4: Predicted Semifinalists ───────────────────────────────────
    semi_labels = [t for t, _ in d['semi_counter']]
    semi_vals = [c for _, c in d['semi_counter']]
    semi_colors = [champ_color(t) for t in semi_labels]

    # ── Section 5: AI spotlight ──────────────────────────────────────────────
    ai_cards_html = ''
    for engine in ['Gemini', 'Claude', 'Grok', 'ChatGPT']:
        champ = d['champion_bets'].get(engine, '–')
        scorer = d['scorer_bets'].get(engine, '–')
        final_bet = d['final_bets'].get(engine, '–')
        ai_cards_html += f"""
        <div class="ai-card">
          <div class="ai-engine-name">{engine}</div>
          <div class="ai-stat"><span class="ai-label">אלוף</span><span class="ai-value">{champ}</span></div>
          <div class="ai-stat"><span class="ai-label">מלך שערים</span><span class="ai-value">{scorer}</span></div>
          <div class="ai-stat ai-final"><span class="ai-label">גמר</span><span class="ai-value">{final_bet}</span></div>
        </div>"""

    # ── Section 6: Contrarians ───────────────────────────────────────────────
    contrarian_html = ''
    if d['contrarians']:
        for name, team in d['contrarians']:
            count = dict(d['champ_counter']).get(team, 1)
            solo = 'בלעדי!' if count == 1 else f'{count} בלבד'
            contrarian_html += f"""
          <div class="contrarian-item">
            <span class="contrarian-name">{name}</span>
            <span class="contrarian-arrow">→</span>
            <span class="contrarian-team">{team}</span>
            <span class="contrarian-badge">{solo}</span>
          </div>"""
    else:
        contrarian_html = '<p class="no-data">כולם בחרו מהמועמדים הפופולריים</p>'

    # ── Section 7: Unique scorer picks ──────────────────────────────────────
    unique_scorer_html = ''
    for name, player in d['unique_scorers']:
        unique_scorer_html += f"""
          <div class="contrarian-item">
            <span class="contrarian-name">{name}</span>
            <span class="contrarian-arrow">→</span>
            <span class="contrarian-team">{player}</span>
          </div>"""

    # ── Section 7b: Goals ranking ─────────────────────────────────────────────
    goals_labels = [name for name, avg, n in d['goals_ranking']]
    goals_vals = [round(avg, 2) for name, avg, n in d['goals_ranking']]
    goals_colors = []
    for name, avg, n in d['goals_ranking']:
        if name in AI_ENGINES:
            goals_colors.append('#9b59b6')
        elif name in FUN_PARTICIPANTS:
            goals_colors.append('#f5a623')
        elif avg >= 3.0:
            goals_colors.append('#e74c3c')
        elif avg >= 2.5:
            goals_colors.append('#4a9eff')
        else:
            goals_colors.append('#2a4a6a')

    # ── Section 8: Full podium ────────────────────────────────────────────────
    podium_positions = [
        ('🥇', 'אלוף', d['champ_counter']),
        ('🥈', 'מקום שני', d['second_counter']),
        ('🥉', 'מקום שלישי', d['third_counter']),
        ('4️⃣', 'מקום רביעי', d['fourth_counter']),
    ]
    podium_html = ''
    for medal, label, counter in podium_positions:
        podium_html += f'<div class="podium-col"><div class="podium-medal">{medal} {label}</div>'
        for team, cnt in counter[:6]:
            bar_w = round(100 * cnt / counter[0][1]) if counter else 0
            podium_html += f"""
          <div class="podium-row">
            <div class="podium-team">{team}</div>
            <div class="podium-bar-wrap"><div class="podium-bar" style="width:{bar_w}%"></div></div>
            <div class="podium-cnt">{cnt}</div>
          </div>"""
        podium_html += '</div>'

    # ── Section 9: Group controversy ─────────────────────────────────────────
    controversy_html = ''
    for g_info in d['group_controversy']:
        g = g_info['group']
        p1_team = g_info['p1_team']
        p1_pct = g_info['p1_pct']
        p2_team = g_info['p2_team']
        p2_pct = g_info['p2_pct']
        if p1_pct <= 75:
            badge_cls = 'badge-hot'
            badge_txt = 'שנוי במחלוקת'
        elif p1_pct >= 95:
            badge_cls = 'badge-settled'
            badge_txt = 'מוסכם'
        else:
            badge_cls = 'badge-mild'
            badge_txt = ''
        controversy_html += f"""
        <div class="group-row">
          <div class="group-letter">בית {g}</div>
          <div class="group-picks">
            <span class="gpick p1">{p1_team} ({p1_pct}%)</span>
            <span class="gpick-sep">·</span>
            <span class="gpick p2">{p2_team} ({p2_pct}%)</span>
          </div>
          {'<span class="group-badge ' + badge_cls + '">' + badge_txt + '</span>' if badge_txt else ''}
        </div>"""

    # ── JS charts ────────────────────────────────────────────────────────────
    charts_js = ''
    charts_js += bar_chart('champChart', champ_labels, champ_vals, champ_colors)
    charts_js += bar_chart('scorerChart', scorer_labels, scorer_vals, scorer_colors)
    charts_js += horizontal_bar_chart('finalChart', final_labels, final_vals, final_colors)
    charts_js += horizontal_bar_chart('semiChart', semi_labels, semi_vals, semi_colors)
    charts_js += horizontal_bar_chart('goalsChart', goals_labels, goals_vals, goals_colors)

    # Stats summary
    total = d['total_participants']
    top_champ, top_champ_n = d['champ_counter'][0]
    top_scorer, top_scorer_n = d['scorer_counter'][0]
    top_final, top_final_n = d['final_matchup_counter'][0]

    html = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ניתוח תחזיות – מונדיאל 2026</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    background: #0f1923;
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #c8d8e8;
    min-height: 100vh;
    padding: 32px 24px;
  }}

  .page-header {{
    text-align: center;
    margin-bottom: 40px;
  }}
  .page-header h1 {{
    font-size: 32px;
    font-weight: 800;
    color: #fff;
    letter-spacing: 1px;
  }}
  .page-header .subtitle {{
    margin-top: 8px;
    font-size: 14px;
    color: #4a9eff;
    letter-spacing: 2px;
    text-transform: uppercase;
  }}
  .trophy {{ font-size: 40px; display: block; margin-bottom: 12px; }}

  /* Summary cards */
  .summary-row {{
    display: flex;
    gap: 16px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 40px;
  }}
  .summary-card {{
    background: #1a2632;
    border-radius: 14px;
    padding: 20px 28px;
    text-align: center;
    min-width: 160px;
    border: 1px solid #263a50;
  }}
  .summary-card .s-value {{
    font-size: 28px;
    font-weight: 800;
    color: #4a9eff;
  }}
  .summary-card .s-label {{
    font-size: 12px;
    color: #8a9bb0;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }}

  /* Section */
  .section {{
    max-width: 860px;
    margin: 0 auto 40px;
    background: #1a2632;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    border: 1px solid #263a50;
  }}
  .section-header {{
    background: linear-gradient(135deg, #1e3a5f, #0d2137);
    padding: 20px 28px;
    border-bottom: 1px solid #263a50;
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .section-header h2 {{
    font-size: 18px;
    font-weight: 700;
    color: #fff;
  }}
  .section-header .icon {{ font-size: 22px; }}
  .section-body {{ padding: 24px 28px; }}

  /* Chart container */
  .chart-wrap {{
    position: relative;
    height: 260px;
    margin-bottom: 24px;
  }}
  .chart-wrap.tall {{ height: 340px; }}

  /* Table */
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
  }}
  th {{
    text-align: right;
    color: #4a9eff;
    font-size: 11px;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 0 0 10px;
    border-bottom: 1px solid #263a50;
  }}
  td {{
    padding: 10px 0;
    border-bottom: 1px solid rgba(38,58,80,0.5);
    vertical-align: top;
  }}
  tr:last-child td {{ border-bottom: none; }}
  .team-cell {{
    font-weight: 700;
    color: #fff;
    width: 120px;
  }}
  .count-cell {{
    color: #4a9eff;
    font-weight: 700;
    font-size: 16px;
    width: 80px;
  }}
  .names-cell {{
    color: #8a9bb0;
    font-size: 13px;
    line-height: 1.6;
  }}

  /* AI tag */
  .ai-tag {{
    display: inline-block;
    background: rgba(74,158,255,0.2);
    color: #4a9eff;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
    letter-spacing: 1px;
    margin-right: 4px;
    vertical-align: middle;
  }}

  /* AI cards grid */
  .ai-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
  }}
  .ai-card {{
    background: #0f1923;
    border-radius: 14px;
    padding: 18px 20px;
    border: 1px solid #263a50;
  }}
  .ai-engine-name {{
    font-size: 16px;
    font-weight: 800;
    color: #4a9eff;
    margin-bottom: 14px;
    text-align: center;
  }}
  .ai-stat {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 8px;
    gap: 8px;
  }}
  .ai-label {{
    font-size: 11px;
    color: #8a9bb0;
    text-transform: uppercase;
    letter-spacing: 1px;
    white-space: nowrap;
  }}
  .ai-value {{
    font-size: 14px;
    font-weight: 700;
    color: #fff;
    text-align: left;
  }}
  .ai-final .ai-value {{
    font-size: 12px;
    color: #c8d8e8;
  }}

  /* Contrarians */
  .contrarian-item {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid rgba(38,58,80,0.5);
  }}
  .contrarian-item:last-child {{ border-bottom: none; }}
  .contrarian-name {{
    font-weight: 700;
    color: #fff;
    min-width: 80px;
  }}
  .contrarian-arrow {{ color: #4a9eff; font-size: 16px; }}
  .contrarian-team {{
    font-weight: 700;
    color: #f5a623;
    flex: 1;
  }}
  .contrarian-badge {{
    background: rgba(245,166,35,0.15);
    color: #f5a623;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
    letter-spacing: 0.5px;
    white-space: nowrap;
  }}

  .no-data {{ color: #8a9bb0; font-style: italic; font-size: 14px; }}

  .divider {{
    height: 1px;
    background: #263a50;
    margin: 24px 0;
  }}

  .subsection-title {{
    font-size: 13px;
    color: #4a9eff;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 700;
    margin-bottom: 16px;
  }}

  /* Podium grid */
  .podium-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
  }}
  .podium-col {{ }}
  .podium-medal {{
    font-size: 13px;
    font-weight: 700;
    color: #4a9eff;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
  }}
  .podium-row {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 7px;
  }}
  .podium-team {{
    font-size: 13px;
    font-weight: 600;
    color: #c8d8e8;
    width: 80px;
    flex-shrink: 0;
  }}
  .podium-bar-wrap {{
    flex: 1;
    background: #0f1923;
    border-radius: 4px;
    height: 16px;
    overflow: hidden;
  }}
  .podium-bar {{
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #1e3a5f, #4a9eff);
  }}
  .podium-cnt {{
    font-size: 13px;
    font-weight: 700;
    color: #4a9eff;
    width: 20px;
    text-align: center;
    flex-shrink: 0;
  }}

  /* Group controversy */
  .group-row {{
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 11px 0;
    border-bottom: 1px solid rgba(38,58,80,0.5);
  }}
  .group-row:last-child {{ border-bottom: none; }}
  .group-letter {{
    font-weight: 700;
    color: #fff;
    font-size: 14px;
    width: 50px;
    flex-shrink: 0;
  }}
  .group-picks {{ flex: 1; font-size: 13px; }}
  .gpick.p1 {{ color: #4a9eff; font-weight: 700; }}
  .gpick.p2 {{ color: #8a9bb0; }}
  .gpick-sep {{ color: #3a5068; margin: 0 6px; }}
  .group-badge {{
    font-size: 11px;
    font-weight: 700;
    padding: 3px 9px;
    border-radius: 6px;
    letter-spacing: 0.5px;
    white-space: nowrap;
  }}
  .badge-hot {{ background: rgba(231,76,60,0.2); color: #e74c3c; }}
  .badge-settled {{ background: rgba(46,204,113,0.2); color: #2ecc71; }}
  .badge-mild {{ background: rgba(74,158,255,0.15); color: #4a9eff; }}
</style>
</head>
<body>

<div class="page-header">
  <span class="trophy">🏆</span>
  <h1>ניתוח תחזיות – מונדיאל 2026</h1>
  <div class="subtitle">World Cup 2026 · Prediction Analysis</div>
</div>

<!-- Summary Row -->
<div class="summary-row">
  <div class="summary-card">
    <div class="s-value">{total}</div>
    <div class="s-label">משתתפים שהגישו</div>
  </div>
  <div class="summary-card">
    <div class="s-value">{top_champ}</div>
    <div class="s-label">מועמד מוביל לאלוף</div>
  </div>
  <div class="summary-card">
    <div class="s-value">{top_scorer}</div>
    <div class="s-label">מלך שערים פופולרי</div>
  </div>
  <div class="summary-card">
    <div class="s-value">{top_champ_n}</div>
    <div class="s-label">הצביעו לאלוף המוביל</div>
  </div>
</div>

<!-- SECTION 1: Champion -->
<div class="section">
  <div class="section-header">
    <span class="icon">🏅</span>
    <h2>מי יהיה האלוף?</h2>
  </div>
  <div class="section-body">
    <div class="chart-wrap">
      <canvas id="champChart"></canvas>
    </div>
    <table>
      <thead><tr>
        <th>קבוצה</th><th>הצבעות</th><th>מי בחר</th>
      </tr></thead>
      <tbody>{champ_rows_html}</tbody>
    </table>
  </div>
</div>

<!-- SECTION 2: Top Scorer -->
<div class="section">
  <div class="section-header">
    <span class="icon">⚽</span>
    <h2>מלך השערים</h2>
  </div>
  <div class="section-body">
    <div class="chart-wrap">
      <canvas id="scorerChart"></canvas>
    </div>
    <table>
      <thead><tr>
        <th>שחקן</th><th>הצבעות</th><th>מי בחר</th>
      </tr></thead>
      <tbody>{scorer_rows_html}</tbody>
    </table>
  </div>
</div>

<!-- SECTION 3: Final Matchup -->
<div class="section">
  <div class="section-header">
    <span class="icon">🥇</span>
    <h2>גמר חלומות – מי נגד מי?</h2>
  </div>
  <div class="section-body">
    <div class="chart-wrap tall">
      <canvas id="finalChart"></canvas>
    </div>
  </div>
</div>

<!-- SECTION 4: Semi-finalists -->
<div class="section">
  <div class="section-header">
    <span class="icon">🔴</span>
    <h2>הקבוצות הצפויות לחצי גמר</h2>
  </div>
  <div class="section-body">
    <div class="chart-wrap tall">
      <canvas id="semiChart"></canvas>
    </div>
  </div>
</div>

<!-- SECTION 5: AI Spotlight -->
<div class="section">
  <div class="section-header">
    <span class="icon">🤖</span>
    <h2>מנועי ה-AI – מה הם חושבים?</h2>
  </div>
  <div class="section-body">
    <div class="ai-grid">
      {ai_cards_html}
    </div>
  </div>
</div>

<!-- SECTION 6: Contrarians -->
<div class="section">
  <div class="section-header">
    <span class="icon">🦄</span>
    <h2>הקונטרריאנים – מי הלך נגד הזרם?</h2>
  </div>
  <div class="section-body">
    <div class="subsection-title">בחירות אלוף נדירות</div>
    {contrarian_html}

    <div class="divider"></div>

    <div class="subsection-title">בחירות מלך שערים ייחודיות</div>
    {unique_scorer_html}
  </div>
</div>

<!-- SECTION 7: Goals personality -->
<div class="section">
  <div class="section-header">
    <span class="icon">🔥</span>
    <h2>תוקפן או שמרן? – ממוצע גולים לניחוש</h2>
  </div>
  <div class="section-body">
    <p style="font-size:13px;color:#8a9bb0;margin-bottom:18px;">
      ממוצע סך הגולים שכל משתתף ניחש לכל אחד מ-72 משחקי שלב הבתים.
      <span style="color:#e74c3c;font-weight:700;">אדום = תוקפן (3.0+)</span> &nbsp;·&nbsp;
      <span style="color:#4a9eff;font-weight:700;">כחול = מאוזן (2.5–3.0)</span> &nbsp;·&nbsp;
      <span style="color:#2a4a6a;font-weight:700;">כהה = שמרן (&lt;2.5)</span> &nbsp;·&nbsp;
      <span style="color:#9b59b6;font-weight:700;">סגול = AI</span>
    </p>
    <div class="chart-wrap" style="height:{max(260, len(goals_labels)*26)}px">
      <canvas id="goalsChart"></canvas>
    </div>
  </div>
</div>

<!-- SECTION 8: Full podium -->
<div class="section">
  <div class="section-header">
    <span class="icon">🏅</span>
    <h2>פודיום שלם – תחזיות מקום 1 עד 4</h2>
  </div>
  <div class="section-body">
    <div class="podium-grid">
      {podium_html}
    </div>
  </div>
</div>

<!-- SECTION 9: Group controversy -->
<div class="section">
  <div class="section-header">
    <span class="icon">🎯</span>
    <h2>בתים שנויים במחלוקת – כמה הסכמה יש?</h2>
  </div>
  <div class="section-body">
    <p style="font-size:13px;color:#8a9bb0;margin-bottom:18px;">אחוז המשתתפים שבחרו את אותה קבוצה לסיים ראשונה בכל בית.</p>
    {controversy_html}
  </div>
</div>

<script>
{charts_js}
</script>
</body>
</html>"""

    return html


def main():
    data = analyze()
    html = generate_html(data)
    OUTPUT_PATH.write_text(html, encoding='utf-8')
    print(f'✅ Generated: {OUTPUT_PATH}')

    # Print quick summary
    print(f'\n📊 Quick Summary:')
    print(f'  Submitted: {data["total_participants"]} humans')
    print(f'  Top champion pick: {data["champ_counter"][0]}')
    print(f'  Top scorer pick: {data["scorer_counter"][0]}')
    print(f'  Most popular final: {data["final_matchup_counter"][0]}')
    print(f'  Contrarians: {len(data["contrarians"])}')


if __name__ == '__main__':
    main()
