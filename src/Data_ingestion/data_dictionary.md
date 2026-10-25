# Data dictionary

Raw columns as returned by the `LeagueGameLog` endpoint of `nba_api`, documented
exactly as they land in `data/raw/` (no renaming, no derived columns).

**Type** gives the pandas dtype after `pd.read_csv(..., dtype={'GAME_ID': str, 'SEASON_ID': str})`.

**Unit / admissible values** states what the column *can* contain, derived from the
rules of basketball and from how the statistic is defined — not from this
dataset. These are the bounds to test new data against.

**Observed** reports the minimum and maximum seen in the documented collection
(2015–16 through 2025–26 regular seasons; 281,163 player-game rows and 26,418
team-game rows). It is a description of this sample only. A future row may fall
outside it without being erroneous, and a row inside it is not thereby valid.

**Variable kind** classifies the column for modeling: identifier, categorical,
ordinal, or continuous. Count columns are discrete but treated as continuous
features.

## `player_gamelogs_regular.csv` — one row per player appearance in one game

Primary key: (`PLAYER_ID`, `GAME_ID`). 281,163 rows, 32 columns, 0 duplicates.
Target variable: `FG3M`.

| # | Column | Type | Unit / admissible values | Observed | Variable kind | Missing | Description |
|---|---|---|---|---|---|---|---|
| 1 | `SEASON_ID` | str | code: `2` + 4-digit starting year | `22015`–`22025` (11 values) | categorical (id) | 0 | Season code (`22015` = 2015–16). |
| 2 | `PLAYER_ID` | int64 | NBA-assigned integer, no numeric meaning | 1,554 unique | identifier | 0 | NBA player identifier. |
| 3 | `PLAYER_NAME` | str | text | 1,554 unique | identifier | 0 | Player name. |
| 4 | `TEAM_ID` | int64 | NBA-assigned integer; 30 franchises | 30 unique | identifier | 0 | NBA team identifier. |
| 5 | `TEAM_ABBREVIATION` | str | 3-letter tricode; 30 franchises | 30 unique | categorical | 0 | Team tricode. |
| 6 | `TEAM_NAME` | str | text; 30 franchises | 30 unique | categorical | 0 | Full team name. |
| 7 | `GAME_ID` | str | 10 digits; `002` prefix = regular season | 13,209 unique | identifier | 0 | Game identifier. |
| 8 | `GAME_DATE` | str | ISO date; regular season runs Oct–Apr | 2015-10-27 to 2026-04-12 | continuous (time) | 0 | Date of the game. |
| 9 | `MATCHUP` | str | `TTT vs. OOO` (home) or `TTT @ OOO` (away) | 140,760 home / 140,403 away | categorical | 0 | Team and opponent tricodes. |
| 10 | `WL` | str | `W` or `L`; no ties in the NBA | both | categorical (binary) | 0 | Win or loss for the player's team. |
| 11 | `MIN` | int64 | integer ≥ 0, ≤ game length (48 + 5 per OT) | 0–60 | continuous | 0 | Minutes played. |
| 12 | `FGM` | int64 | integer ≥ 0, ≤ `FGA` | 0–24 | continuous (count) | 0 | Field goals made. |
| 13 | `FGA` | int64 | integer ≥ 0 | 0–50 | continuous (count) | 0 | Field goals attempted. |
| 14 | `FG_PCT` | float64 | ratio in [0, 1]; `FGM / FGA` | 0.0–1.0 | continuous | 13,305 | Field goal percentage. |
| 15 | `FG3M` | int64 | integer ≥ 0, ≤ `FG3A` | 0–14 | continuous (count) | 0 | Three-point field goals made. |
| 16 | `FG3A` | int64 | integer ≥ 0, ≤ `FGA` | 0–24 | continuous (count) | 0 | Three-point field goals attempted. |
| 17 | `FG3_PCT` | float64 | ratio in [0, 1]; `FG3M / FG3A` | 0.0–1.0 | continuous | 67,138 | Three-point field goal percentage. |
| 18 | `FTM` | int64 | integer ≥ 0, ≤ `FTA` | 0–26 | continuous (count) | 0 | Free throws made. |
| 19 | `FTA` | int64 | integer ≥ 0 | 0–36 | continuous (count) | 0 | Free throws attempted. |
| 20 | `FT_PCT` | float64 | ratio in [0, 1]; `FTM / FTA` | 0.0–1.0 | continuous | 123,388 | Free throw percentage. |
| 21 | `OREB` | int64 | integer ≥ 0 | 0–13 | continuous (count) | 0 | Offensive rebounds. |
| 22 | `DREB` | int64 | integer ≥ 0 | 0–23 | continuous (count) | 0 | Defensive rebounds. |
| 23 | `REB` | int64 | integer ≥ 0; `OREB + DREB` | 0–30 | continuous (count) | 0 | Total rebounds. |
| 24 | `AST` | int64 | integer ≥ 0 | 0–25 | continuous (count) | 0 | Assists. |
| 25 | `STL` | int64 | integer ≥ 0 | 0–10 | continuous (count) | 0 | Steals. |
| 26 | `BLK` | int64 | integer ≥ 0 | 0–11 | continuous (count) | 0 | Blocks. |
| 27 | `TOV` | int64 | integer ≥ 0 | 0–12 | continuous (count) | 0 | Turnovers. |
| 28 | `PF` | int64 | integer 0–6; 6 fouls means ejection | 0–6 | ordinal | 0 | Personal fouls. |
| 29 | `PTS` | int64 | integer ≥ 0; `2*(FGM-FG3M) + 3*FG3M + FTM` | 0–71 | continuous (count) | 0 | Points scored. |
| 30 | `PLUS_MINUS` | int64 | integer, may be negative | −56 to +57 | continuous | 0 | Team point differential while the player was on the court. |
| 31 | `FANTASY_PTS` | float64 | may be negative; fixed formula (see notes) | −3.3 to 105.2 | continuous | 0 | NBA fantasy score. |
| 32 | `VIDEO_AVAILABLE` | int64 | undocumented flag | 0, 1, 2 | categorical | 0 | Video-archive availability flag. |

