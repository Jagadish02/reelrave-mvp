# 🎬 ReelRave MVP – Smart Automated Video Editor for Reels

ReelRave is an AI-powered tool that transforms DSLR or phone event footage into eye-catching, social-ready vertical Reels — in seconds.

## 🚀 Features

- ✅ Upload multiple video clips
- 🎯 Smart face-centered 9:16 cropping
- ✂️ Auto-trimming with start/end time
- 🎨 Visual filters (sepia, blur, gray, etc.)
- 🔥 BeatSync™: auto-cuts to music beats
- ✨ Crossfade transitions between shots
- 🗣️ Subtitle generation using Whisper AI
- 🔤 Hard-burned subtitles on final export
- 📱 9:16, 16:9, and 1:1 aspect ratio support
- 🕐 Auto-capped to 60 seconds for Reels
- ⚙️ Local processing (privacy-safe)

---

## 🧰 Tech Stack

| Layer        | Tools / Libraries                            |
|--------------|-----------------------------------------------|
| Frontend     | Streamlit                                     |
| Backend      | Python, OpenCV, MoviePy, FFmpeg               |
| AI           | Whisper (subtitles), Librosa (BeatSync)       |
| Deployment   | Streamlit Cloud or local                      |
| UX           | Progress bars, video previews, logs           |

---

## 📦 Setup Instructions

### 1. Clone the repo and install dependencies

```bash
git clone https://github.com/your-org/reelrave.git
cd reelrave
pip install -r requirements.txt
