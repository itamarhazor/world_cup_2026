#!/usr/bin/env python3
import re
import os

day_map = {
    'Thu': "יום ה'",
    'Fri': "יום ו'",
    'Sat': 'שבת',
    'Sun': "יום א'",
    'Mon': "יום ב'",
    'Tue': "יום ג'",
    'Wed': "יום ד'",
}

# Parse schedule.txt -> match_num: (day_he, date_str, time_str)
schedule = {}
with open('/Users/itamarhazor/projects/world_cup_2026/schedule.txt', 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) < 5:
            continue
        date_raw, time_raw, match_num_raw = parts[0].strip(), parts[1].strip(), parts[4].strip()
        if not match_num_raw.isdigit():
            continue
        match_num = int(match_num_raw)

        day_abbr = date_raw[:3]
        day_he = day_map.get(day_abbr, day_abbr)

        m = re.search(r'(\d+)/(\d+)/\d+', date_raw)
        date_str = f"{int(m.group(1))}.{int(m.group(2))}" if m else date_raw

        h, mi = time_raw.split(':')
        time_str = f"{int(h):02d}:{mi}"

        schedule[match_num] = (day_he, date_str, time_str)

print(f"Parsed {len(schedule)} matches")

cards_dir = '/Users/itamarhazor/projects/world_cup_2026/visuals/cards'
updated = skipped = errors = 0

for match_num, (day_he, date_str, time_str) in sorted(schedule.items()):
    filename = f'match_{match_num:02d}.html'
    filepath = os.path.join(cards_dir, filename)

    if not os.path.exists(filepath):
        print(f"  NOT FOUND: {filename}")
        errors += 1
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already updated
    if 'class="match-date"' in content:
        skipped += 1
        continue

    date_label = f"{day_he}, {date_str} &nbsp;&nbsp;|&nbsp;&nbsp; {time_str}"

    new_content = re.sub(
        r'(<div class="match-meta">)(.*?)(</div>)',
        r'\1\2\3\n    <div class="match-date">' + date_label + r'</div>',
        content,
        count=1
    )

    if new_content == content:
        print(f"  PATTERN NOT FOUND: {filename}")
        errors += 1
        continue

    # Inject CSS for .match-date before </style>
    if '.match-date' not in new_content:
        css = """  .match-date {
    font-size: 11px;
    color: #7a9bb5;
    letter-spacing: 0.5px;
    margin-top: 6px;
    font-weight: 500;
  }"""
        new_content = new_content.replace('</style>', css + '\n</style>', 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    updated += 1

print(f"\nDone — updated: {updated}, already done: {skipped}, errors: {errors}")
