import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse

# === Your original data loading and preprocessing ===
def load_and_train():
    # Load datasets (update file paths accordingly)
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

    # Fill missing values
    target = 'Production'
    merged[available_features + [target]] = merged[available_features + [target]].fillna(
        merged[available_features + [target]].mean()
    )
    merged = merged.dropna(subset=available_features + [target])

    # Model training
    X = merged[available_features]
    y = merged[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluation (optional print)
    y_pred = model.predict(X_test)
    print(f"Model R2 Score: {r2_score(y_test, y_pred):.2f}")
    print(f"Model RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")

    return merged, available_features, model

# === Prediction function ===
def get_predictions(state, merged, available_features, model):
    state = state.lower().strip()
    filtered = merged[merged['State'] == state]
    if filtered.empty:
        return None
    predictions = model.predict(filtered[available_features])
    filtered = filtered.copy()
    filtered['Predicted_Yield_Tons'] = predictions
    return filtered[['Crop', 'Predicted_Yield_Tons']]

# === HTTP server ===
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/predict":
            params = urllib.parse.parse_qs(parsed_path.query)
            state = params.get('state', [''])[0]

            results = get_predictions(state, merged, available_features, model)
            if results is None:
                response = {"error": f"No data found for state '{state}'"}
            else:
                response = results.to_dict(orient='records')

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')

if __name__ == "__main__":
    print("Loading data and training model...")
    merged, available_features, model = load_and_train()
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Server running on http://localhost:8000")
    httpd.serve_forever()
