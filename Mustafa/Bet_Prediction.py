import streamlit as st
import pandas as pd
import psycopg2
import pandas.io.sql as sqlio
import pickle

st.set_page_config(
    page_title="Football Match Prediction",
    page_icon="📊",)


# Use custom CSS to center the image
st.markdown(
    """
    <style>
    .center {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the centered image
st.markdown(
    """
    <div class="center">
        <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%3Fid%3DOIP.7Ptu3VwdYMUb6TVeMc2i3AHaJA%26pid%3DApi&f=1&ipt=70b97454c19a60d8ebe9dae6e76b35fcb7e22f27944bbc27c3b69071af2f7250&ipo=images" width="100">
    </div>
    """,
    unsafe_allow_html=True
)


# Connect to the PostgreSQL database and load the dataset

db_url = "postgresql://admin:JVDdki5JwDKlAtHsFAdxL58tO9qQZh5j@dpg-crhvmi5umphs73cag3i0-a.frankfurt-postgres.render.com/football_p8l0"
conn = psycopg2.connect(db_url)
query = """
        SELECT name AS team, home_shots_on_target, away_shots_on_target, home_wins_streak, 
               away_wins_streak, home_losses_streak, away_losses_streak, home_goals, 
               away_goals, last_10_home_wins, last_10_away_wins
        FROM season_teams;
"""
teams_statistics = sqlio.read_sql_query(query, conn)
conn.close()

# Title of the app
st.title("Football Match Prediction 📈")

# Function to load the model
def load_model():
    with open(r'/Users/mustafagul/Desktop/fixture_project/Model/Streamlit/model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

# Function to load the LabelEncoder
def load_encoder():
    with open(r'/Users/mustafagul/Desktop/fixture_project/Model/Streamlit/le.pkl', 'rb') as f:
        encoder = pickle.load(f)
    return encoder

# Load the model and encoder
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
Away_Team = st.selectbox("Away Team 💪", options=teams_statistics['team'].unique())
Home_Team = st.selectbox("Home Team 🏟️", options=teams_statistics['team'].unique())

# Function to retrieve team stats from the dataset
def get_team_stats(team, df, team_type='Home'):
    """Extract stats for the selected team from the dataset"""
    stats = {}
    team_stats = df[df['team'] == team]
    if team_type == 'Home':
        stats['HomeShotsOnTarget'] = team_stats['home_shots_on_target'].mean()
        stats['HomeTeamWinStreak'] = team_stats['home_wins_streak'].mean()
        stats['HomeTeamLossStreak'] = team_stats['home_losses_streak'].mean()
        stats['HomeTeamLast10Goals'] = team_stats['home_goals'].mean()
        stats['HomeTeamLast10Wins'] = team_stats['last_10_home_wins'].mean()
    else:
        stats['AwayShotsOnTarget'] = team_stats['away_shots_on_target'].mean()
        stats['AwayTeamWinStreak'] = team_stats['away_wins_streak'].mean()
        stats['AwayTeamLossStreak'] = team_stats['away_losses_streak'].mean()
        stats['AwayTeamLast10Goals'] = team_stats['away_goals'].mean()
        stats['AwayTeamLast10Wins'] = team_stats['last_10_away_wins'].mean()
    return stats

# Automatically retrieve the statistics for both teams
home_stats = get_team_stats(Home_Team, teams_statistics, team_type='Home')
away_stats = get_team_stats(Away_Team, teams_statistics, team_type='Away')

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
        return encoder.fit_transform([team_name])[0]
    except ValueError:
        st.error(f"Unseen label: {team_name}. Please ensure the team names are correct.")
        return -1  # Handle the error in another way if needed

# Encode the team names
input_data['HomeTeam'] = encode_team(Home_Team, label_encoder)
input_data['AwayTeam'] = encode_team(Away_Team, label_encoder)


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
