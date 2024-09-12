import numpy as np
import pandas as pd
import os
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import KNNImputer

# Function to load the dataset
def load_data(file_path):
    return pd.read_csv(file_path)

# Function to drop unwanted columns
def drop_columns(df, columns_to_drop):
    return df.drop(columns=columns_to_drop, axis=1)

# Function to create new features
def create_features(df):
    # 1. Goal difference as a feature
    df['goal_difference'] = df['HomeGoals'] - df['AwayGoals']

    # 4. Win streak difference (HomeTeamWinStreak - AwayTeamWinStreak)
    df['win_streak_difference'] = df['HomeTeamWinStreak'] - df['AwayTeamWinStreak']

    # 5. Loss streak difference (HomeTeamLossStreak - AwayTeamLossStreak)
    df['loss_streak_difference'] = df['HomeTeamLossStreak'] - df['AwayTeamLossStreak']

    # 6. Club value difference
    df['club_value_difference'] = df['club_value']

    # 7. Last 10 games goals for home and away
    df['HomeTeamLast10Goals'] = df['HomeGoals'] - df['HomeGoals'].shift(10)
    df['AwayTeamLast10Goals'] = df['AwayGoals'] - df['AwayGoals'].shift(10)

    # 8. Last 10 games wins for home and away
    df['HomeTeamLast10Wins'] = df['HomeTeamWinStreak'] - df['HomeTeamWinStreak'].shift(10)
    df['AwayTeamLast10Wins'] = df['AwayTeamWinStreak'] - df['AwayTeamWinStreak'].shift(10)

    # 9. Club value for home and away
    df['HomeTeamClubValue'] = df['club_value']
    df['AwayTeamClubValue'] = df['club_value']

    return df

# Function to encode categorical columns
def encode_teams(df, path, filename):
    all_teams = list(df['HomeTeam'].unique()) + list(df['AwayTeam'].unique())
    encoder = LabelEncoder()
    encoder.fit(all_teams)

    file_path = os.path.join(path, filename)
    with open(file_path, 'wb') as f:
        pickle.dump(encoder, f)
    
    print(f"Encoders saved to {file_path}")
    return encoder

# Function to fill missing values using KNNImputer
def fill_missing_values(df):
    imputer = KNNImputer(n_neighbors=50)
    df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
    return df_imputed

# Function to prepare final DataFrame
def prepare_final_df(df, path='../Streamlit/', filename='le.pkl'):
    # Step 1: Drop columns
    columns_to_drop = ['age', 'name', 'position', 'club', 'market']
    df = drop_columns(df, columns_to_drop)

    # Step 2: Create new features
    df = create_features(df)

    # Step 3: Encode categorical features
    encode_teams(df, path, filename)

    # Step 4: Fill missing values
    df_imputed = fill_missing_values(df)

    # Step 5: Return the final DataFrame
    return df_imputed

# Main execution
if __name__ == "__main__":
    # Load dataset
    df = load_data('../Preprocessing/combined_file.csv')

    # Prepare final DataFrame
    final_df = prepare_final_df(df)
    print(final_df.head())
