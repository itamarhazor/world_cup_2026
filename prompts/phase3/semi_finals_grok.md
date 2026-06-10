You are a professional football analyst predicting FIFA World Cup 2026 knockout stage results.

Using web search, gather the latest tournament form, injuries, and squad news for each team below before predicting.

The following team data from pre-tournament research is provided to inform your predictions:

--- TEAM DATA START ---
[
  {
    "team": "Argentina",
    "confederation": "CONMEBOL",
    "fifa_rank": 3,
    "elo_rating": 2113,
    "implied_win_pct": 11.0,
    "form_w": 7,
    "form_d": 2,
    "form_l": 1,
    "gf_last10": 18,
    "ga_last10": 5,
    "xg_for_pg": 1.8,
    "xg_against_pg": 0.8,
    "qualifying_ppg": 2.11,
    "last_tournament_stage": "Winner Copa America 2024",
    "coach_win_pct": 71,
    "squad_avg_age": 27.0,
    "style": "possession",
    "confederation_form": "dominant",
    "host_boost": false,
    "altitude_games": false,
    "key_absence": "none",
    "momentum": "Defending champions, strong qualifying leaders."
  },
  {
    "team": "England",
    "confederation": "UEFA",
    "fifa_rank": 4,
    "elo_rating": 1850,
    "implied_win_pct": 12.5,
    "form_w": 7,
    "form_d": 2,
    "form_l": 1,
    "gf_last10": 20,
    "ga_last10": 6,
    "xg_for_pg": 2.1,
    "xg_against_pg": 0.6,
    "qualifying_ppg": 2.8,
    "last_tournament_stage": "Runner-up Euro 2024",
    "coach_win_pct": 70,
    "squad_avg_age": 25.8,
    "style": "balanced",
    "confederation_form": "dominant",
    "host_boost": false,
    "altitude_games": false,
    "key_absence": "none",
    "momentum": "Strong squad depth and consistent high-level performances."
  },
  {
    "team": "France",
    "confederation": "UEFA",
    "fifa_rank": 1,
    "elo_rating": 1900,
    "implied_win_pct": 18.5,
    "form_w": 8,
    "form_d": 1,
    "form_l": 1,
    "gf_last10": 22,
    "ga_last10": 5,
    "xg_for_pg": 2.4,
    "xg_against_pg": 0.5,
    "qualifying_ppg": 2.67,
    "last_tournament_stage": "SF Euro 2024",
    "coach_win_pct": 75,
    "squad_avg_age": 26.3,
    "style": "high_press",
    "confederation_form": "dominant",
    "host_boost": false,
    "altitude_games": false,
    "key_absence": "none",
    "momentum": "Top-ranked with exceptional depth across all positions."
  },
  {
    "team": "Spain",
    "confederation": "UEFA",
    "fifa_rank": 2,
    "elo_rating": 1880,
    "implied_win_pct": 16.0,
    "form_w": 8,
    "form_d": 1,
    "form_l": 1,
    "gf_last10": 21,
    "ga_last10": 4,
    "xg_for_pg": 2.3,
    "xg_against_pg": 0.6,
    "qualifying_ppg": 2.8,
    "last_tournament_stage": "Winner Euro 2024",
    "coach_win_pct": 78,
    "squad_avg_age": 26.1,
    "style": "possession",
    "confederation_form": "dominant",
    "host_boost": false,
    "altitude_games": false,
    "key_absence": "none",
    "momentum": "Dominant in every metric, best team in Europe last 18 months."
  }
]
--- TEAM DATA END ---

Round: Semi-finals

--- FIXTURES START ---
France vs Spain
England vs Argentina
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
