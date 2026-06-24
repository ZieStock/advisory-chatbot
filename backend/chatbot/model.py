from langchain_openai import ChatOpenAI
from util import load_setting
def get_llm():
    return ChatOpenAI(
        model = 'gpt-4o-mini',
        temperature = 0.1,
        api_key = load_setting.OPENAI_API_KEY
    )