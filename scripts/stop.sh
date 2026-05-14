#!/bin/bash

# PageIndex Testing Application - Stop Script
# This script stops the Streamlit application

echo "🛑 Stopping PageIndex Testing Application..."

# Find and kill Streamlit processes
PIDS=$(pgrep -f "streamlit run src/pageindex_test/main.py")

if [ -z "$PIDS" ]; then
    echo "ℹ️  No running Streamlit application found"
else
    echo "🔍 Found Streamlit process(es): $PIDS"
    echo "Stopping..."
    kill $PIDS
    sleep 2
    
    # Force kill if still running
    PIDS=$(pgrep -f "streamlit run src/pageindex_test/main.py")
    if [ ! -z "$PIDS" ]; then
        echo "⚠️  Force stopping..."
        kill -9 $PIDS
    fi
    
    echo "✅ Application stopped"
fi

# Deactivate virtual environment if active
if [ ! -z "$VIRTUAL_ENV" ]; then
    deactivate
    echo "✅ Virtual environment deactivated"
fi

echo "✨ Done!"

