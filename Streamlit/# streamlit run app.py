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



if __name__ == '__main__':
    main()
