# ⚡ P2P Energy Trading System

A blockchain and machine learning powered peer-to-peer energy trading platform that enables users to trade solar energy using smart contracts and ML-based energy production predictions.

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Blockchain    │
│   (HTML/JS)     │◄──►│   (Flask)       │◄──►│   (Solidity)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   ML Model      │
                       │ (Random Forest) │
                       └─────────────────┘
```

## 🚀 Features

- **Solar Energy Prediction**: ML model predicts energy output based on weather conditions
- **P2P Trading**: Direct energy trading between buyers and sellers
- **Smart Contract**: Automated order matching and trade execution
- **Real-time Updates**: Live blockchain transaction monitoring
- **Weather Integration**: Uses temperature, humidity, wind, cloud cover, and solar radiation data

## 🛠️ Technology Stack

- **Backend**: Python 3.10+, Flask
- **Machine Learning**: scikit-learn, Random Forest Regressor
- **Blockchain**: Solidity, Web3.py, Ganache (local development)
- **Data Processing**: Pandas, NumPy
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

## 📋 Prerequisites

- Python 3.10 or higher
- Node.js and npm (for Ganache)
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd p2p-energy-trading
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install and Start Ganache

```bash
# Install Ganache globally
npm install -g ganache-cli

# Start local blockchain
ganache-cli --port 7545 --accounts 10 --defaultBalanceEther 1000
```

### 4. Deploy Smart Contract

```bash
# Navigate to contracts directory
cd contracts

# Compile and deploy using Hardhat (recommended)
npm install -g hardhat
hardhat compile
hardhat deploy --network localhost

# Or use Remix IDE with Ganache network
```

### 5. Update Contract Address

After deployment, update the contract address in `app/web3_helper.py`:

```python
CONTRACT_ADDRESS = "0x..." # Your deployed contract address
```

## 🎯 Usage

### 1. Start the Application

```bash
python app/server.py
```

The system will be available at: http://localhost:5000

### 2. Solar Energy Prediction

1. Navigate to the "Solar Energy Prediction" section
2. Input weather conditions:
   - Temperature (°C)
   - Humidity (%)
   - Wind Speed (m/s)
   - Cloud Cover (%)
   - Solar Radiation (W/m²)
3. Click "Predict Energy Output" to get ML-based predictions

### 3. Energy Trading

1. Navigate to the "Energy Trading Platform" section
2. Select user type (Buyer/Seller)
3. Input energy amount (kWh) and price (Wei/kWh)
4. Click "Place Order" to submit to blockchain

### 4. Monitor Transactions

- View real-time order matching
- Track trade execution on blockchain
- Monitor system status

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
BLOCKCHAIN_RPC_URL=http://127.0.0.1:7545
CONTRACT_ADDRESS=0x...
PRIVATE_KEY=0x...
```

### Blockchain Network

- **Development**: Ganache (localhost:7545)
- **Testnet**: Sepolia, Goerli
- **Mainnet**: Ethereum mainnet

## 🧪 Testing

### Run Unit Tests

```bash
python -m pytest tests/
```

### Test Smart Contract

```bash
# Navigate to contracts directory
cd contracts
npx hardhat test
```

### Test ML Model

```bash
python ml/solar_predictor.py
```

## 📊 API Endpoints

### ML Prediction
- `POST /predict` - Predict solar energy output

### Trading
- `POST /trade` - Place buy/sell order
- `GET /status/ml` - ML model status
- `GET /status/blockchain` - Blockchain connection status
- `GET /health` - System health check

## 🔍 Troubleshooting

### Common Issues

1. **Blockchain Connection Failed**
   - Ensure Ganache is running on port 7545
   - Check network configuration

2. **ML Model Not Working**
   - Verify all dependencies are installed
   - Check data file paths

3. **Contract Deployment Issues**
   - Ensure sufficient ETH in test accounts
   - Check Solidity compiler version

### Debug Mode

Enable debug mode in Flask:

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Ethereum Foundation for blockchain technology
- scikit-learn team for ML libraries
- Flask community for web framework

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**Note**: This is a prototype system for educational and demonstration purposes. For production use, additional security measures, testing, and compliance checks are required.
