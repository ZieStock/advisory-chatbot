from rag.embedding import EmbeddingService
from rag.vectorstore import MilvusManager
from rag.ingestion import Chunker, PdfOCR
from service import KafkaService
from util import parseTime

class RagService:
    def __init__(self):
        self.milvus = MilvusManager()
        self.embedding = EmbeddingService()
        self.milvus.get_or_create_collection()
        self.chunker = Chunker(chunk_size=1200, chunk_overlap=400)
        self.kafka = KafkaService('cafef')
        self.pdf_ocr = PdfOCR()
    def run(self):
        for msg in self.kafka.msg:
            title = msg.get('title', '')
            link = msg.get('link')
            content = msg.get('text', '')
            symbol = msg.get('symbol')
            published_at = int(dt.timestamp()) if (dt := parseTime(msg.get('time'))) else None
            pdfs = msg.get('pdfs', [])
            data = content if content is not None else ""
            for pdf_url in pdfs:
                pdf_bytes = self.pdf_ocr.download_pdf(pdf_url)
                if pdf_bytes:
                    pdf_text = self.pdf_ocr.extract_text(pdf_bytes)
                    data += "\n" + pdf_text
            chunks = self.chunker.split_text(data)
            for i, chunk in enumerate(chunks):
                vector = self.embedding.create_embedding(f"Tiêu đề: {title} | Nội dung: {chunk}")
                if vector:
                    self.milvus.insert_data(
                        [{
                            "title": f"{title}-{i}",
                            "link": link,
                            "symbol": symbol,
                            "content": chunk,
                            "published_at": published_at,
                            "vector": vector,
                        }]
                    )
if __name__ == "__main__":
    app = RagService()
    app.run()