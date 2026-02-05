from transformers import pipeline
import pyttsx3
import os
import time
from typing import Dict, Tuple

class EmpathyEngine:
    def __init__(self):
        self.classifier = pipeline(
            task="text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=None
        )
        self.emotion_presets = {
            "joy": {"rate_offset": 10, "volume": 0.95, "voice": "soft"},
            "anger": {"rate_offset": 50, "volume": 1.0, "voice": "default"},
            "sadness": {"rate_offset": -50, "volume": 0.6, "voice": "soft"},
            "fear": {"rate_offset": 80, "volume": 1.0, "voice": "soft"},
            "surprise": {"rate_offset": 70, "volume": 1.0, "voice": "soft"},
            "disgust": {"rate_offset": -25, "volume": 0.8, "voice": "default"},
            "neutral": {"rate_offset": 0, "volume": 0.85, "voice": "default"}
        }

    def classify_emotion(self, text: str) -> Tuple[str, float]:
        """Detect emotion from text"""
        scores = sorted(self.classifier(text)[0], key=lambda x: x["score"], reverse=True)
        return scores[0]["label"], scores[0]["score"]

    def init_tts(self) -> tuple:
        """Initialize TTS engine"""
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty("voices")
        soft_voice_id = voices[1].id if len(voices) > 1 else voices[0].id
        default_voice_id = voices[0].id
        return engine, soft_voice_id, default_voice_id

    def generate_emotional_speech(self, text: str) -> Dict:
        """Main method: text → emotion → speech file"""
        emotion, confidence = self.classify_emotion(text)
        
        timestamp = int(time.time())
        filename = f"audio_{timestamp}_{emotion}.wav"
        filepath = f"static/audio/{filename}"
        
        engine, soft_voice_id, default_voice_id = self.init_tts()
        
        # Apply emotion settings
        preset = self.emotion_presets.get(emotion, self.emotion_presets["neutral"])
        base_rate = engine.getProperty("rate")
        rate = max(120, min(280, base_rate + preset["rate_offset"]))
        
        voice_id = soft_voice_id if preset["voice"] == "soft" else default_voice_id
        engine.setProperty("voice", voice_id)
        engine.setProperty("rate", rate)
        engine.setProperty("volume", preset["volume"])
        
        # Save file
        if os.path.exists(filepath):
            os.remove(filepath)
        engine.save_to_file(text, filepath)
        engine.runAndWait()
        
        return {
            "filename": filename,
            "filepath": filepath,
            "emotion": emotion,
            "confidence": confidence,
            "settings": {
                "rate": rate,
                "volume": preset["volume"],
                "voice": preset["voice"]
            }
        }
