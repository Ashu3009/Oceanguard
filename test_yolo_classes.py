"""
Test YOLO Model - Check What Classes It Can Detect
"""

try:
    from ultralytics import YOLO
    print("Loading YOLOv8 model...\n")

    model = YOLO('yolov8n.pt')

    print("=" * 60)
    print("YOLO MODEL CLASS NAMES (COCO Dataset)")
    print("=" * 60)

    # Print all class names
    for class_id, class_name in model.names.items():
        print(f"{class_id:2d}: {class_name}")

    print("\n" + "=" * 60)
    print("BOAT/SHIP RELATED CLASSES:")
    print("=" * 60)

    boat_related = []
    for class_id, class_name in model.names.items():
        if any(keyword in class_name.lower() for keyword in ['boat', 'ship', 'vessel', 'sail']):
            boat_related.append(f"{class_id}: {class_name}")
            print(f"[FOUND] Class {class_id}: {class_name}")

    if not boat_related:
        print("[WARNING] No boat/ship related classes found!")

    print("\n" + "=" * 60)
    print("RECOMMENDATION:")
    print("=" * 60)
    print("Update settings.py BOAT_CLASSES to only include:")
    print("  BOAT_CLASSES = ['boat']")
    print("\nOr add related classes like:")
    print("  - person (for people on boats)")
    print("  - surfboard, kite (for water sports)")

except ImportError:
    print("ERROR: ultralytics not installed")
    print("Install: pip install ultralytics")
except Exception as e:
    print(f"ERROR: {e}")
