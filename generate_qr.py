"""
QR Code Generator for OceanGuard Boats
Generate QR codes for registered boats
"""

import qrcode
import os

# QR codes to generate (match with database entries)
# ⚠️ IMPORTANT: Ye same IDs Django admin mein register karna hai!
boats = [
    {"id": "OCEAN-BOAT-001", "name": "Sea King"},
    {"id": "OCEAN-BOAT-002", "name": "Wave Rider"},
    {"id": "OCEAN-BOAT-003", "name": "Blue Dolphin"},
    {"id": "TEST-BOAT-999", "name": "Test Boat"},  # Testing ke liye
]

# Create output directory
os.makedirs("qr_codes", exist_ok=True)

print("🚢 OceanGuard QR Code Generator\n")

for boat in boats:
    qr_data = boat["id"]

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,
        border=4,
    )

    qr.add_data(qr_data)
    qr.make(fit=True)

    # Create image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save
    filename = f"qr_codes/{boat['id']}.png"
    img.save(filename)

    print(f"✅ Generated: {filename} - {boat['name']}")

print("\n✅ All QR codes generated in 'qr_codes/' folder")
print("📋 Instructions:")
print("   1. Print QR codes at 300 DPI or higher")
print("   2. Laminate for waterproofing")
print("   3. Attach to boat on all 4 sides")
print("   4. Test scanning with phone camera before deployment")
