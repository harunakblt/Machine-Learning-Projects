
import streamlit as st
import pandas as pd
import io
import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor
# --------------------
# Sayfa ayarları
# --------------------
st.set_page_config(
    page_title="Kesici Takım Tahminleme",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------
# MODEL YÜKLE
# --------------------
with open("karcanai_ridge_model.pkl", "rb") as f:
    model = pickle.load(f)

print(type(model))


# --------------------
# CSS
# --------------------
st.markdown("""
<style>
.main { background-color: #111; color: white; }
.stButton>button {
    background-color: #e50914;
    color: white;
    font-weight: bold;
    border-radius: 10px;
}
h1, h2, h3 { color: #e50914; }
</style>
""", unsafe_allow_html=True)

# --------------------
# Başlık
# --------------------
st.title("Kesici Takım Çıkış Süresi Tahminleme")
st.markdown("---")

# ==============================
# 📁 EXCEL İLE TOPLU TAHMİN
# ==============================
st.sidebar.header("📁 Excel ile Toplu Tahmin")
uploaded_file = st.sidebar.file_uploader("Excel yükle", type=["xlsx", "xls"])

if uploaded_file:
    data = pd.read_excel(uploaded_file)

    X = data[[
        "on cap", "saft cap", "ara bosaltma cap",
        "l2", "l3", "clearence",
        "kose turu", "kose degeri", "Z"
    ]]

    if st.sidebar.button("📊 Excel Tahmin"):
        preds = model.predict(X)
        data["Tahmini Sure (dk)"] = preds

        st.dataframe(data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            data.to_excel(writer, index=False)

        st.sidebar.download_button(
            "📥 Sonuçları İndir",
            data=output.getvalue(),
            file_name="tahmin_sonuclari.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# ==============================
# 🔧 MANUEL TAHMİN
# ==============================
st.sidebar.header("🔧 Manuel Parametreler")

on_cap = st.sidebar.number_input("On Cap", 1.0, 20.0, 10.0)
saft_cap = st.sidebar.number_input("Saft Cap", 1.0, 20.0, 8.0)
ara_bosaltma_cap = st.sidebar.number_input("Ara Bosaltma Cap", 0.001, 20.0, 6.0)
l2 = st.sidebar.number_input("L2", 0.0, 200.0, 35.0)
l3 = st.sidebar.number_input("L3", 0.0, 200.0, 20.0)
clearence = st.sidebar.number_input("Clearence", 0.0, 10.0, 0.2)
kose_turu = st.sidebar.selectbox("Köşe Türü", ["KESKİN KÖŞE", "RADIUS"])
kose_degeri = st.sidebar.number_input("Köşe Değeri", 0.0, 5.0, 0.8)
Z = st.sidebar.number_input("Z", 1, 10, 4)

# --------------------
# Tahmin
# --------------------
if st.sidebar.button("🚀 Tahmin Et"):
    input_df = pd.DataFrame([{
        "on cap": on_cap,
        "saft cap": saft_cap,
        "ara bosaltma cap": ara_bosaltma_cap,
        "l2": l2,
        "l3": l3,
        "clearence": clearence,
        "kose turu": kose_turu,
        "kose degeri": kose_degeri,
        "Z": Z
    }])

    dakika = model.predict(input_df)[0]
    dk = int(dakika)
    sn = int((dakika - dk) * 60)

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg,#e50914,#ff4d4d);
        color:white;
        font-size:26px;
        padding:20px;
        border-radius:15px;
        text-align:center;">
        🔮 Tahmini Çıkış Süresi<br>
        <b>{dk} dk {sn} sn</b>
    </div>
    """, unsafe_allow_html=True)