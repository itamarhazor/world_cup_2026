You are a professional football analyst predicting FIFA World Cup 2026 group stage results.

The research data below was compiled in a prior research session. Use ONLY this data — do not perform additional web searches.

Extract the following 16 objects from your Phase 1 output (match by the "team" field):
Mexico, South Africa, Korea Republic, Czechia,
Canada, Bosnia and Herzegovina, Qatar, Switzerland,
United States, Paraguay, Australia, Türkiye,
Brazil, Morocco, Haiti, Scotland

--- PHASE 1 DATA START ---
[PASTE THE 16 JSON OBJECTS HERE]
--- PHASE 1 DATA END ---

Predict the exact final score after 90 minutes for each of the 24 matches across Groups A–D.
The first score is always for the first-named team.

Group A
1.  Mexico vs South Africa
2.  Korea Republic vs Czechia
3.  Mexico vs Korea Republic
4.  Czechia vs South Africa
5.  Czechia vs Mexico
6.  South Africa vs Korea Republic

Group B
7.  Canada vs Bosnia and Herzegovina
8.  Qatar vs Switzerland
9.  Canada vs Qatar
10. Switzerland vs Bosnia and Herzegovina
11. Switzerland vs Canada
12. Bosnia and Herzegovina vs Qatar

Group C
13. United States vs Paraguay
14. Australia vs Türkiye
15. United States vs Australia
16. Türkiye vs Paraguay
17. Türkiye vs United States
18. Paraguay vs Australia

Group D
19. Brazil vs Morocco
20. Haiti vs Scotland
21. Brazil vs Haiti
22. Scotland vs Morocco
23. Scotland vs Brazil
24. Morocco vs Haiti

Output ONLY a valid JSON array of exactly 24 objects.
No preamble. No commentary. No markdown fences. No trailing text.
Start your response with: [

Output format:
[
  {"group": "A", "match": "Mexico vs South Africa", "predicted_score": "X-Y"},
  {"group": "A", "match": "Korea Republic vs Czechia", "predicted_score": "X-Y"},
  {"group": "A", "match": "Mexico vs Korea Republic", "predicted_score": "X-Y"},
  {"group": "A", "match": "Czechia vs South Africa", "predicted_score": "X-Y"},
  {"group": "A", "match": "Czechia vs Mexico", "predicted_score": "X-Y"},
  {"group": "A", "match": "South Africa vs Korea Republic", "predicted_score": "X-Y"},
  {"group": "B", "match": "Canada vs Bosnia and Herzegovina", "predicted_score": "X-Y"},
  {"group": "B", "match": "Qatar vs Switzerland", "predicted_score": "X-Y"},
  {"group": "B", "match": "Canada vs Qatar", "predicted_score": "X-Y"},
  {"group": "B", "match": "Switzerland vs Bosnia and Herzegovina", "predicted_score": "X-Y"},
  {"group": "B", "match": "Switzerland vs Canada", "predicted_score": "X-Y"},
  {"group": "B", "match": "Bosnia and Herzegovina vs Qatar", "predicted_score": "X-Y"},
  {"group": "C", "match": "United States vs Paraguay", "predicted_score": "X-Y"},
  {"group": "C", "match": "Australia vs Türkiye", "predicted_score": "X-Y"},
  {"group": "C", "match": "United States vs Australia", "predicted_score": "X-Y"},
  {"group": "C", "match": "Türkiye vs Paraguay", "predicted_score": "X-Y"},
  {"group": "C", "match": "Türkiye vs United States", "predicted_score": "X-Y"},
  {"group": "C", "match": "Paraguay vs Australia", "predicted_score": "X-Y"},
  {"group": "D", "match": "Brazil vs Morocco", "predicted_score": "X-Y"},
  {"group": "D", "match": "Haiti vs Scotland", "predicted_score": "X-Y"},
  {"group": "D", "match": "Brazil vs Haiti", "predicted_score": "X-Y"},
  {"group": "D", "match": "Scotland vs Morocco", "predicted_score": "X-Y"},
  {"group": "D", "match": "Scotland vs Brazil", "predicted_score": "X-Y"},
  {"group": "D", "match": "Morocco vs Haiti", "predicted_score": "X-Y"}
]
