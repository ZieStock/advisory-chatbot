from rag.retrieval.vector_search import VectorSearch
from dto.request.rag import RAGSearchRequest

class RAGService:
    vector_search = VectorSearch()
    @staticmethod
    def search_news(request: RAGSearchRequest):
        return RAGService.vector_search.search(
            text=request.text,
            symbol=request.symbol,
            k=request.k
        )