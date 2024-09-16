import streamlit as st
import pandas as pd
import pickle

# Load dataset
df = pd.read_csv('../Preprocessing/model_df.csv')

# Title of the app
st.title("Football Match Prediction")

# Function to load the model
def load_model():
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

# Function to load the LabelEncoder
def load_encoder():
    with open('le.pkl', 'rb') as f:
        encoder = pickle.load(f)
    return encoder

# Load the model and encoders
model = load_model()
label_encoder = load_encoder()

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

# Select the Away and Home teams
Away_Team = st.selectbox("Away Team", options=df['AwayTeam'].unique())
Home_Team = st.selectbox("Home Team", options=df['HomeTeam'].unique())

# Function to retrieve team stats
def get_team_stats(team, df, team_type='Home'):
    """Extract team stats for the selected team"""
    stats = {}
    stats[f'{team_type}ShotsOnTarget'] = df[df[f'{team_type}Team'] == team]['ShotsOnTarget'].mean()
    stats[f'{team_type}WinStreak'] = df[df[f'{team_type}Team'] == team]['WinStreak'].mean()
    stats[f'{team_type}LossStreak'] = df[df[f'{team_type}Team'] == team]['LossStreak'].mean()
    stats[f'{team_type}Last10Goals'] = df[df[f'{team_type}Team'] == team]['Last10Goals'].mean()
    stats[f'{team_type}Last10Wins'] = df[df[f'{team_type}Team'] == team]['Last10Wins'].mean()
    return stats

# Automatically retrieve the statistics for both teams
home_stats = get_team_stats(Home_Team, df, team_type='Home')
away_stats = get_team_stats(Away_Team, df, team_type='Away')

# Create the DataFrame for prediction
input_data = pd.DataFrame({
    'AwayTeam': [Away_Team],
    'HomeTeam': [Home_Team],
    'HomeShotsOnTarget': [home_stats['HomeShotsOnTarget']],
    'HomeTeamWinStreak': [home_stats['HomeWinStreak']],
    'AwayTeamWinStreak': [away_stats['AwayWinStreak']],
    'HomeTeamLossStreak': [home_stats['HomeLossStreak']],
    'AwayTeamLossStreak': [away_stats['AwayLossStreak']],
    'win_streak_difference': [home_stats['HomeWinStreak'] - away_stats['AwayWinStreak']],
    'loss_streak_difference': [home_stats['HomeLossStreak'] - away_stats['AwayLossStreak']],
    'HomeTeamLast10Goals': [home_stats['HomeLast10Goals']],
    'AwayTeamLast10Goals': [away_stats['AwayLast10Goals']],
    'HomeTeamLast10Wins': [home_stats['HomeLast10Wins']],
    'AwayTeamLast10Wins': [away_stats['AwayLast10Wins']],
})

st.write("Input Data:", input_data)

# Encode inputs using the LabelEncoder
def encode_team(team_name, encoder):
    try:
        return encoder.transform([team_name])[0]
    except ValueError:
        st.error(f"Unseen label: {team_name}. Please ensure the team names are correct.")
        return -1  # Or handle it in another way

# Encode the team names
input_data['HomeTeam'] = encode_team(Home_Team, label_encoder)
input_data['AwayTeam'] = encode_team(Away_Team, label_encoder)

# Check if encoding was successful
if input_data['HomeTeam'] == -1 or input_data['AwayTeam'] == -1:
    st.error("One or more team names were not recognized. Please check the input.")
else:
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
