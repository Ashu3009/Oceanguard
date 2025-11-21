from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.utils import timezone
from django.conf import settings
from .models import BoatCapture, RegisteredBoat
import os
import glob
import time
# QR Code Scanner Libraries - OpenCV (Windows-friendly, no DLL issues)
try:
    import cv2
    import numpy as np
    QR_AVAILABLE = True
except ImportError:
    # OpenCV not available
    QR_AVAILABLE = False
# ML Boat Detection Libraries (Optional - graceful fallback if not available)
try:
    from ultralytics import YOLO
    import cv2
    import numpy as np
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
from math import radians, cos, sin, asin, sqrt
import datetime
import json
import io


# 🎨 Color Detection Function for RED and BLUE boats
def detect_colored_boat(img_data):
    """
    Detect RED or BLUE colored boats in image using HSV color space
    Returns: (detected, color, percentage)
    - detected: True if RED or BLUE boat found
    - color: 'RED' or 'BLUE' or None
    - percentage: percentage of image that is the detected color
    """
    if not QR_AVAILABLE:  # cv2 and numpy needed
        return False, None, 0.0

    try:
        # Convert bytes to numpy array
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return False, None, 0.0

        # Convert BGR to HSV (better for color detection)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Total pixels in image
        total_pixels = img.shape[0] * img.shape[1]

        # Get color ranges from settings
        color_ranges = settings.COLOR_RANGES
        min_threshold = settings.COLOR_DETECTION_MIN_THRESHOLD
        max_threshold = settings.COLOR_DETECTION_MAX_THRESHOLD

        detected_colors = []

        # Check each color
        for color_name, ranges in color_ranges.items():
            total_color_pixels = 0

            # Check all ranges for this color (RED has 2 ranges)
            for color_range in ranges:
                lower = np.array(color_range['lower'])
                upper = np.array(color_range['upper'])

                # Create mask for this color range
                mask = cv2.inRange(hsv, lower, upper)

                # Count colored pixels
                color_pixels = cv2.countNonZero(mask)
                total_color_pixels += color_pixels

            # Calculate percentage
            percentage = (total_color_pixels / total_pixels) * 100

            # Check if within valid range (not too small, not too big)
            if min_threshold <= percentage <= max_threshold:
                detected_colors.append({
                    'color': color_name,
                    'percentage': round(percentage, 2)
                })

        # Return highest percentage color
        if detected_colors:
            detected_colors.sort(key=lambda x: x['percentage'], reverse=True)
            best = detected_colors[0]
            return True, best['color'], best['percentage']

        return False, None, 0.0

    except Exception as e:
        print(f"❌ Color detection error: {str(e)}")
        return False, None, 0.0


