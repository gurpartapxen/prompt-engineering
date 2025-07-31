import base64
import requests
from PIL import Image
from io import BytesIO

# 🔐 Hugging Face API key (replace this with your key)
HF_API_KEY = "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"

# ✅ Step 1: Encode API key as base64
def encode_api_key(api_key):
    return base64.b64encode(f"{api_key}:".encode()).decode()

# ✅ Step 2: Call Hugging Face Inference API
def generate_image(prompt):
    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

    encoded_key = encode_api_key(HF_API_KEY)

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",  # ✅ Correct header
        "Content-Type": "application/json",
        "Accept": "image/png"
    }

    payload = {
        "inputs": prompt
    }

    print("🚀 Sending request to Hugging Face API...")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.content
    else:
        print(f"❌ Failed with status {response.status_code}")
        print("Response:", response.text)
        return None

# ✅ Step 3: Save and display the image
def save_and_show_image(image_bytes, filename="generated_image.png"):
    with open(filename, "wb") as f:
        f.write(image_bytes)

    print(f"✅ Image saved as {filename}")

    try:
        image = Image.open(BytesIO(image_bytes))
        image.show()
        print("🖼️ Image displayed.")
    except Exception as e:
        print("⚠️ Could not display image:", e)

# ✅ Step 4: Main entry
def main():
    prompt = input("🎨 Enter your image prompt: ").strip()
    image_bytes = generate_image(prompt)

    if image_bytes:
        save_and_show_image(image_bytes)

if __name__ == "__main__":
    main()
