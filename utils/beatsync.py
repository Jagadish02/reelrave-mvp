import librosa
import moviepy.editor as mp

def detect_beats(audio_path, min_interval=0.5):
    """
    Detect beat timestamps from an audio file using Librosa.
    
    Parameters:
        audio_path (str): Path to the audio file.
        min_interval (float): Minimum time between beats to avoid rapid cuts.

    Returns:
        List[float]: Timestamps of filtered beat times in seconds.
    """
    y, sr = librosa.load(audio_path, sr=None)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    raw_times = librosa.frames_to_time(beats, sr=sr)

    # Filter out too-close beat intervals
    beat_times = [raw_times[0]] if len(raw_times) > 0 else []
    for t in raw_times[1:]:
        if t - beat_times[-1] >= min_interval:
            beat_times.append(t)

    return beat_times


def cut_on_beats(video_path, output_path, beat_times, min_duration=0.5):
    """
    Cuts a video into subclips based on beat timestamps and joins them together.

    Parameters:
        video_path (str): Path to the input video.
        output_path (str): Path to save the output video.
        beat_times (List[float]): List of beat timestamps.
        min_duration (float): Minimum clip duration to keep (in seconds).

    Returns:
        str: Path to the final video.
    """
    clip = mp.VideoFileClip(video_path)
    subclips = []

    for i in range(len(beat_times) - 1):
        start = beat_times[i]
        end = beat_times[i + 1]
        if end - start >= min_duration:
            subclips.append(clip.subclip(start, end))

    if not subclips:
        raise ValueError("No valid subclips found based on the beat timings.")

    final_clip = mp.concatenate_videoclips(subclips)
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    return output_path
