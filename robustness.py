import google.generativeai as genai

# Step 1: Configure API key
genai.configure(api_key="AIzaSyCHuHUcPCevRz-75vZIbPaHJ7GsiC9Hc7A")

# Step 2: Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Step 3: Get user inputs for both prompts
print("🧠 Enter the two prompt versions you'd like to compare:")

prompt_original = input("🔹 Original Prompt:\n> ").strip()
prompt_variant = input("🔸 Modified/Variant Prompt:\n> ").strip()

# Step 4: Generate responses from Gemini
print("\n🤖 Generating response to Original Prompt...")
try:
    response_original = model.generate_content(prompt_original).text.strip()
    print("✅ Response to Original Prompt:\n", response_original)
except Exception as e:
    print("❌ Error with Original Prompt:", e)
    response_original = "ERROR"

print("\n🤖 Generating response to Variant Prompt...")
try:
    response_variant = model.generate_content(prompt_variant).text.strip()
    print("✅ Response to Variant Prompt:\n", response_variant)
except Exception as e:
    print("❌ Error with Variant Prompt:", e)
    response_variant = "ERROR"

# Step 5: Judge which prompt is better based on responses
if response_original == "ERROR" or response_variant == "ERROR":
    print("\n❌ Skipping evaluation due to error in generating responses.")
else:
    judge_prompt = f"""
You are an expert evaluator. Compare two prompts and their resulting responses.

🧾 Original Prompt:
{prompt_original}

🗨️ Response to Original Prompt:
{response_original}

🧾 Variant Prompt:
{prompt_variant}

🗨️ Response to Variant Prompt:
{response_variant}

Evaluate which prompt resulted in a better response. Consider:
- Relevance
- Fluency
- Factual accuracy
- Completeness

Your answer must begin with:
"Better Prompt: Original" or "Better Prompt: Variant"

Then provide a brief justification.
"""

    print("\n🧑‍⚖️ Asking Gemini to judge which prompt is better...\n")
    try:
        judgment = model.generate_content(judge_prompt).text.strip()
        print("📊 Gemini's Evaluation:\n")
        print(judgment)
    except Exception as e:
        print("❌ Error during judgment:", e)
