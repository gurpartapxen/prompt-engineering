import google.generativeai as genai

# Step 1: Configure your Gemini API Key
genai.configure(api_key="AIzaSyCHuHUcPCevRz-75vZIbPaHJ7GsiC9Hc7A")

# Step 2: Load Gemini 1.5 Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

# Step 3: Run for 3 iterations
for i in range(1, 4):
    print(f"\n🔁 Iteration {i} of 3\n")

    # Get Prompt A
    prompt_a = input("🔹 Enter Prompt A:\n> ").strip()

    # Generate response for Prompt A
    print("🤖 Generating response for Prompt A...")
    try:
        response_a = model.generate_content(prompt_a).text.strip()
        print("✅ Response A:\n", response_a)
    except Exception as e:
        response_a = "ERROR"
        print("❌ Error with Prompt A:", e)

    # Get Prompt B
    prompt_b = input("\n🔸 Enter Prompt B:\n> ").strip()

    # Generate response for Prompt B
    print("🤖 Generating response for Prompt B...")
    try:
        response_b = model.generate_content(prompt_b).text.strip()
        print("✅ Response B:\n", response_b)
    except Exception as e:
        response_b = "ERROR"
        print("❌ Error with Prompt B:", e)

    # Only judge if both responses are valid
    if response_a != "ERROR" and response_b != "ERROR":
        judge_prompt = f"""
You are a language model evaluator. Compare two different prompts and their responses.

Prompt A:
{prompt_a}

Response A:
{response_a}

Prompt B:
{prompt_b}

Response B:
{response_b}

Your job is to determine which prompt led to a better response based on:
- Relevance
- Clarity and grammar
- Completeness
- Factual accuracy

Respond with:
"Better Prompt: A" or "Better Prompt: B"  
Then give a brief justification.
"""

        print("\n🧑‍⚖️ Evaluating which prompt generated a better response...\n")
        try:
            evaluation = model.generate_content(judge_prompt).text.strip()
            print("📊 Gemini's Evaluation:\n", evaluation)
        except Exception as e:
            print("❌ Error during evaluation:", e)
    else:
        print("⚠️ Skipping judgment due to earlier error.")

print("\n✅ Completed 3 iterations of prompt diversity evaluation.")
