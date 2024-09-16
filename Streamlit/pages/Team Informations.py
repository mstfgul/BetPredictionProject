import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# Load dataset
df = pd.read_csv('../Preprocessing/playerswithclub.csv')

# Title of the app
st.title("Team Informations")

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

st.header("Select a team to view information")

# Create a dropdown menu to select a team
team = st.selectbox('Select a team', df['club'].unique())

# Filter the dataset to display the selected team's information
team_info = df[df['club'] == team]

# Display the team information using AgGrid for an interactive table
def display_team_info(team_data):
    # Create a GridOptionsBuilder for customization
    gb = GridOptionsBuilder.from_dataframe(team_data)
    gb.configure_pagination(paginationAutoPageSize=True)  # Enable pagination
    gb.configure_side_bar()  # Enable a sidebar with filters
    gridOptions = gb.build()
    
    # Use AgGrid to display the DataFrame with custom options
    AgGrid(team_data, gridOptions=gridOptions, enable_enterprise_modules=True)

# Call the function to display the filtered team information
display_team_info(team_info)
