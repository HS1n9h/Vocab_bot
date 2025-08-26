#!/usr/bin/env python3
"""
Email service module for Daily Vocabulary Bot.
Handles sending emails via Gmail SMTP or SendGrid API.
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, List
from config import Config

logger = logging.getLogger(__name__)

class Emailer:
    """Handles email sending via multiple services."""
    
    def __init__(self):
        """Initialize the emailer with configuration."""
        self.recipient_email = Config.RECIPIENT_EMAIL
        self.gmail_user = Config.GMAIL_USER
        self.gmail_password = Config.GMAIL_APP_PASSWORD
        self.sendgrid_api_key = Config.SENDGRID_API_KEY
        self.bot_name = Config.BOT_NAME
        self.subject_prefix = Config.EMAIL_SUBJECT_PREFIX
        
        # Email service configuration
        self.gmail_smtp_server = 'smtp.gmail.com'
        self.gmail_smtp_port = 587
        
    def send_email(self, subject: str, body: str, html_body: Optional[str] = None) -> bool:
        """Send email using the configured service."""
        try:
            email_service = Config.get_email_service()
            
            if email_service == 'gmail':
                return self._send_via_gmail(subject, body, html_body)
            elif email_service == 'sendgrid':
                return self._send_via_sendgrid(subject, body, html_body)
            else:
                logger.error("No email service configured")
                return False
                
        except Exception as e:
            logger.error(f"Email sending failed: {e}")
            return False
    
    def _send_via_gmail(self, subject: str, body: str, html_body: Optional[str] = None) -> bool:
        """Send email via Gmail SMTP."""
        try:
            if not all([self.gmail_user, self.gmail_password, self.recipient_email]):
                logger.error("Gmail configuration incomplete")
                return False
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.bot_name} <{self.gmail_user}>"
            msg['To'] = self.recipient_email
            msg['Subject'] = subject
            
            # Add text and HTML parts
            text_part = MIMEText(body, 'plain', 'utf-8')
            msg.attach(text_part)
            
            if html_body:
                html_part = MIMEText(html_body, 'html', 'utf-8')
                msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.gmail_smtp_server, self.gmail_smtp_port) as server:
                server.starttls()
                server.login(self.gmail_user, self.gmail_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully via Gmail to {self.recipient_email}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            logger.error("Gmail authentication failed. Check your app password.")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"Gmail SMTP error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending via Gmail: {e}")
            return False
    
    def _send_via_sendgrid(self, subject: str, body: str, html_body: Optional[str] = None) -> bool:
        """Send email via SendGrid API."""
        try:
            if not self.sendgrid_api_key:
                logger.error("SendGrid API key not configured")
                return False
            
            # Import SendGrid here to avoid dependency issues
            try:
                from sendgrid import SendGridAPIClient
                from sendgrid.helpers.mail import Mail
            except ImportError:
                logger.error("SendGrid package not installed. Run: pip install sendgrid")
                return False
            
            # Create message
            message = Mail(
                from_email=self.gmail_user or 'noreply@vocabularybot.com',
                to_emails=self.recipient_email,
                subject=subject,
                plain_text_content=body
            )
            
            if html_body:
                message.content = html_body
            
            # Send email
            sg = SendGridAPIClient(api_key=self.sendgrid_api_key)
            response = sg.send(message)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Email sent successfully via SendGrid to {self.recipient_email}")
                return True
            else:
                logger.error(f"SendGrid API error: {response.status_code} - {response.body}")
                return False
                
        except Exception as e:
            logger.error(f"SendGrid sending failed: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Test email service connection."""
        try:
            email_service = Config.get_email_service()
            
            if email_service == 'gmail':
                return self._test_gmail_connection()
            elif email_service == 'sendgrid':
                return self._test_sendgrid_connection()
            else:
                logger.warning("No email service configured for testing")
                return False
                
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def _test_gmail_connection(self) -> bool:
        """Test Gmail SMTP connection."""
        try:
            if not all([self.gmail_user, self.gmail_password]):
                logger.warning("Gmail credentials not configured")
                return False
            
            with smtplib.SMTP(self.gmail_smtp_server, self.gmail_smtp_port) as server:
                server.starttls()
                server.login(self.gmail_user, self.gmail_password)
                logger.info("Gmail connection test successful")
                return True
                
        except smtplib.SMTPAuthenticationError:
            logger.error("Gmail authentication failed")
            return False
        except Exception as e:
            logger.error(f"Gmail connection test failed: {e}")
            return False
    
    def _test_sendgrid_connection(self) -> bool:
        """Test SendGrid API connection."""
        try:
            if not self.sendgrid_api_key:
                logger.warning("SendGrid API key not configured")
                return False
            
            # Import SendGrid here to avoid dependency issues
            try:
                from sendgrid import SendGridAPIClient
            except ImportError:
                logger.error("SendGrid package not installed")
                return False
            
            sg = SendGridAPIClient(api_key=self.sendgrid_api_key)
            # Make a simple API call to test connection
            response = sg.client.api_keys.get()
            
            if response.status_code == 200:
                logger.info("SendGrid connection test successful")
                return True
            else:
                logger.error(f"SendGrid API test failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"SendGrid connection test failed: {e}")
            return False
    
    def format_vocabulary_email(self, words: List[Dict], date: Optional[str] = None) -> Dict[str, str]:
        """Format vocabulary words into email content."""
        if not date:
            from datetime import datetime
            date = datetime.now().strftime('%B %d, %Y')
        
        # Plain text version - more natural and professional
        text_body = f"Hello,\n\nHere are your vocabulary words for {date}:\n\n"
        
        for i, word_data in enumerate(words, 1):
            text_body += f"{i}. {word_data['word'].title()}\n"
            text_body += f"   Definition: {word_data['meaning']}\n"
            if word_data.get('part_of_speech'):
                text_body += f"   Part of Speech: {word_data['part_of_speech']}\n"
            text_body += f"   Example: {word_data.get('example', 'No example available')}\n\n"
        
        text_body += "Best regards,\nYour Vocabulary Assistant"
        
        # HTML version - clean and professional
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #2c3e50; background-color: #f8f9fa; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #3498db; }}
                .header h1 {{ color: #2c3e50; font-size: 28px; margin-bottom: 10px; font-weight: 300; }}
                .header p {{ color: #7f8c8d; font-size: 16px; margin: 0; }}
                .word-card {{ background-color: #ffffff; border: 1px solid #ecf0f1; border-radius: 8px; padding: 25px; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }}
                .word-title {{ color: #3498db; font-size: 22px; font-weight: 600; margin-bottom: 15px; border-bottom: 1px solid #ecf0f1; padding-bottom: 10px; }}
                .definition {{ font-size: 16px; margin-bottom: 12px; color: #2c3e50; }}
                .part-of-speech {{ color: #7f8c8d; font-size: 14px; margin-bottom: 12px; font-style: italic; }}
                .example {{ background-color: #f8f9fa; padding: 15px; border-radius: 6px; font-style: italic; color: #34495e; border-left: 4px solid #3498db; }}
                .footer {{ text-align: center; margin-top: 35px; padding-top: 20px; border-top: 1px solid #ecf0f1; color: #7f8c8d; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Daily Vocabulary</h1>
                    <p>Your vocabulary words for {date}</p>
                </div>
        """
        
        for i, word_data in enumerate(words, 1):
            html_body += f"""
                <div class="word-card">
                    <div class="word-title">{i}. {word_data['word'].title()}</div>
                    <div class="definition"><strong>Definition:</strong> {word_data['meaning']}</div>
            """
            
            if word_data.get('part_of_speech'):
                html_body += f'<div class="part-of-speech"><strong>Part of Speech:</strong> {word_data["part_of_speech"]}</div>'
            
            html_body += f"""
                    <div class="example"><strong>Example:</strong> {word_data.get('example', 'No example available')}</div>
                </div>
            """
        
        html_body += """
                <div class="footer">
                    <p>Best regards,<br>Your Vocabulary Assistant</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return {
            'text': text_body,
            'html': html_body
        }
