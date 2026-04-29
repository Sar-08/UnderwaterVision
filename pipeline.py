from ultralytics import YOLO
from enhancer_model import Enhancer
from PIL import Image
import torch
import os

# Paths
input_path = "sample.jpg"
enhanced_path = "enhanced.jpg"
model_path = "models/yolov8s_trashcan.pt"

# 1️⃣ Load models
enhancer = Enhancer("models/funie_generator.pth")
yolo = YOLO(model_path)

# 2️⃣ Enhance image
img = Image.open(input_path)
enhanced_img = enhancer.enhance_pil(img)
enhanced_img.save(enhanced_path)
print("✔ Enhanced image saved as", enhanced_path)

# 3️⃣ Run YOLO detection **correct method**
results = yolo.predict(
    source=enhanced_path,
    save=True,
    project="det_output",
    name="run1",
    conf=0.25,
    exist_ok=True
)

print("✔ YOLO detection completed")

# Find the saved file
output_dir = "det_output/run1"
detected_image = None

for f in os.listdir(output_dir):
    if f.lower().endswith((".jpg", ".jpeg", ".png")) and "enhanced" in f:
        detected_image = os.path.join(output_dir, f)
        break

print("✔ Detection output saved at:", detected_image)
