#!/bin/bash

# Creative Fatigue Detection System - Auto Start Script
# This script starts both backend and frontend automatically

echo "=================================================="
echo "  Creative Fatigue Detection System"
echo "  Starting application..."
echo "=================================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop first."
    echo "   Download from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "✅ Docker is ready"
echo ""

# Start services with Docker Compose
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to start (this may take 30-60 seconds)..."
sleep 10

# Check if backend is ready
echo "🔍 Checking backend..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health &> /dev/null; then
        echo "✅ Backend is ready!"
        break
    fi
    sleep 2
done

# Check if frontend is ready
echo "🔍 Checking frontend..."
for i in {1..30}; do
    if curl -s http://localhost:3000 &> /dev/null; then
        echo "✅ Frontend is ready!"
        break
    fi
    sleep 2
done

echo ""
echo "=================================================="
echo "  🎉 Application is ready!"
echo "=================================================="
echo ""
echo "  Frontend UI:  http://localhost:3000"
echo "  Backend API:  http://localhost:8000"
echo "  API Docs:     http://localhost:8000/docs"
echo ""
echo "  Opening browser in 3 seconds..."
echo ""
echo "  To stop: Press Ctrl+C or run ./stop.sh"
echo "=================================================="

sleep 3

# Open browser (works on macOS and Linux)
if command -v open &> /dev/null; then
    # macOS
    open http://localhost:3000
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open http://localhost:3000
else
    echo "Please open http://localhost:3000 in your browser"
fi

# Keep script running to show logs
echo ""
echo "📊 Application logs (press Ctrl+C to stop):"
echo ""
docker-compose logs -f
