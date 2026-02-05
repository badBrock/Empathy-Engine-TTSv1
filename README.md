# 🤖 Empathy Engine v2.0

**AI-powered emotional text-to-speech system that detects emotions and generates expressive speech**

Empathy Engine analyzes text, detects emotions, and generates speech with emotion-aware speed, volume, and tone.

---

## ✨ Features

- 🎭 Emotion detection (7 classes)
- 🗣️ Emotion-aware text-to-speech
- 🎨 Clean single-page UI
- ⚡ Fast inference
- 💾 Audio download support
- 🔧 REST API

---

## ▶️ How to Run

### ✅ Prerequisites

- Python 3.8+
- pip
- Git
- Audio support  
  - Windows: SAPI5  
  - Linux: `espeak`  
  - macOS: default TTS  

---

### 🚀 Run Commands (Copy–Paste)

```bash
mkdir -p static/audio
mkdir -p utils
pip install -r requirements.txt
python main.py
OR
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
http://localhost:8000
