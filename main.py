#!/usr/bin/env python3
"""
Daily Vocabulary Bot - Main Entry Point
Sends new English vocabulary words to your email every day.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from config import Config
from word_fetcher import WordFetcher
from database import Database
from emailer import Emailer

def setup_logging():
    """Configure logging for the application."""
    log_file = Path(Config.LOG_FILE)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure logging with rotation
    from logging.handlers import RotatingFileHandler
    
    # Create rotating file handler (max 5MB per file, keep 3 backup files)
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL.upper()),
        handlers=[file_handler, console_handler]
    )

def validate_configuration():
    """Validate the configuration before running."""
    logger = logging.getLogger(__name__)
    
    is_valid, errors = Config.validate()
    
    if not is_valid:
        logger.error("Configuration validation failed:")
        for error in errors:
            logger.error(f"  • {error}")
        
        print("❌ Configuration errors found. Please fix them and try again.")
        print("\nRun 'python config.py' to see your current configuration.")
        print("Copy 'env.template' to '.env' and fill in your values.")
        return False
    
    return True

def get_new_words(word_fetcher: WordFetcher, database: Database, count: int):
    """Get new words that haven't been sent before."""
    logger = logging.getLogger(__name__)
    
    # Get list of already sent words
    sent_words = database.get_sent_words(limit=100)
    sent_word_list = [word['word'].lower() for word in sent_words]
    
    # Get new words
    new_words = word_fetcher.get_new_words(count, exclude_words=sent_word_list)
    
    if not new_words:
        logger.warning("No new words available. All words may have been sent already.")
        return []
    
    logger.info(f"Retrieved {len(new_words)} new words")
    return new_words

def format_email_content(words, date=None):
    """Format the email content with the vocabulary words."""
    if not date:
        date = datetime.now().strftime('%B %d, %Y')
    
    content = f"Hello! Here are your daily vocabulary words for {date}:\n\n"
    
    for i, word_data in enumerate(words, 1):
        content += f"🔤 Word {i}: {word_data['word'].title()}\n"
        content += f"📖 Meaning: {word_data['meaning']}\n"
        
        if word_data.get('part_of_speech'):
            content += f"🏷️ Part of Speech: {word_data['part_of_speech']}\n"
        
        content += f"💬 Example: {word_data.get('example', 'No example available')}\n\n"
    
    content += "Keep learning and expanding your vocabulary! 📚✨"
    return content

def send_vocabulary_email(emailer: Emailer, words, subject_prefix: str):
    """Send the vocabulary email."""
    logger = logging.getLogger(__name__)
    
    try:
        # Get word count statistics
        database = Database(Config.DATABASE_PATH)
        total_words_sent = database.get_total_words_sent()
        words_sent_today = database.get_words_sent_today()
        
        # Get current date for subject line
        from datetime import datetime
        current_date = datetime.now().strftime('%B %d, %Y')
        
        # Format email content with statistics
        email_content = emailer.format_vocabulary_email(words)
        
        # Add statistics to the email content
        stats_text = f"\n\nVocabulary Statistics:\n"
        stats_text += f"Total words sent so far: {total_words_sent}\n"
        stats_text += f"Words sent today: {words_sent_today}\n"
        stats_text += f"Your learning progress continues.\n"
        
        stats_html = f"<hr><h3>Vocabulary Statistics</h3>"
        stats_html += f"<p><strong>Total words sent so far:</strong> {total_words_sent}</p>"
        stats_html += f"<p><strong>Words sent today:</strong> {words_sent_today}</p>"
        stats_html += f"<p><strong>Your learning progress continues.</strong></p>"
        
        # Combine content with statistics
        final_text = email_content['text'] + stats_text
        final_html = email_content['html'] + stats_html
        
        # Send email
        subject = f"Daily Vocabulary - {current_date}"
        success = emailer.send_email(
            subject=subject,
            body=final_text,
            html_body=final_html
        )
        
        if success:
            logger.info(f"Email sent successfully to {Config.RECIPIENT_EMAIL}")
            return True
        else:
            logger.error("Failed to send email")
            return False
            
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

def update_database(database: Database, words):
    """Mark words as sent in the database."""
    logger = logging.getLogger(__name__)
    
    try:
        for word_data in words:
            success = database.mark_word_sent(
                word=word_data['word'],
                meaning=word_data['meaning'],
                part_of_speech=word_data.get('part_of_speech'),
                example=word_data.get('example')
            )
            
            if success:
                logger.info(f"Word '{word_data['word']}' marked as sent")
            else:
                logger.warning(f"Word '{word_data['word']}' already exists in database")
        
        return True
        
    except Exception as e:
        logger.error(f"Error updating database: {e}")
        return False

def main():
    """Main function to run the daily vocabulary bot."""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting Daily Vocabulary Bot...")
        
        # Validate configuration first
        if not validate_configuration():
            return False
        
        # Initialize components
        database = Database(Config.DATABASE_PATH)
        word_fetcher = WordFetcher()
        emailer = Emailer()
        
        # Get new words
        words = get_new_words(word_fetcher, database, Config.WORDS_PER_DAY)
        
        if not words:
            logger.warning("No new words available. All words may have been sent already.")
            print("⚠️ No new words available. The bot may have sent all available words.")
            return False
        
        # Send email
        email_success = send_vocabulary_email(
            emailer, 
            words, 
            Config.EMAIL_SUBJECT_PREFIX
        )
        
        if email_success:
            # Update database
            db_success = update_database(database, words)
            
            if db_success:
                logger.info(f"Successfully processed {len(words)} words")
                print(f"✅ Successfully sent {len(words)} vocabulary words to {Config.RECIPIENT_EMAIL}")
                return True
            else:
                logger.error("Failed to update database")
                print("⚠️ Email sent but database update failed")
                return False
        else:
            logger.error("Failed to send email")
            print("❌ Failed to send email. Check the logs for details.")
            return False
            
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        print(f"❌ An error occurred: {e}")
        return False

def run_demo():
    """Run a demo version without sending emails."""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Running Daily Vocabulary Bot in demo mode...")
        
        # Validate configuration
        if not validate_configuration():
            return False
        
        # Initialize components
        database = Database(Config.DATABASE_PATH)
        word_fetcher = WordFetcher()
        
        # Get new words
        words = get_new_words(word_fetcher, database, Config.WORDS_PER_DAY)
        
        if not words:
            print("⚠️ No new words available for demo")
            return False
        
        # Display words (don't send email)
        print(f"\n🎭 Demo Mode - Found {len(words)} new words:")
        print("=" * 50)
        
        for i, word_data in enumerate(words, 1):
            print(f"\n🔤 Word {i}: {word_data['word'].title()}")
            print(f"📖 Meaning: {word_data['meaning']}")
            
            if word_data.get('part_of_speech'):
                print(f"🏷️ Part of Speech: {word_data['part_of_speech']}")
            
            print(f"💬 Example: {word_data.get('example', 'No example available')}")
        
        print("\n✅ Demo completed successfully!")
        print("💡 Run 'python main.py' to send the actual email")
        return True
        
    except Exception as e:
        logger.error(f"Error in demo mode: {e}")
        print(f"❌ Demo error: {e}")
        return False

if __name__ == "__main__":
    # Setup logging
    setup_logging()
    
    print("🚀 Daily Vocabulary Bot")
    print("=" * 30)
    
    success = main()
    
    if success:
        print("\n🎉 Bot completed successfully!")
    else:
        print("\n💥 Bot encountered an error. Check the logs for details.")
        sys.exit(1)
