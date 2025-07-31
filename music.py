from transformers import MusicgenForConditionalGeneration, AutoProcessor

import torch
import torchaudio

model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")

inputs = processor(
    text=["A relaxing lo-fi hip-hop beat with soft piano."],
    padding=True,
    return_tensors="pt"
)

audio_values = model.generate(**inputs, max_new_tokens=1024)
torchaudio.save("generated_music.wav", audio_values[0], 32000)

print("✅ Music saved to 'generated_music.wav'")