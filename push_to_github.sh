#!/bin/bash

# Script to push P2P Energy Trading System to GitHub

echo "🚀 Pushing P2P Energy Trading System to GitHub..."

# Check if remote origin exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ No remote origin found. Please add your GitHub repository first:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/p2p-energy-trading.git"
    echo ""
    echo "📋 Steps to complete:"
    echo "1. Create a new repository on GitHub named 'p2p-energy-trading'"
    echo "2. Copy the repository URL"
    echo "3. Run: git remote add origin <REPOSITORY_URL>"
    echo "4. Then run this script again"
    exit 1
fi

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "📍 Current branch: $CURRENT_BRANCH"

# Check if there are uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "📝 Staging uncommitted changes..."
    git add .
    git commit -m "Update: P2P Energy Trading System improvements"
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
if git push -u origin $CURRENT_BRANCH; then
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🌐 Your repository is now available at:"
    git remote get-url origin
    echo ""
    echo "📋 Next steps:"
    echo "1. Install dependencies: pip3 install -r requirements.txt"
    echo "2. Start Ganache: ganache-cli --port 7545"
    echo "3. Run the system: python3 deploy.py"
    echo "4. Access at: http://localhost:5000"
else
    echo "❌ Failed to push to GitHub"
    echo "💡 Check your GitHub credentials and try again"
    exit 1
fi
