# utils/face_tracking.py

import cv2

# Load Haar cascade once
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_primary_face(frame):
    """
    Detects the most prominent face in the frame.
    Returns the bounding box (x, y, w, h) of the largest face, or None if no face is found.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        return None

    # Sort faces by size (area), descending
    faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
    return faces[0]  # Return largest face


def center_crop_around_face(frame, target_size=(1080, 1920), margin=0.0):
    """
    Crops the frame to a 9:16 (or target_size) around detected face.
    If no face is found, falls back to center crop.
    """
    h, w, _ = frame.shape
    crop_w = int(h * target_size[0] / target_size[1])  # Maintain target aspect ratio

    face = detect_primary_face(frame)
    if face is not None:
        x, y, fw, fh = face
        cx = x + fw // 2
    else:
        cx = w // 2  # Fallback to center

    # Apply margin (optional)
    face_margin = int(margin * crop_w)
    x1 = max(0, cx - crop_w // 2 - face_margin)
    x2 = min(w, x1 + crop_w + 2 * face_margin)

    cropped = frame[:, x1:x2]
    resized = cv2.resize(cropped, target_size)
    return resized
