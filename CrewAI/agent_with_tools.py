import os
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from serpapi import GoogleSearch

# Set up API keys in environment
os.environ["OPENAI_API_KEY"] = ""
os.environ["OPENAI_BASE_URL"] = ""
os.environ["SERPAPI_API_KEY"] = ""
os.environ["OPENAI_MODEL_NAME"] = ""


@tool("Search Web")
def search_web(query: str) -> str:
    """Useful for answering questions about current events or real-world facts."""
    try:
        search = GoogleSearch({
            "q": query,
            "api_key": os.environ["SERPAPI_API_KEY"]
        })
        results = search.get_dict()
        if "answer_box" in results:
            ans = results["answer_box"].get("answer") or results["answer_box"].get("snippet")
            if ans:
                return ans
        
        if "organic_results" in results and len(results["organic_results"]) > 0:
            return results["organic_results"][0].get("snippet", "No snippet found")
            
        return "No good search result found"
    except Exception as e:
        return f"Search Error: {e}"


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
    backstory="You are a research assistant. Use tools to find accurate information and answer clearly. If multiple questions are there, answer all of them.",
    verbose=True,
    allow_delegation=False,
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
