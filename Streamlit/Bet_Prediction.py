import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="Football Match Prediction",
    page_icon="📊",)

# Load dataset
df = pd.read_csv('../Preprocessing/model_df.csv')



# Title of the app
st.title("Football Match Prediction 📈")

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
st.header("Input Match Details 📋")

# Select the Away and Home teams
Away_Team = st.selectbox("Away Team 💪", options=df['AwayTeam'])
Home_Team = st.selectbox("Home Team 🏟️", options=df['HomeTeam'])

# Function to retrieve team stats from the dataset
def get_team_stats(team, df, team_type='Home'):
    """Extract stats for the selected team from the dataset"""
    stats = {}
    if team_type == 'Home':
        stats['HomeShotsOnTarget'] = df[df['HomeTeam'] == team]['HomeShotsOnTarget'].mean()
        stats['HomeTeamWinStreak'] = df[df['HomeTeam'] == team]['HomeTeamWinStreak'].mean()
        stats['HomeTeamLossStreak'] = df[df['HomeTeam'] == team]['HomeTeamLossStreak'].mean()
        stats['HomeTeamLast10Goals'] = df[df['HomeTeam'] == team].get('HomeTeamLast10Goals', pd.Series([0])).mean()
        stats['HomeTeamLast10Wins'] = df[df['HomeTeam'] == team].get('HomeTeamLast10Wins', pd.Series([0])).mean()
    else:
        stats['AwayShotsOnTarget'] = df[df['AwayTeam'] == team]['AwayShotsOnTarget'].mean()
        stats['AwayTeamWinStreak'] = df[df['AwayTeam'] == team]['AwayTeamWinStreak'].mean()
        stats['AwayTeamLossStreak'] = df[df['AwayTeam'] == team]['AwayTeamLossStreak'].mean()
        stats['AwayTeamLast10Goals'] = df[df['AwayTeam'] == team].get('AwayTeamLast10Goals', pd.Series([0])).mean()
        stats['AwayTeamLast10Wins'] = df[df['AwayTeam'] == team].get('AwayTeamLast10Wins', pd.Series([0])).mean()
    return stats

# Automatically retrieve the statistics for both teams
home_stats = get_team_stats(Home_Team, df, team_type='Home')
away_stats = get_team_stats(Away_Team, df, team_type='Away')

# Calculate win and loss streak differences
win_streak_difference = home_stats['HomeTeamWinStreak'] - away_stats['AwayTeamWinStreak']
loss_streak_difference = home_stats['HomeTeamLossStreak'] - away_stats['AwayTeamLossStreak']

# Create the DataFrame for prediction with all required features
input_data = pd.DataFrame({
    'AwayTeam': [Away_Team],
    'AwayShotsOnTarget': [away_stats['AwayShotsOnTarget']],
    'HomeTeam': [Home_Team],
    'HomeShotsOnTarget': [home_stats['HomeShotsOnTarget']],
    'HomeTeamWinStreak': [home_stats['HomeTeamWinStreak']],
    'AwayTeamWinStreak': [away_stats['AwayTeamWinStreak']],
    'HomeTeamLossStreak': [home_stats['HomeTeamLossStreak']],
    'AwayTeamLossStreak': [away_stats['AwayTeamLossStreak']],
    'win_streak_difference': [win_streak_difference],
    'loss_streak_difference': [loss_streak_difference],
    'HomeTeamLast10Goals': [home_stats['HomeTeamLast10Goals']],
    'AwayTeamLast10Goals': [away_stats['AwayTeamLast10Goals']],
    'HomeTeamLast10Wins': [home_stats['HomeTeamLast10Wins']],
    'AwayTeamLast10Wins': [away_stats['AwayTeamLast10Wins']]
})

st.write("Input Data 📝:", input_data)

# Encode inputs using the LabelEncoder
def encode_team(team_name, encoder):
    try:
        return encoder.transform([team_name])[0]
    except ValueError:
        st.error(f"Unseen label: {team_name}. Please ensure the team names are correct.")
        return -1  # Handle the error in another way if needed

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
        
        # Result map matching the model output
        result_map = {0: "Draw", 1: "Home Win", 2: "Away Win"}
        
        try:
            st.subheader(f"Prediction: {result_map[prediction[0]]}")
        except KeyError as e:
            st.error(f"Unexpected prediction value: {prediction[0]}. Error: {e}")
            st.write(f"Result map keys: {result_map.keys()}")
