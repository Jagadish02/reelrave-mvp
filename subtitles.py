import whisper
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os
from textwrap import wrap

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def transcribe_audio_with_whisper(video_path, model_size="base"):
    model = whisper.load_model(model_size)
    result = model.transcribe(video_path)
    return result['segments']

def add_subtitles(video_path, segments, output_path, font_size=40, max_line_len=40):
    ensure_dir("temp")
    
    clip = VideoFileClip(video_path)
    subtitles = []

    for seg in segments:
        txt = seg['text'].strip()
        start = seg['start']
        end = seg['end']
        duration = end - start
        if duration <= 0 or not txt:
            continue

        # Wrap long text
        wrapped_text = "\n".join(wrap(txt, width=max_line_len))

        try:
            subtitle = (TextClip(wrapped_text,
                                 fontsize=font_size,
                                 font='Arial',  # Use safe font or add custom
                                 color='white',
                                 stroke_color='black',
                                 stroke_width=2,
                                 method='caption',
                                 size=(clip.w * 0.9, None))
                        .set_position(('center', 'bottom'))
                        .set_start(start)
                        .set_duration(duration)
                        .fadein(0.3)
                        .fadeout(0.3))
            subtitles.append(subtitle)
        except Exception as e:
            print(f"Error creating subtitle clip for segment {start}-{end}: {e}")
            continue

    final = CompositeVideoClip([clip] + subtitles)
    final.write_videofile(output_path, codec='libx264', audio_codec='aac')
