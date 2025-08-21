import unittest
from web3 import Web3
import json
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestEnergyTradingContract(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        # Connect to local blockchain (Ganache)
        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
        
        # Test account (you'll need to replace with actual test account)
        self.test_account = self.w3.eth.accounts[0]
        self.test_private_key = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
        
        # Contract ABI and bytecode would be loaded here
        # For now, we'll test the connection
        
    def test_blockchain_connection(self):
        """Test if we can connect to the blockchain"""
        self.assertTrue(self.w3.is_connected())
        
    def test_account_balance(self):
        """Test if test account has ETH"""
        balance = self.w3.eth.get_balance(self.test_account)
        self.assertGreater(balance, 0)
        
    def test_block_number(self):
        """Test if we can get current block number"""
        block_number = self.w3.eth.block_number
        self.assertIsInstance(block_number, int)
        self.assertGreaterEqual(block_number, 0)

class TestSolarPredictor(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from ml.solar_predictor import SolarEnergyPredictor
        self.predictor = SolarEnergyPredictor()
        
    def test_data_generation(self):
        """Test sample data generation"""
        data = self.predictor.generate_sample_data(100)
        self.assertEqual(len(data), 100)
        self.assertIn('energy_output', data.columns)
        self.assertIn('temperature', data.columns)
        
    def test_model_training(self):
        """Test model training"""
        data = self.predictor.generate_sample_data(100)
        mse, r2 = self.predictor.train_model(data)
        self.assertIsInstance(mse, float)
        self.assertIsInstance(r2, float)
        self.assertTrue(self.predictor.is_trained)
        
    def test_prediction(self):
        """Test energy prediction"""
        # Train model first
        data = self.predictor.generate_sample_data(100)
        self.predictor.train_model(data)
        
        # Test prediction
        prediction = self.predictor.predict_energy(25, 60, 3, 20, 600)
        self.assertIsInstance(prediction, float)
        self.assertGreaterEqual(prediction, 0)

if __name__ == '__main__':
    unittest.main()
