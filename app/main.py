from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.tts_engine import EmpathyEngine
import os
import time
import uuid

app = FastAPI(title="🤖 Empathy Engine API", version="2.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/audio", StaticFiles(directory="static/audio"), name="audio")

# Initialize engine
engine = EmpathyEngine()

class SpeechRequest(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
async def home():
    """FIXED: Read HTML with UTF-8 encoding"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <h1>❌ static/index.html not found!</h1>
        <p>1. Create <code>static/index.html</code><br>
        2. Create <code>static/style.css</code><br>
        3. Create <code>static/script.js</code><br>
        4. Create <code>static/audio/</code> folder</p>
        """)

@app.post("/api/speak")
async def generate_speech(request: SpeechRequest):
    """Generate emotional speech"""
    try:
        emotion_data = engine.generate_emotional_speech(request.text)
        return {
            "success": True,
            "filename": emotion_data["filename"],
            "emotion": emotion_data["emotion"],
            "confidence": emotion_data["confidence"],
            "settings": emotion_data["settings"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}, 500

@app.get("/api/audio/{filename}")
async def get_audio(filename: str):
    return FileResponse(f"static/audio/{filename}")

if __name__ == "__main__":
    os.makedirs("static/audio", exist_ok=True)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
