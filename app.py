import streamlit as st
import cv2
import tempfile
import os
from moviepy.editor import VideoFileClip
import uuid
import whisper

# Page config
st.set_page_config(page_title="ReelRave MVP", layout="centered")
st.title("🎬 ReelRave Auto Crop MVP")
st.markdown("### 🧠 Generating subtitles...")

with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_vid:
    tmp_vid.write(video_bytes)
    tmp_vid_path = tmp_vid.name

model = whisper.load_model("base")  # you can try "small" or "medium" later

result = model.transcribe(tmp_vid_path)
transcript_text = result["text"]

st.markdown("### 📝 Transcript Preview")
st.write(transcript_text)

# Upload video
uploaded_file = st.file_uploader("Upload your video (MP4)", type=["mp4"])

def center_crop_frame(frame, target_width, target_height):
    h, w = frame.shape[:2]
    center_x, center_y = w // 2, h // 2

    x1 = max(center_x - target_width // 2, 0)
    y1 = max(center_y - target_height // 2, 0)
    x2 = min(x1 + target_width, w)
    y2 = min(y1 + target_height, h)

    return frame[y1:y2, x1:x2]

def process_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Output target size for 9:16 vertical (e.g. 720x1280)
    out_w = 720
    out_h = 1280

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (out_w, out_h))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cropped = center_crop_frame(frame, out_w, out_h)
        resized = cv2.resize(cropped, (out_w, out_h))
        out.write(resized)

    cap.release()
    out.release()

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_input:
        tmp_input.write(uploaded_file.read())
        input_path = tmp_input.name

    output_path = f"{uuid.uuid4()}.mp4"
    with st.spinner("🔧 Cropping and processing your video..."):
        process_video(input_path, output_path)

    st.success("✅ Video processed successfully!")
    st.video(output_path)

    with open(output_path, "rb") as f:
        st.download_button("⬇️ Download Cropped Video", f, file_name="cropped_video.mp4")

    os.remove(input_path)
    os.remove(output_path)
