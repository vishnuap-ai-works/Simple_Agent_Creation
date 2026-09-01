import os
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Using the API key from your previous script
api_key = ""

llm = ChatOpenAI(
    model="", base_url="", api_key=api_key
)

print("=== Standard PromptTemplate Example ===")
# Example 1: Standard PromptTemplate
template = (
    "Generate a creative list of 3 potential names for a startup that makes {product}."
)
prompt = PromptTemplate.from_template(template)

formatted_prompt = prompt.format(product="smart coffee mugs")
print(f"Formatted Prompt:\n{formatted_prompt}\n")

# Calling the LLM with the formatted prompt
chain1 = prompt | llm
response1 = chain1.invoke({"product": "smart coffee mugs"})
print("Response:")
print(response1.content)
print("\n" + "=" * 40 + "\n")

print("=== ChatPromptTemplate Example ===")

# Example 2: ChatPromptTemplate (Recommended for Chat Models)
chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a knowledgeable historian. Give brief, 1-2 sentence answers about {topic}.",
        ),
        ("user", "{question}"),
    ]
)

chain2 = chat_prompt | llm

topic = "Ancient Rome"
question = "Who was the first emperor?"

print(f"Topic: {topic}")
print(f"Question: {question}\n")

print("Response:")
response2 = chain2.invoke({"topic": topic, "question": question})
print(response2.content)
