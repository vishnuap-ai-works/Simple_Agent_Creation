from langchain_openai import ChatOpenAI
from langchain_community.utilities import SearchApiAPIWrapper
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.agents.factory import create_agent
import os
from langchain_core.globals import set_debug
set_debug(True)
os.environ["LANGCHAIN_TRACING_V2"] = "false"


# Connections to LLM & SerpAPI
llm = ChatOpenAI(
    model="gpt-5-mini",
    base_url="https://openai.vocareum.com/v1",
    api_key="voc-37886132717535051986986aa553a15c3682.30552167",
)

import os
os.environ["SEARCHAPI_API_KEY"] = "f31cASNCQt5XF1oEWoMb7zBj"

# Tool - 1
search = SearchApiAPIWrapper()


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
    system_prompt="""You are a research assistant. 
    Use tools to find accurate information and answer clearly. 
    If multiple questions are there, answer all of them.
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
        "input": """What is the square root of the number of countries in the world?, 
        also give me the total population in world?."""
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
