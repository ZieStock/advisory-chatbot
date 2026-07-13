from fastapi import APIRouter, Depends
from service.bigquery_service import BigQueryService
from core import decode_token

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
@router.get("/company/{symbol}")
def get_company_profile(symbol: str):
    return BigQueryService.get_company_profile(symbol)
@router.get("/foreign/{symbol}/latest")
def get_foreign_investor_latest(symbol: str):
    return BigQueryService.get_foreign_investor_latest(symbol)
@router.get("/foreign/{symbol}/flow/{day}")
def get_foreign_investor_flow(symbol: str, day: int):
    return BigQueryService.get_foreign_investor_flow(symbol, day)