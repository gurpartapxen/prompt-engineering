import google.generativeai as genai

# Step 1: Set your Google AI Studio API key
genai.configure(api_key="AIzaSyCHuHUcPCevRz-75vZIbPaHJ7GsiC9Hc7A")

# Step 2: Load the Gemini 1.5 Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

# Step 3: Provide the prompt and two responses (A and B)
main_prompt = input("🧠 Enter the original user prompt:\n> ")

response_A = input("✍️ Enter Response A:\n> ")
response_B = input("✍️ Enter Response B:\n> ")

# Step 4: Ask Gemini to be the judge
judge_prompt = f"""
You are an expert judge. A user asked the question: "{main_prompt}"

Here are two responses:
Response A: "{response_A}"
Response B: "{response_B}"

Please choose which response is better (A or B), and explain why. Consider helpfulness, accuracy, completeness, and relevance.
Start with 'Better response: A' or 'Better response: B', then give justification.
"""

# Step 5: Get judgment from Gemini
try:
    result = model.generate_content(judge_prompt)
    print("\n🤖 Gemini's Judgment:\n")
    print(result.text)
except Exception as e:
    print("❌ Error generating judgment:", e)
