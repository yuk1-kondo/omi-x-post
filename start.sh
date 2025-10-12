#!/bin/bash

# OMI Twitter Integration - Start Script

echo "🐦 Starting OMI Twitter Integration..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "❗ Please edit .env file and add your API credentials before running the app."
    echo "   Then run this script again."
    exit 1
fi

# Check for required environment variables
source .env

if [ -z "$TWITTER_API_KEY" ] || [ "$TWITTER_API_KEY" = "your_api_key_here" ]; then
    echo "❗ Please configure your Twitter API credentials in .env file"
    exit 1
fi

if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ]; then
    echo "❗ Please configure your OpenAI API key in .env file"
    exit 1
fi

# Start the application
echo ""
echo "✅ Configuration verified!"
echo "🚀 Starting server on port ${APP_PORT:-8000}..."
echo ""
echo "📱 Setup Instructions:"
echo "   1. Open OMI mobile app"
echo "   2. Go to Settings → Developer Mode"
echo "   3. Create Integration App with:"
echo "      - Webhook: http://your-domain:${APP_PORT:-8000}/webhook"
echo "      - Auth URL: http://your-domain:${APP_PORT:-8000}/auth"
echo "      - Setup Check: http://your-domain:${APP_PORT:-8000}/setup-completed"
echo ""
echo "📚 Full documentation: README.md"
echo ""

python main.py

