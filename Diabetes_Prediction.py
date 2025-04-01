import streamlit as st
import pandas as pd
import math
import pickle

st.set_page_config(page_title="Diabetes Prediction", page_icon="", layout="wide")
st.header("Diabetes Prediction")

with st.form("Input Credentials"):
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.radio("Gender", options=["Male", "Female"], horizontal=True)
        age = st.select_slider("Age", options=range(0, 111))
        ht = st.radio("Hypertension", options=["Yes", "No"], horizontal=True)
        hd = st.radio("Heart Diseases", options=["Yes", "No"], horizontal=True)
        sh = st.selectbox("Smoking History", options=['never', 'No Info', 'current', 'former', 'ever', 'not current'])
    
    with col2:
        weight = st.number_input("Weight (kg)", min_value=0.1, format="%.2f")
        feet = st.number_input("Height (Feet)", min_value=0, step=1)
        st.write("1 foot = 12 inches")
        inches = st.number_input("Height (Inches)", min_value=0, step=1)
        total_inches = (feet * 12) + inches
        height_meters = total_inches * 0.0254
        st.write("1 inch = 0.0254 meters")
    
        if height_meters > 0:
            bmi = weight / (height_meters ** 2) 
        else: 
            bmi = 0
        
        hb = st.number_input("Glycated Hemoglobin (HbA1c level)")
        st.write("Overall normal HbA1c level : below 5.7")
        bgl = st.number_input("Blood Glucose Level")
        st.write("Overall normal blood glucose range : 70–140 mg/dL")
    
    button = st.form_submit_button(label="Submit")
    
if button:
    if weight <= 0 or height_meters <= 0 or hb <= 0 or bgl <= 0:
        st.error("Please enter valid positive values for weight, height, HbA1c, and blood glucose.")
    else:
        try:
            model = pickle.load(open("heart.pkl", "rb"))
            data = pd.DataFrame(
                [[gender, age, ht, hd, sh, bmi, hb, bgl]],
                columns=["gender", "age", "hypertension", "heart_disease", "smoking_history", 
                         "bmi", "HbA1c_level", "blood_glucose_level"]
            ) 
            data["gender"]=data["gender"].map({"Female":0,"Male":1})
            data["smoking_history"]=data["smoking_history"].map({"never":0,"No Info":1,"current":2,"former":3,"ever":4,"not current":5})
            data[["hypertension","heart_disease"]] = data[["hypertension","heart_disease"]].replace({"No": 0, "Yes": 1})
            prediction = model.predict(data)
            st.success("Form submitted successfully!")
            if prediction==0:
                st.subheader("Prediction Result: Negative")
            elif prediction==1:
                st.subheader("Prediction Result: positive")
            
        except Exception as e:
            st.error(e)
