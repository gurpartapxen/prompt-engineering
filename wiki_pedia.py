import os
import wikipedia
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from google.api_core.exceptions import ResourceExhausted

# 🔐 Set Gemini API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCHuHUcPCevRz-75vZIbPaHJ7GsiC9Hc7A"

# 📘 Wikipedia Answer
def get_wikipedia_answer(query):
    try:
        return wikipedia.summary(query, sentences=4)
    except Exception as e:
        return f"❌ Wikipedia error: {str(e)}"

# 🤖 Gemini Answer
def get_gemini_answer(query):
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
        prompt = PromptTemplate.from_template("Answer this clearly:\n{question}")
        return (prompt | llm).invoke({"question": query}).content
    except ResourceExhausted:
        return "❌ Gemini error: Quota exceeded. Try again tomorrow."
    except Exception as e:
        return f"❌ Gemini error: {str(e)}"

# 🧠 Evaluate Efficient & Accurate Answer
def evaluate_answers(question, gemini_ans, wiki_ans):
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
        eval_template = (
            "You're an expert evaluator.\n\n"
            "Given a question and two answers (Gemini and Wikipedia), determine:\n\n"
            "1. ✅ Which is more **efficient** (clear, concise, informative)?\n"
            "2. ✅ Which is more **accurate** (factually correct)?\n"
            "3. 🏆 Final best answer overall.\n\n"
            "Question: {question}\n\n"
            "Gemini Answer: {gemini}\n\n"
            "Wikipedia Answer: {wiki}\n\n"
            "Reply in this format:\n\n"
            "✅ Efficient Answer: [Gemini or Wikipedia]\n"
            "🎯 Accurate Answer: [Gemini or Wikipedia]\n"
            "🏆 Best Overall Answer: [Gemini or Wikipedia]\n"
            "📝 Reason: [Explain briefly why you chose that]"
        )
        prompt = PromptTemplate.from_template(eval_template)
        return (prompt | llm).invoke({
            "question": question,
            "gemini": gemini_ans,
            "wiki": wiki_ans
        }).content
    except Exception as e:
        return f"❌ Evaluation error: {str(e)}"

# 🚀 Main Program
def main():
    query = input("🔍 Enter your question: ")

    gemini_ans = get_gemini_answer(query)
    wiki_ans = get_wikipedia_answer(query)

    print("\n🔹 Gemini Answer:\n", gemini_ans)
    print("\n🔹 Wikipedia Answer:\n", wiki_ans)

    if gemini_ans.startswith("❌ Gemini error: Quota exceeded"):
        print("\n📊 Final Verdict:\n Gemini quota exceeded. Only Wikipedia result shown.")
    else:
        final_eval = evaluate_answers(query, gemini_ans, wiki_ans)
        print("\n📊 Gemini Evaluation Result:\n", final_eval)

if __name__ == "__main__":
    main()
