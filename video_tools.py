import cv2
import whisper
import moviepy.editor as mp
import os
import ffmpeg

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def crop_video_opencv(input_path, cropped_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30  # fallback
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        h, w, _ = frame.shape
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        cx = w // 2
        if len(faces) > 0:
            x, y, fw, fh = faces[0]
            cx = x + fw // 2
        crop_w = int(h * 9 / 16)
        x1 = max(0, cx - crop_w // 2)
        x2 = min(w, x1 + crop_w)
        cropped = frame[:, x1:x2]
        resized = cv2.resize(cropped, (1080, 1920))
        if out is None:
            out = cv2.VideoWriter(cropped_path, fourcc, fps, (1080, 1920))
        out.write(resized)
    cap.release()
    if out:
        out.release()

def generate_subtitles_srt(video_path, srt_path):
    model = whisper.load_model("base")
    result = model.transcribe(video_path)
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(result["segments"]):
            start = format_time(seg["start"])
            end = format_time(seg["end"])
            text = seg["text"].strip()
            f.write(f"{i+1}\n{start} --> {end}\n{text}\n\n")

def format_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

def process_videos(paths, output_path, max_duration=60, add_subs=True, crossfade=True):
    ensure_dir("temp")
    cropped_paths = []

    for i, path in enumerate(paths):
        cropped = f"temp/cropped_{i}.mp4"
        crop_video_opencv(path, cropped)
        cropped_paths.append(cropped)

    clips = [mp.VideoFileClip(p) for p in cropped_paths]

    if crossfade:
        final = mp.concatenate_videoclips(clips, method="compose", padding=-0.5)
    else:
        final = mp.concatenate_videoclips(clips, method="compose")

    total_duration = sum([c.duration for c in clips])
    if total_duration > max_duration:
        final = final.subclip(0, max_duration)

    final.write_videofile(output_path, codec="libx264", audio_codec="aac")

    if add_subs:
        srt_path = "temp/subtitles.srt"
        generate_subtitles_srt(output_path, srt_path)
        ffmpeg.input(output_path).output(output_path, vf=f"subtitles={srt_path}").overwrite_output().run()