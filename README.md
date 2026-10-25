# Predicting NBA Players’ Three-Point Production Using Machine Learning

**DATA1030 | Brown University | Fall 2026**  
**Team Awesome:** Yinge Tong, Nyla Lawrence, and Ruben Chung

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

See [the data collection README](src/Data_ingestion/README.md) for additional details about the source, cached files, missing values, and data checks. These descriptive statistics refer to the documented collection; later downloads may contain additional records.

Field definitions are provided in the [data dictionary](src/Data_ingestion/data_dictionary.md).

## Current repository structure

```text
Team_Awesome/
├── README.md
├── LICENSE
├── .gitignore
├── figures/
│   ├── 3_Avg_Team_Game.png
│   ├── Player_Minutes_FG3M.png
│   └── Player_PF_FG3M.png
└── src/
    ├── Data_ingestion/
    │   ├── README.md
    │   ├── data_dictionary.md
    │   └── fetch_gamelogs.py
    └── EDA/
        └── explore.py
```

The EDA code, figures, and data dictionary are included in the repository. The environment file and final midterm report will be added before submission.

## Running the data collection

The script requires Python with `nba_api`, `pandas`, and `requests`. The Python and package versions used by the team will be documented in an environment file; that file is not yet included in the current repository.

For a provisional setup, install the required packages in your Python environment:

```bash
python -m pip install nba_api pandas requests
```

From the repository root, run:

```bash
python src/Data_ingestion/fetch_gamelogs.py
```

The script caches per-season CSV files and combines them into player and team game-log files. Internet access is required for uncached downloads.

The intended output directory is `data/raw/` at the repository root. With the script now located in `src/Data_ingestion/`, this requires `RAW = Path(__file__).resolve().parents[2] / "data" / "raw"`. If the script still uses `parents[1]`, it writes to `src/data/raw/` instead. The output path and the EDA input path need to be aligned before reproducing the analysis.

Optional commands:

```bash
# Start with the 2020–21 season
python src/Data_ingestion/fetch_gamelogs.py --start 2020-21

# Retrieve playoff records instead of regular-season records
python src/Data_ingestion/fetch_gamelogs.py --playoffs

# Download records again instead of using cached files
python src/Data_ingestion/fetch_gamelogs.py --refresh
```

By default, the script requests seasons from 2015–16 through the current season. It does not stop at 2025–26, so running it later may produce a dataset that differs from the midterm dataset.

## Exploratory analysis

The EDA script is located at `src/EDA/explore.py`. The current figures examine team average three-pointers made per game, player cumulative minutes versus cumulative three-pointers, and player average personal fouls versus average three-pointers. Figure files are stored in `figures/`.

## Planned modeling

- Construct historical features without using statistics from the target game.
- Compare regression models on later games and assess their predictive accuracy.
- Examine whether predictions could support opponent preparation and player evaluation.

## License

The team’s original code is released under the [MIT License](LICENSE). This license does not grant rights to NBA data or other third-party materials.

