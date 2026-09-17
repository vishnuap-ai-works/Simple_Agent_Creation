import os
import autogen
from serpapi import GoogleSearch

# Set up API keys in environment
os.environ["OPENAI_API_KEY"] = "voc-37886132717535051986986aa553a15c3682.30552167"
os.environ["OPENAI_BASE_URL"] = "https://openai.vocareum.com/v1"
os.environ["SERPAPI_API_KEY"] = "AvMqybYYnvTs1Czxz364AR9t"
os.environ["OPENAI_MODEL_NAME"] = "gpt-5-mini"


def search_web(query: str) -> str:
    """Useful for answering questions about current events or real-world facts."""
    try:
        search = GoogleSearch({
            "q": query,
            "api_key": os.environ.get("SERPAPI_API_KEY", "")
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


def calculate(expression: str) -> str:
    """Useful for math calculations. Input should be a valid Python math expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"


def main():
    llm_config = {
        "config_list": [
            {
                "model": os.environ.get("OPENAI_MODEL_NAME", ""),
                "api_key": os.environ.get("OPENAI_API_KEY", ""),
            }
        ]
    }
    if os.environ.get("OPENAI_BASE_URL"):
        llm_config["config_list"][0]["base_url"] = os.environ["OPENAI_BASE_URL"]

    research_assistant = autogen.AssistantAgent(
        name="Research_Assistant",
        system_message="You are a research assistant. Use tools to find accurate information and answer clearly. If multiple questions are there, answer all of them.",
        llm_config=llm_config,
    )
    
    user_proxy = autogen.UserProxyAgent(
        name="User_Proxy",
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
        max_consecutive_auto_reply=2,
        code_execution_config=False,
    )

    autogen.agentchat.register_function(
        search_web,
        caller=research_assistant,
        executor=user_proxy,
        name="search_web",
        description="Useful for answering questions about current events or real-world facts."
    )
    
    autogen.agentchat.register_function(
        calculate,
        caller=research_assistant,
        executor=user_proxy,
        name="calculate",
        description="Useful for math calculations. Input should be a valid Python math expression."
    )

    user_input = "What is the square root of the number of countries in the world?, also give me the total population in world?."
    prompt = f"Please research and answer this question thoroughly: {user_input}"
    
    try:
        result = user_proxy.initiate_chat(
            research_assistant,
            message=prompt,
        )
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
