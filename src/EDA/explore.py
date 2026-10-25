"""Get basic statistics about NBA data and making figures to /figures.

Target variable for the project: FG3M (three-pointers made) per player per game.

Usage:
    python src/EDA/explore.py     
"""

import argparse
import time
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from requests.exceptions import ReadTimeout

RAWDATA = Path(__file__).resolve().parents[2] / "data" / "raw"
FIGURESPATH = Path(__file__).resolve().parents[2] / "figures"
START_SEASON = "2015-16"


'''
read all the files in the given directory and describe the two main with visuals
''' 
def read_files() :
    pd.set_option('display.max_columns', None) #do not truncate
    for item in RAWDATA.iterdir() :
        if item.is_file() :
            describe_files(item, 'FG3M')


'''
writes out descriptive statistsics
PARAMS:
    path, path for the file to examine
    target, the column in the data to look for
'''
def describe_files(path, target) :
    if path.stem ==  "player_gamelogs_regular" :
        df = pd.read_csv(path)
        df = df.drop(columns = ['WL', 'VIDEO_AVAILABLE', 'PLUS_MINUS', 'FTM']) #not used
        print("Descriptive Statistics of the regular season player game logs: ")
        print(df.describe())

        print("Column types: ")
        print(df.dtypes)

        print("Shape: ")
        print(df.shape)

        remove = ['FG_PCT', 'FT_PCT', 'FG3_PCT', 'PLAYER_ID', 'PLAYER_NAME', 'SEASON_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_ID', 'MATCHUP', 'GAME_DATE', target]
        print(topCorrelations(df, target, remove, 3))

        playerAvg3Min(df, 15)
        corrPFtoFG3M(df)

    if path.stem == "team_gamelogs_regular" :
        df = pd.read_csv(path)
        df = df.drop(columns = ['WL', 'VIDEO_AVAILABLE', 'PLUS_MINUS', 'FTM']) #not used in analysis
        print("Descriptive statistics of the regular season team game logs: ")
        print(df.describe())

        print("Column types: ")
        print(df.dtypes)

        print("Shape: ")
        print(df.shape)

        remove = ['FG_PCT', 'FT_PCT', 'FG3_PCT', 'SEASON_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_ID', 'MATCHUP', 'GAME_DATE', target]
        print(topCorrelations(df, target, remove, 3))

        teamAvg3(df)


'''
gets the most correlated column names in relation to a given column
PARAMS: 
    df, the dataframe to get the top correlations from 
    target, the target variable to correlate to
    remove, the clist of columns to remove
    topNum, the number of top correlations to return

RETURN:
    the top 1 or topNum amount of most correlated columns
'''
def topCorrelations(df, target, remove, topNum):
    #remove the target and all non useful columns
    tempDf = df.drop(columns = remove)
    targetColumn = df[target]
    correlations = np.zeros(tempDf.shape[1])

    if tempDf.shape[1] == 0: #if the df has no more columns
        return ""
    
    for i in range(len(tempDf.columns)):
        correlations[i] = targetColumn.corr(tempDf.iloc[:,i])

    if topNum > tempDf.shape[1] : #return only the single most correlated if not enough columns
        return str(tempDf.columns[np.argmax(correlations)])
    else :
        topXInd = np.argsort(correlations)[-topNum:][::-1]
        return str(tempDf.columns[topXInd])


'''
Makes hirtorical bar chart of teams vs num 3/min
PARAMS
    df, data to traverse over
'''
def teamAvg3(df):
    names = df.groupby(['TEAM_ID', 'TEAM_ABBREVIATION'])
    names = names.agg(SUM_3 = ('FG3M', 'sum'),
                      TOTAL_GAMES = ('GAME_ID', 'count')).reset_index()

    plt.bar(names['TEAM_ABBREVIATION'], names['SUM_3']/names['TOTAL_GAMES'], color = 'g', edgecolor = 'r')
    plt.xticks(rotation = 70)
    plt.xlim()
    plt.xlabel("Teams")
    plt.ylabel("Average Field Goal 3 Pointers Made")
    plt.title("Historical Average Field Goal 3 Pointers Made Per Team Per Game (Regular Seasons 2015-2026)")
    #plt.tight_layout()
    plt.plot()
    plt.savefig(FIGURESPATH/ "3_Avg_Team_Game", dpi=300, bbox_inches="tight")
    plt.close()


'''
creates a scatter plot of the avgerage personal fould to average fg3m
PARAM:
    df, dataframe to equate over
'''
def corrPFtoFG3M(df):
    grouped = df.groupby(['PLAYER_ID', 'PLAYER_NAME'])
    grouped = grouped.agg(PF = ('PF', 'mean'),
                          FG3M = ('FG3M', 'mean'))

    plt.scatter(grouped['PF'], grouped['FG3M']) #plots
    plt.xlabel('Mean Personal Fouls')
    plt.ylabel('Mean Field Goal 3 Made')
    plt.title("All Personal Fouls vs Field Goal 3 Made Per Player (2015-2026 Regular Season)")
    plt.plot()

    plt.savefig(FIGURESPATH/"Player_PF_FG3M", dpi=300, bbox_inches="tight")
    plt.close()




'''
Calculates and visualizes the per player stats
PARAMS:
    df, the dataframe to iteratoe over
    pct, part of the graphs to show, how many of the top and bottom of each player to show
'''
def playerAvg3Min(df, pct):
    if pct > 10 :
        pct = 10
    names = df.groupby(['PLAYER_ID', 'PLAYER_NAME'])
    names = names.agg(MIN = ('MIN', 'sum'),
                      FG3M = ('FG3M', 'sum')).reset_index()
    names = names[names['MIN'] >= 48] #played at leaast one full game in minutes over the 10 years 
    sortedList = names.sort_values(by = 'MIN')

    top = sortedList[:pct]
    bottom = sortedList[len(sortedList) - pct:]
    extremes = pd.concat([top, bottom]).drop_duplicates()

    for name, player in extremes.groupby('PLAYER_NAME') : #plot, color by name
        plt.scatter( player['MIN'], player['FG3M'], label = name)
    plt.title(f"Total Minutes Played vs Field Goal 3's Made of Top and Bottom {pct} Players (Regular Seasons 2015-2026)")
    plt.xlabel("Total Minutes Played")
    plt.ylabel("Field Goal 3 Pointers Made")

    z = np.polyfit(extremes['MIN'], extremes['FG3M'], 1) #trendline 
    p = np.poly1d(z)
    x = np.sort(extremes['MIN'])
    plt.plot(x, p(x), 'r--', label = "Trendline")

    plt.legend(title = 'Player Name', bbox_to_anchor = (1.05, 1), loc = "upper left" )

    plt.savefig(FIGURESPATH/"Player_Minutes_FG3M", dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    RAWDATA.mkdir(parents=True, exist_ok=True)
    FIGURESPATH.mkdir(parents = True, exist_ok = True)
    read_files()
