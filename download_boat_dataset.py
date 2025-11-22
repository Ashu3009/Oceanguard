"""
Download Boat Dataset from Kaggle
Requires: pip install kaggle
"""

import os
import zipfile

print("=" * 60)
print("BOAT DATASET DOWNLOADER")
print("=" * 60)

# Step 1: Setup Kaggle API
print("\n[STEP 1] Kaggle API Setup")
print("-" * 60)
print("1. Go to: https://www.kaggle.com/settings")
print("2. Click 'Create New API Token'")
print("3. Download kaggle.json")
print("4. Place it at: C:\\Users\\ADMIN\\.kaggle\\kaggle.json")
print("\nPress Enter when done...")
input()

# Step 2: Install Kaggle
print("\n[STEP 2] Installing Kaggle CLI...")
os.system("pip install kaggle")

# Step 3: Download dataset
print("\n[STEP 3] Downloading Ships Dataset...")
print("-" * 60)

# Create data directory
os.makedirs("datasets/boats", exist_ok=True)
os.chdir("datasets/boats")

# Download Ships in Satellite Imagery
print("Downloading: Ships in Satellite Imagery (4,000 images)...")
os.system("kaggle datasets download -d rhammell/ships-in-satellite-imagery")

print("\n[STEP 4] Extracting files...")
if os.path.exists("ships-in-satellite-imagery.zip"):
    with zipfile.ZipFile("ships-in-satellite-imagery.zip", 'r') as zip_ref:
        zip_ref.extractall(".")
    print("[OK] Extracted!")

    # Show stats
    ship_count = len([f for f in os.listdir("shipsnet") if f.endswith(".png") and "1__" in f])
    no_ship_count = len([f for f in os.listdir("shipsnet") if f.endswith(".png") and "0__" in f])

    print(f"\n[STATS]")
    print(f"Ship images: {ship_count}")
    print(f"No-ship images: {no_ship_count}")
    print(f"Total: {ship_count + no_ship_count}")
else:
    print("[ERROR] Download failed!")
    print("Manual download:")
    print("https://www.kaggle.com/datasets/rhammell/ships-in-satellite-imagery")

print("\n" + "=" * 60)
print("DATASET READY!")
print("=" * 60)
print("\nNext steps:")
print("1. Upload to Edge Impulse Studio")
print("2. Or use for training locally")
