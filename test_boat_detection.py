"""
Test Boat Detection with YOLO
Download sample boat images and test detection
"""

import cv2
import numpy as np
from ultralytics import YOLO
import urllib.request
import os

print("=" * 70)
print("BOAT DETECTION TEST")
print("=" * 70)

# Create test folder
os.makedirs("test_images", exist_ok=True)

# Sample boat image URLs (free stock images)
test_images = {
    "boat1": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800",  # Fishing boat
    "boat2": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800",  # Yacht
    "boat3": "https://images.unsplash.com/photo-1535024966711-7ca33ea49825?w=800",  # Ship
}

# Load YOLO model
print("\n[1/4] Loading YOLOv8 model...")
model = YOLO('yolov8n.pt')
print("[OK] Model loaded!")

# Test with each image
print("\n[2/4] Downloading test images...")
for name, url in test_images.items():
    try:
        filepath = f"test_images/{name}.jpg"
        if not os.path.exists(filepath):
            print(f"  - Downloading {name}...")
            urllib.request.urlretrieve(url, filepath)
        else:
            print(f"  - {name} already exists")
    except Exception as e:
        print(f"  [SKIP] Could not download {name}: {e}")

print("\n[3/4] Running boat detection...")
print("-" * 70)

detected_count = 0
confidence_threshold = 0.3

for filename in os.listdir("test_images"):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        filepath = f"test_images/{filename}"
        print(f"\nTesting: {filename}")

        try:
            # Read image
            img = cv2.imread(filepath)
            if img is None:
                print(f"  [ERROR] Could not read image")
                continue

            # Run detection
            results = model(img, verbose=False)

            # Check for boats
            boat_found = False
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    class_name = model.names[class_id]

                    if class_name.lower() == 'boat':
                        if confidence >= confidence_threshold:
                            print(f"  [DETECTED] Boat found! Confidence: {confidence*100:.1f}%")
                            boat_found = True
                            detected_count += 1
                        else:
                            print(f"  [LOW CONF] Boat detected but confidence too low: {confidence*100:.1f}%")

            if not boat_found:
                print(f"  [NOT FOUND] No boat detected")

                # Show what was detected instead
                all_detections = []
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        class_name = model.names[class_id]
                        all_detections.append(f"{class_name} ({confidence*100:.1f}%)")

                if all_detections:
                    print(f"  [INFO] Detected instead: {', '.join(all_detections[:3])}")
                else:
                    print(f"  [INFO] No objects detected at all")

        except Exception as e:
            print(f"  [ERROR] Detection failed: {e}")

print("\n" + "=" * 70)
print(f"[4/4] RESULTS: {detected_count} boats detected successfully")
print("=" * 70)

print("\n[NOTES]")
print("- YOLOv8 COCO can only detect generic 'boat' class")
print("- It cannot distinguish between ship/yacht/sailboat/speedboat")
print("- Detection works even if boat is partially visible")
print("- Confidence threshold: 30% (lowered from 50%)")
print("- For better marine vessel detection, use specialized YOLO models")

print("\n[RECOMMENDATION]")
print("If detection is poor, consider:")
print("1. Use higher quality images from ESP32 (SVGA 800x600)")
print("2. Download YOLOv8 model fine-tuned on ships/boats")
print("3. Train custom YOLO on your specific boat types")
print("4. Use web upload with high-quality phone camera")
