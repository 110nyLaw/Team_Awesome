# Predicting NBA Players’ Three-Point Production Using Machine Learning

**DATA1030 | Brown University | Fall 2026**  
**Team Awesome:** Yinge Tong, Nyla Lawrence, and Ruben Chung

## Project overview

We aim to predict how many three-pointers an NBA player will make in their next game appearance using past performance and game context. The target is three-point field goals made (`FG3M`), framed as a regression problem.

Our midterm work covers data collection and exploratory analysis. Model training is planned for the next stage, using earlier games to predict later games.

## Data

We collect player and team game logs from [NBA Stats](https://www.nba.com/stats/) using the `LeagueGameLog` endpoint of [`nba_api`](https://github.com/swar/nba_api).
The team's documented dataset covers the 2015–16 through 2025–26 regular seasons:

| Dataset | Observations | Unit of observation |
| --- | ---: | --- |
| Player game logs | 281,163 | One player’s appearance in one game |
| Team game logs | 26,418 | One team in one game |

The collection includes 1,554 players and 13,209 games. Raw CSV files are excluded from GitHub.

- [Collection details](src/Data_ingestion/README.md)
- [Data dictionary](src/Data_ingestion/data_dictionary.md)

## Repository structure

```text
Team_Awesome/
├── README.md
├── LICENSE
├── data1030.yml
├── data/
│   └── raw/                  # Combined and per-season CSV files
├── report/
│   └── midterm.pdf
├── figures/                  
└── src/
    ├── Data_ingestion/
    │   ├── README.md
    │   ├── data_dictionary.md
    │   └── fetch_gamelogs.py
    └── EDA/
        ├── README.md
        └── explore.py
```
## Running the scripts

The supplied [Conda environment file](data1030.yml) specifies Python 3.14.6, pandas 3.0.3, NumPy 2.4.6, and Matplotlib 3.11.0, along with other course packages.

From the repository root, create and activate the environment:

```bash
conda env create -f data1030.yml
conda activate data1030
```

The YAML includes a machine-specific `prefix: /opt/conda` line. Remove that line before creating the environment on another computer.

Run EDA using the CSV files already included:

```bash
python src/EDA/explore.py
```

This prints statistics and correlations and saves three plots to `figures/`.

To download fresh data, first install the collection dependencies, which are not explicitly listed in the YAML:

```bash
python -m pip install nba_api requests
python src/Data_ingestion/fetch_gamelogs.py
```

The collection script caches each season and combines the results into player and team CSV files. It requires internet access for new downloads. Available options are `--start 2020-21`, `--playoffs`, and `--refresh`.
**Data range:** The script downloads from 2015–16 through the current season by default. It has no end-season option, so a new download may include games outside the report's period. The existing figures describe the documented 2015–16 through 2025–26 dataset.

## Exploratory analysis
The three figures compare team average three-pointers per game, player cumulative minutes and three-pointers, and player average fouls and three-pointers.

The EDA script removes `WL`, `VIDEO_AVAILABLE`, `PLUS_MINUS`, and `FTM` in memory, leaving 28 player columns and 25 team columns in the documented dataset. It does not change the raw CSV files.


## License

The team’s original code is released under the [MIT License](LICENSE). 


