from repository import MarketIndexRepository, OhlcRepository, StockCompanyRepository, ForeignInvestorRepository

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
    def get_market_liquidity(day: int):
        return MarketIndexRepository.get_market_liquidity(day)
    @staticmethod
    def get_latest_stock_price():
        return OhlcRepository.get_latest_stock_price()
    @staticmethod
    def get_stock_trend():
        return OhlcRepository.get_stock_trend()
    @staticmethod
    def get_stock_performance(day):
        return OhlcRepository.get_stock_performance(day)
    @staticmethod
    def get_stock_rsi():
        return OhlcRepository.get_stock_rsi()
    @staticmethod
    def get_stock_volume(day):
        return OhlcRepository.get_stock_volume(day)
    @staticmethod
    def get_company_profile(symbol):
        return StockCompanyRepository.get_company_profile(symbol)
    @staticmethod
    def get_foreign_investor_latest(symbol):
        return ForeignInvestorRepository.get_foreign_investor_latest(symbol)
    @staticmethod
    def get_foreign_investor_flow(symbol: str, day: int):
        return ForeignInvestorRepository.get_foreign_investor_flow(symbol, day)