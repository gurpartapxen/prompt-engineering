import google.generativeai as genai

# Step 1: Configure Gemini API Key
genai.configure(api_key="AIzaSyCHuHUcPCevRz-75vZIbPaHJ7GsiC9Hc7A")

# Step 2: Load Gemini 1.5 Flash
model = genai.GenerativeModel("gemini-1.5-flash")

# Step 3: Input prompt, generated response, and reference
prompt = input("📥 Enter the original user prompt:\n> ")
generated_response = input("✍️ Enter the model-generated response:\n> ")
reference_response = input("📘 Enter the reference (ideal) response:\n> ")

# Step 4: Metric-based Evaluation Prompt
eval_prompt = f"""
You are an expert evaluator. A user gave the following prompt:

Prompt: "{prompt}"

The AI model responded with:
Generated Response: "{generated_response}"

The ideal (reference) response is:
Reference Response: "{reference_response}"

Evaluate the generated response on the following metrics (score each from 1 to 5):

1. Relevance to the prompt
2. Factual correctness
3. Fluency (grammar and clarity)
4. Completeness (coverage compared to reference)

Provide a score for each metric and a brief justification.
Return output in the format:

Relevance: X/5  
Correctness: X/5  
Fluency: X/5  
Completeness: X/5  
Justification: ...
"""

# Step 5: Get evaluation from Gemini
try:
    evaluation = model.generate_content(eval_prompt)
    print("\n📊 Evaluation Result:\n")
    print(evaluation.text)
except Exception as e:
    print("❌ Error during evaluation:", e)
