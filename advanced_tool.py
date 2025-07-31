import os
from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool, DuckDuckGoSearchRun
from langchain.tools import tool

# 🔐 Gemini API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCHuHUcPCevRz-75vZIbPaHJ7GsiC9Hc7A"

# 🤖 Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

# 🧠 Memory setup
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 🔍 DuckDuckGo search tool
search_tool = DuckDuckGoSearchRun()

# ➗ Custom calculator tool using @tool
@tool
def calculator_tool(expression: str) -> str:
    """Useful for performing basic arithmetic operations. Input should be a math expression."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"

# 🛠️ Tool List
tools = [
    Tool(
        name="DuckDuckGo Search",
        func=search_tool.run,
        description="Use this to search for up-to-date information on the web."
    ),
    Tool(
        name="Calculator",
        func=calculator_tool,
        description="Useful for basic math calculations. Input should be an arithmetic expression."
    )
]

# 🤖 Initialize the Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# 🚀 Main Chat Loop
def main():
    print("🤖 Gemini Agent with Search + Calculator. Type 'exit' to quit.\n")
    while True:
        query = input("👤 You: ")
        if query.lower() in ["exit", "quit"]:
            print("👋 Session ended.")
            break
        try:
            response = agent.run(query)
            print("🤖 Gemini:", response)
        except Exception as e:
            print("❌ Error:", str(e))

if __name__ == "__main__":
    main()
