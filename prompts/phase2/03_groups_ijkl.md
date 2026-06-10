You are a professional football analyst predicting FIFA World Cup 2026 group stage results.

The research data below was compiled in a prior research session. Use ONLY this data — do not perform additional web searches.

Extract the following 16 objects from your Phase 1 output (match by the "team" field):
France, Senegal, Iraq, Norway,
Argentina, Algeria, Austria, Jordan,
Portugal, Congo DR, Uzbekistan, Colombia,
England, Croatia, Ghana, Panama

--- PHASE 1 DATA START ---
[PASTE THE 16 JSON OBJECTS HERE]
--- PHASE 1 DATA END ---

Predict the exact final score after 90 minutes for each of the 24 matches across Groups I–L.
The first score is always for the first-named team.

Group I
1.  France vs Senegal
2.  Iraq vs Norway
3.  France vs Iraq
4.  Norway vs Senegal
5.  Norway vs France
6.  Senegal vs Iraq

Group J
7.  Argentina vs Algeria
8.  Austria vs Jordan
9.  Argentina vs Austria
10. Jordan vs Algeria
11. Jordan vs Argentina
12. Algeria vs Austria

Group K
13. Portugal vs Congo DR
14. Uzbekistan vs Colombia
15. Portugal vs Uzbekistan
16. Colombia vs Congo DR
17. Colombia vs Portugal
18. Congo DR vs Uzbekistan

Group L
19. England vs Croatia
20. Ghana vs Panama
21. England vs Ghana
22. Panama vs Croatia
23. Panama vs England
24. Croatia vs Ghana

Output ONLY a valid JSON array of exactly 24 objects.
No preamble. No commentary. No markdown fences. No trailing text.
Start your response with: [

Output format:
[
  {"group": "I", "match": "France vs Senegal", "predicted_score": "X-Y"},
  {"group": "I", "match": "Iraq vs Norway", "predicted_score": "X-Y"},
  {"group": "I", "match": "France vs Iraq", "predicted_score": "X-Y"},
  {"group": "I", "match": "Norway vs Senegal", "predicted_score": "X-Y"},
  {"group": "I", "match": "Norway vs France", "predicted_score": "X-Y"},
  {"group": "I", "match": "Senegal vs Iraq", "predicted_score": "X-Y"},
  {"group": "J", "match": "Argentina vs Algeria", "predicted_score": "X-Y"},
  {"group": "J", "match": "Austria vs Jordan", "predicted_score": "X-Y"},
  {"group": "J", "match": "Argentina vs Austria", "predicted_score": "X-Y"},
  {"group": "J", "match": "Jordan vs Algeria", "predicted_score": "X-Y"},
  {"group": "J", "match": "Jordan vs Argentina", "predicted_score": "X-Y"},
  {"group": "J", "match": "Algeria vs Austria", "predicted_score": "X-Y"},
  {"group": "K", "match": "Portugal vs Congo DR", "predicted_score": "X-Y"},
  {"group": "K", "match": "Uzbekistan vs Colombia", "predicted_score": "X-Y"},
  {"group": "K", "match": "Portugal vs Uzbekistan", "predicted_score": "X-Y"},
  {"group": "K", "match": "Colombia vs Congo DR", "predicted_score": "X-Y"},
  {"group": "K", "match": "Colombia vs Portugal", "predicted_score": "X-Y"},
  {"group": "K", "match": "Congo DR vs Uzbekistan", "predicted_score": "X-Y"},
  {"group": "L", "match": "England vs Croatia", "predicted_score": "X-Y"},
  {"group": "L", "match": "Ghana vs Panama", "predicted_score": "X-Y"},
  {"group": "L", "match": "England vs Ghana", "predicted_score": "X-Y"},
  {"group": "L", "match": "Panama vs Croatia", "predicted_score": "X-Y"},
  {"group": "L", "match": "Panama vs England", "predicted_score": "X-Y"},
  {"group": "L", "match": "Croatia vs Ghana", "predicted_score": "X-Y"}
]
