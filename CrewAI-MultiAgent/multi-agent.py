import os
from crewai import LLM, Agent, Crew, Process, Task
from crewai.tools import tool
from langchain_community.utilities import SerpAPIWrapper

# openai or ollama
LLM_SERVICE_PROVIDER = 'ollama'

# Set up API keys in environment
os.environ["SEARCHAPI_API_KEY"] = "f31cASNCQt5XF1oEWoMb7zBj"
os.environ["OPENAI_API_KEY"] = "voc-37886132717535051986986aa553a15c3682.30552167"
os.environ["OPENAI_BASE_URL"] = "https://openai.vocareum.com/v1"
os.environ["SERPAPI_API_KEY"] = "1d1d303fb14a2440fb214906c43a16ef610490b7283aacc2269e6d063c4ce5db"
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini"

search = SerpAPIWrapper()

@tool("Web Search")
def search_tool(query : str) -> str:
    """This is a very useful to answering questions about the current events or real world incidents
    this accepts the query as parameter and performs an internet search and retrive contents from online sources
    and retrun to the caller"""
    result = search.run(query)
    return result

llm = None
if LLM_SERVICE_PROVIDER == 'openai':
    llm =  LLM(
        model = os.environ.get("OPENAI_MODEL_NAME", "gpt-4o-mini"),
        api_key = os.environ.get("OPENAI_API_KEY", ""),
        base_url = os.environ.get("OPENAI_BASE_URL", "")
    )

if LLM_SERVICE_PROVIDER == 'ollama':
    llm =  LLM(
        model = "ollama/qwen2.5:7b",
        base_url = 'http://localhost:11434'
    )


data_collection_agent = Agent(
    role = "Online Data Collector",
    goal = "Scrap and gather top news stories of the week about {topic}",
    backstory = (
        "You are an expert news aggregator. Your job is to source the web "
        "to find most relevent, popular, and breaking news articles "
    ),
    verbose= True,
    tool = [search_tool],
    llm = llm
)

curator_agent = Agent(
    role = "Newsletter curator and Editor",
    goal = "Filter the gathered news, select the best 5 articles and " \
    "write engaging summaries for a weekly news letter",
    backstory = (
        "You are a seasoned newsletter editor. You have a sharp "
        "eye for what captivates readers"
        "you filter out clickbait, remove duplicated and write punchy, "
        "2 line sentence summaries that make people want to read more."
    ),
    verbose= True,
    tool = [search_tool],
    llm = llm
)

data_collection_task = Task(
    description = 'Search the web for the top 10 most recent and impactful news articles about {topic}. '
        'Provide a list of these articles with their titles, URLs, and a brief snippet of content.',
    expected_output = 'A raw list of the top 10 news articles with titles, links, and short descriptions.',
    agent = data_collection_agent
)

curator_task = Task(
    description = ('Review the list of 10 articles provided by the Data collection Agent. '
        'Select the absolute best 5 articles. Filter out any spam or low-quality news. '
        'For each of the 5 articles, write a catchy 2-sentence summary. '
        'Format the final output as a polished markdown newsletter with an Intro, Body (the 5 articles), and Outro.'),
    expected_output='A fully formatted markdown newsletter with an intro, 5 curated articles with 2-sentence summaries, and an outro.',
    agent = curator_agent,
    output_file = "newsletter.md"
)

new_letter_crew = Crew(
    agents = [data_collection_agent, curator_agent],
    tasks = [data_collection_task, curator_task],
    process = Process.sequential,
    verbose = True
)

inputs = {'topic' : 'Artificial Intelligence and Agentic workflows'}
result = new_letter_crew.kickoff(inputs=inputs)
print(result)