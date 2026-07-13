from fastapi import APIRouter, Depends
from service.rag_service import RAGService
from core import decode_token
from dto.request.rag import RAGSearchRequest

router = APIRouter(prefix="/rag")

@router.get("/search")
def search_news(request: RAGSearchRequest):
    return RAGService.search_news(request)