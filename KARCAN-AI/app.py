import streamlit as st
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
import io

# --------------------
# Sayfa ayarları (en üstte olmalı)
# --------------------
st.set_page_config(
    page_title="Kesici Takım Tahminleme",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------
# Excel yükleme ve toplu tahmin
# --------------------
st.sidebar.markdown("---")
st.sidebar.header("📁 Excel Dosyası ile Tahmin")

uploaded_file = st.sidebar.file_uploader("Excel dosyanızı yükleyin", type=["xlsx", "xls"])

if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
    st.sidebar.success("Dosya yüklendi!")

    # Özellikler ve hedef
    X = data[["on cap", "saft cap", "ara bosaltma cap", "l1", "l2", "l3", "l4",
              "clearence", "kose turu", "kose degeri", "Z"]]
    y = data["sure(dakika)"]

    # Kategorik sütunları sayısal hale çevirme
    X = pd.get_dummies(X, columns=["kose turu"], drop_first=True)

    # Random Forest modeli
    model_rf = RandomForestRegressor(
        n_estimators=500,
        max_depth=None,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1
    )

    # Modeli eğit
    model_rf.fit(X, y)
    st.sidebar.success("Model yüklendi ve eğitildi!")

    if st.sidebar.button("📊 Dosya ile Tahmin Et"):
        y_pred = model_rf.predict(X)
        data["Tahmini Sure"] = y_pred
        st.dataframe(data)

        # Excel indirme
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            data.to_excel(writer, index=False)
            
            processed_data = output.getvalue()

        st.sidebar.download_button(
            label="Tahmin Sonuçlarını İndir",
            data=processed_data,
            file_name="tahmin_sonuclari.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# --------------------
# CSS ile renk ve stil
# --------------------
st.markdown(
    """
    <style>
    .main {
        background-color: #111;  /* Siyah arka plan */
        color: white;
    }
    .stButton>button {
        background-color: #e50914; /* Kırmızı */
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
    .stSlider>div>div>div>div {
        background: #e50914;
    }
    h1, h2, h3 {
        color: #e50914;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------
# Logo ve başlık
# --------------------
col1, col2 = st.columns([1,5])
with col1:
    st.image("logo.png", use_container_width=True)
with col2:
    st.title("Kesici Takım Çıkış Süresi Tahminleme")

st.image("gif.gif", use_container_width=False)
st.markdown("---")

# --------------------
# Mevcut model yükle (manuel tahmin için)
# --------------------
model = joblib.load("karcanai_model.pkl")

# --------------------
# Manuel giriş parametreleri
# --------------------
st.sidebar.header("🔧 Parametreler")
on_cap = st.sidebar.number_input("on cap", min_value=1.0, max_value=20.0, value=10.0, step=0.1)
saft_cap = st.sidebar.number_input("Saft Cap", min_value=1.0, max_value=20.0, value=10.0, step=0.1)
ara_bosaltma_cap = st.sidebar.number_input("Ara Bosaltma Cap", min_value=1.0, max_value=20.0, value=5.0, step=0.1)
l1 = st.sidebar.number_input("L1", min_value=0.0, max_value=200.0, value=50.0, step=1.0)
l2 = st.sidebar.number_input("L2", min_value=0.0, max_value=200.0, value=50.0, step=1.0)
l3 = st.sidebar.number_input("L3", min_value=0.0, max_value=200.0, value=50.0, step=1.0)
l4 = st.sidebar.number_input("L4", min_value=0.0, max_value=200.0, value=50.0, step=1.0)
clearence = st.sidebar.number_input("Clearence", min_value=0.0, max_value=10.0, value=2.0, step=0.1)
kose_turu = st.sidebar.selectbox("Kose Turu", ["Keskin", "Radius", "Chamfer"])
kose_degeri = st.sidebar.number_input("Kose Degeri", min_value=0.0, max_value=5.0, value=1.0, step=0.1)
Z = st.sidebar.number_input("Z", min_value=1, max_value=10, value=3, step=1)

# --------------------
# Manuel tahmin butonu
# --------------------
if st.sidebar.button("🚀 Tahmin Et"):
    input_data = pd.DataFrame([{
        "on cap": on_cap,
        "saft cap": saft_cap,
        "ara bosaltma cap": ara_bosaltma_cap,
        "l1": l1,
        "l2": l2,
        "l3": l3,
        "l4": l4,
        "clearence": clearence,
        "kose turu": kose_turu,
        "kose degeri": kose_degeri,
        "Z": Z
    }])

    prediction = model.predict(input_data)[0]

    st.markdown(
        f"""
        <div style="
            background: repeating-linear-gradient(
                45deg,
                #e50914,
                #e50914 10px,
                #ff4d4d 10px,
                #ff4d4d 20px
            );
            color: white;
            font-size: 24px;
            font-weight: bold;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        ">
            🔮 Tahmini Çıkış Süresi: {prediction:.2f} dakika
        </div>
        """,
        unsafe_allow_html=True
    )
