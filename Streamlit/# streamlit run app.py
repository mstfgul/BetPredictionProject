import streamlit as st
import pandas as pd
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

# Load the encoders
encoders = load_encoders()

# Define predefined team names
Home_teams = ['Aalst', 'Anderlecht', 'Antwerp', 'Beerschot VA', 'Bergen', 'Beveren', 
              'Cercle Brugge', 'Charleroi', 'Club Brugge', 'Dender', 'Eupen', 'FC Brussels', 
              'Genk', 'Gent', 'Germinal', 'Harelbeke', 'Heusden Zolder', 'Kortrijk', 'Lierse', 
              'Lokeren', 'Lommel', 'Louvieroise', 'Mechelen', 'Molenbeek', 'Mouscron', 'Mouscron-Peruwelz', 
              'Oostende', 'Oud-Heverlee Leuven', 'RWD Molenbeek', 'Roeselare', 'Seraing', 'St Truiden', 
              'St. Gilloise', 'Standard', 'Tubize', 'Waasland-Beveren', 'Waregem', 'Westerlo']
Away_teams = Home_teams  # Same list for away teams

# Map the team names to their encoded values
home_team_mapping = {team: i for i, team in enumerate(Home_teams)}
away_team_mapping = {team: i for i, team in enumerate(Away_teams)}

# Main function to run the Streamlit app

def main():
    st.title('Football Match Predictor')

    # Load model
    model = load_model()

    # Sidebar
    st.sidebar.header('Match Details')
    st.sidebar.markdown('Enter the details of the match to predict the outcome:')

    # Get user input from sidebar
    user_input = {}
    
    user_input['HomeTeam'] = st.sidebar.selectbox('Home Team', list(home_team_mapping.keys()))
    user_input['AwayTeam'] = st.sidebar.selectbox('Away Team', list(away_team_mapping.keys()))

    # Preprocess the input
    def preprocess_input(user_input):
        user_input_df = pd.DataFrame([user_input])

        # Map the real team names to their encoded values
        user_input_df['HomeTeam'] = home_team_mapping.get(user_input['HomeTeam'])
        user_input_df['AwayTeam'] = away_team_mapping.get(user_input['AwayTeam'])
        
        

        return user_input_df

    input_data = preprocess_input(user_input)

    # Predict button
    if st.button('Predict Outcome'):
        if None in input_data.values:
            st.write('Error: One or more team names are not recognized. Please check the team names and try again.')
        else:
            prediction = model.predict(input_data)
            st.write(f'The predicted outcome is: {prediction[0]}')

if __name__ == '__main__':
    main()
