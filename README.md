# BetPredictionProject



⚽ Pro Jupiler Pro League Football Match Prediction

## 🚀 Project Overview

🎯 **Objective:** This project aims to deliver highly accurate and insightful match predictions.
📊 **Data Source:** https://www.football-data.co.uk/notes.txt
🔧 **Techniques Used:**
- Data collecting 
- Data Cleaning
- Feature Encoding
- Imputation of Missing Values
- Model Training & Evaluation
- Deployement with streamlit on Render

1. **Data Preparation**

    - 🔍 **Data Collection:** Data Collection: Gathered and pre-processed historical match data from the Pro Jupiler            League, including scores, team lineups, and match events.
    - 🧹 **Data Cleaning:** Dropped irrelevant columns and handled missing values.
    - 🏷️ **Feature Encoding:** Transformed categorical variables using OneHotEncoder.
    - 🔄 **Imputation:** Applied KNN Imputation to handle missing values.

![Data Preparation](https://media.giphy.com/media/iFwgAGLxwHevR1ppM7/giphy.gif)

2. **Model Training**
   - 🛠️ Feature Engineering: Developed various features such as team form, head-to-head statistics, player injuries, and other factors influencing match outcomes.
   - 📈 Machine Learning Models: Implemented and compared several machine learning models, including Logistic Regression, Random Forest, Gradient Boosting, to predict match results. 
   - 🔍 Performed Grid Search to optimize hyperparameters.

![Model Trainin](https://media.giphy.com/media/qcsGTXHP8JkxaAa0cE/giphy.gif)

3. **Model Evaluation**
   - 🧑💻Assessed the performance of each model using accuracy, precision, recall, F1 score, and AUC-ROC curves to select the best-performing model.
   - 🎯 Fine-tuned the model based on evaluation results.

   ![Model Evaluation](https://media.giphy.com/media/vSGzVywEkoS6QCzfWN/giphy.gif)

4. **Prediction Interface**
    💻:Built a user-friendly interface where users can input upcoming match details and receive predictions.

5. **Project Structure**

    📂 Pro Jupiler League-prediction
├── 📁 data
│   ├── 📂 raw               ## Raw data straight from the sources
│   ├── 📂 processed         ## Cleaned and ready-to-use data
│   └── 📂 features          ## Engineered features for modeling
├── 📁 notebooks             # Jupyter notebooks for EDA and model experiments
├── 📁 models                # Trained and saved models
├── 📁 src
│   ├── 📂 data_processing   # Scripts for data cleaning and feature extraction
│   ├── 📂 modeling          # Scripts for model training and evaluation
│   ├── 📂 prediction        # Prediction generation scripts
│   └── 📂 app               # Source code for the web application
├── 📁 tests                 # Unit tests to ensure robustness
├── 📝 README.md             # Project documentation
└── 📄 requirements.txt      # Python dependencies


5. **Deployement with streamlit on Render**

   🌐 Deployment: Deployed the final model as a web application for easy access and usage.

   🔗 Deployment with Streamlit on Render

    To deploy the model using Streamlit on Render, follow these steps:

    ⚙️ Set Up Streamlit App: Create a streamlit_app.py file in the project directory. This file should include the code to load the model and present the prediction interface.

    ✅ Create a requirements.txt for Deployment: List all required packages for the Streamlit app. Include packages like streamlit, catboost, and any other dependencies.

    📂 Deploy on Render: Go to Render and create a new Web Service. Connect your GitHub repository and select the streamlit_app.py file. Configure the build and start commands (e.g., streamlit run streamlit_app.py).

    🧱 Test Your Deployment: Once deployed, test the Streamlit app to ensure it functions correctly and provides accurate predictions.

    


## ⏳ Usage


Select the teams for the upcoming match.
Input additional factors such as injuries or suspensions.
Generate predictions for the match outcome and potential scoreline.

## 📊 Model Performance
The chosen model, Gradient Boosting Classifier, achieved the best performance with the following metrics:

Accuracy: 
Precision: 
Recall: 
F1 Score: 


## 📈 Visualization
