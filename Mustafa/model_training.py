import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import os
import pickle

def preprocess_data(file_path):
    # Load the data
    df = pd.read_csv(file_path)

    # Feature engineering
    df['win_streak_difference'] = df['HomeTeamWinStreak'] - df['AwayTeamWinStreak']
    df['loss_streak_difference'] = df['HomeTeamLossStreak'] - df['AwayTeamLossStreak']
    
    # Create new columns for 'HomeTeamLast10Wins' and 'AwayTeamLast10Wins'
    
    # Encode categorical features
    columns = ['HomeTeam', 'AwayTeam', 'FullTimeResult']
    le = LabelEncoder()
    df[columns] = df[columns].apply(le.fit_transform)

    # Impute missing values
    def fill_missing_values(df):
        imputer = KNNImputer(n_neighbors=50)
        df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
        return df_imputed

    df_imputed = fill_missing_values(df)

    return df_imputed, le

def train_and_evaluate(df_imputed, le):
    # Define features and target
    features = ['AwayTeam', 'AwayShotsOnTarget', 'HomeTeam', 'HomeShotsOnTarget',
                'HomeTeamWinStreak', 'AwayTeamWinStreak', 'HomeTeamLossStreak',
                'AwayTeamLossStreak', 'win_streak_difference', 'loss_streak_difference']

    X = df_imputed[features]
    y = df_imputed['FullTimeResult']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define a grid of hyperparameters for Logistic Regression
    param_grid = {
        'C': [0.01, 0.1, 1, 10, 100],
        'penalty': ['l1', 'l2'],
        'solver': ['liblinear', 'saga']
    }

    # Initialize the Logistic Regression model
    log_model = LogisticRegression(max_iter=1000, random_state=42)

    # Perform grid search with cross-validation
    grid_search = GridSearchCV(log_model, param_grid, cv=5)
    grid_search.fit(X_train, y_train)

    # Best parameters from the grid search
    print(f"Best parameters for Logistic Regression: {grid_search.best_params_}")

    # Retrain Logistic Regression with the best parameters
    best_log_model = grid_search.best_estimator_
    y_pred = best_log_model.predict(X_test)

    # Evaluate the model performance
    print("Logistic Regression Model Performance Report with Best Parameters:")
    print(classification_report(y_test, y_pred))

    return best_log_model

def save_model_and_encoder(model, encoder, model_path, encoder_path):
    # Save the best model to file
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)

    # Save the encoder to file
    with open(encoder_path, 'wb') as file:
        pickle.dump(encoder, file)

def main():
    # File paths
    data_file_path = 'fixture_project/Model/model_df.csv'
    model_save_path = 'fixture_project/Model/Streamlit/model.pkl'
    encoder_save_path = 'fixture_project/Model/Streamlit/le.pkl'

    # Preprocess data
    df_imputed, le = preprocess_data(data_file_path)

    # Train and evaluate the model
    best_log_model = train_and_evaluate(df_imputed, le)

    # Save the model and encoder
    save_model_and_encoder(best_log_model, le, model_save_path, encoder_save_path)

