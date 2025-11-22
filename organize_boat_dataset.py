"""
Organize Kaggle Ships Dataset for Edge Impulse
Separates boat and not-boat images
"""

import os
import shutil
from pathlib import Path

print("=" * 70)
print("BOAT DATASET ORGANIZER FOR EDGE IMPULSE")
print("=" * 70)

# Paths
source_dir = "shipsnet"  # Kaggle dataset folder
output_dir = "datasets"
boat_dir = os.path.join(output_dir, "boat")
not_boat_dir = os.path.join(output_dir, "not-boat")

# Create directories
os.makedirs(boat_dir, exist_ok=True)
os.makedirs(not_boat_dir, exist_ok=True)

print(f"\n[INFO] Source: {source_dir}")
print(f"[INFO] Output: {output_dir}")

# Check if source exists
if not os.path.exists(source_dir):
    print(f"\n❌ ERROR: {source_dir} not found!")
    print("\nSteps to fix:")
    print("1. Download dataset from Kaggle:")
    print("   https://www.kaggle.com/datasets/rhammell/ships-in-satellite-imagery")
    print("2. Extract to 'shipsnet' folder")
    print("3. Run this script again")
    exit(1)

# Process files
print("\n[PROCESSING] Organizing images...")
boat_count = 0
not_boat_count = 0

for filename in os.listdir(source_dir):
    if not filename.endswith(".png"):
        continue

    source_path = os.path.join(source_dir, filename)

    # Kaggle naming: 1__xxx.png = ship, 0__xxx.png = no ship
    if filename.startswith("1__"):
        dest_path = os.path.join(boat_dir, filename)
        shutil.copy(source_path, dest_path)
        boat_count += 1
    elif filename.startswith("0__"):
        dest_path = os.path.join(not_boat_dir, filename)
        shutil.copy(source_path, dest_path)
        not_boat_count += 1

print(f"\n[RESULTS]")
print(f"✅ Boat images: {boat_count}")
print(f"✅ Not-boat images: {not_boat_count}")
print(f"✅ Total: {boat_count + not_boat_count}")

# Check balance
if boat_count > 0 and not_boat_count > 0:
    ratio = boat_count / not_boat_count
    print(f"\n[BALANCE] Boat:Not-boat ratio = {ratio:.2f}:1")

    if 0.8 < ratio < 1.2:
        print("✅ Dataset is well balanced!")
    else:
        print("⚠️ Dataset imbalanced - consider balancing for better accuracy")

print("\n[NEXT STEPS]")
print("1. Go to: https://studio.edgeimpulse.com")
print("2. Create/open your project")
print("3. Data acquisition → Upload data")
print("4. Upload images from:")
print(f"   - {boat_dir} (label: boat)")
print(f"   - {not_boat_dir} (label: not-boat)")
print("5. Split 80% training, 20% testing")

print("\n" + "=" * 70)
print("DATASET READY FOR EDGE IMPULSE!")
print("=" * 70)
