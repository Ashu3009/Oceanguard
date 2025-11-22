"""
Quick QR Scanner Test
Tests if pyzbar is working properly
"""

print("Testing QR Code Scanner...\n")

# Test 1: Check if library exists
print("Step 1: Checking pyzbar installation...")
try:
    from PIL import Image
    from pyzbar.pyzbar import decode
    print("[OK] Libraries imported successfully!")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("\n💡 Fix: Run 'pip install pyzbar-dll'")
    exit(1)
except FileNotFoundError as e:
    print(f"❌ DLL missing: {e}")
    print("\n💡 Fix: Run 'pip install pyzbar-dll'")
    exit(1)

# Test 2: Check if QR codes exist
print("\nStep 2: Checking for QR code images...")
import os
if os.path.exists("qr_codes/TEST-BOAT-999.png"):
    print("✅ QR code file found!")
    test_image = "qr_codes/TEST-BOAT-999.png"
elif os.path.exists("qr_codes/OCEAN-BOAT-001.png"):
    print("✅ QR code file found!")
    test_image = "qr_codes/OCEAN-BOAT-001.png"
else:
    print("❌ No QR code images found!")
    print("\n💡 Fix: Run 'python generate_qr.py' first")
    exit(1)

# Test 3: Try to scan
print(f"\nStep 3: Attempting to scan {test_image}...")
try:
    image = Image.open(test_image)
    decoded_objects = decode(image)

    if decoded_objects:
        print(f"✅ SUCCESS! QR Code Detected!")
        print(f"\n📱 QR Data: {decoded_objects[0].data.decode('utf-8')}")
        print(f"🔍 Type: {decoded_objects[0].type}")
        print(f"📍 Location: {decoded_objects[0].rect}")
        print("\n🎉 QR Scanner is working perfectly!")
    else:
        print("❌ No QR code detected in image")
        print("\n⚠️ This could mean:")
        print("   - QR code image is corrupted")
        print("   - Image resolution too low")
        print("   - pyzbar can't decode this format")

except Exception as e:
    print(f"❌ Scan failed: {e}")
    print("\n⚠️ QR scanner has issues!")

print("\n" + "="*50)
print("TEST COMPLETE")
print("="*50)
