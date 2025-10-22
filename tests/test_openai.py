# test_openai.py
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

llm_response = llm.predict("Hello, how are you?")
print(llm_response)