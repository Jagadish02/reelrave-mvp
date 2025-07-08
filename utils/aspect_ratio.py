import cv2

def resize_to_aspect_ratio(frame, target_aspect=(9, 16), output_size=(720, 1280)):
    """
    Resize and crop a frame to a target aspect ratio and resolution.

    Parameters:
        frame (np.ndarray): The input image frame.
        target_aspect (tuple): Target aspect ratio, e.g., (9, 16) for portrait.
        output_size (tuple): Final size (width, height) to resize to.

    Returns:
        np.ndarray: The resized and cropped frame.
    """
    height, width = frame.shape[:2]
    current_aspect = width / height
    target_ratio = target_aspect[0] / target_aspect[1]

    if current_aspect > target_ratio:
        # Crop width
        new_width = int(height * target_ratio)
        start_x = (width - new_width) // 2
        cropped = frame[:, start_x:start_x + new_width]
    else:
        # Crop height
        new_height = int(width / target_ratio)
        start_y = (height - new_height) // 2
        cropped = frame[start_y:start_y + new_height, :]

    return cv2.resize(cropped, output_size)
