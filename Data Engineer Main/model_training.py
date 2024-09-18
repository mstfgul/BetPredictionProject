import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import os
import pickle

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def feature_engineering(df):
    df['win_streak_difference'] = df['HomeTeamWinStreak'] - df['AwayTeamWinStreak']
    df['loss_streak_difference'] = df['HomeTeamLossStreak'] - df['AwayTeamLossStreak']
    df['HomeTeamLast10Goals'] = df['HomeGoals'] - df['HomeGoals'].shift(10)
    df['AwayTeamLast10Goals'] = df['AwayGoals'] - df['AwayGoals'].shift(10)
    df['HomeTeamLast10Wins'] = df['HomeTeamWinStreak'] - df['HomeTeamWinStreak'].shift(10)
    df['AwayTeamLast10Wins'] = df['AwayTeamWinStreak'] - df['AwayTeamWinStreak'].shift(10)
    return df

def encode_categorical_features(df, columns):
    le = LabelEncoder()
    df[columns] = df[columns].apply(le.fit_transform)
    return df

def fill_missing_values(df):
    imputer = KNNImputer(n_neighbors=50)
    df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
    return df_imputed

def train_model(df, features, target):
    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    param_grid = {
        'C': [0.01, 0.1, 1, 10, 100],
        'penalty': ['l1', 'l2'],
        'solver': ['liblinear', 'saga']
    }
    
    log_model = LogisticRegression(max_iter=1000, random_state=42)
    grid_search = GridSearchCV(log_model, param_grid, cv=5)
    grid_search.fit(X_train, y_train)
    
    best_log_model = grid_search.best_estimator_
    y_pred = best_log_model.predict(X_test)
    
    return best_log_model, y_test, y_pred

def evaluate_model(y_test, y_pred):
    report = classification_report(y_test, y_pred)
    return report

def save_model(model, encoder, path):
    filename_model = 'model.pkl'
    file_path_model = os.path.join(path, filename_model)
    
    with open(file_path_model, 'wb') as file:
        pickle.dump(model, file)
    
    filename_encoder = 'le.pkl'
    file_path_encoder = os.path.join(path, filename_encoder)
    
    # Define 'le' variable
    le = encoder
    with open(file_path_encoder, 'wb') as file:
        pickle.dump(le, file)

# Define 'encoder' variable
encoder = LabelEncoder()
        
# Main function
def main():
    file_path = '/Users/mustafagul/Desktop/fixture_project/Model/model_df.csv'
    columns = ['HomeTeam', 'AwayTeam', 'FullTimeResult']
    features = ['AwayTeam', 'AwayShotsOnTarget', 'HomeTeam', 'HomeShotsOnTarget',
                'HomeTeamWinStreak', 'AwayTeamWinStreak', 'HomeTeamLossStreak',
                'AwayTeamLossStreak', 'win_streak_difference', 'loss_streak_difference',
                'HomeTeamLast10Goals', 'AwayTeamLast10Goals', 'HomeTeamLast10Wins',
                'AwayTeamLast10Wins']
    target = 'FullTimeResult'
    path = '/Users/mustafagul/Desktop/fixture_project/Model/Streamlit'
    
    df = load_data(file_path)
    df = feature_engineering(df)
    df = encode_categorical_features(df, columns)
    df_imputed = fill_missing_values(df)
    
    model, y_test, y_pred = train_model(df_imputed, features, target)
    report = evaluate_model(y_test, y_pred)
    
    print(f"Best parameters for Logistic Regression: {model.get_params()}")
    print("Logistic Regression Model Performance Report with Best Parameters:")
    print(report)
    
    save_model(model, encoder, path)

if __name__ == "__main__":
    main()
