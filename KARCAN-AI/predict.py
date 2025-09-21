import joblib
import pandas as pd

# Eğitilen modeli yükle
model = joblib.load("karcanai_model.pkl")

def predict_from_input(data: dict):
    df = pd.DataFrame([data])
    pred = model.predict(df)[0]
    return pred

# Örnek giriş
sample = {
    "on cap": 6.0,
    "saft cap": 3.0,
    "ara bosaltma cap": 2.0,
    "l1": 10.0,
    "l2": 5.0,
    "l3": 0.5,
    "l4": 0.0,
    "clearence": 0.2,     # dikkat: sondaki boşluk önemli
    "kose turu": "radius", # örnek kategori
    "Z": 1.0
}

print("Tahmini süre (dakika):", predict_from_input(sample))
