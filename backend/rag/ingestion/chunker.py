from langchain_text_splitters import RecursiveCharacterTextSplitter

class Chunker:
    def __init__(self, chunk_size: int, chunk_overlap: int):
        self.text_spliter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap
        )
    def split_text(self, text):
        if not text or not text.strip():
            return []
        return self.text_spliter.split_text(text)