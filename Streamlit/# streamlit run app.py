import streamlit as st
import pandas as pd
import pickle

# Load dataset
df = pd.read_csv('../Preprocessing/combined_file.csv')

# Title of the app
st.title("Football Match Prediction")

# Function to load the model
def load_model():
    with open('XGBoost.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

# Function to load the LabelEncoder
def load_encoder():
    with open('label_encoder.pkl', 'rb') as f:
        encoder = pickle.load(f)
    return encoder

# Load the model and encoders
model = load_model()
label_encoder = load_encoder()  # Ensure this is a LabelEncoder object

# Add a background image using custom CSS
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://www.fcbarcelona.com/fcbarcelona/photo/2021/03/13/632f9382-56cb-4d35-af4f-20bc3869ef9c/Low-camp-nou.jpeg");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function to apply the background
add_bg_from_url()

# User Input Section
st.header("Input Match Details")

# Input fields
club_value = st.number_input("Club Value", min_value=0, max_value=1000000000, step=1000000)
Away_Team = st.selectbox("Away Team", df['AwayTeam'].unique())
Away_Goals = st.number_input("Away Goals past 10 games", min_value=0, max_value=10, step=1)
Away_Shots_On_Target = st.number_input("Away Shots on Target past 10 games", min_value=0, max_value=30, step=1)
Home_Team = st.selectbox("Home Team", df['HomeTeam'].unique())
Home_Goals = st.number_input("Home Goals past 10 games", min_value=0, max_value=10, step=1)
Home_Shots_On_Target = st.number_input("Home Shots on Target past 10 games", min_value=0, max_value=30, step=1)
Home_Team_Wins_Streak = st.number_input("Home Team Wins Streak", min_value=0, max_value=10, step=1)
Away_Team_Wins_Streak = st.number_input("Away Team Wins Streak", min_value=0, max_value=10, step=1)
Home_Team_Losses_Streak = st.number_input("Home Team Losses Streak", min_value=0, max_value=10, step=1)
Away_Team_Losses_Streak = st.number_input("Away Team Losses Streak", min_value=0, max_value=10, step=1)

# Calculate differences
win_streak_difference = Home_Team_Wins_Streak - Away_Team_Wins_Streak
loss_streak_difference = Home_Team_Losses_Streak - Away_Team_Losses_Streak
club_value_difference = club_value  # This is currently the same as club_value, adjust if needed

# Create the DataFrame with feature names and their corresponding values
input_data = pd.DataFrame({
    'club_value': [club_value],
    'AwayTeam': [Away_Team],
    'AwayShotsOnTarget': [Away_Shots_On_Target],
    'HomeTeam': [Home_Team],
    'HomeShotsOnTarget': [Home_Shots_On_Target],
    'HomeTeamWinStreak': [Home_Team_Wins_Streak],
    'AwayTeamWinStreak': [Away_Team_Wins_Streak],
    'HomeTeamLossStreak': [Home_Team_Losses_Streak],
    'AwayTeamLossStreak': [Away_Team_Losses_Streak],
    'win_streak_difference': [win_streak_difference],
    'loss_streak_difference': [loss_streak_difference],
    'club_value_difference': [club_value_difference],
    'HomeTeamLast10Goals': [Home_Goals],
    'AwayTeamLast10Goals': [Away_Goals],
    'HomeTeamLast10Wins': [Home_Team_Wins_Streak],  # Adjust if needed
    'AwayTeamLast10Wins': [Away_Team_Wins_Streak]   # Adjust if needed
})

st.write(input_data)

# Encode inputs using the LabelEncoder
input_data['HomeTeam'] = label_encoder.transform(input_data['HomeTeam'])
input_data['AwayTeam'] = label_encoder.transform(input_data['AwayTeam'])

# Button to predict the match result
if st.button("Predict Result"):
    prediction = model.predict(input_data)
    st.write(f"Predicted Value: {prediction[0]}")  # Debug line to check the prediction value
    
    result_map = {0: "Draw", 1: "Home Win", 2: "Away Win"}  # Ensure these keys match the model's output
    
    try:
        st.subheader(f"Prediction: {result_map[prediction[0]]}")
    except KeyError as e:
        st.error(f"Unexpected prediction value: {prediction[0]}. Error: {e}")
        st.write(f"Result map keys: {result_map.keys()}")


