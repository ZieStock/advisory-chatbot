from fastapi import APIRouter, Depends
from service.bigquery_service import BigQueryService
from core import decode_token
from dto.request.stock import SymbolsRequest

router = APIRouter(prefix='/stock')
@router.get("/market/performance/{days}")
def get_market_index_performance(days: int):
    return BigQueryService.get_market_index_performance(days)
@router.get("/market/current")
def get_current_market_index():
    return BigQueryService.get_current_market_index()
@router.get("/market/breadth/{day}")
def get_market_breadth(day: int):
    return BigQueryService.get_market_breadth(day)
@router.get("/market/liquidity/{day}")
def get_market_liquidity(day: int):
    return BigQueryService.get_market_liquidity(day)
@router.get("/ohlc/latest-price")
def get_latest_stock_price():
    return BigQueryService.get_latest_stock_price()
@router.get("/ohlc/trend")
def get_stock_trend():
    return BigQueryService.get_stock_trend()
@router.get("/ohlc/performance/{day}")
def get_stock_performance(day: int):
    return BigQueryService.get_stock_performance(day)
@router.get("/ohlc/rsi")
def get_stock_rsi():
    return BigQueryService.get_stock_rsi()
@router.get("/ohlc/volume/{day}")
def get_stock_volume(day: int):
    return BigQueryService.get_stock_volume(day)
@router.get("/ohlc/price-range/{day}")
def get_price_range(request: SymbolsRequest, day: int):
    return BigQueryService.get_price_range(request.symbols, day)
@router.get("/ohlc/volatility/{day}")
def get_price_volatility(request: SymbolsRequest, day: int):
    return BigQueryService.get_price_volatility(request.symbols, day)
@router.get("/ohlc/ma20-distance")
def get_price_close_to_ma20(request: SymbolsRequest):
    return BigQueryService.get_price_close_to_ma20(request.symbols)
@router.get("/ohlc/history/{day}")
def get_price_history(request: SymbolsRequest, day: int):
    return BigQueryService.get_price_history(request.symbols, day)
@router.get("/ohlc/drawdown/{day}")
def get_drawdown(request: SymbolsRequest, day: int):
    return BigQueryService.get_drawdown(request.symbols, day)
@router.get("/ohlc/signal")
def get_price_signal(request: SymbolsRequest):
    return BigQueryService.get_price_signal(request.symbols)
@router.get("/company/{symbol}")
def get_company_profile(symbol: str):
    return BigQueryService.get_company_profile(symbol)
@router.get("/foreign/top")
def get_top_foreign_flow(day: int = 1, limit: int = 10, flow_type: str = "NET_BUY"):
    return BigQueryService.get_top_foreign_flow(day, limit, flow_type)
@router.get("/foreign/latest")
def get_foreign_investor_latest(request: SymbolsRequest):
    return BigQueryService.get_foreign_investor_latest(request.symbols)
@router.get("/foreign/flow/{day}")
def get_foreign_investor_flow(request: SymbolsRequest, day: int):
    return BigQueryService.get_foreign_investor_flow(request.symbols, day)
@router.get("/quote/latest")
def get_latest_quote(request: SymbolsRequest):
    return BigQueryService.get_latest_quote(request.symbols)
@router.get("/quote/history//{minute}")
def get_quote_history(request: SymbolsRequest, minute: int):
    return BigQueryService.get_quote_history(request.symbols, minute)
@router.get("/quote/spread")
def get_spread(request: SymbolsRequest):
    return BigQueryService.get_spread(request.symbols)
@router.get("/quote/imbalance")
def get_order_imbalance(request: SymbolsRequest):
    return BigQueryService.get_order_imbalance(request.symbols)
@router.get("/quote/history/{minute}")
def get_quote_history(request: SymbolsRequest, minute: int):
    return BigQueryService.get_quote_history(request.symbols, minute)
@router.get("/quote/latest")
def get_latest_quote(request: SymbolsRequest):
    return BigQueryService.get_latest_quote(request.symbols)
@router.get("/quote/bid-depth")
def get_bid_depth(request: SymbolsRequest):
    return BigQueryService.get_bid_depth(request.symbols)
@router.get("/quote/bid-pressure")
def get_bid_pressure(request: SymbolsRequest):
    return BigQueryService.get_bid_pressure(request.symbols)
@router.get("/quote/bid-volume-change/{minute}")
def get_bid_volume_change(request: SymbolsRequest, minute: int):
    return BigQueryService.get_bid_volume_change(request.symbols, minute)