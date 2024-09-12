import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os
import pickle
import pandas as pd

# Function to load the saved encoder
def load_encoder(encoder_path):
    with open(encoder_path, 'rb') as f:
        encoder = pickle.load(f)
    print(f"Encoder loaded from {encoder_path}")
    return encoder

# Function to load df_imputed
def load_imputed_df(df_imputed_path):
    return pd.read_pickle(df_imputed_path)

# Function to encode categorical features using the loaded encoder
def encode_categorical_features_with_saved_encoder(df, encoder, columns):
    for col in columns:
        df[col] = encoder.transform(df[col])
    return df

# Function to define features and target
def get_features_and_target(df, feature_cols, target_col):
    X = df[feature_cols]
    y = df[target_col]
    return X, y

# Function to split the data
def split_data(X, y, test_size=0.2, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

# Function to convert to DMatrix
def create_dmatrix(X_train, X_test, y_train, y_test):
    train_dmatrix = xgb.DMatrix(X_train, label=y_train)
    test_dmatrix = xgb.DMatrix(X_test, label=y_test)
    return train_dmatrix, test_dmatrix

# Function to train XGBoost model
def train_xgb_model(params, train_dmatrix, num_boost_round=100):
    return xgb.train(params=params, dtrain=train_dmatrix, num_boost_round=num_boost_round)

# Function to evaluate model performance
def evaluate_model(y_test, y_pred):
    print("XGBoost Model Performance Report:")
    print(classification_report(y_test, y_pred))

# Function to save the trained model
def save_model(model, path, model_name):
    file_path = os.path.join(path, f'{model_name}.pkl')
    with open(file_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to {file_path}")

# Main execution
if __name__ == "__main__":
    # Load the imputed DataFrame
    df_imputed_path = './Preprocessing/df_imputed.pkl'
    df_imputed = load_imputed_df(df_imputed_path)
    print(f"Imputed DataFrame loaded from {df_imputed_path}")
    
    # Define features and target columns
    features = ['AwayTeam', 'AwayShotsOnTarget', 'HomeTeam', 
                'HomeShotsOnTarget', 'HomeTeamWinStreak', 'AwayTeamWinStreak', 
                'HomeTeamLossStreak', 'AwayTeamLossStreak', 'win_streak_difference', 
                'loss_streak_difference', 'club_value_difference', 
                'HomeTeamLast10Goals', 'AwayTeamLast10Goals', 'HomeTeamLast10Wins', 
                'AwayTeamLast10Wins', 'HomeTeamClubValue', 'AwayTeamClubValue']
    
    target = 'FullTimeResult'
    
    # Load the saved encoder
    encoder_path = './Streamlit/le.pkl'
    encoder = load_encoder(encoder_path)
    
    # Encode categorical columns using the loaded encoder
    categorical_columns = ['HomeTeam', 'AwayTeam']
    df_imputed = encode_categorical_features_with_saved_encoder(df_imputed, encoder, categorical_columns)
    
    # Get features and target
    X, y = get_features_and_target(df_imputed, features, target)
    
    # Split data
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # Create DMatrix
    train_dmatrix, test_dmatrix = create_dmatrix(X_train, X_test, y_train, y_test)
    
    # Define XGBoost parameters
    xgb_params = {
        'objective': 'multi:softmax',
        'num_class': len(y.unique()),
        'max_depth': 10,
        'learning_rate': 0.1,
        'n_estimators': 100,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'seed': 42
    }
    
    # Train the model
    xgb_model = train_xgb_model(xgb_params, train_dmatrix)
    
    # Make predictions
    y_pred = xgb_model.predict(test_dmatrix)
    
    # Evaluate the model
    evaluate_model(y_test, y_pred)
    
    # Save the trained model
    model_path = './Streamlit/'
    model_name = 'best_model'
    save_model(xgb_model, model_path, model_name)
