#!/usr/bin/env python3
"""
Configuration management for Daily Vocabulary Bot.
Handles environment variables, validation, and default settings.
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Centralized configuration management."""
    
    # Email Configuration
    RECIPIENT_EMAIL: str = os.getenv('RECIPIENT_EMAIL', '')
    GMAIL_USER: str = os.getenv('GMAIL_USER', '')
    GMAIL_APP_PASSWORD: str = os.getenv('GMAIL_APP_PASSWORD', '')
    SENDGRID_API_KEY: str = os.getenv('SENDGRID_API_KEY', '')
    
    # Bot Configuration
    BOT_NAME: str = os.getenv('BOT_NAME', 'Daily Vocabulary Bot')
    EMAIL_SUBJECT_PREFIX: str = os.getenv('EMAIL_SUBJECT_PREFIX', '📚')
    WORDS_PER_DAY: int = int(os.getenv('WORDS_PER_DAY', '2'))
    SCHEDULE_TIME: str = os.getenv('SCHEDULE_TIME', '09:00')
    
    # Database Configuration
    DATABASE_PATH: str = os.getenv('DATABASE_PATH', 'vocabulary.db')
    
    # API Configuration
    DICTIONARY_API_URL: str = os.getenv('DICTIONARY_API_URL', 'https://api.dictionaryapi.dev/api/v2/entries/en/')
    API_TIMEOUT: int = int(os.getenv('API_TIMEOUT', '10'))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', 'vocabulary_bot.log')
    
    @classmethod
    def validate(cls) -> Tuple[bool, List[str]]:
        """Validate configuration and return (is_valid, error_messages)."""
        errors = []
        
        # Check required email configuration
        if not cls.RECIPIENT_EMAIL:
            errors.append("RECIPIENT_EMAIL is required")
        elif '@' not in cls.RECIPIENT_EMAIL:
            errors.append("RECIPIENT_EMAIL must be a valid email address")
        
        # Check Gmail configuration
        if not cls.GMAIL_USER and not cls.SENDGRID_API_KEY:
            errors.append("Either GMAIL_USER or SENDGRID_API_KEY must be configured")
        
        if cls.GMAIL_USER and not cls.GMAIL_APP_PASSWORD:
            errors.append("GMAIL_APP_PASSWORD is required when using Gmail")
        
        # Check bot configuration
        if cls.WORDS_PER_DAY < 1 or cls.WORDS_PER_DAY > 10:
            errors.append("WORDS_PER_DAY must be between 1 and 10")
        
        # Check schedule format
        try:
            hour, minute = cls.SCHEDULE_TIME.split(':')
            int(hour), int(minute)
        except (ValueError, AttributeError):
            errors.append("SCHEDULE_TIME must be in HH:MM format (e.g., 09:00)")
        
        return len(errors) == 0, errors
    
    @classmethod
    def get_email_service(cls) -> str:
        """Determine which email service to use."""
        if cls.SENDGRID_API_KEY:
            return 'sendgrid'
        elif cls.GMAIL_USER and cls.GMAIL_APP_PASSWORD:
            return 'gmail'
        else:
            return 'none'
    
    @classmethod
    def get_config_summary(cls) -> Dict[str, str]:
        """Get a summary of current configuration."""
        return {
            'recipient_email': cls.RECIPIENT_EMAIL,
            'email_service': cls.get_email_service(),
            'words_per_day': str(cls.WORDS_PER_DAY),
            'schedule_time': cls.SCHEDULE_TIME,
            'database': cls.DATABASE_PATH,
            'bot_name': cls.BOT_NAME
        }
    
    @classmethod
    def print_config(cls):
        """Print current configuration status."""
        print("🔧 Daily Vocabulary Bot Configuration")
        print("=" * 40)
        
        summary = cls.get_config_summary()
        for key, value in summary.items():
            if key == 'recipient_email':
                print(f"📧 Recipient Email: {value or 'Not configured'}")
            elif key == 'email_service':
                print(f"📨 Email Service: {value.title()}")
            elif key == 'words_per_day':
                print(f"🔤 Words Per Day: {value}")
            elif key == 'schedule_time':
                print(f"⏰ Schedule Time: {value}")
            elif key == 'database':
                print(f"🗄️ Database: {value}")
            elif key == 'bot_name':
                print(f"🤖 Bot Name: {value}")
        
        print()
        is_valid, errors = cls.validate()
        print(f"✅ Configuration Valid: {is_valid}")
        
        if is_valid:
            print("🎉 Configuration is ready to use!")
        else:
            print("❌ Configuration errors found:")
            for error in errors:
                print(f"   • {error}")
        
        return is_valid

def create_env_template():
    """Create a .env.template file for users."""
    template_content = """# Daily Vocabulary Bot Environment Configuration
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

# Optional: Customize the bot behavior
BOT_NAME=Daily Vocabulary Bot
EMAIL_SUBJECT_PREFIX=📚
WORDS_PER_DAY=2
SCHEDULE_TIME=09:00
DATABASE_PATH=vocabulary.db
API_TIMEOUT=10
LOG_LEVEL=INFO
LOG_FILE=vocabulary_bot.log
"""
    
    with open('.env.template', 'w') as f:
        f.write(template_content)
    print("✅ Created .env.template file")

if __name__ == "__main__":
    Config.print_config()
    if not os.path.exists('.env.template'):
        create_env_template()
