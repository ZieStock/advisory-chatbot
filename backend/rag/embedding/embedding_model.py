from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
    def encode_text(self, text):
        if not text:
            return None
        return self.model.encode(text).tolist()