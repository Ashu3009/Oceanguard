# 🔐 Environment Variables Setup

## 📁 Files

### `.env` (Secret - Never Commit!)
- Contains actual passwords and secrets
- Already in `.gitignore`
- **NEVER push to GitHub!**
- Keep this safe and private

### `.env.example` (Template - Safe to Commit)
- Template file for others
- Shows what variables are needed
- Can be pushed to GitHub
- No actual secrets

---

## 🚀 Quick Setup

### **For You (Project Owner):**

Already done! ✅
- `.env` file created with your actual credentials
- All sensitive data stored securely
- File is ignored by Git

### **For Others (Cloning Your Repo):**

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/oceanguard.git
cd oceanguard

# 2. Copy template to .env
cp .env.example .env

# 3. Edit .env with actual values
notepad .env  # Windows
# OR
nano .env     # Linux/Mac

# 4. Update credentials:
# - WIFI_SSID
# - WIFI_PASSWORD
# - SECRET_KEY
# - ADMIN_PASSWORD
# - SERVER_IP
```

---

## 📋 Environment Variables Explained

### **Django Core**
```env
SECRET_KEY=your-secret-key
# Used for cryptographic signing
# MUST be unique and secret in production

DEBUG=True
# Development: True
# Production: False (IMPORTANT!)

ALLOWED_HOSTS=*
# Development: * (allow all)
# Production: your-domain.com
```

### **WiFi (ESP32)**
```env
WIFI_SSID=Your-WiFi-Name
WIFI_PASSWORD=Your-WiFi-Password
# ESP32-CAM needs these to connect
# Update ESP32 code with these values
```

### **Admin Credentials**
```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
# For Django admin panel
# Change password for production!
```

### **Server Config**
```env
SERVER_IP=192.168.0.177
SERVER_PORT=8000
# Your PC's local IP address
# ESP32 connects to this
# Find using: ipconfig (Windows) or ifconfig (Linux)
```

### **ML Settings**
```env
ML_BOAT_DETECTION_ENABLED=True
ML_CONFIDENCE_THRESHOLD=0.5
# Enable/disable ML detection
# Confidence: 0.0 to 1.0 (0.5 = 50%)
```

### **Camera GPS**
```env
CAMERA_LATITUDE=19.0760
CAMERA_LONGITUDE=72.8777
CAMERA_LOCATION_NAME=Mumbai Port
CAMERA_HEIGHT=10
# Your camera's installation location
# Height in meters
```

---

## 🔧 Using .env in Python (Optional)

If you want to use `.env` in `settings.py`:

### **1. Install python-dotenv**
```bash
pip install python-dotenv
```

### **2. Update settings.py**
```python
# At top of settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Use environment variables
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# ML Settings
ML_BOAT_DETECTION_ENABLED = os.getenv('ML_BOAT_DETECTION_ENABLED', 'True') == 'True'
ML_CONFIDENCE_THRESHOLD = float(os.getenv('ML_CONFIDENCE_THRESHOLD', '0.5'))
```

### **3. Update requirements.txt**
```
python-dotenv==1.0.0
```

---

## 🔒 Security Best Practices

### ✅ DO:
- Keep `.env` file secret
- Use different passwords for dev/production
- Change default admin password
- Use strong SECRET_KEY in production
- Set DEBUG=False in production
- Limit ALLOWED_HOSTS in production

### ❌ DON'T:
- Never commit `.env` to Git
- Never share `.env` file publicly
- Never use same passwords everywhere
- Never deploy with DEBUG=True
- Never use default SECRET_KEY in production

---

## 📊 Current Configuration

Your `.env` contains:
```
✅ Django SECRET_KEY (for development)
✅ WiFi credentials (The Student Scoop)
✅ Admin credentials (admin/admin123)
✅ Server IP (192.168.0.177)
✅ ML settings (enabled, 50% threshold)
✅ Camera GPS (Mumbai Port example)
```

---

## 🔄 Updating Values

### **When WiFi Changes:**
```env
# Update in .env
WIFI_SSID=New-WiFi-Name
WIFI_PASSWORD=New-Password

# Update in ESP32 code too!
# esp32_camera_optimized.ino
const char* ssid = "New-WiFi-Name";
const char* password = "New-Password";
```

### **When IP Changes:**
```env
# 1. Find new IP
ipconfig  # Windows

# 2. Update .env
SERVER_IP=192.168.0.XXX

# 3. Update ESP32 code
String serverURL = "http://192.168.0.XXX:8000/upload-image/";

# 4. Restart Django server
python manage.py runserver 0.0.0.0:8000
```

---

## 🎯 Quick Reference

| Variable | Current Value | Where Used |
|----------|---------------|------------|
| WIFI_SSID | The Student Scoop | ESP32 code |
| WIFI_PASSWORD | TSS@2023 | ESP32 code |
| SERVER_IP | 192.168.0.177 | ESP32 code |
| ADMIN_USERNAME | admin | Django admin |
| ADMIN_PASSWORD | admin123 | Django admin |
| SECRET_KEY | (long string) | Django security |

---

## 🆘 Troubleshooting

### **ESP32 can't connect?**
```
1. Check WIFI_SSID matches exactly
2. Check WIFI_PASSWORD is correct
3. Check SERVER_IP is up to date
4. Update ESP32 code with new values
```

### **Admin login failed?**
```
1. Check ADMIN_USERNAME
2. Check ADMIN_PASSWORD
3. Or create new superuser:
   python manage.py createsuperuser
```

### **.env not loading?**
```
1. File must be named exactly ".env"
2. Must be in project root folder
3. Install: pip install python-dotenv
4. Restart server after changes
```

---

**🔐 Keep .env Safe - Never Commit to Git!**
