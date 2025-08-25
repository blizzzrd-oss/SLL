# SLL Executable Builder - PowerShell Version
Write-Host "🚀 Building SLL executable with embedded resources..." -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Check if PyInstaller is installed
try {
    python -c "import PyInstaller; print('PyInstaller found')" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller not found"
    }
    Write-Host "✅ PyInstaller is available" -ForegroundColor Green
} catch {
    Write-Host "⚠️  PyInstaller not found. Installing..." -ForegroundColor Yellow
    pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install PyInstaller" -ForegroundColor Red
        exit 1
    }
}

# Run the build script
Write-Host "🔨 Running build script..." -ForegroundColor Cyan
python build_exe.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "🎉 Build completed successfully!" -ForegroundColor Green
    Write-Host "📁 Your executable is in the 'dist' folder" -ForegroundColor Cyan
} else {
    Write-Host "💥 Build failed!" -ForegroundColor Red
    exit 1
}
