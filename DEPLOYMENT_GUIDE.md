# 🚀 **24/7 Email Bot Deployment Guide**

## 🌐 **Option 1: Render (Recommended - Free)**

### **Step 1: Prepare Your Code**
1. Make sure all files are committed to Git
2. Ensure `requirements.txt` and `Procfile` are in your project root

### **Step 2: Deploy to Render**
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `daily-vocab-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn web_interface:app`
   - **Plan**: Free

### **Step 3: Set Environment Variables**
In Render dashboard, go to Environment → Environment Variables:
```
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient@example.com
```

### **Step 4: Deploy**
Click "Create Web Service" and wait for deployment.

---

## ☁️ **Option 2: Railway (Free Tier)**

### **Step 1: Deploy to Railway**
1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Choose "Deploy from GitHub repo"
4. Select your repository

### **Step 2: Configure**
- Railway will auto-detect Python
- Add environment variables in Variables tab
- Deploy automatically

---

## 🐳 **Option 3: Docker Deployment**

### **Create Dockerfile:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "web_interface:app", "--bind", "0.0.0.0:5000"]
```

---

## 🔧 **Option 4: VPS Setup**

### **Requirements:**
- VPS with Ubuntu 20.04+
- Domain name (optional)
- SSH access

### **Setup Commands:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# Clone your repository
git clone <your-repo-url>
cd daily_vocab_bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create systemd service
sudo nano /etc/systemd/system/vocab-bot.service
```

### **Systemd Service File:**
```ini
[Unit]
Description=Daily Vocabulary Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/daily_vocab_bot
Environment=PATH=/home/ubuntu/daily_vocab_bot/venv/bin
ExecStart=/home/ubuntu/daily_vocab_bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

## 📱 **Option 5: Raspberry Pi (Home Server)**

### **Requirements:**
- Raspberry Pi 4 (2GB+ RAM)
- MicroSD card (32GB+)
- Power supply
- Internet connection

### **Setup:**
1. Install Raspberry Pi OS
2. Enable SSH
3. Install Python and dependencies
4. Clone your repository
5. Set up cron jobs for scheduling

---

## ⚠️ **Important Notes:**

### **Environment Variables:**
Make sure these are set in your cloud platform:
- `GMAIL_ADDRESS`
- `GMAIL_PASSWORD` (App Password)
- `RECIPIENT_EMAIL`
- `DATABASE_URL` (if using external database)

### **Database Considerations:**
- SQLite works for small deployments
- For production, consider PostgreSQL or MySQL
- Cloud databases: Supabase (free), PlanetScale, AWS RDS

### **Monitoring:**
- Set up health checks
- Monitor logs
- Set up alerts for failures

---

## 🎯 **Recommended Path:**

1. **Start with Render** (free, easy)
2. **Test thoroughly** for a few days
3. **Move to VPS** if you need more control
4. **Scale up** as needed

---

## 🔗 **Quick Deploy Links:**
- [Render](https://render.com)
- [Railway](https://railway.app)
- [Heroku](https://heroku.com)
- [DigitalOcean](https://digitalocean.com)

---

## 📞 **Need Help?**
- Check platform documentation
- Monitor application logs
- Test locally before deploying
- Use health check endpoints
