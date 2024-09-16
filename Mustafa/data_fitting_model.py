import numpy as np
import pandas as pd

def calculate_streaks(df, team, is_home=True):
    results = df['FTR'][df['HomeTeam'] == team] if is_home else df['FTR'][df['AwayTeam'] == team]
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

def preprocess_data(df):
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

    # Calculate win streaks
    df['HomeTeamWinStreak'] = df['HomeTeam'].apply(lambda x: calculate_streaks(df, x, is_home=True))
    df['AwayTeamWinStreak'] = df['AwayTeam'].apply(lambda x: calculate_streaks(df, x, is_home=False))

    # Calculate loss streaks
    df['HomeTeamLossStreak'] = df['HomeTeam'].apply(lambda x: calculate_streaks(df, x, is_home=True))
    df['AwayTeamLossStreak'] = df['AwayTeam'].apply(lambda x: calculate_streaks(df, x, is_home=False))

    # Create new DataFrame for model selection
    model_df = pd.DataFrame()

    # Add features for away and home teams
    model_df['AwayTeam'] = df['AwayTeam']
    model_df['AwayGoals'] = df['FTAG']
    model_df['AwayShotsOnTarget'] = df['AST']
    model_df['HomeTeam'] = df['HomeTeam']
    model_df['HomeGoals'] = df['FTHG']
    model_df['HomeShotsOnTarget'] = df['HST']
    model_df['FullTimeResult'] = df['FTR']

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

    return model_df

def save_data(model_df, save_path):
    # Save to CSV
    model_df.to_csv(save_path, index=False)

def main_process():
    # File paths
    data_file_path = 'fixture_project/data/mergeddata/masterupdateafter2000.csv'
    save_path = 'fixture_project/Model/model_df.csv'

    # Load data
    df = pd.read_csv(data_file_path)

    # Process data
    model_df = preprocess_data(df)

    # Save processed data
    save_data(model_df, save_path)

