# -*- coding: utf-8 -*-
"""Quick QR Scanner Test"""

print("Testing QR Code Scanner...")
print("-" * 50)

# Test 1: Import
print("\nStep 1: Checking pyzbar...")
try:
    from PIL import Image
    from pyzbar.pyzbar import decode
    print("[OK] Libraries imported!")
except Exception as e:
    print(f"[FAIL] {e}")
    print("\nFix: pip install pyzbar-dll")
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

# Test 3: Scan
print(f"\nStep 3: Scanning QR code...")
try:
    image = Image.open(test_image)
    decoded = decode(image)

    if decoded:
        qr_data = decoded[0].data.decode('utf-8')
        print(f"[SUCCESS] QR Detected: {qr_data}")
        print(f"Type: {decoded[0].type}")
        print("\n*** QR SCANNER IS WORKING! ***")
    else:
        print("[FAIL] No QR detected in image")
        print("QR scanner might not be working properly")

except Exception as e:
    print(f"[FAIL] Error: {e}")
    print("QR scanner has issues")

print("\n" + "="*50)
