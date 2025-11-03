# Development startup script for Task Management API

Write-Host "Starting Task Management API development environment..." -ForegroundColor Green

# Start backend in background
Write-Host "Starting backend server..." -ForegroundColor Yellow
Start-Process -FilePath "venv\Scripts\python.exe" -ArgumentList "backend\app\main.py" -WorkingDirectory "." -NoNewWindow

# Start frontend
Write-Host "Starting frontend development server..." -ForegroundColor Yellow
Set-Location -Path "frontend"
npm start