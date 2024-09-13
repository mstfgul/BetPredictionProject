# Import libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import os
import pickle

# Load the data
df = pd.read_csv('../Preprocessing/model_df.csv')

# Feature engineering
df['win_streak_difference'] = df['HomeTeamWinStreak'] - df['AwayTeamWinStreak']
df['loss_streak_difference'] = df['HomeTeamLossStreak'] - df['AwayTeamLossStreak']
df['HomeTeamLast10Goals'] = df['HomeGoals'] - df['HomeGoals'].shift(10)
df['AwayTeamLast10Goals'] = df['AwayGoals'] - df['AwayGoals'].shift(10)
df['HomeTeamLast10Wins'] = df['HomeTeamWinStreak'] - df['HomeTeamWinStreak'].shift(10)
df['AwayTeamLast10Wins'] = df['AwayTeamWinStreak'] - df['AwayTeamLast10Wins'].shift(10)

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

# Define features and target
features = ['AwayTeam', 'AwayShotsOnTarget', 'HomeTeam', 'HomeShotsOnTarget',
            'HomeTeamWinStreak', 'AwayTeamWinStreak', 'HomeTeamLossStreak',
            'AwayTeamLossStreak', 'win_streak_difference', 'loss_streak_difference',
            'HomeTeamLast10Goals', 'AwayTeamLast10Goals', 'HomeTeamLast10Wins',
            'AwayTeamLast10Wins']

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

# Save the best model to file
path = '../Streamlit/'
filename_model = 'model.pkl'
file_path_model = os.path.join(path, filename_model)

with open(file_path_model, 'wb') as file:
    pickle.dump(best_log_model, file)

# Save the encoder to file
filename_encoder = 'le.pkl'
file_path_encoder = os.path.join(path, filename_encoder)

with open(file_path_encoder, 'wb') as file:
    pickle.dump(le, file)
