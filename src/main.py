import os
import cv2

# Input image path
image_path = "G:/Zeb-Photo-App/assets/raw_photos/input.jpeg"

# Validate file
valid_extensions = ['.jpg', '.jpeg', '.png']
_, ext = os.path.splitext(image_path)
is_valid = os.path.exists(image_path) and ext.lower() in valid_extensions
print("Valid image:", is_valid)

# Load image
image = cv2.imread(image_path)

# Load Haar Cascade face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
print(f"Faces found: {len(faces)}")

if len(faces) > 0:
    # Pick largest face
    (x, y, w, h) = max(faces, key=lambda f: f[2] * f[3])

    # Padding
    pad_x = int(w * 0.3)
    pad_y = int(h * 0.5)

    # Crop coordinates with padding
    x1 = max(x - pad_x, 0)
    y1 = max(y - pad_y, 0)
    x2 = min(x + w + pad_x, image.shape[1])
    y2 = min(y + h + pad_y, image.shape[0])

    cropped = image[y1:y2, x1:x2]

    # Adjust to 3:4 aspect ratio
    target_ratio = 3 / 4
    h_c, w_c = cropped.shape[:2]
    current_ratio = w_c / h_c

    if current_ratio > target_ratio:
        # Too wide → crop width
        new_w = int(h_c * target_ratio)
        start_x = (w_c - new_w) // 2
        cropped = cropped[:, start_x:start_x + new_w]
    else:
        # Too tall → crop height
        new_h = int(w_c / target_ratio)
        start_y = (h_c - new_h) // 2
        cropped = cropped[start_y:start_y + new_h, :]

    # Resize to Pakistan passport digital size
    passport_img = cv2.resize(cropped, (826, 1062), interpolation=cv2.INTER_AREA)

    # Save output
    output_path = r"G:\Zeb-Photo-App\output_passport_pk.jpg"
    cv2.imwrite(output_path, passport_img)
    print(f"Pakistan passport photo saved: {output_path}")
else:
    print("No face detected.")
