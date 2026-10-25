# EDA

Target: **FG3M** — three-pointers made by a player in a game.

## Source

all raw data in ../data/raw

## Run

```bash
/Users/rubenchung/DATA1030-fall2026/.venv/bin/python src/EDA/explore.py
```

utilizes DATA1030 environment with no changes

## What lands in `figures` 

| file | grain |
| --- | --- |
| `3_Avg_Team_Game.png` | historical bar chart team average FG3M |
| `Player_Minutes_FG3M.png` | top and bottom X players minutes played to FG3M over 2015-2026 |
| `Player_PF_FG3M.png` | all players mean PF to FG3M over 2015-2026 |


## Terminal outputs
  - Seasons 2015-16 and  2025-26 regular season .describe() stats
  - top X correlated column(s) and the correlation coefficient for player_gamelogs_regular and team_gamelogs_regular
  - player_gamelogs_regular and team_gamelogs_regular column .dtypes
  - player_gamelogs_regular and team_gamelogs_regular shape


