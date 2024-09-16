# Import the necessary libraries
import pandas as pd
import numpy as np
import csv
import datetime

# Load data
df = pd.read_csv("database/csv_files/masterupdateafter2000.csv")

# Full-time result analysis
away_team_ftr = df[df['FTR'] == 'A']['AwayTeam'].value_counts()
home_team_ftr = df[df['FTR'] == 'H']['HomeTeam'].value_counts()

# Goals scored
goals_away = df.groupby('AwayTeam')['FTAG'].sum().sort_values(ascending=False)
goals_home = df.groupby('HomeTeam')['FTHG'].sum().sort_values(ascending=False)

# Shots on target
shots_on_target_away = df.groupby('AwayTeam')['AST'].sum().sort_values(ascending=False)
shots_on_target_home = df.groupby('HomeTeam')['HST'].sum().sort_values(ascending=False)

# Head-to-Head Records
h2h_records = df.groupby(['HomeTeam', 'AwayTeam'])['FTR'].value_counts().unstack(fill_value=0)

# A function to calculate win streaks
def win_streaks(df, team):
    wins = df['FTR'][df['HomeTeam'] == team].apply(
        lambda x: 1 if x == 'H' else 0).values
    streaks = []
    streak = 0
    for win in wins:
        if win == 1:
            streak += 1
        else:
            streaks.append(streak)
            streak = 0
    streaks.append(streak)
    return max(streaks)


# Calculate win streaks for home and away teams
df['HomeTeamWinStreak'] = df['HomeTeam'].apply(lambda x: win_streaks(df, x))
df['AwayTeamWinStreak'] = df['AwayTeam'].apply(lambda x: win_streaks(df, x))

# A function to calculate loss streaks
def loss_streaks(df, team):
    losses = df['FTR'][df['HomeTeam'] == team].apply(
        lambda x: 1 if x == 'A' else 0).values
    streaks = []
    streak = 0
    for loss in losses:
        if loss == 1:
            streak += 1
        else:
            streaks.append(streak)
            streak = 0
    streaks.append(streak)
    return max(streaks)


# Calculate loss streaks for home and away teams
df['HomeTeamLossStreak'] = df['HomeTeam'].apply(lambda x: loss_streaks(df, x))
df['AwayTeamLossStreak'] = df['AwayTeam'].apply(lambda x: loss_streaks(df, x))

# Create new DataFrame for model selection
model_df = pd.DataFrame()

# Add features for away and home teams
model_df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True)
model_df['AwayTeam'] = df['AwayTeam']
model_df['AwayGoals'] = df['FTAG']
model_df['AwayShotsOnTarget'] = df['AST']
model_df['HomeTeam'] = df['HomeTeam']
model_df['HomeGoals'] = df['FTHG']
model_df['HomeShotsOnTarget'] = df['HST']
model_df['FullTimeResult'] = df['FTR']

# Calculate win and loss streaks for each team


def calculate_streaks(df, team, is_home=True):
    results = df['FTR'][df['HomeTeam'] ==
                        team] if is_home else df['FTR'][df['AwayTeam'] == team]
    streaks = []
    streak = 0
    for result in results:
        if (is_home and result == 'H') or (not is_home and result == 'A'):
            streak += 1
        else:
            if streak > 0:
                streaks.append(streak)
            streak = 0
    if streak > 0:
        streaks.append(streak)
    return max(streaks) if streaks else 0

# Pre-calculate streaks
home_team_win_streaks = {team: calculate_streaks(df, team, is_home=True) for team in df['HomeTeam'].unique()}
away_team_win_streaks = {team: calculate_streaks(df, team, is_home=False) for team in df['AwayTeam'].unique()}
home_team_loss_streaks = {team: calculate_streaks(df, team, is_home=True) for team in df['HomeTeam'].unique()}
away_team_loss_streaks = {team: calculate_streaks(df, team, is_home=False) for team in df['AwayTeam'].unique()}

# Map streaks to the DataFrame
model_df['HomeTeamWinStreak'] = df['HomeTeam'].map(home_team_win_streaks)
model_df['AwayTeamWinStreak'] = df['AwayTeam'].map(away_team_win_streaks)
model_df['HomeTeamLossStreak'] = df['HomeTeam'].map(home_team_loss_streaks)
model_df['AwayTeamLossStreak'] = df['AwayTeam'].map(away_team_loss_streaks)

# Save the DataFrame to a CSV file
model_df.to_csv('database/csv_files/model_df.csv')

