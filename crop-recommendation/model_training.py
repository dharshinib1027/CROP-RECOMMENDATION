import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

data = pd.read_csv("data/Crop_recommendation.csv")


x = data.drop("label", axis=1)
y = data["label"]


X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)


scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)

joblib.dump(model, "crop_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("Model saved successfully!")
