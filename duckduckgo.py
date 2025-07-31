from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from duckduckgo_search import DDGS
import os

# 🔑 Set your Gemini API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCinnrFJHds_HUj5IsFx5_8_mp4ksJs8MA"  # 🔐 Secure this in env var

# 🌐 DuckDuckGo Search Function
def duckduckgo_search(query, max_results=3):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append(r['body'])
    return " ".join(results) if results else "No results found."

# 🤖 Gemini LLM Function
def gemini_response(query):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
    prompt = PromptTemplate(
        input_variables=["question"],
        template="Answer this question clearly and concisely:\n{question}"
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(query)

# 🧠 Gemini Evaluator Function to judge accuracy
def gemini_accuracy_judge(question, gemini_ans, duckduckgo_ans):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    evaluation_prompt = PromptTemplate(
        input_variables=["question", "llm_answer", "search_answer"],
        template="""
You're an AI evaluator. Given a user question, a Gemini LLM answer, and a DuckDuckGo search answer — analyze both and determine which one is **factually more accurate**.

Question: {question}

Gemini LLM Answer: {llm_answer}

DuckDuckGo Search Answer: {search_answer}

Reply with:
- ✅ Most accurate answer: [Gemini or DuckDuckGo]
- 🎯 Reason: [Explain why that one is more accurate]
"""
    )
    chain = LLMChain(llm=llm, prompt=evaluation_prompt)
    return chain.run({
        "question": question,
        "llm_answer": gemini_ans,
        "search_answer": duckduckgo_ans
    })

# 🔎 Compare Results
def compare_outputs(llm_result, search_result):
    llm_len = len(llm_result.split())
    search_len = len(search_result.split())

    print("\n🔹 Gemini LLM Response:\n", llm_result)
    print("\n🔹 DuckDuckGo Search Response:\n", search_result)

    if llm_len > search_len * 1.2:
        detail_result = "✅ Gemini LLM response is more detailed."
    elif search_len > llm_len * 1.2:
        detail_result = "✅ DuckDuckGo Search response is more detailed."
    else:
        detail_result = "🤝 Both responses are equally detailed."

    return detail_result

# 🚀 Run the Comparison
def main():
    query = input("🔍 Enter your question: ")

    # Step 1: Get both responses
    llm_result = gemini_response(query)
    search_result = duckduckgo_search(query)

    # Step 2: Compare length/detail
    detail_judgement = compare_outputs(llm_result, search_result)

    # Step 3: Judge factual accuracy via Gemini itself
    accuracy_judgement = gemini_accuracy_judge(query, llm_result, search_result)

    # Step 4: Show final output
    print("\n📊 Final Comparison Result:")
    print(detail_judgement)
    print(accuracy_judgement)

if __name__ == "__main__":
    main()
