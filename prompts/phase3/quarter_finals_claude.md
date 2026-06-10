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
    "implied_win_pct": 10.0,
    "form_w": 7,
    "form_d": 1,
    "form_l": 2,
    "gf_last10": 18,
    "ga_last10": 7,
    "xg_for_pg": 1.8,
    "xg_against_pg": 0.7,
    "qualifying_ppg": 2.11,
    "last_tournament_stage": "Winner Copa America 2024",
    "coach_win_pct": 75,
    "squad_avg_age": 28.4,
    "style": "balanced",
    "confederation_form": "strong",
    "host_boost": false,
    "altitude_games": false,
    "key_absence": "Romero, MCL partial tear, may miss group stage",
    "momentum": "Topped CONMEBOL qualifying by 9 points, won last 3 major trophies."
  },
  {
    "team": "Belgium",
    "confederation": "UEFA",
    "fifa_rank": 9,
    "elo_rating": 1860,
    "implied_win_pct": 2.8,
    "form_w": 6,
    "form_d": 4,
    "form_l": 0,
    "gf_last10": 31,
    "ga_last10": 8,
    "xg_for_pg": 2.9,
    "xg_against_pg": 0.7,
    "qualifying_ppg": 2.25,
    "last_tournament_stage": "Round of 16 Euro 2024",
    "coach_win_pct": 53,
    "squad_avg_age": 28.5,
    "style": "possession",
    "confederation_form": "strong",
    "host_boost": false,
    "altitude_games": false,
    "key_absence": "none",
    "momentum": "De Bruyne-led Belgium scored 29 qualifying goals; squad renewal around Doku and De Ketelaere adds pace and youth."
  },
  {
    "team": "England",
    "confederation": "UEFA",
    "fifa_rank": 4,
    "elo_rating": 2060,
    "implied_win_pct": 13.3,
    "form_w": 10,
    "form_d": 0,
    "form_l": 0,
    "gf_last10": 26,
    "ga_last10": 0,
    "xg_for_pg": 2.6,
    "xg_against_pg": 0.3,
    "qualifying_ppg": 3.0,
    "last_tournament_stage": "Runner-Up Euro 2024",
    "coach_win_pct": 57,
    "squad_avg_age": 27.0,
    "style": "high_press",
    "confederation_form": "dominant",
    "host_boost": false,
    "altitude_games": false,
    "key_absence": "none",
    "momentum": "Only European nation to win all 8 qualifying games while conceding zero; Tuchel's defensive organisation is historically exceptional."
  },
  {
    "team": "France",
    "confederation": "UEFA",
    "fifa_rank": 1,
    "elo_rating": 2080,
    "implied_win_pct": 16.7,
    "form_w": 8,
    "form_d": 2,
    "form_l": 0,
    "gf_last10": 22,
    "ga_last10": 6,
    "xg_for_pg": 2.7,
    "xg_against_pg": 0.5,
    "qualifying_ppg": 2.67,
    "last_tournament_stage": "SF Euro 2024",
    "coach_win_pct": 68,
    "squad_avg_age": 26.3,
    "style": "balanced",
    "confederation_form": "dominant",
    "host_boost": false,
    "altitude_games": false,
    "key_absence": "Hugo Ekitike, torn Achilles, all matches",
    "momentum": "FIFA's No. 1 ranked side enters with Mbappé, Saliba, and Camavinga; Deschamps chasing third consecutive World Cup final."
  },
  {
    "team": "Japan",
    "confederation": "AFC",
    "fifa_rank": 18,
    "elo_rating": 1879,
    "implied_win_pct": 1.5,
    "form_w": 7,
    "form_d": 2,
    "form_l": 1,
    "gf_last10": 30,
    "ga_last10": 3,
    "xg_for_pg": 2.8,
    "xg_against_pg": 0.4,
    "qualifying_ppg": 2.3,
    "last_tournament_stage": "R16 WC 2022",
    "coach_win_pct": 65,
    "squad_avg_age": 26.5,
    "style": "high_press",
    "confederation_form": "strong",
    "host_boost": false,
    "altitude_games": false,
    "key_absence": "none",
    "momentum": "First to qualify globally, 30 goals in 10 qualifying games, dominant throughout."
  },
  {
    "team": "Norway",
    "confederation": "UEFA",
    "fifa_rank": 31,
    "elo_rating": 1960,
    "implied_win_pct": 2.8,
    "form_w": 10,
    "form_d": 0,
    "form_l": 0,
    "gf_last10": 41,
    "ga_last10": 6,
    "xg_for_pg": 3.2,
    "xg_against_pg": 0.6,
    "qualifying_ppg": 3.0,
    "last_tournament_stage": "Did not qualify Euro 2024",
    "coach_win_pct": 56,
    "squad_avg_age": 26.6,
    "style": "counter",
    "confederation_form": "strong",
    "host_boost": false,
    "altitude_games": false,
    "key_absence": "none",
    "momentum": "Haaland scored 16 qualifying goals; Norway's perfect 8-0-0 campaign with 37 goals is a European qualifying record."
  },
  {
    "team": "Portugal",
    "confederation": "UEFA",
    "fifa_rank": 5,
    "elo_rating": 2010,
    "implied_win_pct": 9.1,
    "form_w": 7,
    "form_d": 2,
    "form_l": 1,
    "gf_last10": 27,
    "ga_last10": 9,
    "xg_for_pg": 3.5,
    "xg_against_pg": 0.9,
    "qualifying_ppg": 2.17,
    "last_tournament_stage": "QF Euro 2024",
    "coach_win_pct": 52,
    "squad_avg_age": 27.2,
    "style": "possession",
    "confederation_form": "dominant",
    "host_boost": false,
    "altitude_games": false,
    "key_absence": "none",
    "momentum": "Nations League 2024-25 champions at FIFA No. 5; Ronaldo at 41 still contributes but Bruno Fernandes is now the engine."
  },
  {
    "team": "Spain",
    "confederation": "UEFA",
    "fifa_rank": 2,
    "elo_rating": 2140,
    "implied_win_pct": 17.4,
    "form_w": 8,
    "form_d": 2,
    "form_l": 0,
    "gf_last10": 27,
    "ga_last10": 4,
    "xg_for_pg": 3.2,
    "xg_against_pg": 0.5,
    "qualifying_ppg": 2.67,
    "last_tournament_stage": "Winner Euro 2024",
    "coach_win_pct": 70,
    "squad_avg_age": 26.7,
    "style": "high_press",
    "confederation_form": "dominant",
    "host_boost": false,
    "altitude_games": false,
    "key_absence": "Lamine Yamal, hamstring, opening game doubtful",
    "momentum": "Euro 2024 champions lead FIFA rankings; 21 qualifying goals in 6 games underscore elite attacking depth beyond any one player."
  }
]
--- TEAM DATA END ---

Round: Quarter-finals

--- FIXTURES START ---
France vs Japan
Spain vs Belgium
Norway vs England
Argentina vs Portugal
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
