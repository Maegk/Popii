#!/bin/bash

# Creative Fatigue Detection System - Stop Script

echo "=================================================="
echo "  Stopping Creative Fatigue Detection System..."
echo "=================================================="
echo ""

# Stop Docker Compose services
docker-compose down

echo ""
echo "✅ Application stopped successfully!"
echo ""
