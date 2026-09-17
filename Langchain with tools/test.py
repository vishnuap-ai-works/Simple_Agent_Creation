import os
import serpapi

from langchain_community.utilities import SearchApiAPIWrapper

import os
os.environ["SEARCHAPI_API_KEY"] = "f31cASNCQt5XF1oEWoMb7zBj"

# Tool - 1
search = SearchApiAPIWrapper()

result = search.run("Top 10 countries in the world")
print(result)