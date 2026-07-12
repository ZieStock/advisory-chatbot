from langchain.tools import tool
from rag.retrieval.vector_search import VectorSearch
from util import get_logger

logger = get_logger(__name__)

class ToolChatbot:
    def __init__(self):
        self.vector_search = VectorSearch()
    def search_knowledge(self, text: str, symbol: str):
        return self.vector_search.search(text, symbol)

chatbot = ToolChatbot()
def build_tool():
    @tool(description="Tìm kiếm tin tức chứng khoán từ cơ sở dữ liệu Milvus với dữ liệu, Cần cung cấp văn bản tìm kiếm (text) và mã chứng khoán (symbol)")
    def search_news(text: str, symbol: str):
        res = chatbot.search_knowledge(text, symbol)
        logger.info(res)
        return [
            {
                "title": item.get("title"),
                "content": item.get("content")
            }
            for item in res
        ]
    return [search_news]