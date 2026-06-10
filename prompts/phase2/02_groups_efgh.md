You are a professional football analyst predicting FIFA World Cup 2026 group stage results.

The research data below was compiled in a prior research session. Use ONLY this data — do not perform additional web searches.

Extract the following 16 objects from your Phase 1 output (match by the "team" field):
Germany, Curaçao, Côte d'Ivoire, Ecuador,
Netherlands, Japan, Sweden, Tunisia,
Spain, Cabo Verde, Saudi Arabia, Uruguay,
Belgium, Egypt, IR Iran, New Zealand

--- PHASE 1 DATA START ---
[PASTE THE 16 JSON OBJECTS HERE]
--- PHASE 1 DATA END ---

Predict the exact final score after 90 minutes for each of the 24 matches across Groups E–H.
The first score is always for the first-named team.

Group E
1.  Germany vs Curaçao
2.  Côte d'Ivoire vs Ecuador
3.  Germany vs Côte d'Ivoire
4.  Ecuador vs Curaçao
5.  Ecuador vs Germany
6.  Curaçao vs Côte d'Ivoire

Group F
7.  Netherlands vs Japan
8.  Sweden vs Tunisia
9.  Netherlands vs Sweden
10. Tunisia vs Japan
11. Tunisia vs Netherlands
12. Japan vs Sweden

Group G
13. Spain vs Cabo Verde
14. Saudi Arabia vs Uruguay
15. Spain vs Saudi Arabia
16. Uruguay vs Cabo Verde
17. Uruguay vs Spain
18. Cabo Verde vs Saudi Arabia

Group H
19. Belgium vs Egypt
20. IR Iran vs New Zealand
21. Belgium vs IR Iran
22. New Zealand vs Egypt
23. New Zealand vs Belgium
24. Egypt vs IR Iran

Output ONLY a valid JSON array of exactly 24 objects.
No preamble. No commentary. No markdown fences. No trailing text.
Start your response with: [

Output format:
[
  {"group": "E", "match": "Germany vs Curaçao", "predicted_score": "X-Y"},
  {"group": "E", "match": "Côte d'Ivoire vs Ecuador", "predicted_score": "X-Y"},
  {"group": "E", "match": "Germany vs Côte d'Ivoire", "predicted_score": "X-Y"},
  {"group": "E", "match": "Ecuador vs Curaçao", "predicted_score": "X-Y"},
  {"group": "E", "match": "Ecuador vs Germany", "predicted_score": "X-Y"},
  {"group": "E", "match": "Curaçao vs Côte d'Ivoire", "predicted_score": "X-Y"},
  {"group": "F", "match": "Netherlands vs Japan", "predicted_score": "X-Y"},
  {"group": "F", "match": "Sweden vs Tunisia", "predicted_score": "X-Y"},
  {"group": "F", "match": "Netherlands vs Sweden", "predicted_score": "X-Y"},
  {"group": "F", "match": "Tunisia vs Japan", "predicted_score": "X-Y"},
  {"group": "F", "match": "Tunisia vs Netherlands", "predicted_score": "X-Y"},
  {"group": "F", "match": "Japan vs Sweden", "predicted_score": "X-Y"},
  {"group": "G", "match": "Spain vs Cabo Verde", "predicted_score": "X-Y"},
  {"group": "G", "match": "Saudi Arabia vs Uruguay", "predicted_score": "X-Y"},
  {"group": "G", "match": "Spain vs Saudi Arabia", "predicted_score": "X-Y"},
  {"group": "G", "match": "Uruguay vs Cabo Verde", "predicted_score": "X-Y"},
  {"group": "G", "match": "Uruguay vs Spain", "predicted_score": "X-Y"},
  {"group": "G", "match": "Cabo Verde vs Saudi Arabia", "predicted_score": "X-Y"},
  {"group": "H", "match": "Belgium vs Egypt", "predicted_score": "X-Y"},
  {"group": "H", "match": "IR Iran vs New Zealand", "predicted_score": "X-Y"},
  {"group": "H", "match": "Belgium vs IR Iran", "predicted_score": "X-Y"},
  {"group": "H", "match": "New Zealand vs Egypt", "predicted_score": "X-Y"},
  {"group": "H", "match": "New Zealand vs Belgium", "predicted_score": "X-Y"},
  {"group": "H", "match": "Egypt vs IR Iran", "predicted_score": "X-Y"}
]
