from langchain.tools import tool
from rag.retrieval.vector_search import VectorSearch
from util import get_logger
from service.bigquery_service import BigQueryService
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
    @tool(description="Lấy tổng quan chỉ số thị trường hiện tại")
    def get_current_market_index():
        res = BigQueryService.get_current_market_index()
        logger.info(res)
        return res
    @tool(description="Lấy hiệu suất chỉ số thị trường trong N ngày gần nhất. Cần cung cấp số ngày (day)")
    def get_market_index_performance(day: int):
        res = BigQueryService.get_market_index_performance(day)
        logger.info(res)
        return res
    @tool(description="Lấy độ rộng thị trường (số mã tăng/giảm) trong N ngày gần nhất. Cần cung cấp số ngày (day)")
    def get_market_breadth(day: int):
        res = BigQueryService.get_market_breadth(day)
        logger.info(res)
        return res
    @tool(description="Lấy giá cổ phiếu mới nhất và % thay đổi so với phiên trước")
    def get_latest_stock_price():
        res = BigQueryService.get_latest_stock_price()
        logger.info(res)
        return res
    @tool(description="Lấy xu hướng cổ phiếu (UPTREND/DOWNTREND/SIDEWAY) dựa trên MA20 và MA50")
    def get_stock_trend():
        res = BigQueryService.get_stock_trend()
        logger.info(res)
        return res
    @tool(description="Lấy tín hiệu hành động của cổ phiếu (STRONG_UPTREND, STRONG_DOWNTREND, RECOVERING, WEAK). Cần cung cấp danh sách mã chứng khoán (symbols)")
    def get_price_signal(symbols: list[str]):
        res = BigQueryService.get_price_signal(symbols)
        logger.info(res)
        return res
    @tool(description="Lấy chỉ số RSI của cổ phiếu và tín hiệu quá mua/quá bán (OVERBOUGHT/OVERSOLD/NORMAL)")
    def get_stock_rsi():
        res = BigQueryService.get_stock_rsi()
        logger.info(res)
        return res
    @tool(description="Lấy mức sụt giảm của cổ phiếu so với đỉnh giá trong N ngày. Cần cung cấp danh sách mã chứng khoán (symbols) và số ngày (day)")
    def get_drawdown(symbols: list[str], day: int):
        res = BigQueryService.get_drawdown(symbols, day)
        logger.info(res)
        return res
    @tool(description="Lấy dòng tiền mua/bán ròng của khối ngoại theo mã trong N ngày. Cần cung cấp danh sách mã chứng khoán (symbols) và số ngày (day)")
    def get_foreign_investor_flow(symbols: list[str], day: int):
        res = BigQueryService.get_foreign_investor_flow(symbols, day)
        logger.info(res)
        return res
    @tool(description="Lấy danh sách top mã được khối ngoại mua ròng hoặc bán ròng nhiều nhất trong N ngày. Cần cung cấp số ngày (day), số lượng kết quả (limit) và loại dòng tiền (flow_type: NET_BUY hoặc NET_SELL)")
    def get_top_foreign_flow(day: int, limit: int, flow_type: str):
        res = BigQueryService.get_top_foreign_flow(day, limit, flow_type)
        logger.info(res)
        return res
    @tool(description="Lấy thông tin hồ sơ công ty (tên, sàn giao dịch, ngành, lĩnh vực). Cần cung cấp mã chứng khoán (symbol)")
    def get_company_profile(symbol: str):
        res = BigQueryService.get_company_profile(symbol)
        logger.info(res)
        return res
    return [search_news, get_current_market_index, get_market_index_performance, get_market_breadth, get_latest_stock_price,
            get_stock_trend, get_price_signal, get_stock_rsi, get_drawdown, get_foreign_investor_flow,
            get_top_foreign_flow, get_company_profile]