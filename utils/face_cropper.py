# utils/face_cropper.py

import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_largest_centered_face(frame):
    """
    Detects the most prominent face (by size and closeness to center).
    Returns the best (x, y, w, h) or None if no faces found.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    if len(faces) == 0:
        return None

    # Score by size and center proximity
    h, w = gray.shape
    cx_frame = w // 2
    scores = []
    for (x, y, fw, fh) in faces:
        face_area = fw * fh
        face_cx = x + fw // 2
        center_distance = abs(cx_frame - face_cx)
        scores.append((face_area - center_distance * 0.8, (x, y, fw, fh)))

    # Return face with best score
    _, best_face = max(scores, key=lambda item: item[0])
    return best_face


def smart_crop_frame(frame, target_size=(1080, 1920), debug=False):
    """
    Crops frame to given target_size around face. Falls back to center crop if needed.
    - `target_size`: (width, height), e.g., (1080, 1920)
    - `debug`: if True, draws face box and crop region
    """
    h, w, _ = frame.shape
    target_w, target_h = target_size
    aspect_ratio = target_w / target_h
    crop_width = int(h * aspect_ratio)

    face = detect_largest_centered_face(frame)
    if face:
        x, y, fw, fh = face
        cx = x + fw // 2
    else:
        cx = w // 2  # fallback

    x1 = max(0, cx - crop_width // 2)
    x2 = min(w, x1 + crop_width)
    x1 = max(0, x2 - crop_width)  # prevent overflow

    cropped = frame[:, x1:x2]

    # Debug: draw bounding boxes
    if debug:
        debug_frame = frame.copy()
        if face:
            cv2.rectangle(debug_frame, (x, y), (x + fw, y + fh), (0, 255, 0), 2)
        cv2.rectangle(debug_frame, (x1, 0), (x2, h), (255, 0, 0), 2)
        return cv2.resize(debug_frame[:, x1:x2], target_size)

    return cv2.resize(cropped, target_size)
