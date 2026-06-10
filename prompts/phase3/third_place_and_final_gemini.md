You are a professional football analyst predicting FIFA World Cup 2026 knockout stage results.

Using web search, gather the latest tournament form, injuries, and squad news for each team below before predicting.

The following team data from pre-tournament research is provided to inform your predictions:

--- TEAM DATA START ---
[
  {
    "team": "Argentina",
    "confederation": "CONMEBOL",
    "fifa_rank": 3,
    "elo_rating": 2135,
    "implied_win_pct": 11.0,
    "form_w": 7,
    "form_d": 1,
    "form_l": 2,
    "gf_last10": 20,
    "ga_last10": 6,
    "xg_for_pg": 1.8,
    "xg_against_pg": 0.6,
    "qualifying_ppg": 2.11,
    "last_tournament_stage": "Winner Copa America 2024",
    "coach_win_pct": 72,
    "squad_avg_age": 28.2,
    "style": "possession",
    "confederation_form": "dominant",
    "host_boost": false,
    "altitude_games": false,
    "key_absence": "none",
    "momentum": "Defending world and continental champions entering the tournament as steady title contenders with an elite qualification record."
  },
  {
    "team": "England",
    "confederation": "UEFA",
    "fifa_rank": 4,
    "elo_rating": 1980,
    "implied_win_pct": 13.0,
    "form_w": 8,
    "form_d": 0,
    "form_l": 0,
    "gf_last10": 22,
    "ga_last10": 0,
    "xg_for_pg": 2.5,
    "xg_against_pg": 0.4,
    "qualifying_ppg": 3.0,
    "last_tournament_stage": "Runner-up Euro 2024",
    "coach_win_pct": 68,
    "squad_avg_age": 26.6,
    "style": "balanced",
    "confederation_form": "strong",
    "host_boost": false,
    "altitude_games": false,
    "key_absence": "none",
    "momentum": "Perfect qualification record with zero goals conceded indicates elite structural stability and defensive tactical dominance."
  },
  {
    "team": "France",
    "confederation": "UEFA",
    "fifa_rank": 1,
    "elo_rating": 2085,
    "implied_win_pct": 14.3,
    "form_w": 5,
    "form_d": 1,
    "form_l": 0,
    "gf_last10": 16,
    "ga_last10": 4,
    "xg_for_pg": 2.3,
    "xg_against_pg": 0.7,
    "qualifying_ppg": 2.67,
    "last_tournament_stage": "SF Euro 2024",
    "coach_win_pct": 66,
    "squad_avg_age": 26.5,
    "style": "counter",
    "confederation_form": "strong",
    "host_boost": false,
    "altitude_games": false,
    "key_absence": "none",
    "momentum": "Maintains world number one ranking backed by world-class attacking verticality and structural solidity under tournament-tested coaching."
  },
  {
    "team": "Spain",
    "confederation": "UEFA",
    "fifa_rank": 2,
    "elo_rating": 2055,
    "implied_win_pct": 18.0,
    "form_w": 5,
    "form_d": 1,
    "form_l": 0,
    "gf_last10": 21,
    "ga_last10": 2,
    "xg_for_pg": 2.9,
    "xg_against_pg": 0.5,
    "qualifying_ppg": 2.67,
    "last_tournament_stage": "Winner Euro 2024",
    "coach_win_pct": 74,
    "squad_avg_age": 26.2,
    "style": "high_press",
    "confederation_form": "strong",
    "host_boost": false,
    "altitude_games": false,
    "key_absence": "none",
    "momentum": "Enters tournament as betting favorite displaying peerless underlying technical metrics and elite territorial compression."
  }
]
--- TEAM DATA END ---

Round: Third-place playoff & Final

--- FIXTURES START ---
Third-place playoff: France vs Argentina
Final: Spain vs England
--- FIXTURES END ---

Rules:
- Predict the exact final score after 90 minutes of regular time
- If the score is level after 90 minutes, set "advances" to the team you predict goes through, formatted as "[Team] (AET)" or "[Team] (penalties)"
- If a winner is decided in 90 minutes, set "advances" to the winning team
- The first score is always for the first-named team

Output ONLY a valid JSON array with both matches.
No preamble. No commentary. No markdown fences. No trailing text.
Start your response with: [

Output format:
[
  {"match": "Third-place playoff: France vs England", "predicted_score": "2-1", "advances": "France"},
  {"match": "Final: Spain vs Argentina", "predicted_score": "1-1", "advances": "Spain (penalties)"}
]
