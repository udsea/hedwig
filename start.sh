#!/bin/bash

# Hedwig - Start Script
# This script starts both the backend and frontend services

echo "🦉 Starting Hedwig - Research Paper Search Tool"
echo "=============================================="

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

if ! command_exists bun && ! command_exists npm; then
    echo "❌ Either Bun or npm is required but neither is installed."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Start backend
echo ""
echo "🐍 Starting Backend (FastAPI)..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Start backend in background
echo "Starting backend server at http://localhost:8000"
python -m src.main &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo ""
echo "⚛️  Starting Frontend (React + Vite)..."
cd ../frontend

# Install dependencies and start frontend
if command_exists bun; then
    echo "Using Bun for frontend..."
    bun install > /dev/null 2>&1
    echo "Starting frontend server at http://localhost:5173"
    bun run dev &
else
    echo "Using npm for frontend..."
    npm install > /dev/null 2>&1
    echo "Starting frontend server at http://localhost:5173"
    npm run dev &
fi

FRONTEND_PID=$!

echo ""
echo "🎉 Hedwig is now running!"
echo "Frontend: http://localhost:5173"
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"

# Function to cleanup processes
cleanup() {
    echo ""
    echo "🛑 Shutting down Hedwig..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Set trap to cleanup on script termination
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
