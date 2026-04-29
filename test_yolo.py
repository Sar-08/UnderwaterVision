from ultralytics import YOLO

model = YOLO("models/yolov8s_trashcan.pt")

results = model.predict(
    source="static/results/20251130_204931_vid_000539_frame0000054.jpg",  # kisi ek image ka full path
    imgsz=256,
    conf=0.25,
    save=True
)

print("✅ Detection finished")