# 🌊 OceanGuard - Maritime Security System

Simple QR-based boat monitoring system for ports and harbors.

---

## 🎯 How It Works

```
Boat enters port with QR code box
    ↓
ESP32-CAM auto-captures image (every 8 seconds)
    ↓
Django server receives image
    ↓
ML Boat Detection (YOLO)
    ↓
    ├─ NOT a boat → DELETE (birds, waves, debris filtered)
    └─ IS a boat → Continue to QR Scan
        ↓
        QR Code Scanning
        ↓
        ├─ QR Found + Registered → PENDING (Manual review)
        ├─ QR Found + NOT Registered → WARNING (Auto-alert)
        └─ No QR Found → WARNING (Unregistered vessel)
        ↓
Coast Guard reviews on dashboard
```

---

## 📦 Quick Setup

### 1. Install Dependencies
```bash
# Install all dependencies from requirements.txt
pip install -r requirements.txt

# OR install manually:
pip install django pillow pyzbar ultralytics opencv-python torch torchvision
```

**Note:** ML libraries (torch, ultralytics) are optional. System will work without them but won't filter non-boat images.

### 2. Setup Database
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 3. Register Boats
```bash
python manage.py shell
```

```python
from camera.models import RegisteredBoat

RegisteredBoat.objects.create(
    boat_id="BOAT-001",
    boat_name="Sea Explorer",
    owner_name="John Doe",
    registration_number="MH-2024-001",
    qr_code="BOAT-001"
)
```

### 4. Start Server
```bash
python manage.py runserver 0.0.0.0:8000
```

### 5. Access Dashboard
- All Captures: http://localhost:8000/gallery/
- Approved: http://localhost:8000/approved/
- Warnings: http://localhost:8000/warnings/

---

## 🚢 QR Code Box for Boats

### Box Design
```
Size: 20cm x 20cm x 10cm
Material: Waterproof plastic
QR Placement: All 4 sides + top (360° visibility)
Mounting: Secure to boat deck/roof
```

### Generate QR Code
```python
import qrcode

qr = qrcode.QRCode(version=5, box_size=10, border=4)
qr.add_data("BOAT-001")
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("BOAT-001.png")
```

**Print:** 15cm x 15cm on waterproof sticker paper
**Install:** On highest visible point of boat

---

## 📸 ESP32-CAM Setup

### Hardware
- Board: AI Thinker ESP32-CAM
- Power: 5V/2A
- WiFi: 2.4GHz network

### Arduino Code
```cpp
const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASSWORD";
const char* serverName = "http://192.168.0.64:8000/upload-image/";
```

Update `YOUR_WIFI`, `YOUR_PASSWORD`, and IP address.

---

## 🎮 Dashboard Usage

### Review Captures
1. **Pending** - New captures awaiting review
   - Click ✓ OK to approve
   - Click ⚠ WARNING to flag

2. **Approved** - Safe vessels cleared for entry

3. **Warnings** - Suspicious/Unregistered vessels
   - No QR detected
   - Unregistered QR codes

### Delete Captures
- Click ✕ button on any card to delete

---

## 🔍 System Logic

### Status Determination (with ML)
```python
# STEP 1: ML Boat Detection
if NOT_A_BOAT:
    DELETE_IMAGE  # Don't save to database

# STEP 2: QR Scanning (only if boat detected)
if QR_DETECTED:
    if QR_IN_DATABASE:
        status = "PENDING"  # Manual review
    else:
        status = "WARNING"  # Unregistered QR
else:
    status = "WARNING"  # No QR found
```

### Why Warnings?
- **No QR:** Boat must have QR box installed
- **Unregistered QR:** Not in authorized database
- **Coast Guard reviews all warnings manually**

### ML Boat Detection
- **Filters out:** Birds, waves, debris, empty frames
- **Detects:** Boats, ships, sailboats, speedboats, vessels
- **Confidence:** 50% threshold (configurable in settings.py)
- **Model:** YOLOv8 Nano (fast, lightweight)
- **Fallback:** If ML disabled/unavailable, all images are processed

---

## 📊 Features

✅ **ML Boat Detection** - YOLO-based filtering (birds, waves, debris ignored)
✅ **QR Code Scanning** - Automatic boat identification
✅ **3 Gallery Pages** - Organized by status (All, Approved, Warnings)
✅ **Manual Review** - Coast Guard approval system
✅ **Auto Warnings** - Flags suspicious/unregistered vessels
✅ **Delete Function** - Remove false positives
✅ **Real-time Updates** - Auto-refresh every 10 seconds
✅ **Smart Filtering** - Only saves boat images, reduces storage waste

