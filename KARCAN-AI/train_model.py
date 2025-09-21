import pandas as pd

# Excel dosyasını oku (dosya adı değişirse güncelle)
df = pd.read_excel("KARCAN DATASET.xlsx")

print("Veri seti boyutu:", df.shape)
print("Sütunlar:", df.columns.tolist())
print(df.head())

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# Hedef sütun (çıkış süresi)
target_col = "sure(dakika)"

# Kullanacağımız özellikler
features = ["on cap", "saft cap", "ara bosaltma cap", "l1", "l2", "l3", "l4", "clearence", "kose turu", "Z"]

X = df[features]
y = df[target_col]

# Sayısal ve kategorik sütunları ayır
numeric_feats = X.select_dtypes(include=["number"]).columns.tolist()
categorical_feats = [c for c in X.columns if c not in numeric_feats]

# Eksik değer doldurma
X[numeric_feats] = X[numeric_feats].fillna(X[numeric_feats].median())
X[categorical_feats] = X[categorical_feats].fillna("MISSING")

# Pipeline oluştur
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numeric_feats),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_feats)
])

model = Pipeline([
    ("pre", preprocessor),
    ("reg", RandomForestRegressor(n_estimators=500,max_depth=None,min_samples_leaf=1, random_state=42, n_jobs=-1))
])

# Veriyi ayır ve eğit
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

# Performans
y_pred = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, y_pred))
print("R²:", r2_score(y_test, y_pred))

# Modeli kaydet
joblib.dump(model, "karcanaı_model.pkl")
print("Model kaydedildi: deneme_model.pkl")
