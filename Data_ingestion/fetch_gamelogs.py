"""Pull NBA game logs from stats.nba.com into data/raw/.

Target variable for the project: FG3M (three-pointers made) per player per game.

One request per season returns every player's box score for that season, so the
whole dataset is ~15 requests, not one per player. Team logs come from the same
endpoint and carry opponent context (pace, 3PT defense) for later features.

Raw files are written untouched -- no renaming, no derived columns. Cleaning and
feature engineering belong downstream.

Usage:
    python fetch_gamelogs.py                      # 2015-16 .. current, regular season
    python fetch_gamelogs.py --start 2020-21
    python fetch_gamelogs.py --playoffs
    python fetch_gamelogs.py --refresh            # re-download cached seasons
"""

import argparse
import time
from pathlib import Path

import pandas as pd
from nba_api.stats.endpoints import leaguegamelog
from requests.exceptions import ReadTimeout

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
START_SEASON = "2015-16"
PAUSE = 1.5          # seconds between requests; stats.nba.com throttles bursts
TIMEOUT = 60
RETRIES = 3


def season_str(start_year):
    """2024 -> '2024-25'"""
    return f"{start_year}-{str(start_year + 1)[-2:]}"


def current_season_start(today=None):
    """NBA seasons open in October, so Jan-Sep belongs to the previous start year."""
    today = today or pd.Timestamp.today()
    return today.year if today.month >= 10 else today.year - 1


def seasons_through_now(start=START_SEASON):
    first = int(start[:4])
    return [season_str(y) for y in range(first, current_season_start() + 1)]


def fetch(season, player_or_team, season_type):
    for attempt in range(RETRIES):
        try:
            return leaguegamelog.LeagueGameLog(
                player_or_team_abbreviation=player_or_team,
                season=season,
                season_type_all_star=season_type,
                timeout=TIMEOUT,
            ).get_data_frames()[0]
        except (ReadTimeout, ConnectionError) as e:
            wait = PAUSE * 2 ** attempt
            print(f"  retry {attempt + 1}/{RETRIES} after {type(e).__name__}, {wait:.0f}s")
            time.sleep(wait)
    raise RuntimeError(f"{season} {player_or_team} failed after {RETRIES} tries")


def pull(seasons, season_type, refresh):
    tag = "playoffs" if season_type == "Playoffs" else "regular"
    frames = {"player": [], "team": []}

    for season in seasons:
        for kind, abbr in (("player", "P"), ("team", "T")):
            path = RAW / f"{kind}_gamelogs_{tag}_{season}.csv"
            if path.exists() and not refresh:
                df = pd.read_csv(path, dtype={"GAME_ID": str, "SEASON_ID": str})
                print(f"{season} {kind:6s} cached {df.shape}")
            else:
                df = fetch(season, abbr, season_type)
                if df.empty:
                    print(f"{season} {kind:6s} no games yet")
                    continue
                df.to_csv(path, index=False)
                print(f"{season} {kind:6s} pulled {df.shape} -> {path.name}")
                time.sleep(PAUSE)
            frames[kind].append(df)

    for kind, parts in frames.items():
        if not parts:
            continue
        out = RAW / f"{kind}_gamelogs_{tag}.csv"
        combined = pd.concat(parts, ignore_index=True)
        combined.to_csv(out, index=False)
        print(f"\ncombined {kind}: {combined.shape} -> {out}")
        if kind == "player":
            summarize(combined)


def summarize(df):
    df = df.copy()
    df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])
    print(f"  dates     {df.GAME_DATE.min():%Y-%m-%d} .. {df.GAME_DATE.max():%Y-%m-%d}")
    print(f"  players    {df.PLAYER_ID.nunique()}   games {df.GAME_ID.nunique()}")
    print(f"  FG3M       mean {df.FG3M.mean():.2f}  max {df.FG3M.max()}  zero-share {(df.FG3M == 0).mean():.1%}")
    missing = df.isna().sum()
    print(f"  missing    {dict(missing[missing > 0])}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--start", default=START_SEASON, help="first season, e.g. 2015-16")
    p.add_argument("--playoffs", action="store_true", help="pull Playoffs instead of Regular Season")
    p.add_argument("--refresh", action="store_true", help="ignore cached CSVs")
    a = p.parse_args()

    RAW.mkdir(parents=True, exist_ok=True)
    pull(seasons_through_now(a.start), "Playoffs" if a.playoffs else "Regular Season", a.refresh)
