import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from serpapi import GoogleSearch
from langchain_community.utilities import SearchApiAPIWrapper
import os
os.environ["SEARCHAPI_API_KEY"] = "f31cASNCQt5XF1oEWoMb7zBj"

# Set up API keys in environment
os.environ["OPENAI_API_KEY"] = "voc-37886132717535051986986aa553a15c3682.30552167"
os.environ["OPENAI_BASE_URL"] = "https://openai.vocareum.com/v1"
os.environ["SERPAPI_API_KEY"] = ""
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini"
search = SearchApiAPIWrapper()

llm = LLM(
    model = "ollama/qwen2.5:7b",
    base_url = 'http://localhost:11434'
)

@tool("Search Web")
def search_web(query: str) -> str:
    """Useful for answering questions about current events or real-world facts."""
    result = search.run(query)
    return result


@tool("Calculator")
def calculate(expression: str) -> str:
    """Useful for math calculations. Input should be a valid Python math expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"


research_assistant = Agent(
    role="Research Assistant",
    goal="Find accurate information and answer clearly.",
    backstory="""You are a research assistant. 
    Always Use search_web tool to find the current date, then with current date use tools 
    find accurate information and answer clearly. 
    If multiple questions are there, answer all of them.
    """,
    verbose=True,
    allow_delegation=False,
    llm = llm,
    tools=[search_web, calculate]
)


def main():
    user_input = "What is the square root of the number of countries in the world?, also give me the total population in world?."
    prompt = f"Please research and answer this question thoroughly: {user_input}"
    
    research_task = Task(
        description=prompt,
        expected_output="A comprehensive response answering all parts of the user's question.",
        agent=research_assistant
    )
    
    crew = Crew(
        agents=[research_assistant],
        tasks=[research_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        result = crew.kickoff()
        print(result)
    except Exception as e:
        print(f"Error running agent: {e}")


if __name__ == "__main__":
    main()

# Receiving and analyzing the user input
# System prompt analysis
# Making a step by step plan to complete the task based on user input and system prompt
# Execution of this steps (It tool call is required it performs tool call)
# Process the final output
