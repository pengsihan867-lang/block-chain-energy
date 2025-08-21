import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

class SolarEnergyPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def generate_sample_data(self, n_samples=1000):
        """Generate sample weather and solar energy data"""
        np.random.seed(42)
        
        # Weather features
        temperature = np.random.normal(20, 10, n_samples)  # Celsius
        humidity = np.random.uniform(30, 90, n_samples)    # Percentage
        wind_speed = np.random.exponential(5, n_samples)   # m/s
        cloud_cover = np.random.uniform(0, 100, n_samples) # Percentage
        solar_radiation = np.random.normal(500, 150, n_samples)  # W/m²
        
        # Generate solar energy output (kWh) based on weather conditions
        # Simplified model: energy = f(temperature, humidity, wind, clouds, solar_radiation)
        base_energy = 10.0  # Base energy output
        temp_factor = 1 + 0.02 * (temperature - 20)  # Optimal at 20°C
        humidity_factor = 1 - 0.005 * humidity  # Lower humidity = better
        wind_factor = 1 - 0.01 * wind_speed  # Lower wind = better
        cloud_factor = 1 - 0.008 * cloud_cover  # Lower clouds = better
        radiation_factor = solar_radiation / 500  # Normalized radiation
        
        # Calculate energy output with some randomness
        energy_output = (base_energy * temp_factor * humidity_factor * 
                        wind_factor * cloud_factor * radiation_factor * 
                        np.random.normal(1, 0.1, n_samples))
        
        # Ensure positive values
        energy_output = np.maximum(energy_output, 0)
        
        # Create DataFrame
        data = pd.DataFrame({
            'temperature': temperature,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'cloud_cover': cloud_cover,
            'solar_radiation': solar_radiation,
            'energy_output': energy_output
        })
        
        return data
    
    def train_model(self, data=None):
        """Train the solar energy prediction model"""
        if data is None:
            print("Generating sample data...")
            data = self.generate_sample_data()
        
        # Save sample data
        data.to_csv('../data/solar_weather.csv', index=False)
        print(f"Sample data saved to ../data/solar_weather.csv")
        
        # Prepare features and target
        X = data[['temperature', 'humidity', 'wind_speed', 'cloud_cover', 'solar_radiation']]
        y = data['energy_output']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        print("Training Random Forest model...")
        self.model.fit(X_train_scaled, y_train)
        
        # Make predictions
        y_pred = self.model.predict(X_test_scaled)
        
        # Evaluate model
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Model trained successfully!")
        print(f"Mean Squared Error: {mse:.4f}")
        print(f"R² Score: {r2:.4f}")
        
        self.is_trained = True
        
        # Save model and scaler
        self.save_model()
        
        return mse, r2
    
    def predict_energy(self, temperature, humidity, wind_speed, cloud_cover, solar_radiation):
        """Predict solar energy output based on weather conditions"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Create feature array
        features = np.array([[temperature, humidity, wind_speed, cloud_cover, solar_radiation]])
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make prediction
        prediction = self.model.predict(features_scaled)[0]
        
        return max(0, prediction)  # Ensure non-negative
    
    def save_model(self):
        """Save the trained model and scaler"""
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        # Create models directory if it doesn't exist
        os.makedirs('../models', exist_ok=True)
        
        # Save model and scaler
        joblib.dump(self.model, '../models/solar_model.pkl')
        joblib.dump(self.scaler, '../models/solar_scaler.pkl')
        print("Model and scaler saved to ../models/")
    
    def load_model(self):
        """Load the trained model and scaler"""
        try:
            self.model = joblib.load('../models/solar_model.pkl')
            self.scaler = joblib.load('../models/solar_scaler.pkl')
            self.is_trained = True
            print("Model and scaler loaded successfully!")
            return True
        except FileNotFoundError:
            print("No saved model found. Please train the model first.")
            return False

def main():
    """Main function to train the model"""
    predictor = SolarEnergyPredictor()
    
    # Train the model
    mse, r2 = predictor.train_model()
    
    # Test prediction
    test_weather = {
        'temperature': 25,
        'humidity': 60,
        'wind_speed': 3,
        'cloud_cover': 20,
        'solar_radiation': 600
    }
    
    prediction = predictor.predict_energy(**test_weather)
    print(f"\nTest prediction for weather conditions:")
    for key, value in test_weather.items():
        print(f"  {key}: {value}")
    print(f"Predicted energy output: {prediction:.2f} kWh")

if __name__ == "__main__":
    main()
