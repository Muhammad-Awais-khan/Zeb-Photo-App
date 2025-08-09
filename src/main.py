import os
import cv2

image_path = "F:/python/Zeb-Photo-App/assets/raw_photos/input.jpeg"

valid_extensions = ['.jpg', '.jpeg', '.png']
_, ext = os.path.splitext(image_path)
is_valid = os.path.exists(image_path) and ext.lower() in valid_extensions
print(is_valid)

image = cv2.imread(image_path)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
