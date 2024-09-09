import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pickle

# Function to load the model
def load_model():
    with open('Gradient Boosting.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

# Function to load the encoders
def load_encoders():
    with open('encoder.pkl', 'rb') as f:
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
    with open('encoder.pkl', 'wb') as f:
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

    # Sidebar

    st.sidebar.header('Match Details')
    st.sidebar.markdown('Enter the details of the match to predict the outcome:')
    user_input = {}

    # Get user input

    user_input['Date'] = st.sidebar.date_input('Date')
    user_input['HomeTeam'] = st.sidebar.text_input('Home Team')
    user_input['AwayTeam'] = st.sidebar.text_input('Away Team')
    

                                            

    # Preprocess the input
    input_data = preprocess_input(user_input, encoders)

    # Predict button
    if st.button('Predict Outcome'):
        # Perform prediction
        prediction = model.predict(input_data)
        st.write(f'Predicted result: {prediction[0]}')

if __name__ == '__main__':
    main()
