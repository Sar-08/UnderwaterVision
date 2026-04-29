import cv2

def enhance_image(input_path, output_path):
    # Read image
    image = cv2.imread(input_path)

    if image is None:
        raise ValueError("Could not read input image")

    # Simple enhancement (you can replace with your deep model later)
    enhanced = cv2.convertScaleAbs(image, alpha=1.2, beta=20)

    # Save enhanced image
    cv2.imwrite(output_path, enhanced)

    return output_path
