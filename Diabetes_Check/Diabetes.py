import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import seaborn as sns

# Load the diabetes dataset
df = pd.read_csv("C:/Users/PRANITHA/Desktop/archive/diabetes.csv")

# Set up the Streamlit app layout
st.title('Diabetes Checkup')
st.sidebar.header('Patient Data')
st.subheader('Training Data Stats')
st.write(df.describe())

# Split the dataset into features (X) and target (y)
X = df.drop(['Outcome'], axis=1)
y = df['Outcome']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Function to get user input for patient data
def user_report():
    pregnancies = st.sidebar.slider('Pregnancies', 0, 17, 3)
    glucose = st.sidebar.slider('Glucose', 0, 200, 120)
    bp = st.sidebar.slider('Blood Pressure', 0, 122, 70)
    skinthickness = st.sidebar.slider('Skin Thickness', 0, 100, 20)
    insulin = st.sidebar.slider('Insulin', 0, 846, 79)
    bmi = st.sidebar.slider('BMI', 0, 67, 20)
    dpf = st.sidebar.slider('Diabetes Pedigree Function', 0.0, 2.4, 0.47)
    age = st.sidebar.slider('Age', 0, 88, 33)

    user_report_data = {
        'Pregnancies': pregnancies,
        'Glucose': glucose,
        'BloodPressure': bp,
        'SkinThickness': skinthickness,
        'Insulin': insulin,
        'BMI': bmi,
        'DiabetesPedigreeFunction': dpf,
        'Age': age
    }
    report_data = pd.DataFrame(user_report_data, index=[0])
    return report_data

# Display user input for patient data
user_data = user_report()
st.subheader('Patient Data')
st.write(user_data)

# Train a Random Forest classifier
rf = RandomForestClassifier()
rf.fit(X_train, y_train)

# Predict diabetes outcome for user data
user_result = rf.predict(user_data)

# Set up visualizations
st.title('Visualized Patient Report')

# Define color based on prediction
color = 'red' if user_result[0] == 1 else 'blue'

# Scatter plot: Age vs Pregnancies
st.header('Pregnancy count Graph (Healthy vs Unhealthy)')
fig_preg = plt.figure()
ax1 = sns.scatterplot(x='Age', y='Pregnancies', data=df, hue='Outcome', palette='Greens')
ax2 = sns.scatterplot(x=user_data['Age'], y=user_data['Pregnancies'], s=150, color=color)
plt.xticks(np.arange(10, 100, 5))
plt.yticks(np.arange(0, 20, 2))
plt.title('0 - Healthy & 1 - Unhealthy')
st.pyplot(fig_preg)

# Scatter plot: Age vs Glucose
# Add similar visualization code for other features

# Output
st.subheader('Your Report:')
output = 'You are Diabetic' if user_result[0] == 1 else 'You are not Diabetic'
st.title(output)
st.subheader('Accuracy:')
st.write(str(accuracy_score(y_test, rf.predict(X_test)) * 100) + '%')
