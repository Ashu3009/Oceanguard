# -*- coding: utf-8 -*-
"""QR Scanner Test with OpenCV (Windows-friendly)"""

print("Testing QR Code Scanner with OpenCV...")
print("-" * 50)

# Test 1: Import
print("\nStep 1: Checking OpenCV...")
try:
    import cv2
    print("[OK] OpenCV imported!")
except Exception as e:
    print(f"[FAIL] {e}")
    exit(1)

# Test 2: Find QR image
print("\nStep 2: Looking for QR codes...")
import os
test_image = None
if os.path.exists("qr_codes/TEST-BOAT-999.png"):
    test_image = "qr_codes/TEST-BOAT-999.png"
elif os.path.exists("qr_codes/OCEAN-BOAT-001.png"):
    test_image = "qr_codes/OCEAN-BOAT-001.png"

if not test_image:
    print("[FAIL] No QR images found")
    print("\nFix: python generate_qr.py")
    exit(1)

print(f"[OK] Found: {test_image}")

# Test 3: Scan with OpenCV
print(f"\nStep 3: Scanning QR code with OpenCV...")
try:
    # Load image
    img = cv2.imread(test_image)

    # Initialize QR code detector
    detector = cv2.QRCodeDetector()

    # Detect and decode
    data, bbox, straight_qrcode = detector.detectAndDecode(img)

    if data:
        print(f"[SUCCESS] QR Detected: {data}")
        print("\n*** QR SCANNER IS WORKING with OpenCV! ***")
    else:
        print("[FAIL] No QR detected")
        print("QR might be too small or image quality low")

except Exception as e:
    print(f"[FAIL] Error: {e}")

print("\n" + "="*50)
