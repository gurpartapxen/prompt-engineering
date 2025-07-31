from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

# 🔑 Set your Gemini API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCinnrFJHds_HUj5IsFx5_8_mp4ksJs8MA"

# ⚙️ Load Gemini 1.5 Flash
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7
)

# 🧠 Create Prompt Template
prompt = PromptTemplate(
    input_variables=["place"],
    template="What are some interesting facts about {place}?"
)

# 🔗 Create a Chain
chain = LLMChain(llm=llm, prompt=prompt)

# 🚀 Run the Chain
response = chain.run("Japan")
print("Gemini Response:", response)
