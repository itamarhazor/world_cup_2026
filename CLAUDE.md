# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

FIFA World Cup 2026 prediction tracker. The goal is to collect AI predictions from 4 engines (Claude, Grok, ChatGPT, Gemini) across 3 phases, then score each engine's accuracy against actual results during the tournament.

## Workflow

The project is prompt-driven — no code yet, only structured prompts and saved results.

**Phase 1 — Research** (`prompts/phase1/`)
5 prompts, one per confederation. Each asks the AI to web-search and return a JSON array of team data objects. Run once per engine, save raw JSON output to `results/<engine>/phase1/`.

| File | Confederation | Teams |
|------|--------------|-------|
| `01_conmebol.md` | CONMEBOL | 6 teams |
| `02_concacaf.md` | CONCACAF | 6 teams (incl. hosts USA/Canada/Mexico) |
| `03_caf.md` | CAF | 10 teams |
| `04_afc_ofc.md` | AFC + OFC | 10 teams |
| `05_uefa.md` | UEFA | 16 teams |

**Phase 2 — Group stage predictions** (`prompts/phase2/`)
12 prompts, one per group (A–L). Each prompt has a `--- PHASE 1 DATA START ---` placeholder — paste the 4 relevant team JSON objects from Phase 1 output before sending. Returns 6 predicted scores per group (72 total). Save output to `results/<engine>/phase2/`.

**Phase 3 — Knockout predictions** (`prompts/phase3/`)
Single template `knockout_template.md`. Fill in the round name and fixture list, then send. Returns predicted score + `advances` field (handles draws via AET/penalties). Save output to `results/<engine>/phase3/`.

## Results directory layout

```
results/
  claude/
    phase1/   ← raw JSON arrays from Phase 1 calls
    phase2/   ← JSON arrays, one file per group
    phase3/   ← JSON arrays, one file per knockout round
  grok/
  chatgpt/
  gemini/
```

## Team name reference

Some teams have official FIFA names that differ from common usage. Use the official names (as in the prompts) when saving or comparing results:

| Common | Official (used in prompts) |
|--------|---------------------------|
| South Korea | Korea Republic |
| Turkey | Türkiye |
| Ivory Coast | Côte d'Ivoire |
| Cape Verde | Cabo Verde |
| Iran | IR Iran |
| DR Congo | Congo DR |
