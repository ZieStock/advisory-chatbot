from repository import MarketIndexRepository, OhlcRepository, StockCompanyRepository, ForeignInvestorRepository, QuoteRepository

class BigQueryService:
    @staticmethod
    def get_market_index_performance(day: int):
        return MarketIndexRepository.get_market_index_performance(day)
    @staticmethod
    def get_current_market_index():
        return MarketIndexRepository.get_current_market_index()
    @staticmethod
    def get_market_breadth(day: int):
        return MarketIndexRepository.get_market_breadth(day)
    @staticmethod
    def get_price_signal(symbols: list[str]):
        return OhlcRepository.get_price_signal(symbols)
    @staticmethod
    def get_stock_trend():
        return OhlcRepository.get_stock_trend()
    @staticmethod
    def get_stock_rsi():
        return OhlcRepository.get_stock_rsi()
    @staticmethod
    def get_drawdown(symbols: list[str], day: int):
        return OhlcRepository.get_drawdown(symbols, day)
    @staticmethod
    def get_foreign_investor_flow(symbols: list[str], day: int):
        return ForeignInvestorRepository.get_foreign_investor_flow(symbols, day)
    @staticmethod
    def get_top_foreign_flow(day: int, limit: int, flow_type: str):
        return ForeignInvestorRepository.get_top_foreign_flow(day, limit, flow_type)
    @staticmethod
    def get_price_volatility(symbols: list[str], day: int):
        return OhlcRepository.get_price_volatility(symbols, day)

    @staticmethod
    def get_quote_history(symbols: list[str], minute: int):
        return  QuoteRepository.get_quote_history(symbols, minute)
    @staticmethod
    def get_latest_quote(symbols: list[str]):
        return QuoteRepository.get_latest_quote(symbols)
    @staticmethod
    def get_price_history(symbols: list[str], day: int):
        return OhlcRepository.get_price_history(symbols, day)
    @staticmethod
    def get_price_close_to_ma20(symbols: list[str]):
        return OhlcRepository.get_price_close_to_ma20(symbols)
    @staticmethod
    def get_price_range(symbols: list[str], day: int):
        return OhlcRepository.get_price_range(symbols, day)
    @staticmethod
    def get_market_liquidity(day: int):
        return MarketIndexRepository.get_market_liquidity(day)
    @staticmethod
    def get_latest_stock_price():
        return OhlcRepository.get_latest_stock_price()
    @staticmethod
    def get_stock_performance(day):
        return OhlcRepository.get_stock_performance(day)
    @staticmethod
    def get_stock_volume(day):
        return OhlcRepository.get_stock_volume(day)
    @staticmethod
    def get_company_profile(symbol):
        return StockCompanyRepository.get_company_profile(symbol)
    @staticmethod
    def get_foreign_investor_latest(symbols: list[str]):
        return ForeignInvestorRepository.get_foreign_investor_latest(symbols)
    @staticmethod
    def get_bid_depth(symbols: list[str]):
        return QuoteRepository.get_bid_depth(symbols)
    @staticmethod
    def get_bid_pressure(symbols: list[str]):
        return QuoteRepository.get_bid_pressure(symbols)
    @staticmethod
    def get_bid_volume_change(symbols: list[str], minute: int):
        return QuoteRepository.get_bid_volume_change(symbols, minute)
