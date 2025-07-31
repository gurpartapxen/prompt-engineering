import requests
import os
import uuid
from playsound import playsound

# 🔐 Your ElevenLabs API key here
ELEVEN_API_KEY = "sk_d57de3d2292d78ef63f64e7eae4aa514529065aedb81aa29"

# 🔈 Voice ID (default is Rachel, you can change this to any available voice)
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Default ElevenLabs voice (Rachel)

# 📂 Output directory
OUTPUT_DIR = "elevenlabs_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 🎤 Convert text to speech and save/play
def text_to_speech(text, voice_id=VOICE_ID):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",  # You can change this if needed
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    print("📡 Sending request to ElevenLabs...")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        filename = os.path.join(OUTPUT_DIR, f"tts_{uuid.uuid4().hex[:8]}.mp3")
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Audio saved to: {filename}")
        print("🔊 Playing audio...")
        playsound(filename)
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

# 🚀 Main app
def run_app():
    print("🎙️ ElevenLabs Text-to-Speech")
    text = input("📝 Enter the text to convert to speech: ").strip()
    if text:
        text_to_speech(text)
    else:
        print("⚠️ No text entered.")

# 🏁 Entry point
if __name__ == "__main__":
    run_app()
