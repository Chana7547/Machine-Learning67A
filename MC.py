# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 15:58:19 2026
@author: khxwwcx
"""

import pickle
from streamlit_option_menu import option_menu
import streamlit as st

used_car_model = pickle.load(open(r"C:\Users\khxwwcx\Desktop\ML\used_cars_model.sav", "rb"))
riding_model = pickle.load(open(r"C:\Users\khxwwcx\Desktop\ML\RidingMowers_model.sav", "rb"))

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

with st.sidebar:
    selected = option_menu(
        menu_title="Prediction",
        options=["Riding Mower", "Used Cars"],
        icons=["activity", "car-front"],
        default_index=0
    )

if selected == "Riding Mower":
    st.title("Riding Mower Prediction")

    Income = st.text_input("income")
    LotSize = st.text_input("Lotsize")

    if st.button("Predict Riding"):
        try:
            Ridding_prediction = riding_model.predict([[float(Income), float(LotSize)]])[0]
            st.success(Ridding_prediction)
        except:
            st.error("กรอกตัวเลขให้ครบ")

elif selected == "Used Cars":

    st.title("ประเมินราคารถมือ 2")

    make_year = st.text_input("ปีที่ผลิต")
    mileage_kmpl = st.text_input("กินน้ำมัน (KM/L)")
    owner_count = st.text_input("จำนวนเจ้าของเดิม")
    accidents_reported = st.text_input("จำนวนอุบัติเหตุที่เคยเกิด")

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
            st.success(round(float(price_predict), 2))

        except:
            st.error("กรอกข้อมูลให้ครบ")