# The list of teams for the 2024/2025 season
teams_season_24_25 = sorted(list(model_df[model_df['Date'] > '2024-07-24']['HomeTeam'].unique()))

# A dictionary to map team names to team ids
map_teams_names = {
    "Dender": 8,
    "Standard": 25,
    "Kortrijk": 13,
    "Club Brugge": 7,
    "Anderlecht": 1,
    "Westerlo": 28,
    "Cercle Brugge": 5,
    "Genk": 10,
    "Antwerp": 2,
    "St. Gilloise": 24,
    "St Truiden": 23,
    "Oud-Heverlee Leuven": 20,
    "Charleroi": 6,
    "Beerschot VA": 3,
    "Gent": 11,
    "Mechelen": 16
}

# Create a DataFrame with the current statistics of the teams for the 2024/2025 season
teams_season_24_25_df = pd.DataFrame(teams_season_24_25, columns=["team_name"])

# A function to calculate the number of shots on target for the home team
def home_shots_on_target(team):
    return model_df[model_df['HomeTeam'] == team]\
        .sort_values(by="Date", ascending=False).head(1)['HomeShotsOnTarget'].iloc[0]

# A function to calculate the number of shots on target for the away team
def away_shots_on_target(team):
    return model_df[model_df['AwayTeam'] == team]\
        .sort_values(by="Date", ascending=False).head(1)['AwayShotsOnTarget'].iloc[0]

# A function to calculate the number of goals scored by the home team
def home_goals(team):
    return model_df[model_df['HomeTeam'] == team].sort_values(by="Date", ascending=False).head(1)['HomeGoals'].iloc[0]

# A function to calculate the number of goals scored by the away team
def away_goals(team):
    return model_df[model_df['AwayTeam'] == team].sort_values(by="Date", ascending=False).head(1)['AwayGoals'].iloc[0]

# A function to calculate the number of wins for the home team in the last 10 matches
def home_team_last_10_wins(team):
    return model_df[model_df['HomeTeam'] == team]\
        .sort_values(by="Date", ascending=False)['FullTimeResult'].head(10).value_counts().get('A', 0)

# A function to calculate the number of wins for the away team in the last 10 matches
def away_team_last_10_wins(team):
    return model_df[model_df['AwayTeam'] == team]\
        .sort_values(by="Date", ascending=False)['FullTimeResult'].head(10).value_counts().get('A', 0)

# Fill the DataFrame with the statistics
teams_season_24_25_df["team_id"] = teams_season_24_25_df["team_name"].map(map_teams_names)

teams_season_24_25_df["home_shots_on_target"] = teams_season_24_25_df["team_name"].map(
    lambda x: home_shots_on_target(x))

teams_season_24_25_df["away_shots_on_target"] = teams_season_24_25_df["team_name"].map(
    lambda x: away_shots_on_target(x))

teams_season_24_25_df["home_wins_streak"] = teams_season_24_25_df["team_name"].map(
    lambda x: home_team_win_streaks[x])

teams_season_24_25_df["away_wins_streak"] = teams_season_24_25_df["team_name"].map(
    lambda x: away_team_win_streaks[x])

teams_season_24_25_df["home_losses_streak"] = teams_season_24_25_df["team_name"].map(
    lambda x: home_team_loss_streaks[x])

teams_season_24_25_df["away_losses_streak"] = teams_season_24_25_df["team_name"].map(
    lambda x: away_team_loss_streaks[x])

teams_season_24_25_df["home_goals"] = teams_season_24_25_df["team_name"].map(
    lambda x: home_goals(x))

teams_season_24_25_df["away_goals"] = teams_season_24_25_df["team_name"].map(
    lambda x: away_goals(x))

teams_season_24_25_df["last_10_home_wins"] = teams_season_24_25_df["team_name"].map(
    lambda x: home_team_last_10_wins(x))

teams_season_24_25_df["away_10_awy_wins"] = teams_season_24_25_df["team_name"].map(
    lambda x: away_team_last_10_wins(x))

# Convert float columns to integer columns
for name in teams_season_24_25_df.columns:
    if teams_season_24_25_df[name].dtype == "float64":
        teams_season_24_25_df[name] = teams_season_24_25_df[name].astype(
            "int64")

# Save the DataFrame to a CSV file to be used to fill in the season_teams table in the database
teams_season_24_25_df.to_csv('database/csv_files/season_table.csv', header=False, index=False)
