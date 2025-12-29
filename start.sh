#!/bin/bash

echo "🚀 Starting Finance AI Chatbot..."
echo ""

echo "📦 Installing Python dependencies..."
cd backend
pip install -q -r requirements.txt

echo ""
echo "🧠 Training the neural network..."
python model.py

echo ""
echo "🌐 Starting Flask backend on port 5000..."
python app.py &
BACKEND_PID=$!

echo ""
echo "⚡ Backend is running!"
echo ""
echo "📝 Instructions:"
echo "   - Backend: http://localhost:5000"
echo "   - Frontend: Check your dev server"
echo ""
echo "To stop the backend: kill $BACKEND_PID"
echo ""
echo "Press Ctrl+C to stop the backend server"

wait $BACKEND_PID
