import streamlit as st
import pandas as pd

# Load dataset
#df = pd.read_csv()

# Title of the app
st.title("Team Information")

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

team = st.selectbox('Select a team', ['Barcelona', 'Real Madrid', 'Manchester United', 'Liverpool', 'Bayern Munich'])
