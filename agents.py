import os
from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool  # ✅ Correct import

# 🔐 Set your Gemini API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCHuHUcPCevRz-75vZIbPaHJ7GsiC9Hc7A"

# 🤖 Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

# 🧠 Memory for multi-turn chat
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 🛠️ Tools for the agent (can add real ones later)
tools = [
    Tool(
        name="EchoTool",
        func=lambda x: f"Echo: {x}",
        description="Just repeats what the user says."
    )
]

# 🧠 Initialize the agent with memory
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True  # Set to False for clean output
)

# 🚀 Conversation Loop
def main():
    print("🤖 Gemini Agent with Memory. Type 'exit' to end the conversation.\n")
    while True:
        user_input = input("👤 You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Session ended.")
            break
        response = agent.run(user_input)
        print("🤖 Gemini:", response)

if __name__ == "__main__":
    main()
