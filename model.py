from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
model1 = ChatOpenAI(model="gpt-4o", temperature=0)
model2= ChatOpenAI(model="gpt-4o-mini", temperature=0)
model3 = ChatOpenAI(model="claude-3-5-sonnet", temperature=0)
model4 = ChatOpenAI(model="gpt-5.4-mini", temperature=0)
