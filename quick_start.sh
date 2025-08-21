#!/bin/bash

# Quick Start Script for P2P Energy Trading System

echo "⚡ P2P Energy Trading System - Quick Start"
echo "=========================================="

# Check Python version
echo "🔍 Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    echo "✅ Python $PYTHON_VERSION found"
else
    echo "❌ Python 3 not found. Please install Python 3.10+ first."
    exit 1
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
if pip3 install -r requirements.txt; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Train ML model
echo "🤖 Training ML model..."
if python3 ml/solar_predictor.py; then
    echo "✅ ML model trained successfully"
else
    echo "❌ Failed to train ML model"
    exit 1
fi

# Check blockchain connection
echo "⛓️  Checking blockchain connection..."
echo "💡 Make sure Ganache is running on port 7545"
echo "   Command: ganache-cli --port 7545"

# Start the application
echo "🚀 Starting P2P Energy Trading System..."
echo "🌐 The system will be available at: http://localhost:5000"
echo "💡 Press Ctrl+C to stop the application"
echo ""

python3 app/server.py
