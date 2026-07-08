from rag.vectorstore import MilvusManager
from rag.embedding import EmbeddingService
from .reranker import Reranker
from util import get_logger

logger = get_logger(__name__)

class VectorSearch:
    def __init__(self):
        milvus = MilvusManager()
        self.collection = milvus.get_or_create_collection()
        self.embedding = EmbeddingService()
        self.reranker = Reranker()
    def search(self, text: str, symbol: str, k:int = 20):
        vector = self.embedding.create_embedding(text)
        if vector is None or len(vector) == 0:
            logger.info("Không có dữ liệu")
            return []
        filter = f"symbol == '{symbol}'"
        res = self.collection.search(
            collection_name = 'news',
            data=[vector],
            anns_field="vector",
            search_param={"metric_type": "COSINE", "params": {"nprobe": 10}},
            limit=k,
            filter=filter,
            output_fields=["title", "link", "content", "source", "published_at"]
        )
        hits = res[0] if res else []
        documents = [
            {
                "title": h.entity.get("title"),
                "link": h.entity.get("link"),
                "content": h.entity.get("content"),
                "source": h.entity.get("source"),
                "published_at": h.entity.get("published_at"),
                "score": float(h.score),
            }
            for h in hits
        ]
        return self.reranker.rerank(query=text, documents=documents, k=5)