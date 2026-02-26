# -*- coding: utf-8 -*-
"""
Full Prediction App (No Encoder Version)
"""

import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# -----------------------------
# Load Models
# -----------------------------
used_car_model = pickle.load(open("used_cars_model.sav", "rb"))
riding_model = pickle.load(open("RidingMowers_model.sav", "rb"))
bmi_model = pickle.load(open("bmi_model.sav", "rb"))

# -----------------------------
# Mapping Dictionaries
# -----------------------------
fuel_map = {"Diesel": 0, "Electric": 1, "Petrol": 2}

engine_map = {
    800: 0, 1000: 1, 1200: 2, 1500: 3, 1800: 4,
    2000: 5, 2500: 6, 3000: 7, 4000: 8, 5000: 9
}

brand_map = {
    "BMW": 0, "Chevrolet": 1, "Ford": 2, "Honda": 3,
    "Hyundai": 4, "Kia": 5, "Nissan": 6, "Tesla": 7,
    "Toyota": 8, "Volkswagen": 9
}

transmission_map = {"Automatic": 0, "Manual": 1}

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    selected = option_menu(
        menu_title="Prediction",
        options=["Riding Mower", "Used Cars", "BMI"],
        icons=["activity", "car-front", "heart"],
        default_index=0
    )

# =====================================================
# RIDING MOWER
# =====================================================
if selected == "Riding Mower":

    st.title("Riding Mower Prediction")

    Income = st.text_input("Income")
    LotSize = st.text_input("Lot Size")

    if st.button("Predict Riding"):
        try:
            prediction = riding_model.predict([[float(Income), float(LotSize)]])[0]
            st.success(str(prediction))
        except:
            st.error("กรอกตัวเลขให้ครบ")

# =====================================================
# USED CAR
# =====================================================
elif selected == "Used Cars":

    st.title("Used Car Price Prediction")

    make_year = st.text_input("ปีที่ผลิต")
    mileage_kmpl = st.text_input("กินน้ำมัน (KM/L)")
    owner_count = st.text_input("จำนวนเจ้าของเดิม")
    accidents_reported = st.text_input("จำนวนอุบัติเหตุ")

    brand = st.selectbox("ยี่ห้อรถ", list(brand_map.keys()))
    engine_cc = st.selectbox("ขนาดเครื่องยนต์ (CC)", list(engine_map.keys()))
    fuel_type = st.selectbox("ประเภทน้ำมัน", list(fuel_map.keys()))
    transmission = st.selectbox("ประเภทเกียร์", list(transmission_map.keys()))

    if st.button("Predict Used Car"):
        try:
            X = [[
                float(make_year),
                float(mileage_kmpl),
                engine_map[engine_cc],
                fuel_map[fuel_type],
                float(owner_count),
                brand_map[brand],
                transmission_map[transmission],
                float(accidents_reported)
            ]]

            price_predict = used_car_model.predict(X)[0]
            st.success(str(round(float(price_predict), 2)))
        except:
            st.error("กรอกข้อมูลให้ครบ")

# =====================================================
# BMI
# =====================================================
elif selected == "BMI":

    st.title("BMI Classification")

    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.text_input("Height (cm)")
    weight = st.text_input("Weight (kg)")

    if st.button("Predict"):
        try:
            # 🔥 ไม่ใช้ encoder แล้ว
            gender_encoded = 1 if gender == "Male" else 0

            X = [[
                gender_encoded,
                float(height),
                float(weight)
            ]]

            prediction = bmi_model.predict(X)[0]

            bmi_labels = {
                0: "Extremely Weak (ผอมมาก)",
                1: "Weak (ผอม)",
                2: "Normal (ปกติ)",
                3: "Overweight (ท้วม)",
                4: "Obesity (อ้วน)",
                5: "Extreme Obesity (อ้วนมาก)"
            }

            st.success(bmi_labels[prediction])

        except:
            st.error("กรอกข้อมูลให้ครบ")
