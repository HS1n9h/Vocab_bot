@echo off
chcp 65001 >nul
echo 🚀 Daily Vocabulary Bot Deployment Script
echo ========================================

REM Check if git is initialized
if not exist ".git" (
    echo ❌ Git repository not found. Please initialize git first:
    echo    git init
    echo    git add .
    echo    git commit -m "Initial commit"
    pause
    exit /b 1
)

REM Check if all required files exist
echo 📋 Checking required files...
set missing_files=
if not exist "requirements.txt" set missing_files=!missing_files! requirements.txt
if not exist "Procfile" set missing_files=!missing_files! Procfile
if not exist "runtime.txt" set missing_files=!missing_files! runtime.txt
if not exist "Dockerfile" set missing_files=!missing_files! Dockerfile

if defined missing_files (
    echo ❌ Missing required files: %missing_files%
    pause
    exit /b 1
)

echo ✅ All required files found!

REM Check environment variables
echo 🔧 Checking environment variables...
if not exist ".env" (
    echo ⚠️  .env file not found. Please create one with:
    echo    GMAIL_ADDRESS=your_email@gmail.com
    echo    GMAIL_PASSWORD=your_app_password
    echo    RECIPIENT_EMAIL=recipient@example.com
    echo.
    echo Or run: python setup_env.py
)

REM Show deployment options
echo.
echo 🌐 Choose your deployment platform:
echo 1. Render (Free, Easy) - Recommended for beginners
echo 2. Railway (Free tier) - Good alternative to Render
echo 3. Heroku (Free tier) - Classic choice
echo 4. Docker (Local/Cloud) - For advanced users
echo 5. VPS Setup - For full control

echo.
echo 📚 For detailed instructions, see: DEPLOYMENT_GUIDE.md
echo.
echo 🔗 Quick deploy links:
echo    Render: https://render.com
echo    Railway: https://railway.app
echo    Heroku: https://heroku.com

echo.
echo 💡 Pro tip: Start with Render (option 1) - it's free and easy!
pause
