import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# --------------------
# Veri
# --------------------
df = pd.read_excel("KARCAN DATASET.xlsx")

X = df.drop(columns=["sure(dakika)", "Kod", "ucret"])
y = df["sure(dakika)"]

num_cols = X.select_dtypes(include=["int64", "float64"]).columns
cat_cols = ["kose turu"]

# --------------------
# Preprocess
# --------------------
preprocess = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(drop="first"), cat_cols)
])

# --------------------
# FINAL MODEL
# --------------------
final_model = Pipeline([
    ("prep", preprocess),
    ("model", Ridge(alpha=1.0))
])

final_model.fit(X, y)

# --------------------
# KAYDET
# --------------------
joblib.dump(final_model, "karcanai_ridge_model.pkl")

print("✅ Model kaydedildi: karcanai_ridge_model.pkl")
