"""
Test Color Detection for WHITE and BLUE Boats
==============================================
This script tests the color detection algorithm on sample images.
Use this to verify your color ranges before testing with ESP32!
"""

import cv2
import numpy as np
import os

# Same color ranges as in settings.py
COLOR_RANGES = {
    'WHITE': [
        # White = Low saturation (almost no color) + High brightness
        {'lower': (0, 0, 200), 'upper': (180, 30, 255)}    # Any hue, very low saturation, high brightness
    ],
    'BLUE': [
        {'lower': (100, 100, 100), 'upper': (130, 255, 255)}    # Blue range
    ]
}

COLOR_DETECTION_MIN_THRESHOLD = 5.0   # 5% minimum (filters small objects)
COLOR_DETECTION_MAX_THRESHOLD = 60.0  # 60% maximum (filters large backgrounds)


def detect_colored_boat(img_path):
    """
    Test color detection on an image file
    """
    print(f"\n{'='*60}")
    print(f"Testing: {os.path.basename(img_path)}")
    print(f"{'='*60}")

    # Read image
    img = cv2.imread(img_path)

    if img is None:
        print(f"❌ Could not read image: {img_path}")
        return

    print(f"Image size: {img.shape[1]}x{img.shape[0]} pixels")

    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Total pixels
    total_pixels = img.shape[0] * img.shape[1]

    detected_colors = []

    # Check each color
    for color_name, ranges in COLOR_RANGES.items():
        total_color_pixels = 0

        # Check all ranges for this color (RED has 2 ranges)
        for i, color_range in enumerate(ranges):
            lower = np.array(color_range['lower'])
            upper = np.array(color_range['upper'])

            # Create mask for this color range
            mask = cv2.inRange(hsv, lower, upper)

            # Count colored pixels
            color_pixels = cv2.countNonZero(mask)
            total_color_pixels += color_pixels

            print(f"  {color_name} range {i+1}: {color_pixels} pixels")

        # Calculate percentage
        percentage = (total_color_pixels / total_pixels) * 100

        print(f"  {color_name} Total: {total_color_pixels} pixels ({percentage:.2f}%)")

        # Check with min/max thresholds
        if percentage < COLOR_DETECTION_MIN_THRESHOLD:
            print(f"    → Too small (< {COLOR_DETECTION_MIN_THRESHOLD}%) - Ignored")
        elif percentage > COLOR_DETECTION_MAX_THRESHOLD:
            print(f"    → Too large (> {COLOR_DETECTION_MAX_THRESHOLD}%) - Ignored")
        else:
            print(f"    → Within range ({COLOR_DETECTION_MIN_THRESHOLD}-{COLOR_DETECTION_MAX_THRESHOLD}%) ✓")
            detected_colors.append({
                'color': color_name,
                'percentage': round(percentage, 2)
            })

    print()

    if detected_colors:
        # Sort by percentage
        detected_colors.sort(key=lambda x: x['percentage'], reverse=True)
        best = detected_colors[0]

        print(f"✅ DETECTED: {best['color']} Boat ({best['percentage']}% of image)")
        print(f"   Status: IMAGE WOULD BE SAVED")

        if len(detected_colors) > 1:
            print(f"\n   Also detected:")
            for c in detected_colors[1:]:
                print(f"   - {c['color']}: {c['percentage']}%")
    else:
        print(f"❌ NO COLORED BOAT DETECTED")
        print(f"   Must be {COLOR_DETECTION_MIN_THRESHOLD}% - {COLOR_DETECTION_MAX_THRESHOLD}% of image")
        print(f"   Status: IMAGE WOULD BE REJECTED")

    return detected_colors


def test_webcam():
    """
    Test color detection with webcam (live)
    """
    print("\n" + "="*60)
    print("WEBCAM COLOR DETECTION TEST")
    print("="*60)
    print("Press 'q' to quit")
    print("Press 's' to save current frame")
    print()

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Could not open webcam")
        return

    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            print("❌ Failed to grab frame")
            break

        frame_count += 1

        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Total pixels
        total_pixels = frame.shape[0] * frame.shape[1]

        # Create combined mask
        combined_mask = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)

        detected_text = []

        # Check each color
        for color_name, ranges in COLOR_RANGES.items():
            total_color_pixels = 0

            for color_range in ranges:
                lower = np.array(color_range['lower'])
                upper = np.array(color_range['upper'])

                mask = cv2.inRange(hsv, lower, upper)
                total_color_pixels += cv2.countNonZero(mask)

                # Add to combined mask
                combined_mask = cv2.bitwise_or(combined_mask, mask)

            percentage = (total_color_pixels / total_pixels) * 100

            # Check min/max thresholds
            if COLOR_DETECTION_MIN_THRESHOLD <= percentage <= COLOR_DETECTION_MAX_THRESHOLD:
                detected_text.append(f"{color_name}: {percentage:.1f}%")

        # Show original frame
        display_frame = frame.copy()

        # Add text overlay
        y_offset = 30
        if detected_text:
            cv2.putText(display_frame, "BOAT DETECTED!", (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            y_offset += 35
            for text in detected_text:
                cv2.putText(display_frame, text, (10, y_offset),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                y_offset += 30
        else:
            cv2.putText(display_frame, "No boat detected", (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Show frames
        cv2.imshow('Camera Feed', display_frame)
        cv2.imshow('Color Mask (White = Detected)', combined_mask)

        # Handle key press
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('s'):
            filename = f'test_frame_{frame_count}.jpg'
            cv2.imwrite(filename, frame)
            print(f"✅ Saved: {filename}")

    cap.release()
    cv2.destroyAllWindows()


def main():
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║   🎨 Color Detection Test for WHITE & BLUE Boats           ║
    ╚════════════════════════════════════════════════════════════╝
    """)

    print("Color Detection Settings:")
    print(f"  - WHITE range: Saturation 0-30, Brightness 200-255 (bright white)")
    print(f"  - BLUE range: Hue 100-130, Saturation 100-255")
    print(f"  - Valid range: {COLOR_DETECTION_MIN_THRESHOLD}% - {COLOR_DETECTION_MAX_THRESHOLD}% of image")
    print(f"    (Filters out: < {COLOR_DETECTION_MIN_THRESHOLD}% = too small, > {COLOR_DETECTION_MAX_THRESHOLD}% = too large)")
    print()

    # Check for test images
    test_images = []

    # Look in test_images folder
    if os.path.exists('test_images'):
        for file in os.listdir('test_images'):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                test_images.append(os.path.join('test_images', file))

    # Look in current folder
    for file in os.listdir('.'):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            if 'test' in file.lower() or 'boat' in file.lower():
                test_images.append(file)

    if test_images:
        print(f"Found {len(test_images)} test image(s):")
        for img in test_images:
            print(f"  - {img}")
        print()

        choice = input("Test with these images? (y/n): ").strip().lower()

        if choice == 'y':
            for img_path in test_images:
                detect_colored_boat(img_path)
                input("\nPress Enter to continue...")
    else:
        print("No test images found in current directory or test_images/ folder")
        print()

    # Webcam test
    print("\n" + "="*60)
    webcam_choice = input("Test with webcam/ESP32 feed? (y/n): ").strip().lower()

    if webcam_choice == 'y':
        test_webcam()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✋ Test stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
