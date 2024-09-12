# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

# Load the data
def load_data_1():
    df = pd.read_csv('../Preprocessing/masterupdateafter2000.csv')
    return df

def load_data_2():
    df = pd.read_csv('../Preprocessing/playerswithclub.csv')
    return df

# Creating new columns based on match statistics
def create_new_columns(df):
    # Full-time result for Away Team
    away_team_ftr = df[df['FTR'] == 'A']['AwayTeam'].value_counts()

    # Full-time result for Home Team
    home_team_ftr = df[df['FTR'] == 'H']['HomeTeam'].value_counts()

    # Goals scored by Away Team
    goals_away = df.groupby('AwayTeam')['FTAG'].sum().sort_values(ascending=False)

    # Goals scored by Home Team
    goals_home = df.groupby('HomeTeam')['FTHG'].sum().sort_values(ascending=False)

    # Shots on target by Away Team
    shots_on_target_away = df.groupby('AwayTeam')['AST'].sum().sort_values(ascending=False)

    # Shots on target by Home Team
    shots_on_target_home = df.groupby('HomeTeam')['HST'].sum().sort_values(ascending=False)

    # Head-to-Head Records between HomeTeam and AwayTeam
    h2h_records = df.groupby(['HomeTeam', 'AwayTeam'])['FTR'].value_counts().unstack(fill_value=0)


# Function to calculate win streaks
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

# Process data for model
def prepare_model_data(df):
    model_df = pd.DataFrame()

    # Add raw features for away teams
    model_df['AwayTeam'] = df['AwayTeam']
    model_df['AwayGoals'] = df['FTAG']  # Full-time Away Goals
    model_df['AwayShotsOnTarget'] = df['AST']  # Away Shots on Target

    # Add raw features for home teams
    model_df['HomeTeam'] = df['HomeTeam']
    model_df['HomeGoals'] = df['FTHG']  # Full-time Home Goals
    model_df['HomeShotsOnTarget'] = df['HST']  # Home Shots on Target

    # Add full-time result column for raw match outcome
    model_df['FullTimeResult'] = df['FTR']  # Full-time result: H (Home win), A (Away win), D (Draw)

    # Pre-calculate win and loss streaks for each team
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

# Main function to execute steps
def main():
    df_1 = load_data_1()
    df_2 = load_data_2()

    # Create new columns and generate basic statistics
    create_new_columns(df_1)

    # Prepare data for model
    model_df = prepare_model_data(df_1)

    # Save model_df as CSV file
    model_df.to_csv('../Preprocessing/model_data.csv', index=False)
    print("Model data saved to 'model_data.csv'.")

    # Combine CSV files into one DataFrame
    combined_df = pd.concat([df_2, model_df])

    # Save the combined CSV to a new file
    combined_df.to_csv('../Preprocessing/combined_file.csv', index=False)
    print("Combined data saved to 'combined_file.csv'.")

    # Display the columns of the combined DataFrame
    print(combined_df.columns)

# Run the main function
if __name__ == "__main__":
    main()
