# Data ingestion

Target: **FG3M** — three-pointers made by a player in a game.

## Source

`stats.nba.com` via [`nba_api`](https://github.com/swar/nba_api), endpoint
`LeagueGameLog`. One request returns every box score for a season, so a decade
of data is ~22 requests. No key needed; the endpoint throttles bursts, hence the
1.5 s pause in the script.

## Run

```bash
/Users/rubenchung/DATA1030-fall2026/.venv/bin/python Data_ingestion/fetch_gamelogs.py
```

Per-season CSVs are cached, so a re-run only fetches what is missing. Flags:
`--start 2020-21`, `--playoffs`, `--refresh`.

`nba_api` is installed in the repo-root `.venv` (not in `requirements.txt`,
which is pinned to the course conda env).

## What lands in `data/raw/` (gitignored, ~88 MB)

| file | rows | grain |
| --- | --- | --- |
| `player_gamelogs_regular.csv` | 281,163 | player × game |
| `team_gamelogs_regular.csv` | 26,418 | team × game |
| `*_regular_<season>.csv` | — | per-season cache |

Seasons 2015-16 … 2025-26 regular season (11 complete seasons, 13,209 games,
1,554 players). 2026-27 has no games yet.

Player columns: `SEASON_ID PLAYER_ID PLAYER_NAME TEAM_ID TEAM_ABBREVIATION
TEAM_NAME GAME_ID GAME_DATE MATCHUP WL MIN FGM FGA FG_PCT FG3M FG3A FG3_PCT
FTM FTA FT_PCT OREB DREB REB AST STL BLK TOV PF PTS PLUS_MINUS FANTASY_PTS
VIDEO_AVAILABLE`.

## Validity checks (passed on the current pull)

- no duplicate `(PLAYER_ID, GAME_ID)` rows
- no negative `MIN`, `FG3M`, `FG3A`, `PTS`; never `FG3M > FG3A`
- rows per season ≈ 26,000, except 2019-20 (22,393) and 2020-21 (23,054) — the
  COVID-shortened seasons, not missing data

## Gotchas

- **`FG3_PCT` is NaN exactly when `FG3A == 0`** (67,138 rows). Missing means *no
  attempts*, not unknown — writing 0 would assert a miss that never happened.
  Same for `FG_PCT` and `FT_PCT`. Use the counts, not the percentages.
- `FG3M` is a **count**, heavily zero-inflated: 47.4% of player-games are 0,
  mean 1.10, max 14. Plain linear regression on this will be a weak baseline.
- `MIN` is integer minutes — seconds are already rounded off upstream.
- `MIN == 0` on 1,020 rows (played, under 30 s). True DNPs are absent from the
  endpoint, so "did the player play" is itself a prediction problem.
- `GAME_ID` and `SEASON_ID` have leading zeros / are codes → read as `str`.
- `MATCHUP` encodes home/away: `"BOS vs. NYK"` is home, `"BOS @ NYK"` is away.
