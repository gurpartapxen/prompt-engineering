import google.generativeai as genai
import os
import csv

# Step 1: Set your Gemini API key
genai.configure(api_key="AIzaSyCHuHUcPCevRz-75vZIbPaHJ7GsiC9Hc7A")

# Step 2: Load Gemini 1.5 Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

# Step 3: Create or open a CSV to store evaluation logs
csv_file = "human_eval_log.csv"
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Prompt", "Response", "Rating (1-5)"])

# Step 4: Loop for human evaluation
while True:
    prompt = input("🧠 Enter your prompt (or type 'exit' to quit):\n> ")
    if prompt.lower() == "exit":
        break

    # Step 5: Generate response from Gemini
    try:
        response = model.generate_content(prompt)
        output_text = response.text
        print("\n🤖 Gemini's Response:\n", output_text)
    except Exception as e:
        print("❌ Error generating response:", e)
        continue

    # Step 6: Human rating
    while True:
        try:
            rating = int(input("⭐ Please rate this response (1-5): "))
            if 1 <= rating <= 5:
                break
            else:
                print("⚠️ Enter a number between 1 and 5.")
        except ValueError:
            print("⚠️ Invalid input. Please enter an integer.")

    # Step 7: Log the evaluation
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([prompt, output_text, rating])

    print("✅ Evaluation saved!\n")

print("👋 Exiting. Thank you for evaluating!")
