#!/bin/bash

echo "🐦 OMI Twitter Integration - Ngrok Setup"
echo "========================================"
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ Ngrok is not installed!"
    echo ""
    echo "📥 Install ngrok:"
    echo "   macOS: brew install ngrok/ngrok/ngrok"
    echo "   Or download from: https://ngrok.com/download"
    echo ""
    exit 1
fi

echo "✅ Ngrok is installed"
echo ""

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

echo ""
echo "🚀 Starting the app on port 8000..."
echo ""
echo "⚠️  IMPORTANT: After ngrok starts, you need to:"
echo "   1. Copy the ngrok HTTPS URL (e.g., https://xxxx.ngrok.io)"
echo "   2. Update .env file: OAUTH_REDIRECT_URL=https://xxxx.ngrok.io/auth/callback"
echo "   3. Update Twitter Developer Portal with the same callback URL"
echo "   4. Restart the app (Ctrl+C and run again)"
echo ""
echo "Press Enter to continue..."
read

# Start the FastAPI app in background
echo "🌟 Starting FastAPI app..."
python main.py &
APP_PID=$!

# Wait for app to start
sleep 3

# Start ngrok
echo ""
echo "🌐 Starting ngrok tunnel..."
echo ""
echo "Your webhook URLs will be:"
echo "  - Webhook: https://YOUR-NGROK-URL/webhook"
echo "  - Auth: https://YOUR-NGROK-URL/auth"
echo "  - Setup Check: https://YOUR-NGROK-URL/setup-completed"
echo ""

ngrok http 8000

# Cleanup on exit
kill $APP_PID 2>/dev/null

