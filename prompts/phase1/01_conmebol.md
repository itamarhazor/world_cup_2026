You are a professional football analyst building a prediction model for FIFA World Cup 2026.

Using web search, collect current data for the following 6 CONMEBOL teams:
Argentina, Brazil, Colombia, Ecuador, Paraguay, Uruguay

For each team output EXACTLY this JSON object (format example only — do not output Spain):

{
  "team": "Spain",
  "confederation": "UEFA",
  "fifa_rank": 2,
  "elo_rating": 2041,
  "implied_win_pct": 11.2,
  "form_w": 5,
  "form_d": 1,
  "form_l": 0,
  "gf_last10": 14,
  "ga_last10": 3,
  "xg_for_pg": 2.3,
  "xg_against_pg": 0.7,
  "qualifying_ppg": 2.6,
  "last_tournament_stage": "Winner Euro 2024",
  "coach_win_pct": 71,
  "squad_avg_age": 26.1,
  "style": "high_press",
  "confederation_form": "strong",
  "host_boost": false,
  "altitude_games": false,
  "key_absence": "none",
  "momentum": "Dominant in every metric, best team in Europe last 18 months."
}

Field rules — follow exactly:

- form_w / form_d / form_l: last 10 competitive matches only (no friendlies)
- gf_last10 / ga_last10: goals in those same 10 matches
- xg_for_pg / xg_against_pg: from qualifying campaign; round to 1 decimal
- qualifying_ppg: points per game in their World Cup qualifying group; round to 2 decimals
- last_tournament_stage: most recent major tournament result, e.g. "SF Copa America 2024", "QF Euro 2024", "Group Stage WC 2022". Use "Did not qualify" if they missed the last tournament
- coach_win_pct: manager's career competitive win % as integer (0-100). If new coach with <10 games, write null
- squad_avg_age: average age of expected 23-man squad; round to 1 decimal
- style: MUST be one of → "high_press" | "counter" | "possession" | "balanced" | "physical"
- confederation_form: MUST be one of → "dominant" | "strong" | "average" | "weak" — based on how CONMEBOL teams performed in the last 18 months of international football
- host_boost: false for all CONMEBOL teams (none are co-hosts)
- altitude_games: true if this team is scheduled to play at Estadio Azteca (Mexico City, 2,240m altitude) AND they do not regularly train or compete at altitude
- implied_win_pct: decimal percentage from current betting markets (e.g. 11.2 means 11.2%). If genuinely unavailable write 0
- key_absence: "[Player name], [reason], [matches affected]" in under 15 words total. Write "none" if no significant absences
- momentum: one sentence, max 20 words, factual and specific — no hype

Output ONLY a valid JSON array of all 6 objects.
No preamble. No commentary. No markdown fences. No trailing text.
Start your response with: [
