from langchain_openai import ChatOpenAI
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.agents.factory import create_agent


# Connections to LLM & SerpAPI
llm = ChatOpenAI(
    model="",
    base_url="",
    api_key="",
)

from langchain_community.utilities import serpapi
class DummyHiddenPrints:
    def __enter__(self): pass
    def __exit__(self, *args): pass
serpapi.HiddenPrints = DummyHiddenPrints

search = SerpAPIWrapper(
    serpapi_api_key=""
)


# Calculator Tool
def calculate(expression: str) -> str:
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"


tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful for answering questions about current events or real-world facts.",
    ),
    Tool(
        name="Calculator",
        func=calculate,
        description="Useful for math calculations. Input should be a valid Python math expression.",
    ),
]

# User input prompt template
user_prompt = ChatPromptTemplate.from_messages(
    [("user", "Please research and answer this question thoroughly: {input}")]
)

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""You are a research assistant. Use tools to find accurate information and answer clearly. If multiple questions are there, answer all of them.
""",
)


def run_agent(messages):
    try:
        return agent.invoke(
            {"messages": [{"role": "user", "content": messages.messages[-1].content}]}
        )
    except Exception as e:
        print(e)


chain = user_prompt | RunnableLambda(run_agent)  # user_prompt -> run_agent

result = chain.invoke(
    {
        "input": "What is the square root of the number of countries in the world?, also give me the total population in world?."
    }
)

import sys
if sys.stdout.closed:
    sys.stdout = sys.__stdout__

print(result["messages"][-1].content)

# Receiving and analyzing the user input
# System prompt analysis
# Making a step by step plan to complete the task based on user input and system prompt
# Execution of this steps (It tool call is required it performs tool call)
# Process the final output
