#!/bin/bash

# PageIndex Testing Application - Launch Script
# This script starts the Streamlit application

set -e

echo "🚀 Starting PageIndex Testing Application..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file."
    echo ""
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""

# Check if user wants detached mode
if [ "$1" = "--detached" ] || [ "$1" = "-d" ]; then
    echo "🌐 Starting Streamlit application in detached mode..."
    echo "📍 Application will run at http://localhost:8501"
    echo ""
    
    # Start Streamlit in background
    nohup streamlit run src/pageindex_test/main.py > streamlit.log 2>&1 &
    STREAMLIT_PID=$!
    
    # Wait a moment for startup
    sleep 3
    
    # Check if process is still running
    if ps -p $STREAMLIT_PID > /dev/null; then
        echo "✅ Application started successfully!"
        echo "📍 Process ID: $STREAMLIT_PID"
        echo "📝 Logs: streamlit.log"
        echo "🌐 URL: http://localhost:8501"
        echo ""
        echo "To stop: ./scripts/stop.sh"
        echo "To view logs: tail -f streamlit.log"
    else
        echo "❌ Failed to start application"
        echo "Check streamlit.log for errors"
        exit 1
    fi
else
    echo "🌐 Starting Streamlit application..."
    echo "📍 The application will open in your browser at http://localhost:8501"
    echo ""
    echo "Press Ctrl+C to stop the application"
    echo "💡 Tip: Use './scripts/launch.sh --detached' to run in background"
    echo ""
    
    # Start Streamlit in foreground
    streamlit run src/pageindex_test/main.py
fi

