import streamlit as st
import pandas as pd
import pickle

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
label_encoder = load_encoder()  # This should be a LabelEncoder object

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

# Input: Home Team, Away Team, and other features
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



# Feature inputs
input_data = pd.DataFrame({
    'club_value':[club_value],
    'AwayTeam': [Away_Team],
    'AwayGoals': [Away_Goals],
    'AwayShotsOnTarget': [Away_Shots_On_Target],
    'HomeTeam': [Home_Team],
    'HomeGoals': [Home_Goals],
    'HomeShotsOnTarget': [Home_Shots_On_Target],
    'HomeTeamWinsStreak': [Home_Team_Wins_Streak],
    'AwayTeamWinsStreak': [Away_Team_Wins_Streak],
    'HomeTeamLossesStreak': [Home_Team_Losses_Streak],
    'AwayTeamLossesStreak': [Away_Team_Losses_Streak]
    
})

# Encode inputs using the LabelEncoder
input_data['HomeTeam'] = label_encoder.transform(input_data['HomeTeam'])
input_data['AwayTeam'] = label_encoder.transform(input_data['AwayTeam'])

# Button to predict the match result
if st.button("Predict Result"):
    prediction = model.predict(input_data)
    result_map = {0: "Draw", 1: "Home Win", 2: "Away Win"}  # Example of mapping output
    st.subheader(f"Prediction: {result_map[prediction[0]]}")

# Additional Information or Outputs (e.g., probabilities, explanations)
if st.checkbox("Show Prediction Probabilities"):
    probabilities = model.predict_proba(input_data)
    st.write(f"Probability (Draw): {probabilities[0][0]:.2f}")
    st.write(f"Probability (Home Win): {probabilities[0][1]:.2f}")
    st.write(f"Probability (Away Win): {probabilities[0][2]:.2f}")
