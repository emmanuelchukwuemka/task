#!/bin/bash

# Development startup script for Task Management API

echo "Starting Task Management API development environment..."

# Start backend in background
echo "Starting backend server..."
python backend/app/main.py &

# Start frontend
echo "Starting frontend development server..."
cd frontend
npm start