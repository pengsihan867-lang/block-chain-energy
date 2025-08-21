#!/usr/bin/env python3
"""
Deployment script for P2P Energy Trading System
"""

import os
import sys
import subprocess
import time

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_prerequisites():
    """Check if all prerequisites are installed"""
    print("🔍 Checking prerequisites...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 10):
        print("❌ Python 3.10+ is required")
        return False
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check pip
    if run_command("pip --version", "Checking pip"):
        print("✅ pip is available")
    else:
        print("❌ pip is not available")
        return False
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    if run_command("pip install -r requirements.txt", "Installing requirements"):
        print("✅ Dependencies installed successfully")
        return True
    else:
        print("❌ Failed to install dependencies")
        return False

def setup_ml_model():
    """Setup and train the ML model"""
    print("🤖 Setting up ML model...")
    
    # Create models directory
    os.makedirs("models", exist_ok=True)
    
    # Run ML training
    if run_command("python ml/solar_predictor.py", "Training ML model"):
        print("✅ ML model setup completed")
        return True
    else:
        print("❌ ML model setup failed")
        return False

def check_blockchain():
    """Check blockchain connection"""
    print("⛓️ Checking blockchain connection...")
    
    try:
        import web3
        from web3 import Web3
        
        # Try to connect to local Ganache
        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
        
        if w3.is_connected():
            block_number = w3.eth.block_number
            print(f"✅ Connected to blockchain at block {block_number}")
            return True
        else:
            print("⚠️  Could not connect to local blockchain")
            print("💡 Make sure Ganache is running on port 7545")
            return False
            
    except ImportError:
        print("❌ web3 library not available")
        return False
    except Exception as e:
        print(f"❌ Blockchain check failed: {e}")
        return False

def start_application():
    """Start the Flask application"""
    print("🚀 Starting P2P Energy Trading System...")
    
    print("\n📋 Deployment Summary:")
    print("========================")
    print("✅ Python environment: Ready")
    print("✅ Dependencies: Installed")
    print("✅ ML Model: Trained")
    
    blockchain_status = "✅ Connected" if check_blockchain() else "⚠️  Not Connected"
    print(f"⛓️  Blockchain: {blockchain_status}")
    
    print("\n🌐 Starting web application...")
    print("💡 The system will be available at: http://localhost:5000")
    print("💡 Press Ctrl+C to stop the application")
    
    # Start Flask app
    try:
        run_command("python app/server.py", "Starting Flask server")
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Failed to start application: {e}")

def main():
    """Main deployment function"""
    print("🚀 P2P Energy Trading System - Deployment Script")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        print("❌ Prerequisites check failed. Please fix the issues and try again.")
        return
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Dependency installation failed. Please check the requirements.txt file.")
        return
    
    # Setup ML model
    if not setup_ml_model():
        print("❌ ML model setup failed. Please check the ml/solar_predictor.py file.")
        return
    
    # Check blockchain
    check_blockchain()
    
    # Start application
    start_application()

if __name__ == "__main__":
    main()
