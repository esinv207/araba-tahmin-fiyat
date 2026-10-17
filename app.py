import streamlit as st
import numpy as np

st.set_page_config(page_title="İkinci El Araç Fiyat Tahmini", page_icon="🚗", layout="centered")

st.title("🚗 İkinci El Araç Fiyat Tahmin Motoru")
st.markdown("Ekonometrik **OLS Çoklu Regresyon Modeli** ile eğitilmiş canlı piyasa değerleme aracı.")

# Model Katsayıları (OLS Sonuçları)
SABIT = 14.0558
KATSAYI_YIL = 0.0845
KATSAYI_KM = -0.0000031
KATSAYI_OTOMATIK = 0.1820
KATSAYI_YARI_OTO = 0.0950

MARKA_ETKISI = {
    'Renault': 0.0,
    'Fiat': -0.1250,
    'Ford': 0.0450,
    'Volkswagen': 0.2150,
    'Opel': -0.0520,
    'Peugeot': -0.0310,
    'Hyundai': -0.0210,
    'Toyota': 0.1420,
    'BMW': 0.4850,
    'Mercedes - Benz': 0.5210
}

col1, col2 = st.columns(2)

with col1:
    marka = st.selectbox("Araba Markası", list(MARKA_ETKISI.keys()), index=3)
    yil = st.slider("Model Yılı", 1995, 2024, 2018)

with col2:
    vites = st.selectbox("Vites Tipi", ["Düz", "Otomatik", "Yarı Otomatik"], index=1)
    km = st.number_input("Kilometre", min_value=0, max_value=1000000, value=95000, step=5000)

if st.button("Piyasa Değerini Hesapla", type="primary"):
    vites_katsayisi = 0.0
    if vites == "Otomatik":
        vites_katsayisi = KATSAYI_OTOMATIK
    elif vites == "Yarı Otomatik":
        vites_katsayisi = KATSAYI_YARI_OTO

    marka_katsayisi = MARKA_ETKISI[marka]

    # Regresyon Denklemi: ln(Fiyat) = Sabit + b1*Yıl + b2*Km + b3*Vites + b4*Marka
    log_fiyat = (
        SABIT 
        + (KATSAYI_YIL * (yil - 2018)) 
        + (KATSAYI_KM * km) 
        + vites_katsayisi 
        + marka_katsayisi
    )
    
    tahmini_fiyat = np.exp(log_fiyat)
    
    st.divider()
    st.success(f"### Modelin Tahmin Ettiği Değer: {tahmini_fiyat:,.0f} TL")
    st.caption("Not: Değerleme %90 açıklayıcılık oranına ($R^2 \\approx 0.903$) sahip log-linear OLS modeli üzerinden hesaplanmıştır.")
