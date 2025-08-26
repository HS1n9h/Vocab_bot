#!/usr/bin/env python3
"""
Environment Setup Helper for Daily Vocabulary Bot
Creates and configures the .env file for users.
"""

import os
import shutil

def create_env_file():
    """Create the .env file from template."""
    template_file = 'env.template'
    env_file = '.env'
    
    if os.path.exists(env_file):
        print("⚠️ .env file already exists")
        response = input("Do you want to overwrite it? (y/N): ").lower()
        if response != 'y':
            print("Keeping existing .env file")
            return True
    
    # Create .env.template if it doesn't exist
    if not os.path.exists(template_file):
        template_content = """# Daily Vocabulary Bot Environment Configuration
# ================================================
# Copy this file to .env and fill in your actual values

# Required: Your email address where you want to receive vocabulary words
RECIPIENT_EMAIL=your.email@gmail.com

# Option 1: Gmail SMTP Configuration (Recommended for personal use)
# Make sure to enable 2FA and generate an App Password
GMAIL_USER=your.email@gmail.com
GMAIL_APP_PASSWORD=your-16-character-app-password

# Option 2: SendGrid Configuration (Alternative to Gmail)
# Uncomment and fill in if you prefer SendGrid
# SENDGRID_API_KEY=your-sendgrid-api-key

# Bot Configuration
BOT_NAME=Daily Vocabulary Bot
EMAIL_SUBJECT_PREFIX=📚
WORDS_PER_DAY=2
SCHEDULE_TIME=09:00

# Database Configuration
DATABASE_PATH=vocabulary.db

# API Configuration
DICTIONARY_API_URL=https://api.dictionaryapi.dev/api/v2/entries/en/
API_TIMEOUT=10

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=vocabulary_bot.log
"""
        
        with open(template_file, 'w') as f:
            f.write(template_content)
        print("✅ Created .env.template file")
    
    # Copy template to .env
    shutil.copy2(template_file, env_file)
    print("✅ Created .env file from template")
    
    print("\n📝 Now you need to edit the .env file with your email credentials:")
    print("   1. Open .env file in Notepad")
    print("   2. Replace 'your.email@gmail.com' with your actual Gmail address")
    print("   3. Replace 'your-16-character-app-password' with your Gmail app password")
    print("   4. Save the file")
    
    return True

def main():
    """Main setup function."""
    print("🔧 Daily Vocabulary Bot - Environment Setup")
    print("=" * 50)
    
    if create_env_file():
        print("\n🎉 Environment file created successfully!")
        print("\nNext steps:")
        print("1. Edit .env file with your credentials")
        print("2. Test configuration: python config.py")
        print("3. Run demo: python -c \"from main import run_demo; run_demo()\"")
        print("4. Send first email: python main.py")
    else:
        print("\n❌ Setup failed. Please check the errors above.")

if __name__ == "__main__":
    main()

