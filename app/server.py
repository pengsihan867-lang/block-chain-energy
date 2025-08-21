from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.solar_predictor import SolarEnergyPredictor
from app.web3_helper import Web3Helper

app = Flask(__name__)
CORS(app)

# Initialize components
predictor = SolarEnergyPredictor()
web3_helper = None

# HTML template for the interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>P2P Energy Trading System</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #333;
        }
        .container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        .card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .card h2 {
            color: #2c3e50;
            margin-bottom: 20px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #555;
        }
        input, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        button {
            background: #3498db;
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s;
        }
        button:hover {
            background: #2980b9;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            border-radius: 5px;
            background: #e8f5e8;
            border-left: 4px solid #27ae60;
        }
        .error {
            background: #ffeaea;
            border-left: 4px solid #e74c3c;
        }
        .status {
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
        }
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        .full-width {
            grid-column: 1 / -1;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>⚡ P2P Energy Trading System</h1>
        <p>Blockchain + Machine Learning Powered Energy Exchange</p>
    </div>
    
    <div class="container">
        <!-- Solar Energy Prediction -->
        <div class="card">
            <h2>🔮 Solar Energy Prediction</h2>
            <form id="predictionForm">
                <div class="grid-2">
                    <div class="form-group">
                        <label for="temperature">Temperature (°C)</label>
                        <input type="number" id="temperature" name="temperature" value="25" step="0.1" required>
                    </div>
                    <div class="form-group">
                        <label for="humidity">Humidity (%)</label>
                        <input type="number" id="humidity" name="humidity" value="60" min="0" max="100" required>
                    </div>
                </div>
                <div class="grid-2">
                    <div class="form-group">
                        <label for="wind_speed">Wind Speed (m/s)</label>
                        <input type="number" id="wind_speed" name="wind_speed" value="3" step="0.1" required>
                    </div>
                    <div class="form-group">
                        <label for="cloud_cover">Cloud Cover (%)</label>
                        <input type="number" id="cloud_cover" name="cloud_cover" value="20" min="0" max="100" required>
                    </div>
                </div>
                <div class="form-group">
                    <label for="solar_radiation">Solar Radiation (W/m²)</label>
                    <input type="number" id="solar_radiation" name="solar_radiation" value="600" step="10" required>
                </div>
                <button type="submit">Predict Energy Output</button>
            </form>
            <div id="predictionResult"></div>
        </div>
        
        <!-- Energy Trading -->
        <div class="card">
            <h2>💱 Energy Trading Platform</h2>
            <form id="tradingForm">
                <div class="form-group">
                    <label for="user_type">User Type</label>
                    <select id="user_type" name="user_type" required>
                        <option value="buyer">Buyer</option>
                        <option value="seller">Seller</option>
                    </select>
                </div>
                <div class="grid-2">
                    <div class="form-group">
                        <label for="energy_amount">Energy Amount (kWh)</label>
                        <input type="number" id="energy_amount" name="energy_amount" value="10" step="0.1" required>
                    </div>
                    <div class="form-group">
                        <label for="price">Price (Wei/kWh)</label>
                        <input type="number" id="price" name="price" value="1000000000000000" step="100000000000000" required>
                    </div>
                </div>
                <button type="submit">Place Order</button>
            </form>
            <div id="tradingResult"></div>
        </div>
        
        <!-- System Status -->
        <div class="card full-width">
            <h2>📊 System Status</h2>
            <div class="grid-2">
                <div>
                    <h3>ML Model Status</h3>
                    <div id="mlStatus" class="status">
                        <strong>Status:</strong> <span id="mlStatusText">Checking...</span>
                    </div>
                </div>
                <div>
                    <h3>Blockchain Status</h3>
                    <div id="blockchainStatus" class="status">
                        <strong>Status:</strong> <span id="blockchainStatusText">Checking...</span>
                    </div>
                </div>
            </div>
            <div class="form-group">
                <button onclick="checkSystemStatus()">Refresh Status</button>
            </div>
        </div>
    </div>

    <script>
        // Check system status on page load
        window.onload = function() {
            checkSystemStatus();
        };
        
        // Prediction form submission
        document.getElementById('predictionForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                const resultDiv = document.getElementById('predictionResult');
                
                if (result.success) {
                    resultDiv.innerHTML = `
                        <div class="result">
                            <h4>Prediction Result:</h4>
                            <p><strong>Predicted Energy Output:</strong> ${result.prediction.toFixed(2)} kWh</p>
                            <p><strong>Weather Conditions:</strong></p>
                            <ul>
                                <li>Temperature: ${data.temperature}°C</li>
                                <li>Humidity: ${data.humidity}%</li>
                                <li>Wind Speed: ${data.wind_speed} m/s</li>
                                <li>Cloud Cover: ${data.cloud_cover}%</li>
                                <li>Solar Radiation: ${data.solar_radiation} W/m²</li>
                            </ul>
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `<div class="error">Error: ${result.error}</div>`;
                }
            } catch (error) {
                document.getElementById('predictionResult').innerHTML = `<div class="error">Error: ${error.message}</div>`;
            }
        });
        
        // Trading form submission
        document.getElementById('tradingForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            try {
                const response = await fetch('/trade', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                const resultDiv = document.getElementById('tradingResult');
                
                if (result.success) {
                    resultDiv.innerHTML = `
                        <div class="result">
                            <h4>Order Placed Successfully!</h4>
                            <p><strong>Order ID:</strong> ${result.order_id}</p>
                            <p><strong>User Type:</strong> ${data.user_type}</p>
                            <p><strong>Energy Amount:</strong> ${data.energy_amount} kWh</p>
                            <p><strong>Price:</strong> ${data.price} Wei/kWh</p>
                            <p><strong>Transaction Hash:</strong> ${result.tx_hash}</p>
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `<div class="error">Error: ${result.error}</div>`;
                }
            } catch (error) {
                document.getElementById('tradingResult').innerHTML = `<div class="error">Error: ${error.message}</div>`;
            }
        });
        
        // Check system status
        async function checkSystemStatus() {
            try {
                // Check ML model status
                const mlResponse = await fetch('/status/ml');
                const mlResult = await mlResponse.json();
                document.getElementById('mlStatusText').textContent = mlResult.status;
                
                // Check blockchain status
                const blockchainResponse = await fetch('/status/blockchain');
                const blockchainResult = await blockchainResponse.json();
                document.getElementById('blockchainStatusText').textContent = blockchainResult.status;
                
            } catch (error) {
                document.getElementById('mlStatusText').textContent = 'Error checking status';
                document.getElementById('blockchainStatusText').textContent = 'Error checking status';
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Main page with the trading interface"""
    return HTML_TEMPLATE

@app.route('/predict', methods=['POST'])
def predict_energy():
    """Predict solar energy output based on weather data"""
    try:
        data = request.get_json()
        
        # Extract weather parameters
        temperature = float(data.get('temperature', 25))
        humidity = float(data.get('humidity', 60))
        wind_speed = float(data.get('wind_speed', 3))
        cloud_cover = float(data.get('cloud_cover', 20))
        solar_radiation = float(data.get('solar_radiation', 600))
        
        # Load or train model
        if not predictor.is_trained:
            try:
                predictor.load_model()
            except:
                # If no saved model, train a new one
                predictor.train_model()
        
        # Make prediction
        prediction = predictor.predict_energy(
            temperature, humidity, wind_speed, cloud_cover, solar_radiation
        )
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'weather_data': {
                'temperature': temperature,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'cloud_cover': cloud_cover,
                'solar_radiation': solar_radiation
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/trade', methods=['POST'])
def place_trade_order():
    """Place a buy or sell order for energy"""
    try:
        data = request.get_json()
        
        # Extract trade parameters
        user_type = data.get('user_type', 'buyer')
        energy_amount = int(float(data.get('energy_amount', 10)))
        price = int(data.get('price', 1000000000000000))  # 0.001 ETH per kWh
        
        # Determine if it's a buy or sell order
        is_buy_order = (user_type == 'buyer')
        
        # For demo purposes, use placeholder values
        # In production, you'd get these from user authentication
        account_address = "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
        private_key = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
        
        if web3_helper is None:
            return jsonify({
                'success': False,
                'error': 'Blockchain connection not available'
            }), 500
        
        # Place order on blockchain
        tx_hash = web3_helper.place_order(
            account_address, private_key, energy_amount, price, is_buy_order
        )
        
        if tx_hash:
            return jsonify({
                'success': True,
                'order_id': 'DEMO_001',  # Placeholder
                'tx_hash': tx_hash,
                'message': f'Order placed successfully for {energy_amount} kWh at {price} Wei/kWh'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to place order on blockchain'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/status/ml')
def ml_status():
    """Check ML model status"""
    try:
        if predictor.is_trained:
            status = "Model trained and ready"
        else:
            status = "Model not trained"
        return jsonify({'status': status})
    except Exception as e:
        return jsonify({'status': f'Error: {str(e)}'})

@app.route('/status/blockchain')
def blockchain_status():
    """Check blockchain connection status"""
    try:
        if web3_helper and web3_helper.w3.is_connected():
            status = f"Connected to block {web3_helper.w3.eth.block_number}"
        else:
            status = "Not connected"
        return jsonify({'status': status})
    except Exception as e:
        return jsonify({'status': f'Error: {str(e)}'})

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'P2P Energy Trading System',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    try:
        # Initialize blockchain connection
        web3_helper = Web3Helper()
        print("Blockchain connection established")
    except Exception as e:
        print(f"Warning: Could not connect to blockchain: {e}")
        web3_helper = None
    
    print("Starting P2P Energy Trading System...")
    print("Access the system at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
