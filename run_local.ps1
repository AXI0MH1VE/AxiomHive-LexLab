#!/usr/bin/env pwsh
# AxiomHive Local Development Server
# Starts the backend and serves frontend assets

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AxiomHive Local Development Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ and add it to your PATH" -ForegroundColor Yellow
    exit 1
}

# Check if we're in the right directory
if (-not (Test-Path "backend\requirements.txt")) {
    Write-Host "ERROR: Please run this script from the repository root directory" -ForegroundColor Red
    Write-Host "Expected to find: backend\requirements.txt" -ForegroundColor Yellow
    exit 1
}

Write-Host "Setting up backend environment..." -ForegroundColor Yellow

# Change to backend directory and install requirements
Push-Location backend
try {
    Write-Host "Installing Python dependencies..." -ForegroundColor Gray
    python -m pip install -r requirements.txt
    
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install Python dependencies"
    }
    
    Write-Host "✓ Backend dependencies installed" -ForegroundColor Green
    
    # Check if there's a main.py, app.py, or run.py
    $serverScript = $null
    if (Test-Path "main.py") { $serverScript = "main.py" }
    elseif (Test-Path "app.py") { $serverScript = "app.py" }
    elseif (Test-Path "run.py") { $serverScript = "run.py" }
    elseif (Test-Path "server.py") { $serverScript = "server.py" }
    
    if ($serverScript) {
        Write-Host "Starting backend server ($serverScript)..." -ForegroundColor Yellow
        Write-Host "Backend will be available at http://127.0.0.1:8000" -ForegroundColor Green
        Write-Host "Frontend assets will be mounted at http://127.0.0.1:8000/ui/" -ForegroundColor Green
        Write-Host ""
        Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
        Write-Host ""
        
        # Start the Python server
        python $serverScript
    } else {
        Write-Host "⚠ Warning: No main server script found (main.py, app.py, run.py, server.py)" -ForegroundColor Yellow
        Write-Host "Trying to start with uvicorn..." -ForegroundColor Gray
        
        # Try to start with uvicorn if available
        try {
            python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
        } catch {
            Write-Host "⚠ Could not start with uvicorn. Please check your backend configuration." -ForegroundColor Yellow
            Write-Host "You may need to manually start your backend server." -ForegroundColor Gray
        }
    }
    
} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
} finally {
    Pop-Location
}

Write-Host ""
Write-Host "Local development server stopped." -ForegroundColor Yellow