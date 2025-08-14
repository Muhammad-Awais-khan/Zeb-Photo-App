import os
import cv2
import time
import torch
import numpy as np
from PIL import Image
from rembg import remove
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet
# Input image

def main():

    image_path = r"assets\raw_photos\input-3.jpeg"
    output_path = r"output.png"

    # Validate file
    valid_extensions = ['.jpg', '.jpeg', '.png']
    _, ext = os.path.splitext(image_path)
    if not (os.path.exists(image_path) and ext.lower() in valid_extensions):
        raise FileNotFoundError("Image missing or invalid extension.")
   
    # Read image
    image = cv2.imread(image_path)

    faces = detect_faces(image)

    resized_crop, final_w, final_h = resize_image(faces, image)

    white_background = white_bg(resized_crop, final_w, final_h)

    enhance_image = image_enhancement(np.array(white_background))

    enhance_image.save(output_path)

    print(f"Passport photo with clean white background saved: {output_path}")

# Face detection

def detect_faces(image):
    if image is None:
        raise ValueError("Image not found or could not be read.")
    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    
    return faces


def resize_image(faces, image):
    
    if len(faces) > 0:
        # Largest face
        (x, y, w, h) = max(faces, key=lambda f: f[2] * f[3])

        # Padding
        pad_x = int(w * 0.4)
        pad_top = int(h * 0.5)
        pad_bottom = int(h * 1.1)

        x1 = max(x - pad_x, 0)
        y1 = max(y - pad_top, 0)
        x2 = min(x + w + pad_x, image.shape[1])
        y2 = min(y + h + pad_bottom, image.shape[0])

        cropped = image[y1:y2, x1:x2]

        # Maintain 3:4 aspect ratio
        target_ratio = 3 / 4
        h_c, w_c = cropped.shape[:2]
        current_ratio = w_c / h_c
        if current_ratio > target_ratio:
            new_w = int(h_c * target_ratio)
            start_x = (w_c - new_w) // 2
            cropped = cropped[:, start_x:start_x + new_w]
        else:
            new_h = int(w_c / target_ratio)
            start_y = max((h_c - new_h) // 2, 0)
            cropped = cropped[start_y:start_y + new_h, :]

        # Resize to passport size
        final_w, final_h = 826, 1062
        resized_crop = cv2.resize(cropped, (final_w, final_h), interpolation=cv2.INTER_AREA)

        return resized_crop, final_w, final_h
    
    else:
        raise ValueError("No faces detected in the image.")


def white_bg(resized_crop, final_w, final_h):
    # Remove background
    pil_image = Image.fromarray(cv2.cvtColor(resized_crop, cv2.COLOR_BGR2RGB))
    no_bg = remove(pil_image)  # Transparent background

    # Add white background
    white_bg = Image.new("RGB", (final_w, final_h), (255, 255, 255))
    white_bg.paste(no_bg, mask=no_bg.split()[3])  # Use alpha channel as mask
    return white_bg


def image_enhancement(image):
    # Load Real-ESRGAN model
    model_path = "src/RealESRGAN_x4plus.pth"

    state_dict = torch.load(model_path, map_location=torch.device('cpu'))['params_ema']

    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
    model.load_state_dict(state_dict, strict=True)

    upsampler = RealESRGANer(
        scale=4,
        model_path=model_path,
        model=model,
        tile=0,
        tile_pad=10,
        pre_pad=0,
        half=False,
    )

    image = np.array(image)

    output, _ = upsampler.enhance(image, outscale=4)

    return Image.fromarray(output)


if __name__ == "__main__":
    time_start = time.time()
    try:
        main()
        print(f"Execution time: {time.time() - time_start:.2f} seconds")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)