## `team_gamelogs_regular.csv` — one row per team in one game

Primary key: (`TEAM_ID`, `GAME_ID`). 26,418 rows, 29 columns — exactly two rows
per game, one for each side.

| # | Column | Type | Unit / admissible values | Observed | Variable kind | Missing | Description |
|---|---|---|---|---|---|---|---|
| 1 | `SEASON_ID` | str | code: `2` + 4-digit starting year | `22015`–`22025` (11 values) | categorical (id) | 0 | Season code. |
| 2 | `TEAM_ID` | int64 | NBA-assigned integer; 30 franchises | 30 unique | identifier | 0 | NBA team identifier. |
| 3 | `TEAM_ABBREVIATION` | str | 3-letter tricode | 30 unique | categorical | 0 | Team tricode. |
| 4 | `TEAM_NAME` | str | text | 30 unique | categorical | 0 | Full team name. |
| 5 | `GAME_ID` | str | 10 digits; `002` prefix = regular season | 13,209 unique, 2 rows each | identifier | 0 | Game identifier. |
| 6 | `GAME_DATE` | str | ISO date; regular season runs Oct–Apr | 2015-10-27 to 2026-04-12 | continuous (time) | 0 | Date of the game. |
| 7 | `MATCHUP` | str | `TTT vs. OOO` (home) or `TTT @ OOO` (away) | half of each | categorical | 0 | Team and opponent tricodes. |
| 8 | `WL` | str | `W` or `L`; no ties in the NBA | both | categorical (binary) | 0 | Win or loss for this team. |
| 9 | `MIN` | int64 | 240 + 25 per OT (5 players × game length) | 240, 265, 290, 315, 340 | continuous | 0 | Total team minutes played. |
| 10 | `FGM` | int64 | integer ≥ 0, ≤ `FGA` | 19–65 | continuous (count) | 0 | Team field goals made. |
| 11 | `FGA` | int64 | integer ≥ 0 | 60–128 | continuous (count) | 0 | Team field goals attempted. |
| 12 | `FG_PCT` | float64 | ratio in [0, 1]; `FGM / FGA` | 0.269–0.689 | continuous | 0 | Team field goal percentage. |
| 13 | `FG3M` | int64 | integer ≥ 0, ≤ `FG3A` | 0–29 | continuous (count) | 0 | Team three-point field goals made. |
| 14 | `FG3A` | int64 | integer ≥ 0, ≤ `FGA` | 4–70 | continuous (count) | 0 | Team three-point field goals attempted. |
| 15 | `FG3_PCT` | float64 | ratio in [0, 1]; `FG3M / FG3A` | 0.0–0.842 | continuous | 0 | Team three-point field goal percentage. |
| 16 | `FTM` | int64 | integer ≥ 0, ≤ `FTA` | 0–47 | continuous (count) | 0 | Team free throws made. |
| 17 | `FTA` | int64 | integer ≥ 0 | 0–64 | continuous (count) | 0 | Team free throws attempted. |
| 18 | `FT_PCT` | float64 | ratio in [0, 1]; `FTM / FTA` | 0.143–1.0 | continuous | 1 | Team free throw percentage. |
| 19 | `OREB` | int64 | integer ≥ 0 | 0–29 | continuous (count) | 0 | Team offensive rebounds. |
| 20 | `DREB` | int64 | integer ≥ 0 | 14–60 | continuous (count) | 0 | Team defensive rebounds. |
| 21 | `REB` | int64 | integer ≥ 0; `OREB + DREB` | 20–74 | continuous (count) | 0 | Team total rebounds. |
| 22 | `AST` | int64 | integer ≥ 0, ≤ `FGM` | 7–50 | continuous (count) | 0 | Team assists. |
| 23 | `STL` | int64 | integer ≥ 0 | 0–22 | continuous (count) | 0 | Team steals. |
| 24 | `BLK` | int64 | integer ≥ 0 | 0–20 | continuous (count) | 0 | Team blocks. |
| 25 | `TOV` | int64 | integer ≥ 0 | 1–31 | continuous (count) | 0 | Team turnovers. |
| 26 | `PF` | int64 | integer ≥ 0; not capped at team level | 4–42 | continuous (count) | 0 | Team personal fouls. |
| 27 | `PTS` | int64 | integer ≥ 0 | 64–176 | continuous (count) | 0 | Team points scored. |
| 28 | `PLUS_MINUS` | int64 | integer, never 0 (no ties); sums to 0 per game | −73 to +73 | continuous | 0 | Final point margin for this team. |
| 29 | `VIDEO_AVAILABLE` | int64 | undocumented flag | 0, 1, 2 | categorical | 0 | Video-archive availability flag. |
