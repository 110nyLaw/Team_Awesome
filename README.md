# Team_Awesome
Data 1030 Project
# Predicting NBA Players’ Three-Point Production Using Machine Learning

**DATA1030 | Brown University | Fall 2026**  
 Yinge Tong, Nyla Lawrence, and Ruben Chung

## Project overview

This project investigates whether historical player performance and game context can predict the number of three-pointers a player will make in their next NBA game appearance. The target variable is three-point field goals made (`FG3M`), and we frame the prediction as a supervised regression task.

The midterm work focuses on data collection, documentation, and exploratory data analysis. Planned predictors include recent shooting performance, historical playing time, and opponent statistics computed from previous games. We plan to train models on earlier games and evaluate them on later games, using only information available before the target game. Predictions are conditional on player participation.

## Data

Player and team game logs are collected from [NBA Stats](https://www.nba.com/stats/) through the `LeagueGameLog` endpoint of the [`nba_api`](https://github.com/swar/nba_api) Python package.

The documented data collection covers the **2015–16 through 2025–26 regular seasons**:

| Dataset | Observations | Unit of observation |
| --- | ---: | --- |
| Player game logs | 281,163 | One player’s appearance in one game |
| Team game logs | 26,418 | One team in one game |

The player records cover 1,554 distinct players and 13,209 games. Raw CSV files are excluded from version control and can be generated using the collection script.

See [the data collection README](Data_ingestion/README.md) for additional details about the source, cached files, missing values, and data checks. These descriptive statistics refer to the documented collection; later downloads may contain additional records.

## Current repository structure

```text
Team_Awesome/
├── README.md
├── LICENSE
├── .gitignore
└── Data_ingestion/
    ├── README.md
    └── fetch_gamelogs.py
```

The EDA code, figures, data dictionary, environment file, and midterm report will be added as they are finalized.

## Running the data collection

The script requires Python with `nba_api`, `pandas`, and `requests`. The Python and package versions used by the team will be documented in an environment file; that file is not yet included in the current repository.

For a provisional setup, install the required packages in your Python environment:

```bash
python -m pip install nba_api pandas requests
```

From the repository root, run:

```bash
python Data_ingestion/fetch_gamelogs.py
```

The script saves output in `data/raw/`. It caches per-season CSV files and combines them into player and team game-log files. Internet access is required for uncached downloads.

Optional commands:

```bash
# Start with the 2020–21 season
python Data_ingestion/fetch_gamelogs.py --start 2020-21

# Retrieve playoff records instead of regular-season records
python Data_ingestion/fetch_gamelogs.py --playoffs

# Download records again instead of using cached files
python Data_ingestion/fetch_gamelogs.py --refresh
```

By default, the script requests seasons from 2015–16 through the current season. It does not stop at 2025–26, so running it later may produce a dataset that differs from the midterm dataset.

## Planned analysis

- Explore the distribution of player-game `FG3M` and variation across players and teams.
- Construct historical features without using statistics from the target game.
- Compare regression models on later games and assess their predictive accuracy.
- Examine whether predictions could support opponent preparation and player evaluation.

## License

The team’s original code is released under the [MIT License](LICENSE). This license does not grant rights to NBA data or other third-party materials.

