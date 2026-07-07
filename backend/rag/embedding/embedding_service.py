from .embedding_model import EmbeddingModel

class EmbeddingService:
    def __init__(self):
        self.model = EmbeddingModel()
    def create_embedding(self, text):
        return self.model.encode_text(text)