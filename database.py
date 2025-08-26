#!/usr/bin/env python3
"""
Database management for Daily Vocabulary Bot.
Handles SQLite operations for tracking sent words and managing vocabulary data.
"""

import sqlite3
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class Database:
    """SQLite database manager for vocabulary tracking."""
    
    def __init__(self, db_path: str):
        """Initialize database connection."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables if they don't exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create words table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS words (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        word TEXT UNIQUE NOT NULL,
                        meaning TEXT NOT NULL,
                        part_of_speech TEXT,
                        example TEXT,
                        sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create settings table for bot configuration
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS settings (
                        key TEXT PRIMARY KEY,
                        value TEXT NOT NULL,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create indexes for better performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_word ON words(word)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_sent_date ON words(sent_date)")
                
                conn.commit()
                logger.info(f"Database initialized: {self.db_path}")
                
        except sqlite3.Error as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    def is_word_sent(self, word: str) -> bool:
        """Check if a word has already been sent."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM words WHERE word = ?", (word.lower(),))
                return cursor.fetchone() is not None
                
        except sqlite3.Error as e:
            logger.error(f"Error checking word status: {e}")
            return False
    
    def mark_word_sent(self, word: str, meaning: str, part_of_speech: str = None, 
                       example: str = None) -> bool:
        """Mark a word as sent and store its details."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO words (word, meaning, part_of_speech, example)
                    VALUES (?, ?, ?, ?)
                """, (word.lower(), meaning, part_of_speech, example))
                conn.commit()
                
                logger.info(f"Word marked as sent: {word}")
                return True
                
        except sqlite3.IntegrityError:
            logger.warning(f"Word already exists in database: {word}")
            return False
        except sqlite3.Error as e:
            logger.error(f"Error marking word as sent: {e}")
            return False
    
    def get_total_words_sent(self) -> int:
        """Get total count of words sent so far."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM words")
                result = cursor.fetchone()
                return result[0] if result else 0
                
        except sqlite3.Error as e:
            logger.error(f"Error getting total words count: {e}")
            return 0
    
    def get_words_sent_today(self) -> int:
        """Get count of words sent today."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COUNT(*) FROM words 
                    WHERE DATE(sent_date) = DATE('now')
                """)
                result = cursor.fetchone()
                return result[0] if result else 0
                
        except sqlite3.Error as e:
            logger.error(f"Error getting today's words count: {e}")
            return 0
    
    def get_sent_words(self, limit: int = 100) -> List[Dict]:
        """Get recently sent words."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT word, meaning, part_of_speech, example, sent_date
                    FROM words
                    ORDER BY sent_date DESC
                    LIMIT ?
                """, (limit,))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except sqlite3.Error as e:
            logger.error(f"Error retrieving sent words: {e}")
            return []
    
    def get_word_count(self) -> int:
        """Get total number of words in database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM words")
                return cursor.fetchone()[0]
                
        except sqlite3.Error as e:
            logger.error(f"Error getting word count: {e}")
            return 0
    
    def get_database_info(self) -> Dict:
        """Get database statistics and information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get total word count
                cursor.execute("SELECT COUNT(*) FROM words")
                total_words = cursor.fetchone()[0]
                
                # Get words sent today
                cursor.execute("""
                    SELECT COUNT(*) FROM words 
                    WHERE DATE(sent_date) = DATE('now')
                """)
                words_today = cursor.fetchone()[0]
                
                # Get first and last sent dates
                cursor.execute("""
                    SELECT MIN(sent_date), MAX(sent_date) FROM words
                """)
                date_range = cursor.fetchone()
                first_date = date_range[0] if date_range[0] else None
                last_date = date_range[1] if date_range[1] else None
                
                return {
                    'total_words': total_words,
                    'words_today': words_today,
                    'first_sent_date': first_date,
                    'last_sent_date': last_date,
                    'database_path': str(self.db_path),
                    'database_size': self.db_path.stat().st_size if self.db_path.exists() else 0
                }
                
        except sqlite3.Error as e:
            logger.error(f"Error getting database info: {e}")
            return {}
    
    def cleanup_old_words(self, days_to_keep: int = 365) -> int:
        """Remove words older than specified days (optional maintenance)."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM words 
                    WHERE sent_date < DATE('now', '-{} days')
                """.format(days_to_keep))
                
                deleted_count = cursor.rowcount
                conn.commit()
                
                if deleted_count > 0:
                    logger.info(f"Cleaned up {deleted_count} old words")
                
                return deleted_count
                
        except sqlite3.Error as e:
            logger.error(f"Error cleaning up old words: {e}")
            return 0
    
    def reset_database(self) -> bool:
        """Reset database by removing all words (use with caution)."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM words")
                conn.commit()
                
                logger.warning("Database reset - all words removed")
                return True
                
        except sqlite3.Error as e:
            logger.error(f"Error resetting database: {e}")
            return False
