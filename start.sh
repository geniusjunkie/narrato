#!/bin/bash
# Narrato Startup Script

echo "🎬 Starting Narrato API..."
echo ""

# Check if API keys are set
if [ -z "$GROQ_API_KEY" ]; then
    echo "⚠️  Warning: GROQ_API_KEY not set"
    echo "   Get your key at: https://console.groq.com"
fi

if [ -z "$GOOGLE_API_KEY" ]; then
    echo "⚠️  Warning: GOOGLE_API_KEY not set"
    echo "   Get your key at: https://aistudio.google.com/app/apikey"
fi

echo ""
echo "📡 API will be available at:"
echo "   http://localhost:8000"
echo "   http://localhost:8000/docs (API documentation)"
echo ""

# Run the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
