import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="Araç Fiyat Tahmini", page_icon="🚗")

st.title("🚗 İkinci El Araç Fiyat Tahmin Motoru")
st.markdown("Ekonometrik OLS regresyon modeli ile eğitilmiş piyasa fiyatlaması.")

@st.cache_resource
def modeli_yukle():
    return joblib.load('model_araba.pkl')

model = modeli_yukle()

markalar = ['BMW', 'Mercedes - Benz', 'Volkswagen', 'Renault', 'Fiat', 'Opel', 'Ford', 'Hyundai', 'Toyota', 'Peugeot']
vitesler = ['Düz', 'Otomatik', 'Yarı Otomatik']

col1, col2 = st.columns(2)

with col1:
    marka = st.selectbox("Araba Markası", markalar, index=2)
    yil = st.slider("Model Yılı", 1995, 2024, 2018)

with col2:
    vites = st.selectbox("Vites Tipi", vitesler, index=1)
    km = st.number_input("Kilometre", min_value=0, max_value=1000000, value=95000, step=5000)

if st.button("Fiyatı Hesapla", type="primary"):
    veri = pd.DataFrame({
        'marka': [marka],
        'yil': [int(yil)],
        'kilometre': [float(km)],
        'vites_tipi': [vites]
    })
    log_tahmin = model.predict(veri)
    tl_fiyat = np.exp(log_tahmin.iloc[0])
    
    st.success(f"### Tahmini Piyasa Değeri: {tl_fiyat:,.2f} TL")
