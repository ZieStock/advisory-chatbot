from pymilvus.model.reranker import BGERerankFunction

class Reranker:
    def __init__(self, model_name: str = "BAAI/bge-reranker-v2-m3", device: str = 'cpu'):
        self.reranker = BGERerankFunction(model_name=model_name, device=device)
    def rerank(self, query: str, documents: list, k: int = 5):
        if not documents:
            return []
        texts = [
            f"{doc['title']}\n{doc['content']}"
            for doc in documents
        ]
        results = self.reranker(
            query=query,
            documents=texts,
            top_k=k,
        )
        reranked = []
        for r in results:
            doc = documents[r.index].copy()
            doc["rerank_score"] = float(r.score)
            reranked.append(doc)
        return reranked