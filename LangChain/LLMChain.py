from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer."),
    ("user","{input}")
])
output_parser = StrOutputParser()

chain = prompt | llm | output_parser

result = chain.invoke({"input": "how can langsmith help with testing?"})
print(result)