#!/bin/bash

# 🚀 Daily Vocabulary Bot Deployment Script
# This script helps deploy your bot to various cloud platforms

echo "🚀 Daily Vocabulary Bot Deployment Script"
echo "========================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

# Check if all required files exist
echo "📋 Checking required files..."
required_files=("requirements.txt" "Procfile" "runtime.txt" "Dockerfile")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo "❌ Missing required files: ${missing_files[*]}"
    exit 1
fi

echo "✅ All required files found!"

# Check environment variables
echo "🔧 Checking environment variables..."
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Please create one with:"
    echo "   GMAIL_ADDRESS=your_email@gmail.com"
    echo "   GMAIL_PASSWORD=your_app_password"
    echo "   RECIPIENT_EMAIL=recipient@example.com"
    echo ""
    echo "Or run: python setup_env.py"
fi

# Show deployment options
echo ""
echo "🌐 Choose your deployment platform:"
echo "1. Render (Free, Easy) - Recommended for beginners"
echo "2. Railway (Free tier) - Good alternative to Render"
echo "3. Heroku (Free tier) - Classic choice"
echo "4. Docker (Local/Cloud) - For advanced users"
echo "5. VPS Setup - For full control"

echo ""
echo "📚 For detailed instructions, see: DEPLOYMENT_GUIDE.md"
echo ""
echo "🔗 Quick deploy links:"
echo "   Render: https://render.com"
echo "   Railway: https://railway.app"
echo "   Heroku: https://heroku.com"

echo ""
echo "💡 Pro tip: Start with Render (option 1) - it's free and easy!"
