import os
import asyncio
from agents import Agent, Runner, function_tool, enable_verbose_stdout_logging, set_tracing_disabled
from serpapi import GoogleSearch
from langchain_community.utilities import SearchApiAPIWrapper

# Disable external tracing to remove the 401 errors
set_tracing_disabled(True)

# Enable verbose logging to see agent traces locally
enable_verbose_stdout_logging()
# Set up API keys in environment
os.environ["OPENAI_API_KEY"] = "voc-37886132717535051986986aa553a15c3682.30552167"
os.environ["OPENAI_BASE_URL"] = "https://openai.vocareum.com/v1"


import os
os.environ["SEARCHAPI_API_KEY"] = "f31cASNCQt5XF1oEWoMb7zBj"
search = SearchApiAPIWrapper()

@function_tool
def search_web(query: str) -> str:
    result = search.run(query)
    return result

# Calculator Tool
@function_tool
def calculate(expression: str) -> str:
    """Useful for math calculations. Input should be a valid Python math expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"


agent = Agent(
    name="Research Assistant",
    model="gpt-4o-mini",
    instructions="""You are a research assistant. Use tools to find accurate information and answer clearly. If multiple questions are there, answer all of them.
    Ensure that the answer is precise and does not have any content that is not require. Just answer the question.""",
    tools=[search_web, calculate],
)


async def main():
    user_input = "What is the square root of the number of countries in the world?, also give me the total population in world?."
    prompt = f"Please research and answer this question thoroughly: {user_input}"
    
    try:
        result = await Runner.run(agent, prompt)
        print(result.final_output)
    except Exception as e:
        print(f"Error running agent: {e}")


if __name__ == "__main__":
    asyncio.run(main())

# Receiving and analyzing the user input
# System prompt analysis
# Making a step by step plan to complete the task based on user input and system prompt
# Execution of this steps (It tool call is required it performs tool call)
# Process the final output
