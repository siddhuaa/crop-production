import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Load datasets
# crop_data = pd.read_csv(r"G:\climatic crop1 zip\climatic crop\crop_yield.csv")
crop_data = pd.read_csv(r"C:\Users\DELL\Desktop\climatic project crop1 zip\climatic crop1 zip\climatic crop\crop_yield.csv")
rainfall_data = pd.read_csv(r"C:\Users\DELL\Desktop\climatic project crop1 zip\climatic crop1 zip\climatic crop\district_wise_rainfall_normal_fixed.csv")
weather_data = pd.read_csv(r"C:\Users\DELL\Desktop\climatic project crop1 zip\climatic crop1 zip\climatic crop\weather-1.csv")

# Normalize column names
crop_data['State'] = crop_data['State'].str.strip().str.lower()
rainfall_data['State'] = rainfall_data['State'].str.strip().str.lower()
weather_data.rename(columns={'state': 'State'}, inplace=True)
weather_data['State'] = weather_data['State'].str.strip().str.lower()

# Rename columns to match expected names
weather_data.rename(columns={
    'Temperature (°C)': 'temperature',
    'Humidity (%)': 'humidity'
}, inplace=True)

crop_data.rename(columns={
    'Annual_Rainfall': 'annual_rainfall'
}, inplace=True)

# Group rainfall and weather data
rainfall_avg = rainfall_data.groupby('State').mean(numeric_only=True).reset_index()
weather_avg = weather_data.groupby('State').mean(numeric_only=True).reset_index()

# Merge all datasets
merged = pd.merge(crop_data, rainfall_avg, on='State', how='inner')
merged = pd.merge(merged, weather_avg, on='State', how='inner')

# Check columns for valid features
possible_features = ['temperature', 'humidity', 'annual_rainfall', 'Fertilizer', 'Pesticide']
available_features = [col for col in possible_features if col in merged.columns]

print("✅ Available features:", available_features)

# Check and fill missing values
target = 'Production'
print("📊 Rows before cleaning:", len(merged))
print("🧪 Missing values:\n", merged[available_features + [target]].isnull().sum())

merged[available_features + [target]] = merged[available_features + [target]].fillna(
    merged[available_features + [target]].mean()
)

# Final cleaning
merged = merged.dropna(subset=available_features + [target])
print("✅ Merged data rows after cleaning:", len(merged))

# Model training
X = merged[available_features]
y = merged[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
print(f"✅ Model R2 Score: {r2_score(y_test, y_pred):.2f}")
print(f"✅ Model RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")

# Prediction function
def predict_yield_by_state(state):
    state = state.lower().strip()
    filtered = merged[merged['State'] == state]
    if filtered.empty:
        print(f"⚠️ No data found for {state}")
        return
    predictions = model.predict(filtered[available_features])
    filtered = filtered.copy()
    filtered['Predicted_Yield_Tons'] = predictions
    print(f"\n📍 Predicted Crop Production in {state.title()}:")
    print(filtered[['Crop', 'Predicted_Yield_Tons']])
    top_crop = filtered.loc[filtered['Predicted_Yield_Tons'].idxmax(), 'Crop']
    print(f"\n🌾 Suggested Crop for {state.title()}: {top_crop}")
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Crop', y='Predicted_Yield_Tons', data=filtered, hue='Crop', legend=False, palette='viridis')
    plt.xticks(rotation=45)
    plt.title(f'Predicted Crop Production in {state.title()} (Tons)')
    plt.tight_layout()
    plt.show()

# Example usage
predict_yield_by_state('Karnataka')
