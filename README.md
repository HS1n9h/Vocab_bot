# 🚀 Daily Vocabulary Bot

A professional Python application that automatically sends new English vocabulary words to your email every day. Built with clean architecture, proper error handling, and production-ready code.

## ✨ Features

- **📚 Smart Word Selection**: Fetches words from Dictionary API with intelligent fallback
- **📧 Multiple Email Services**: Support for Gmail SMTP and SendGrid
- **🗄️ Persistent Storage**: SQLite database to track sent words and prevent repetition
- **⏰ Automated Scheduling**: Built-in scheduler for daily execution
- **🎭 Demo Mode**: Test functionality without sending actual emails
- **📝 Comprehensive Logging**: Detailed logging for monitoring and debugging
- **🔧 Configuration Management**: Environment-based configuration with validation

## 🏗️ Architecture

```
daily_vocab_bot/
├── main.py              # Main application entry point
├── config.py            # Configuration management
├── word_fetcher.py      # Word retrieval and API handling
├── database.py          # Database operations and word tracking
├── emailer.py           # Email service management
├── scheduler.py         # Task scheduling and automation
├── requirements.txt     # Python dependencies
├── .env.template        # Environment configuration template
└── README.md           # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.7 or higher
- Gmail account with 2-Factor Authentication enabled
- Gmail App Password (16 characters)

### 2. Installation

```bash
# Clone or download the project
cd daily_vocab_bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.template .env

# Edit .env file with your credentials
# Windows: notepad .env
# macOS/Linux: nano .env
```

**Required Configuration:**
```bash
RECIPIENT_EMAIL=your.email@gmail.com
GMAIL_USER=your.email@gmail.com
GMAIL_APP_PASSWORD=your-16-character-app-password
```

### 4. Test Configuration

```bash
# Validate your configuration
python config.py
```

### 5. Run the Bot

```bash
# Send vocabulary email immediately
python main.py

# Run in demo mode (no emails sent)
python -c "from main import run_demo; run_demo()"

# Start automated daily scheduler
python scheduler.py
```

## 📧 Email Setup

### Gmail Configuration

1. **Enable 2-Factor Authentication**
   - Go to [Google Account Settings](https://myaccount.google.com/)
   - Security → 2-Step Verification → Turn ON

2. **Generate App Password**
   - Security → 2-Step Verification → App passwords
   - Select "Mail" → Generate
   - Copy the 16-character password

3. **Configure .env File**
   ```bash
   GMAIL_USER=your.email@gmail.com
   GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
   ```

### SendGrid Alternative

```bash
# Install SendGrid package
pip install sendgrid

# Configure .env file
SENDGRID_API_KEY=your-sendgrid-api-key
```

## 🎯 Usage Examples

### Manual Execution

```bash
# Send vocabulary words now
python main.py

# Check configuration status
python config.py

# View database information
python -c "from database import Database; db = Database('vocabulary.db'); print(db.get_database_info())"
```

### Automated Scheduling

```bash
# Start daily scheduler (runs at 09:00 by default)
python scheduler.py

# Customize schedule time in .env
SCHEDULE_TIME=18:00  # Run at 6:00 PM
```

### Demo and Testing

```bash
# Test word fetching
python -c "from word_fetcher import WordFetcher; wf = WordFetcher(); print(wf.get_new_words(2))"

# Test database operations
python -c "from database import Database; db = Database('vocabulary.db'); print(db.get_word_count())"

# Run full demo
python -c "from main import run_demo; run_demo()"

# Launch web interface for easy configuration
python run_web.py
# Then open http://localhost:5000 in your browser

## ⚙️ Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `RECIPIENT_EMAIL` | Required | Your email address |
| `GMAIL_USER` | Required | Gmail account for sending |
| `GMAIL_APP_PASSWORD` | Required | Gmail app password |
| `SENDGRID_API_KEY` | Optional | SendGrid API key |
| `WORDS_PER_DAY` | 2 | Number of words to send daily |
| `SCHEDULE_TIME` | 09:00 | Daily execution time (HH:MM) |
| `DATABASE_PATH` | vocabulary.db | SQLite database file |
| `LOG_LEVEL` | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `LOG_FILE` | vocabulary_bot.log | Log file path |

## 🔍 Troubleshooting

### Common Issues

1. **Gmail Authentication Failed**
   - Ensure 2FA is enabled
   - Use App Password, not regular password
   - Check App Password is exactly 16 characters

2. **No Words Available**
   - Bot may have sent all available words
   - Check database: `python -c "from database import Database; db = Database('vocabulary.db'); print(db.get_word_count())"`

3. **API Connection Issues**
   - Dictionary API may be temporarily unavailable
   - Bot will use fallback word list automatically

4. **Configuration Errors**
   - Run `python config.py` to see validation errors
   - Check .env file format and values

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python main.py

# Check log files
tail -f vocabulary_bot.log
```

## 📊 Database Management

```bash
# View database statistics
python -c "from database import Database; db = Database('vocabulary.db'); info = db.get_database_info(); [print(f'{k}: {v}') for k, v in info.items()]"

# Reset database (removes all words)
python -c "from database import Database; db = Database('vocabulary.db'); db.reset_database()"

# Clean up old words (keep last 365 days)
python -c "from database import Database; db = Database('vocabulary.db'); db.cleanup_old_words(365)"
```

## 🚀 Deployment

### Local Development

```bash
# Development mode with debug logging
export LOG_LEVEL=DEBUG
python main.py
```

### Production Deployment

```bash
# Production mode
export LOG_LEVEL=INFO
export SCHEDULE_TIME=09:00

# Start scheduler as service
nohup python scheduler.py > scheduler.log 2>&1 &
```

### Docker (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "scheduler.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

- **Issues**: Check the troubleshooting section above
- **Configuration**: Run `python config.py` for validation
- **Logs**: Check `vocabulary_bot.log` for detailed error information

---

**🎉 Happy vocabulary building!** 📚✨
