import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import numpy as np
import threading
import wave
import datetime
import requests
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# ===== Hugging Face API Details =====
HF_API_KEY = "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"  # ⛔ Replace this with your actual key
MODEL_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

# ===== Audio Settings =====
SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = 'int16'

# ===== Globals =====
is_recording = False
recorded_chunks = []
current_audio_data = None


# ===== Utility Functions =====
def timestamp_filename(ext):
    return datetime.datetime.now().strftime(f"recording_%Y%m%d_%H%M%S.{ext}")


def save_wav(filename, data):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(data.tobytes())
    return filename


def save_transcript(text, audio_file):
    txt_file = audio_file.replace(".wav", ".txt")
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(text)
    return txt_file


def transcribe_audio(filepath):
    try:
        with open(filepath, "rb") as f:
            audio_bytes = f.read()

        headers = {
            "Authorization": f"Bearer {HF_API_KEY}",
            "Content-Type": "audio/wav"
        }

        res = requests.post(MODEL_URL, headers=headers, data=audio_bytes)

        if res.status_code == 200:
            result = res.json()
            text = result.get("text", "No text found")
            transcript_box.delete("1.0", tk.END)
            transcript_box.insert(tk.END, text)
            save_transcript(text, filepath)
        else:
            messagebox.showerror("API Error", res.text)
    except Exception as e:
        messagebox.showerror("Exception", str(e))


# ===== Recording Functions =====
def start_fixed_recording():
    duration = int(duration_entry.get())
    status_label.config(text="🎙 Recording fixed duration...")
    def task():
        global current_audio_data
        audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype=DTYPE)
        sd.wait()
        current_audio_data = audio
        draw_waveform(audio)
        filename = timestamp_filename("wav")
        save_wav(filename, audio)
        status_label.config(text="✅ Recorded. Transcribing...")
        transcribe_audio(filename)

    threading.Thread(target=task).start()


def start_manual_recording():
    global is_recording, recorded_chunks
    is_recording = True
    recorded_chunks = []

    def callback(indata, frames, time, status):
        if is_recording:
            recorded_chunks.append(indata.copy())

    stream = sd.InputStream(callback=callback, samplerate=SAMPLE_RATE, channels=CHANNELS, dtype=DTYPE)
    stream.start()

    def monitor():
        while is_recording:
            sd.sleep(100)
        stream.stop()
        audio = np.concatenate(recorded_chunks)
        draw_waveform(audio)
        filename = timestamp_filename("wav")
        save_wav(filename, audio)
        status_label.config(text="✅ Stopped. Transcribing...")
        transcribe_audio(filename)

    threading.Thread(target=monitor).start()


def stop_recording():
    global is_recording
    is_recording = False
    status_label.config(text="🛑 Recording stopped")


# ===== Waveform Visualization =====
def draw_waveform(audio_data):
    ax.clear()
    ax.plot(audio_data)
    ax.set_ylim([-2 ** 15, 2 ** 15])
    canvas.draw()


# ===== GUI Setup =====
app = tk.Tk()
app.title("🎧 Whisper Pro - Speech-to-Text")
app.geometry("1000x650")
app.configure(bg="#fef6ed")

# ===== Header =====
header = tk.Label(app, text="🎧 Whisper Recorder", bg="#f29727", fg="white", font=("Segoe UI", 20, "bold"), pady=10)
header.pack(fill="x")

# ===== Controls =====
control_frame = tk.Frame(app, bg="#fef6ed", pady=15)
control_frame.pack()

tk.Label(control_frame, text="⏱ Fixed Duration (sec):", font=("Segoe UI", 11), bg="#fef6ed").grid(row=0, column=0, padx=5)
duration_entry = tk.Entry(control_frame, width=5, font=("Segoe UI", 11))
duration_entry.insert(0, "5")
duration_entry.grid(row=0, column=1, padx=5)

tk.Button(control_frame, text="🎙 Record Fixed", font=("Segoe UI", 10), command=start_fixed_recording, bg="#ffa447").grid(row=0, column=2, padx=10)
tk.Button(control_frame, text="🎤 Start Manual", font=("Segoe UI", 10), command=start_manual_recording, bg="#ffa447").grid(row=0, column=3, padx=10)
tk.Button(control_frame, text="🛑 Stop & Transcribe", font=("Segoe UI", 10), command=stop_recording, bg="#ff6d60").grid(row=0, column=4, padx=10)

# ===== Status =====
status_label = tk.Label(app, text="⚪ Waiting...", font=("Segoe UI", 11, "italic"), bg="#fef6ed", pady=5)
status_label.pack()

# ===== Transcript Box =====
transcript_frame = tk.LabelFrame(app, text="📜 Transcript Output", font=("Segoe UI", 12, "bold"), bg="#fff", padx=10, pady=5)
transcript_frame.pack(fill="both", expand=True, padx=20, pady=10)
transcript_box = tk.Text(transcript_frame, height=8, font=("Consolas", 12))
transcript_box.pack(fill="both", expand=True)

# ===== Waveform =====
waveform_frame = tk.LabelFrame(app, text="📈 Waveform", font=("Segoe UI", 12, "bold"), bg="#fff", padx=5, pady=5)
waveform_frame.pack(fill="both", expand=True, padx=20, pady=10)

fig, ax = plt.subplots(figsize=(6, 2))
canvas = FigureCanvasTkAgg(fig, master=waveform_frame)
canvas.get_tk_widget().pack()

# ===== Footer =====
footer = tk.Label(app, text="🔒 Whisper Turbo API | Audio saved locally | Created with ❤️", bg="#f29727", fg="white", font=("Segoe UI", 10), pady=5)
footer.pack(fill="x", side="bottom")

# ===== Start App =====
app.mainloop()
