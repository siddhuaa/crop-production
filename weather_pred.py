import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# ==============================
#       Load the Datasets
# ==============================

# Initialize DataFrames to avoid NoneType errors
rainfall_data = pd.DataFrame()
weather_data = pd.DataFrame()

try:
    # Load the datasets
    weather_data = pd.read_csv(r'C:\Users\DELL\Desktop\climatic project crop1 zip\climatic crop1 zip\climatic crop\Dataset/weather-1.csv')
    rainfall_data = pd.read_csv(r'C:\Users\DELL\Desktop\climatic project crop1 zip\climatic crop1 zip\climatic crop\district_wise_rainfall_normal_fixed.csv', sep=',', engine='python')
    
    # Debugging: Show initial structure
    print("Weather Data Columns:", weather_data.columns)
    print("Rainfall Data Columns:", rainfall_data.columns)
    
    # If the first row is misaligned as headers, correct it
    if len(rainfall_data.columns) == 1:
        rainfall_data.columns = rainfall_data.columns[0].split(',')
        rainfall_data = rainfall_data[1:]
    
    # Rename columns for easier access
    rainfall_data.rename(columns={'STATE_UT_NAME': 'State', 'DISTRICT': 'District'}, inplace=True)

    print("Datasets loaded successfully!")
except Exception as e:
    print(f"Error loading datasets: {e}")

# Display initial info
if not weather_data.empty:
    print("\nWeather Data Sample:")
    print(weather_data.head())

if not rainfall_data.empty:
    print("\nRainfall Data Sample:")
    print(rainfall_data.head())
else:
    print("Rainfall data could not be loaded. Please check the file path and formatting.")

# ==============================
#     Helper Functions
# ==============================

def get_district_data(state, district):
    """
    Fetches rainfall and weather information for a specific state and district.
    """
    rainfall_info = rainfall_data[(rainfall_data['State'] == state) & 
                                  (rainfall_data['District'] == district)]
    weather_info = weather_data[(weather_data['State/UT'] == state) & 
                                (weather_data['District'] == district)]
    
    if rainfall_info.empty:
        print(f"No rainfall data found for {district}, {state}.")
    if weather_info.empty:
        print(f"No weather data found for {district}, {state}.")
    
    return rainfall_info, weather_info

def plot_yearly_rainfall(rainfall_info):
    """
    Plots yearly rainfall data for the selected district.
    """
    plt.figure(figsize=(10, 6))
    years = rainfall_info.columns[3:]
    rainfall_values = rainfall_info.iloc[0, 3:]
    sns.barplot(x=years, y=rainfall_values, palette='Blues_d')
    plt.xticks(rotation=45)
    plt.title('Yearly Rainfall Data')
    plt.xlabel('Year')
    plt.ylabel('Rainfall (mm)')
    plt.tight_layout()
    plt.show()

def train_model(rainfall_info):
    """
    Trains a Linear Regression model to predict future rainfall.
    """
    try:
        # Extract years and rainfall values
        years = rainfall_info.columns[3:].astype(int)
        rainfall_values = rainfall_info.iloc[0, 3:].values
        
        # Create the DataFrame for training
        X = years.values.reshape(-1, 1)
        y = rainfall_values
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Initialize and train the model
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Predictions and evaluation
        y_pred = model.predict(X_test)
        print(f"\nModel Performance Metrics:")
        print(f"R^2 Score: {r2_score(y_test, y_pred):.2f}")
        print(f"Mean Squared Error: {mean_squared_error(y_test, y_pred):.2f}")
        
        return model
    except Exception as e:
        print(f"Error training model: {e}")
        return None

# ==============================
#         Example Usage
# ==============================

# Replace these with your state and district
state = 'MAHARASHTRA'
district = 'PUNE'

# Fetch data for the state and district
rainfall_info, weather_info = get_district_data(state, district)

if not rainfall_info.empty:
    print(f"\nRainfall Data for {district}, {state}:")
    print(rainfall_info.head())
    
    # Plot the rainfall data
    plot_yearly_rainfall(rainfall_info)
    
    # Train the model and predict
    model = train_model(rainfall_info)
    
    if model:
        # Predict for the next 5 years
        future_years = [[year] for year in range(2025, 2030)]
        predictions = model.predict(future_years)

        print("\nPredicted Rainfall for 2025 to 2029:")
        for year, prediction in zip(range(2025, 2030), predictions):
            print(f"{year}: {prediction:.2f} mm")
else:
    print("No data found for the selected state and district.")

if not weather_info.empty:
    print(f"\nWeather Data for {district}, {state}:")
    print(weather_info[['Temperature (°C)', 'Humidity (%)']])
else:
    print("No weather data found for the selected state and district.")

