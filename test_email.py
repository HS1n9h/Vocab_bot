#!/usr/bin/env python3
"""
Test Email Configuration Script
Tests the email configuration and sends a test email.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_email_config():
    """Test email configuration and send a test email."""
    print("🔧 Email Configuration Test")
    print("=" * 40)
    
    # Force reload environment variables from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv(override=True)
        print("✅ Environment variables reloaded from .env file")
    except ImportError:
        print("❌ python-dotenv not installed. Install with: pip install python-dotenv")
        return False
    except Exception as e:
        print(f"⚠️  Warning: Could not reload environment: {e}")
    
    # Check required environment variables
    recipient_email = os.getenv('RECIPIENT_EMAIL')
    gmail_user = os.getenv('GMAIL_USER')
    gmail_app_password = os.getenv('GMAIL_APP_PASSWORD')
    
    print(f"📧 Recipient Email: {recipient_email or 'NOT SET'}")
    print(f"📨 Gmail User: {gmail_user or 'NOT SET'}")
    print(f"🔑 Gmail App Password: {'SET' if gmail_app_password else 'NOT SET'}")
    
    if not all([recipient_email, gmail_user, gmail_app_password]):
        print("\n❌ Missing required configuration!")
        print("💡 Use the web interface at http://localhost:5000 to configure")
        return False
    
    print("\n✅ Configuration looks good!")
    
    # Test email sending
    print("\n🧪 Testing email sending...")
    
    try:
        from word_fetcher import WordFetcher
        from emailer import Emailer
        
        # Get a test word
        wf = WordFetcher()
        word_data = wf.get_new_words(1)
        
        if not word_data:
            print("❌ Could not fetch test word")
            return False
        
        word = word_data[0]['word']
        print(f"📚 Test word: {word}")
        
        # Send test email
        emailer = Emailer()
        
        # Use the correct method from main.py
        from main import send_vocabulary_email
        success = send_vocabulary_email(emailer, word_data, "🧪 Test")
        
        if success:
            print("✅ Test email sent successfully!")
            print(f"📧 Check your inbox: {recipient_email}")
            return True
        else:
            print("❌ Test email failed to send")
            print("💡 Check the logs for detailed error information")
            return False
            
    except Exception as e:
        print(f"❌ Error during email test: {e}")
        return False

if __name__ == "__main__":
    success = test_email_config()
    sys.exit(0 if success else 1)
