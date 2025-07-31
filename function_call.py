import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel

# ----------------------------
# 🔑 Set your API keys here
# ----------------------------
GOOGLE_API_KEY = "AIzaSyCHuHUcPCevRz-75vZIbPaHJ7GsiC9Hc7A"
WEATHER_API_KEY = "5907bfae4e719e94fcd2249abcfcb620"

# ----------------------------
# ✅ FUNCTION DEFINITIONS
# ----------------------------

class WeatherInput(BaseModel):
    city: str

def get_weather(city: str) -> str:
    """Fetch weather info using OpenWeather API."""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url).json()

        if response.get("cod") != 200:
            return f"Error: {response.get('message', 'Unable to fetch weather')}"

        weather = response["weather"][0]["description"]
        temp = response["main"]["temp"]
        humidity = response["main"]["humidity"]
        return (f"Weather in {city.title()}: {weather}, Temp: {temp}°C, Humidity: {humidity}%.")
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

class DummyInput(BaseModel):
    input: Optional[str] = "default"

def get_quote(_: str) -> str:
    quotes = [
        "Push yourself, because no one else is going to do it for you.",
        "The struggle you're in today is developing the strength you need for tomorrow.",
        "Believe in yourself even when no one else does.",
        "Your hard work today builds your success tomorrow."
    ]
    import random
    return random.choice(quotes)

def health_tips(_: str) -> str:
    tips = [
        "Drink enough water daily.",
        "Exercise at least 30 minutes a day.",
        "Get 7–9 hours of sleep each night.",
        "Eat a balanced diet rich in fruits and vegetables.",
        "Limit screen time and take mental breaks."
    ]
    import random
    return random.choice(tips)

def include_name(_: str) -> str:
    return "Hello! I'm Gurpartap Singh, here to assist you with weather, quotes, and health tips!"

# ----------------------------
# 🔧 LangChain Tool Wrappers
# ----------------------------

tools = [
    Tool(
        name="get_weather",
        func=get_weather,
        description="Get weather info for a city. Input must be the city name.",
        args_schema=WeatherInput
    ),
    Tool(
        name="get_quote",
        func=get_quote,
        description="Returns a motivational quote for someone in need or working hard.",
        args_schema=DummyInput
    ),
    Tool(
        name="health_tips",
        func=health_tips,
        description="Returns health tips for well-being.",
        args_schema=DummyInput
    ),
    Tool(
        name="include_name",
        func=include_name,
        description="Includes Gurpartap Singh's name in a friendly greeting.",
        args_schema=DummyInput
    ),
]

# ----------------------------
# 🧠 Gemini LLM Setup
# ----------------------------

llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash",
    temperature=0.7,
    google_api_key=GOOGLE_API_KEY
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# ----------------------------
# 🧪 Run in CLI
# ----------------------------

if __name__ == "__main__":
    print("🤖 Gemini Assistant with Function Calling is Ready!")
    while True:
        query = input("\n🗣️ Ask anything (or type 'exit'): ")
        if query.lower() == "exit":
            break
        try:
            response = agent.invoke(HumanMessage(content=query))
            print(f"💬 {response.content}")
        except Exception as e:
            print(f"❌ Error: {e}")
