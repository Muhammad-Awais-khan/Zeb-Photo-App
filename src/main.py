import os
import cv2
import time
import numpy as np
from io import BytesIO
from rembg import remove
from PIL import Image, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A6
from reportlab.lib.utils import ImageReader


def main():

    image_path = r"assets\raw_photos\input-0.jpeg"

    # Validate file
    valid_extensions = ['.jpg', '.jpeg', '.png']
    _, ext = os.path.splitext(image_path)
    if not (os.path.exists(image_path) and ext.lower() in valid_extensions):
        raise FileNotFoundError("Image missing or invalid extension.")
   
    # Read image
    image = cv2.imread(image_path)
    print(f"Image loaded: {image_path}")

    faces = detect_faces(image)
    print(f"Faces detected: {len(faces)}")

    enhance_image = photo_enhancment(image)
    print("Image enhanced with brightness, contrast, denoising, and sharpening.")

    resized_crop, final_w, final_h = resize_image(faces, enhance_image)
    print(f"Image resized to passport dimensions: {final_w}x{final_h}")

    white_background = white_bg(resized_crop, final_w, final_h)
    print("Background removed and white background added.")

    bordered_image = add_outline(white_background)
    print("Outline added to the image.")

    image_pdf = image_to_pdf(bordered_image)
    print("Image converted to PDF.")

    with open("passport_pics.pdf", "wb") as f:
        f.write(image_pdf.read())
    print("Passport PDF with 9 photos saved: passport_pics.pdf")



def detect_faces(image):
    if image is None:
        raise ValueError("Image not found or could not be read.")
    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    
    return faces


def photo_enhancment(img, brightness=15, contrast=1.1):
    adjusted = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)
    return adjusted


def resize_image(faces, image):
    
    if len(faces) > 0:
        # Largest face
        (x, y, w, h) = max(faces, key=lambda f: f[2] * f[3])

        # Padding
        pad_x = int(w * 0.4)
        pad_top = int(h * 0.7)
        pad_bottom = int(h * 0.9)

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


def add_outline(image: Image.Image, color=(0, 0, 0), thickness=5) -> Image.Image:
    #Add a thin outline (border) around the image.
    outlined = ImageOps.expand(image, border=thickness, fill=color)
    return outlined


def image_to_pdf(image, rows=3, cols=3, gap_mm=2, margin_mm=2):
    """
    Create an A6 PDF with multiple copies of a passport photo.
    - Keeps 3:4 ratio (no stretch)
    - Adds spacing (gap) between photos
    - Adds page margins
    Returns a PDF in memory (BytesIO).
    """

    mm_to_pt = 2.8346
    page_w, page_h = A6
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A6)

    # Handle PIL.Image or path
    if hasattr(image, "save"):
        img_bytes = BytesIO()
        image.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        img_input = ImageReader(img_bytes)
    else:
        img_input = ImageReader(image)

    # Convert values to points
    gap = gap_mm * mm_to_pt
    margin = margin_mm * mm_to_pt

    # Available area inside margins
    avail_w = page_w - 2 * margin - (cols - 1) * gap
    avail_h = page_h - 2 * margin - (rows - 1) * gap

    # Max cell size
    cell_w = avail_w / cols
    cell_h = avail_h / rows

    # Passport ratio 3:4
    ratio = 3 / 4
    if cell_w / cell_h > ratio:
        ph = cell_h
        pw = ph * ratio
    else:
        pw = cell_w
        ph = pw / ratio

    # Total grid size
    total_w = cols * pw + (cols - 1) * gap
    total_h = rows * ph + (rows - 1) * gap

    # Starting offsets (with margin + centering)
    start_x = (page_w - total_w) / 2
    start_y = (page_h - total_h) / 2

    # Draw grid
    for r in range(rows):
        for c_idx in range(cols):
            x = start_x + c_idx * (pw + gap)
            y = page_h - start_y - (r + 1) * ph - r * gap
            c.drawImage(img_input, x, y, pw, ph)

    c.save()
    buffer.seek(0)
    return buffer


if __name__ == "__main__":
    time_start = time.time()
    try:
        main()
        print(f"Execution time: {time.time() - time_start:.2f} seconds")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)