---

## 🎤 Presentation Q&A

### Q: What if QR code is damaged/dirty?
**A:** System marks as WARNING. Coast Guard manually verifies the boat through other means (registration documents, visual inspection).

### Q: Can boats fake QR codes?
**A:** Each QR is unique and registered in database. Fake/duplicate QRs are flagged as "Unregistered" → WARNING.

### Q: How to handle multiple cameras?
**A:** Each ESP32-CAM connects to same Django server. All images appear in single dashboard.

### Q: Night time operation?
**A:** Install spotlights near camera. QR codes work well with proper lighting.

### Q: What about GPS tracking?
**A:** Current system is QR-based (simple & effective). GPS tracking can be added later with hardware GPS modules on boats.

### Q: How many boats can the system handle?
**A:** Database supports unlimited boats. Django can handle 50+ images/second.

### Q: How does ML boat detection work?
**A:** Uses YOLOv8 (pre-trained on COCO dataset) to detect boats before QR scanning. Filters out birds, waves, debris - only saves actual boat images. Configurable confidence threshold (default 50%). If ML unavailable, system falls back to regular QR scanning.

### Q: What if ML model fails or is disabled?
**A:** System automatically falls back to regular QR scanning. All images are processed normally. ML is optional enhancement, not a requirement.

---

## 🔮 Future Upgrades

**Phase 1 (Completed):** ✅
- QR scanning
- Coast Guard dashboard (3 pages: All, Approved, Warnings)
- Auto warnings
- ML boat detection (YOLOv8)
- Smart image filtering

**Phase 2 (Planned):**
- Mobile app for Coast Guard
- SMS/Email alerts
- Night vision cameras
- Multi-camera network
- Real-time notifications

**Phase 3 (Advanced):**
- GPS tracking with hardware modules
- Boat movement tracking
- Speed analysis
- Government database integration
- Advanced analytics dashboard

---

## 🐛 Troubleshooting

### ESP32 can't connect?
- Check WiFi credentials
- Use 2.4GHz network (not 5GHz)
- Update server IP address

### QR not detected?
- Increase QR size (15cm minimum)
- Improve lighting
- Clean QR codes
- Print high-resolution (300 DPI+)

### Images not showing?
- Run server with `0.0.0.0:8000` (not 127.0.0.1)
- Check firewall settings
- Verify ESP32 IP matches server IP

### ML boat detection not working?
- Install required libraries: `pip install ultralytics opencv-python torch`
- First run downloads YOLOv8 model (~6MB) - needs internet
- Check console for ML detection logs
- Disable ML in settings.py if not needed: `ML_BOAT_DETECTION_ENABLED = False`

### Too many false rejections (boats not detected)?
- Lower confidence threshold in settings.py (default 0.5)
- Change to 0.3 for more sensitive detection
- Check boat is visible in frame (not too far away)

---

## 📄 Project Structure

```
oceanguard/
├── camera/
│   ├── models.py       # Database models
│   ├── views.py        # Core logic
│   ├── admin.py        # Admin panel
│   └── templates/
│       └── gallery.html    # Dashboard UI
├── oceanguard/
│   ├── settings.py     # Configuration
│   └── urls.py         # URL routing
├── media/
│   └── captures/       # Saved images
└── manage.py           # Django CLI
```

---

## ⚙️ Configuration (settings.py)

### ML Boat Detection Settings
```python
# Enable/Disable ML boat detection
ML_BOAT_DETECTION_ENABLED = True

# Confidence threshold (0.0 to 1.0)
ML_CONFIDENCE_THRESHOLD = 0.5  # 50% confidence

# Boat classes to detect (COCO dataset)
BOAT_CLASSES = ['boat', 'ship', 'sailboat', 'speedboat', 'vessel']
```

### Camera GPS Location
```python
CAMERA_GPS_LOCATION = {
    'latitude': 19.0760,   # Update with actual location
    'longitude': 72.8777,  # Update with actual location
    'location_name': 'Mumbai Port - Entry Gate',
    'installation_height': 10,  # meters
}
```

---

## 🌟 Key Advantages

1. **Simple Setup** - No complex hardware required
2. **Cost-Effective** - ESP32-CAM costs ~$10
3. **Scalable** - Add unlimited cameras
4. **Reliable** - QR codes work in all conditions
5. **Fast** - Instant image capture & processing
6. **Secure** - Database-backed authentication
7. **Smart Filtering** - ML removes false captures (birds, waves, debris)
8. **Storage Efficient** - Only boat images saved

---

**🌊 OceanGuard - Securing Maritime Borders, Simply.**

*Developed for port security and coastal surveillance*
