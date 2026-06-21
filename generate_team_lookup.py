#!/usr/bin/env python3
"""Generate team_lookup.html - interactive per-team knockout prediction lookup."""
import csv
import json
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), 'World_Cup_Bets.csv')
OUT_PATH = os.path.join(os.path.dirname(__file__), 'visuals', 'knockout', 'team_lookup.html')

with open(CSV_PATH, encoding='utf-8') as f:
    rows = list(csv.reader(f))

header = rows[0]
participants = []
for i in range(2, len(header), 2):
    name = header[i].strip()
    if name:
        participants.append({'col': i, 'name': name})

SECTIONS = [
    ('🔵 בונוס – קבוצות בשלב ה-32',          'round32',      'שלב ה-32'),
    ('🟢 בונוס – קבוצות בשלב ה-16',          'round16',      'שלב ה-16'),
    ('🟡 בונוס – קבוצות ברבע גמר',           'quarterfinal', 'רבע גמר'),
    ('🔴 בונוס – קבוצות בחצי גמר',           'semifinal',    'חצי גמר'),
    ('🥉 בונוס – קבוצות במשחק על המקום השלישי', 'thirdplace',   'מקום שלישי'),
    ('🏅 בונוס – קבוצות בגמר',               'final',        'גמר'),
]

SECTION_HEADERS = {s[0] for s in SECTIONS}

def row_key(row):
    return row[0].strip() if row else ''

# Find start index of each section
section_starts = {}
for i, row in enumerate(rows):
    k = row_key(row)
    for header_text, stage_id, _ in SECTIONS:
        if k == header_text:
            section_starts[stage_id] = i

# For each stage collect team->participants mapping
stage_data = {}
for header_text, stage_id, stage_label in SECTIONS:
    if stage_id not in section_starts:
        continue
    start = section_starts[stage_id]
    team_preds = {}  # team -> [participant_name]
    for i in range(start + 1, len(rows)):
        row = rows[i]
        k = row_key(row)
        if not k:
            continue
        # Stop when we hit another section header
        if k in SECTION_HEADERS and i != start:
            break
        if k.startswith('קבוצה') and '–' in k:
            for p in participants:
                col = p['col']
                if col < len(row):
                    team = row[col].strip()
                    if team:
                        team_preds.setdefault(team, []).append(p['name'])
    stage_data[stage_id] = {'label': stage_label, 'teams': team_preds}

# All teams across all stages
all_teams = sorted({team for sd in stage_data.values() for team in sd['teams']})

data_js = json.dumps({
    'participants': [p['name'] for p in participants],
    'stages': stage_data,
    'allTeams': all_teams,
}, ensure_ascii=False, indent=2)

html = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>חיפוש קבוצה – מונדיאל 2026</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',Arial,sans-serif;background:#0a0e1a;color:#e2e8f0;min-height:100vh;padding:28px 16px 60px}}
h1{{text-align:center;font-size:1.8rem;font-weight:900;margin-bottom:6px;background:linear-gradient(135deg,#fbbf24,#f97316,#ef4444);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.subtitle{{text-align:center;color:#64748b;font-size:.85rem;margin-bottom:28px}}
.search-wrap{{max-width:420px;margin:0 auto 24px;position:relative}}
#teamInput{{width:100%;padding:12px 16px;border-radius:12px;border:2px solid #334155;background:#111827;color:#e2e8f0;font-size:1rem;outline:none;transition:border-color .2s}}
#teamInput:focus{{border-color:#f97316}}
#suggestions{{position:absolute;top:calc(100% + 4px);right:0;left:0;background:#1e293b;border-radius:10px;border:1px solid #334155;z-index:100;max-height:220px;overflow-y:auto;display:none}}
.suggestion{{padding:10px 16px;cursor:pointer;font-size:.92rem}}
.suggestion:hover,.suggestion.active{{background:#334155}}
.stages{{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin-bottom:28px;max-width:820px;margin-inline:auto}}
.stage-btn{{padding:7px 18px;border-radius:999px;border:none;cursor:pointer;font-size:.82rem;font-weight:700;background:#1e293b;color:#94a3b8;transition:all .2s}}
.stage-btn:hover{{background:#334155;color:#e2e8f0}}
.stage-btn.active{{background:linear-gradient(135deg,#fbbf24,#f97316);color:#0a0e1a}}
.results{{max-width:820px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:16px}}
@media(max-width:540px){{.results{{grid-template-columns:1fr}}}}
.list-card{{background:#111827;border-radius:14px;padding:20px;box-shadow:0 4px 20px rgba(0,0,0,.4)}}
.list-card.yes{{border-top:3px solid #22c55e}}
.list-card.no{{border-top:3px solid #ef4444}}
.card-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}}
.card-title{{font-size:.95rem;font-weight:700}}
.card-title.yes{{color:#22c55e}}
.card-title.no{{color:#ef4444}}
.count-badge{{font-size:.8rem;background:#1e293b;border-radius:999px;padding:3px 10px;color:#94a3b8}}
.copy-btn{{font-size:.75rem;padding:5px 12px;border-radius:8px;border:1px solid #334155;background:#1e293b;color:#94a3b8;cursor:pointer;transition:all .2s;white-space:nowrap}}
.copy-btn:hover{{background:#334155;color:#e2e8f0}}
.copy-btn.copied{{border-color:#22c55e;color:#22c55e}}
.names{{display:flex;flex-wrap:wrap;gap:6px}}
.name-chip{{padding:5px 11px;border-radius:8px;font-size:.82rem;font-weight:600}}
.yes .name-chip{{background:#14532d;color:#86efac}}
.no .name-chip{{background:#450a0a;color:#fca5a5}}
.empty{{color:#475569;font-size:.85rem;font-style:italic}}
.placeholder{{text-align:center;color:#475569;margin-top:60px;font-size:1rem}}
nav{{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin-bottom:32px}}
.nav-btn{{padding:7px 16px;border-radius:999px;text-decoration:none;font-size:.82rem;font-weight:700;background:#1e293b;color:#94a3b8;transition:all .2s;border:1px solid #334155}}
.nav-btn:hover{{background:#334155;color:#e2e8f0}}
</style>
</head>
<body>

<h1>מונדיאל 2026 – חיפוש לפי קבוצה</h1>
<p class="subtitle">בחר קבוצה ושלב כדי לראות מי ניבא ומי לא</p>

<nav>
  <a class="nav-btn" href="knockout_predictions.html">תחזיות כלליות</a>
  <a class="nav-btn" href="round32.html">שלב ה-32</a>
  <a class="nav-btn" href="round16.html">שלב ה-16</a>
  <a class="nav-btn" href="quarterfinal.html">רבע גמר</a>
  <a class="nav-btn" href="semifinal.html">חצי גמר</a>
  <a class="nav-btn" href="final.html">גמר</a>
</nav>

<div class="search-wrap">
  <input id="teamInput" type="text" placeholder="🔍 חפש קבוצה..." autocomplete="off" />
  <div id="suggestions"></div>
</div>

<div class="stages" id="stages"></div>

<div id="output"><p class="placeholder">בחר קבוצה כדי להתחיל</p></div>

<script>
const DATA = {data_js};

let selectedTeam = null;
let selectedStage = null;

const stageOrder = ['round32','round16','quarterfinal','semifinal','thirdplace','final'];
const stagesDiv = document.getElementById('stages');
stageOrder.forEach(sid => {{
  const s = DATA.stages[sid];
  if (!s) return;
  const btn = document.createElement('button');
  btn.className = 'stage-btn';
  btn.dataset.stage = sid;
  btn.textContent = s.label;
  btn.onclick = () => selectStage(sid);
  stagesDiv.appendChild(btn);
}});

const input = document.getElementById('teamInput');
const suggestionsEl = document.getElementById('suggestions');
let activeSuggestion = -1;

input.addEventListener('input', () => {{
  const q = input.value.trim();
  if (!q) {{ hideSuggestions(); return; }}
  const matches = DATA.allTeams.filter(t => t.includes(q));
  showSuggestions(matches);
}});

input.addEventListener('keydown', e => {{
  const items = suggestionsEl.querySelectorAll('.suggestion');
  if (e.key === 'ArrowDown') {{ activeSuggestion = Math.min(activeSuggestion+1, items.length-1); highlightSugg(items); e.preventDefault(); }}
  else if (e.key === 'ArrowUp') {{ activeSuggestion = Math.max(activeSuggestion-1, 0); highlightSugg(items); e.preventDefault(); }}
  else if (e.key === 'Enter') {{ if (activeSuggestion >= 0 && items[activeSuggestion]) {{ pickTeam(items[activeSuggestion].textContent); }} else if (items.length === 1) {{ pickTeam(items[0].textContent); }} e.preventDefault(); }}
  else if (e.key === 'Escape') {{ hideSuggestions(); }}
}});

document.addEventListener('click', e => {{ if (!e.target.closest('.search-wrap')) hideSuggestions(); }});

function showSuggestions(teams) {{
  activeSuggestion = -1;
  if (!teams.length) {{ hideSuggestions(); return; }}
  suggestionsEl.innerHTML = teams.map(t => `<div class="suggestion" onclick="pickTeam('${{t}}')">${{t}}</div>`).join('');
  suggestionsEl.style.display = 'block';
}}

function highlightSugg(items) {{
  items.forEach((el, i) => el.classList.toggle('active', i === activeSuggestion));
}}

function hideSuggestions() {{ suggestionsEl.style.display = 'none'; activeSuggestion = -1; }}

function pickTeam(team) {{
  selectedTeam = team;
  input.value = team;
  hideSuggestions();
  render();
}}

function selectStage(sid) {{
  selectedStage = sid;
  document.querySelectorAll('.stage-btn').forEach(b => b.classList.toggle('active', b.dataset.stage === sid));
  render();
}}

// Auto-select first available stage
if (stageOrder.length) selectStage(stageOrder[0]);

function render() {{
  const out = document.getElementById('output');
  if (!selectedTeam) {{ out.innerHTML = '<p class="placeholder">בחר קבוצה כדי להתחיל</p>'; return; }}
  if (!selectedStage) {{ out.innerHTML = '<p class="placeholder">בחר שלב</p>'; return; }}
  const stage = DATA.stages[selectedStage];
  if (!stage) {{ out.innerHTML = '<p class="placeholder">אין נתונים לשלב זה</p>'; return; }}
  const predicted = stage.teams[selectedTeam] || [];
  const predictedSet = new Set(predicted);
  const notPredicted = DATA.participants.filter(p => !predictedSet.has(p));
  out.innerHTML = `
    <div class="results">
      ${{listCard('yes', `✓ ניבאו – ${{stage.label}}`, predicted, selectedTeam)}}
      ${{listCard('no',  `✗ לא ניבאו – ${{stage.label}}`, notPredicted, selectedTeam)}}
    </div>`;
}}

function listCard(cls, title, names, team) {{
  const chips = names.length
    ? names.map(n => `<span class="name-chip">${{n}}</span>`).join('')
    : `<span class="empty">אין</span>`;
  const listText = names.join(' ');
  return `
    <div class="list-card ${{cls}}">
      <div class="card-header">
        <span class="card-title ${{cls}}">${{title}} (${{names.length}})</span>
        <button class="copy-btn" onclick="copyList(this, '${{listText.replace(/'/g,"\\'")}}')" ${{names.length ? '' : 'disabled'}}>העתק</button>
      </div>
      <div class="names">${{chips}}</div>
    </div>`;
}}

function copyList(btn, text) {{
  if (!text) return;
  navigator.clipboard.writeText(text).then(() => {{
    btn.textContent = '✓ הועתק';
    btn.classList.add('copied');
    setTimeout(() => {{ btn.textContent = 'העתק'; btn.classList.remove('copied'); }}, 2000);
  }});
}}
</script>
</body>
</html>"""

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated: {OUT_PATH}")
total_teams = len(all_teams)
print(f"Teams found: {total_teams}")
for sid, sdata in stage_data.items():
    print(f"  {sdata['label']}: {len(sdata['teams'])} teams")
