import google.generativeai as genai
import os
import csv
import random

# Step 1: Configure your API key
genai.configure(api_key="AIzaSyCHuHUcPCevRz-75vZIbPaHJ7GsiC9Hc7A")

# Step 2: Load the Gemini 1.5 Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

# Step 3: Create or open the CSV file to log A/B test results
csv_file = "prompt_ab_test_results.csv"
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Prompt A", "Prompt B",
            "Response A", "Response B",
            "Preferred Prompt (A or B)", "User Notes"
        ])

# Step 4: Main A/B testing loop
while True:
    print("\n🧠 Enter two different prompt formulations (A and B) to test:\n")

    prompt_a = input("🅰️ Enter Prompt A:\n> ").strip()
    prompt_b = input("🅱️ Enter Prompt B:\n> ").strip()

    if prompt_a.lower() == "exit" or prompt_b.lower() == "exit":
        break

    # Step 5: Generate response for Prompt A
    try:
        response_a = model.generate_content(prompt_a, generation_config={"temperature": 0.7})
        text_a = response_a.text
    except Exception as e:
        print("❌ Error generating response for Prompt A:", e)
        continue

    # Step 6: Generate response for Prompt B
    try:
        response_b = model.generate_content(prompt_b, generation_config={"temperature": 0.7})
        text_b = response_b.text
    except Exception as e:
        print("❌ Error generating response for Prompt B:", e)
        continue

    # Step 7: Randomize the order for unbiased A/B display
    responses = [("A", prompt_a, text_a), ("B", prompt_b, text_b)]
    random.shuffle(responses)

    # Step 8: Display responses and ask for preference
    print("\n🔍 Evaluate the responses below and choose which prompt gave the better result:\n")

    print("🔹 Response 1:\n", responses[0][2])
    print("\n🔹 Response 2:\n", responses[1][2])

    while True:
        choice = input("\n✅ Which response do you prefer? (1 or 2): ").strip()
        if choice in ["1", "2"]:
            preferred_prompt = responses[int(choice) - 1][0]  # 'A' or 'B'
            break
        else:
            print("⚠️ Invalid input. Please enter 1 or 2.")

    notes = input("📝 Any comments on your choice? (optional): ")

    # Step 9: Save the results
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            prompt_a, prompt_b,
            text_a, text_b,
            preferred_prompt, notes
        ])

    print("✅ A/B test result saved!\n")

print("👋 Exiting A/B tester. Goodbye!")
