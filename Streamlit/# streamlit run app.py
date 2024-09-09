import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pickle

# Function to load the model
def load_model():
    with open('gradient_boosting.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

# Function to load the encoders
def load_encoders():
    with open('label_encoders.pkl', 'rb') as f:
        encoders = pickle.load(f)
    return encoders

# Load the cleaned dataset
df = pd.read_csv('../visualizations/df_filled.csv')

# Define columns to encode (just the column names, without descriptions)
columns_to_encode = ['FTR', 'HTR', 'Date', 'HomeTeam', 'AwayTeam']

# Function to label encode the dataset
def label_encode(df, columns_to_encode):
    encoders = {}
    for col in columns_to_encode:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le  # Store the encoder for each column

    # Save the encoders to a file
    with open('label_encoders.pkl', 'wb') as f:
        pickle.dump(encoders, f)

    return df

# Ensure dataset is label encoded
df = label_encode(df, columns_to_encode)

# Function to preprocess user input
def preprocess_input(user_input, encoders):
    user_input_df = pd.DataFrame([user_input])
    
    # Apply the encoders to the relevant columns
    for col in columns_to_encode:
        if col in user_input_df:
            user_input_df[col] = encoders[col].transform(user_input_df[col])
    
    return user_input_df

# Main function to run the Streamlit app
def main():
    st.title('Football Match Predictor')

    # Load model and encoders
    model = load_model()
    encoders = load_encoders()

    # User input fields
    st.header('Enter match details:')
    home_team = st.selectbox('Home Team', df['HomeTeam'].unique())
    away_team = st.selectbox('Away Team', df['AwayTeam'].unique())
    date = st.date_input('Match Date')
    half_time_result = st.selectbox('Half Time Result (H/D/A)', ['H', 'D', 'A'])
    full_time_result = st.selectbox('Full Time Result (H/D/A)', ['H', 'D', 'A'])

    # Collect user input
    user_input = {
        'HomeTeam': home_team,
        'AwayTeam': away_team,
        'Date': date.strftime('%Y-%m-%d'),  # Convert date to string
        'HTR': half_time_result,
        'FTR': full_time_result
    }

    # Preprocess the input
    input_data = preprocess_input(user_input, encoders)

    # Predict button
    if st.button('Predict Outcome'):
        # Perform prediction
        prediction = model.predict(input_data)
        st.write(f'Predicted result: {prediction[0]}')

if __name__ == '__main__':
    main()
