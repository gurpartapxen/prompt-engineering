import google.generativeai as genai

# Step 1: Configure Gemini API key
genai.configure(api_key="AIzaSyCHuHUcPCevRz-75vZIbPaHJ7GsiC9Hc7A")

# Step 2: Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Step 3: Get original and sensitivity prompt from user
print("🧠 Sensitivity Evaluation Mode")
original_prompt = input("🔹 Enter the original prompt:\n> ").strip()
sensitive_prompt = input("🔸 Enter the modified/sensitive prompt:\n> ").strip()

# Step 4: Generate responses for both prompts
print("\n🔄 Generating responses from Gemini...\n")
try:
    response_original = model.generate_content(original_prompt).text.strip()
    print("✅ Response to Original Prompt:\n", response_original)
except Exception as e:
    print("❌ Error generating response to original prompt:", e)
    response_original = "ERROR"

try:
    response_sensitive = model.generate_content(sensitive_prompt).text.strip()
    print("\n✅ Response to Sensitive Prompt:\n", response_sensitive)
except Exception as e:
    print("❌ Error generating response to sensitive prompt:", e)
    response_sensitive = "ERROR"

# Step 5: Evaluate prompt sensitivity
if response_original == "ERROR" or response_sensitive == "ERROR":
    print("\n⚠️ Cannot perform evaluation due to earlier error.")
else:
    judge_prompt = f"""
You are a language model evaluator. A user wants to test how small variations in prompt phrasing affect model output.

Compare the two prompts and their responses:

🧾 Original Prompt:
{original_prompt}

🗨️ Response to Original Prompt:
{response_original}

🧾 Modified/Sensitive Prompt:
{sensitive_prompt}

🗨️ Response to Modified Prompt:
{response_sensitive}

Your task:
1. Determine whether the small change in prompt led to a significantly different response.
2. Evaluate if one response is better than the other in terms of relevance, clarity, accuracy, and helpfulness.

Begin with:
- "Better Prompt: Original" or "Better Prompt: Modified"
- Then a brief justification.
- If there's no meaningful difference, say "No significant difference".
"""

    print("\n🤖 Asking Gemini to evaluate sensitivity between the prompts...\n")
    try:
        result = model.generate_content(judge_prompt)
        print("📊 Gemini's Sensitivity Evaluation:\n")
        print(result.text)
    except Exception as e:
        print("❌ Error during Gemini evaluation:", e)