# GPS Distance Calculator (Haversine Formula)
def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two GPS coordinates in kilometers
    """
    if not all([lat1, lon1, lat2, lon2]):
        return None
    
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Earth radius in kilometers
    r = 6371
    
    return c * r


# Live Monitoring Folder Cleanup
def cleanup_live_folder():
    """
    Delete images older than 5 minutes from live monitoring folder
    """
    try:
        live_folder = os.path.join(settings.MEDIA_ROOT, 'live_monitoring')
        if not os.path.exists(live_folder):
            return

        current_time = time.time()
        max_age = 5 * 60  # 5 minutes in seconds

        # Find all jpg files in live folder
        pattern = os.path.join(live_folder, '*.jpg')
        files = glob.glob(pattern)

        deleted_count = 0
        for file_path in files:
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > max_age:
                os.remove(file_path)
                deleted_count += 1

        if deleted_count > 0:
            print(f"🗑️ Cleaned up {deleted_count} old images from live monitoring folder")
    except Exception as e:
        print(f"⚠️ Cleanup error: {str(e)}")


def save_to_live_monitoring(image_data, filename):
    """
    Save image to live monitoring folder (5 min auto-delete)
    """
    try:
        # Create live monitoring folder
        live_folder = os.path.join(settings.MEDIA_ROOT, 'live_monitoring')
        os.makedirs(live_folder, exist_ok=True)

        # Save image
        file_path = os.path.join(live_folder, filename)
        with open(file_path, 'wb') as f:
            f.write(image_data)

        print(f"📁 Saved to live monitoring: {filename}")
    except Exception as e:
        print(f"⚠️ Live monitoring save error: {str(e)}")


# ML Boat Detection
def detect_boat(image_data):
    """
    Detect if image contains a boat using YOLO ML model
    Returns: (is_boat, confidence, detected_class)
    """
    if not ML_AVAILABLE or not settings.ML_BOAT_DETECTION_ENABLED:
        # If ML not available or disabled, assume it's a boat (fallback)
        return True, 1.0, "unknown"

    try:
        # Load YOLO model (using YOLOv8 pre-trained on COCO dataset)
        model = YOLO('yolov8n.pt')  # Nano model - fast and lightweight

        # Convert image data to numpy array
        image_array = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        # Run inference
        results = model(image, verbose=False)

        # Check detections
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get class name and confidence
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = model.names[class_id]

                # Check if it's a boat-related class
                if class_name.lower() in [c.lower() for c in settings.BOAT_CLASSES]:
                    if confidence >= settings.ML_CONFIDENCE_THRESHOLD:
                        print(f"🚢 Boat Detected: {class_name} ({confidence*100:.1f}% confidence)")
                        return True, confidence, class_name

        # No boat detected
        print("❌ No boat detected in image")
        return False, 0.0, None

    except Exception as e:
        print(f"⚠️ ML Detection Error: {str(e)}")
        # On error, assume it's a boat (fail-safe approach)
        return True, 0.0, "error"


# QR Code Validator with GPS Tracking
def validate_qr_with_gps(qr_data, latitude=None, longitude=None):
    """
    Validate QR code and check for cloning attempts using GPS
    Returns: (is_valid, is_suspicious, message, boat)
    """
    try:
        # Check if boat is registered
        boat = RegisteredBoat.objects.filter(qr_code=qr_data).first()

        if not boat:
            return False, True, "❌ Unregistered QR Code", None

        # Check if boat is blacklisted
        if boat.is_blacklisted:
            return False, True, "🚫 BLACKLISTED BOAT", boat

        # Get last scan log
        last_scan = boat.scan_logs.first()

        is_suspicious = False
        suspicion_reasons = []

        if last_scan and latitude and longitude:
            # Calculate time difference
            time_diff = (timezone.now() - last_scan.scanned_at).total_seconds() / 60  # minutes

            # Calculate distance
            distance = calculate_distance(
                last_scan.latitude, last_scan.longitude,
                latitude, longitude
            )

            if distance and time_diff > 0:
                # Calculate speed (km/h)
                speed = (distance / time_diff) * 60

                # Suspicious if speed > 100 km/h (boats don't go this fast!)
                if speed > 100:
                    is_suspicious = True
                    suspicion_reasons.append(
                        f"⚠️ Impossible speed: {speed:.1f} km/h (Distance: {distance:.1f}km in {time_diff:.1f} min)"
                    )

                # Suspicious if same QR used within 5 minutes
                if time_diff < 5:
                    is_suspicious = True
                    suspicion_reasons.append(
                        f"⚠️ Same QR used {time_diff:.1f} minutes ago at different location"
                    )

        message = " | ".join(suspicion_reasons) if is_suspicious else "✅ Valid QR Code"

        return True, is_suspicious, message, boat

    except Exception as e:
        return False, True, f"❌ Validation Error: {str(e)}", None


@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        img_data = request.body

        # Create filename
        filename = f"capture_{int(datetime.datetime.now().timestamp())}.jpg"

        # ============================================
        # STEP 0: LIVE MONITORING (5-min auto-delete)
        # ============================================
        cleanup_live_folder()  # Delete old images first
        save_to_live_monitoring(img_data, filename)  # Save new image

        # ============================================
        # STEP 1: SUSPICIOUS COLOR DETECTION
        # ============================================
        color_detected = False
        detected_color = None
        color_percentage = 0.0

        try:
            if settings.COLOR_DETECTION_ENABLED:
                print("🎨 Step 1: Checking for suspicious activity...")
                color_detected, detected_color, color_percentage = detect_colored_boat(img_data)

                if color_detected:
                    print(f"✅ Suspicious Color Found! ({color_percentage}% of image)")
                else:
                    print(f"❌ No suspicious activity detected - Rejecting image")
            else:
                print("⚠️ Color detection disabled in settings")
        except Exception as e:
            print(f"❌ Color Detection Error: {str(e)}")

        # ============================================
        # DECISION LOGIC: Suspicious Activity Detection
        # ============================================

        # Suspicious color detected → Save to database
        if color_detected:
            print(f"✅ SUSPICIOUS ACTIVITY DETECTED → Saving to database")

            # Save to database
            boat_capture = BoatCapture()
            boat_capture.image.save(filename, ContentFile(img_data), save=True)
            boat_capture.qr_detected = False
            boat_capture.qr_data = None
            boat_capture.qr_valid = False
            boat_capture.status = 'pending'
            boat_capture.notes = "Unidentified vessel detected - Security review required"
            boat_capture.save()

            print(f"✅ Image Saved: {boat_capture.id} - Suspicious Activity Detected - Status: PENDING")

            return JsonResponse({
                "status": "received",
                "id": boat_capture.id,
                "filename": filename,
                "suspicious_detected": True,
                "color_percentage": color_percentage
            })

        # No suspicious color → Reject
        else:
            print("❌ No suspicious activity detected → Image rejected")
            return JsonResponse({
                "status": "rejected",
                "reason": "no_suspicious_activity",
                "message": "No suspicious activity detected"
            })

    return JsonResponse({"error": "POST only"})


def gallery(request):
    # Get all boat captures from database, newest first
    captures = BoatCapture.objects.all().order_by('-captured_at')

    # Calculate stats
    total = captures.count()
    pending = captures.filter(status='pending').count()
    approved = captures.filter(status='approved').count()
    warnings = captures.filter(status='warning').count()

    return render(request, "gallery.html", {
        "captures": captures,
        "total": total,
        "pending": pending,
        "approved": approved,
        "warnings": warnings,
        "page_title": "All Captures",
        "current_page": "all"
    })


def update_status(request, capture_id):
    """Update the status of a boat capture (approve/warning)"""
    if request.method == 'POST':
        try:
            capture = BoatCapture.objects.get(id=capture_id)
            new_status = request.POST.get('status')

            if new_status in ['approved', 'warning', 'pending']:
                capture.status = new_status
                capture.save()
                print(f"✅ Updated capture #{capture_id} status to: {new_status}")
        except BoatCapture.DoesNotExist:
            print(f"❌ Capture #{capture_id} not found")
        except Exception as e:
            print(f"❌ Status update error: {str(e)}")

    return redirect('/gallery/')


def approved_gallery(request):
    # Only approved captures
    captures = BoatCapture.objects.filter(status='approved')

    # Calculate stats
    total = BoatCapture.objects.count()
    pending = BoatCapture.objects.filter(status='pending').count()
    approved = captures.count()
    warnings = BoatCapture.objects.filter(status='warning').count()

    return render(request, "gallery.html", {
        "captures": captures,
        "total": total,
        "pending": pending,
        "approved": approved,
        "warnings": warnings,
        "page_title": "Approved Boats",
        "current_page": "approved"
    })


def warning_gallery(request):
    # Only warning captures
    captures = BoatCapture.objects.filter(status='warning')

    # Calculate stats
    total = BoatCapture.objects.count()
    pending = BoatCapture.objects.filter(status='pending').count()
    approved = BoatCapture.objects.filter(status='approved').count()
    warnings = captures.count()

    return render(request, "gallery.html", {
        "captures": captures,
        "total": total,
        "pending": pending,
        "approved": approved,
        "warnings": warnings,
        "page_title": "Warning Boats",
        "current_page": "warnings"
    })


@csrf_exempt
def update_status(request, capture_id):
    if request.method == "POST":
        try:
            # Get the capture
            capture = BoatCapture.objects.get(id=capture_id)

            # Get data from request
            data = json.loads(request.body)
            new_status = data.get('status')
            reviewed_by = data.get('reviewed_by', 'Coast Guard')

            # Update status
            capture.status = new_status
            capture.reviewed_by = reviewed_by
            capture.reviewed_at = timezone.now()
            capture.save()

            print(f"✅ Status Updated: Capture #{capture_id} → {new_status}")

            return JsonResponse({
                "success": True,
                "message": f"Status updated to {new_status}"
            })

        except BoatCapture.DoesNotExist:
            return JsonResponse({
                "success": False,
                "error": "Capture not found"
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            })

    return JsonResponse({"error": "POST only"})


@csrf_exempt
def delete_capture(request, capture_id):
    if request.method == "POST":
        try:
            # Get the capture
            capture = BoatCapture.objects.get(id=capture_id)

            # Delete the image file from filesystem
            if capture.image:
                capture.image.delete(save=False)

            # Delete from database
            capture.delete()

            print(f"✅ Deleted: Capture #{capture_id}")

        except BoatCapture.DoesNotExist:
            print(f"❌ Capture #{capture_id} not found")
        except Exception as e:
            print(f"❌ Delete error: {str(e)}")

    return redirect('/gallery/')