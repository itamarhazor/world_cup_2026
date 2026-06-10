You are a professional football analyst predicting FIFA World Cup 2026 knockout stage results.

Using web search, gather the latest tournament form, injuries, and squad news for each team below before predicting.

Round: [REPLACE WITH: Round of 32 / Round of 16 / Quarter-finals / Semi-finals / Third-place playoff / Final]

--- FIXTURES START ---
[PASTE FIXTURES HERE — one per line, format: Team A vs Team B]
--- FIXTURES END ---

Rules:
- Predict the exact final score after 90 minutes of regular time
- If the score is level after 90 minutes, set "advances" to the team you predict goes through, formatted as "[Team] (AET)" or "[Team] (penalties)"
- If a winner is decided in 90 minutes, set "advances" to the winning team
- The first score is always for the first-named team

Output ONLY a valid JSON array.
No preamble. No commentary. No markdown fences. No trailing text.
Start your response with: [

Output format:
[
  {"match": "Brazil vs France", "predicted_score": "1-1", "advances": "France (penalties)"},
  {"match": "Spain vs Germany", "predicted_score": "2-0", "advances": "Spain"}
]
