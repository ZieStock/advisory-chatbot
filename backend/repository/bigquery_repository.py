from bigquery import client, execute
from util import load_setting
from google.cloud import bigquery

class MarketIndexRepository:
    @staticmethod
    def get_market_index_performance(day: int):
        query = f"""
            with range_data as(
                select indexName, time, valueIndexes
                from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_market_index`
                WHERE time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {day} DAY)
            ),
            calc as (
                select 
                    indexName,
                    first_value(valueIndexes) over(
                        partition by indexName
                        order by time asc
                    ) as start_value,
                    first_value(valueIndexes) over (
                        partition by indexName
                        order by time desc
                    ) as end_value
                from range_data
            )
            select distinct
                indexName,
                start_value,
                end_value,
                round (
                    ((end_value - start_value) / start_value) * 100, 2
                ) as change_percent
            from calc
        """
        return list(client.query(query).result())
    @staticmethod
    def get_current_market_index():
        query = f"""
            with latest_index as (
                select
                    indexName, time, valueIndexes,
                    lag(valueIndexes) over(partition by indexName order by time) as previous_value
                from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_market_index`
            )
            select
                indexName, time, valueIndexes as current_index,
                round(safe_divide(valueIndexes -previous_value, previous_value)* 100, 2) as change_percent,
                case
                    when valueIndexes > previous_value then 'UP'
                    when valueIndexes < previous_value then 'DOWN'
                    else 'FLAT'
                end as market_status
            from latest_index
            qualify ROW_NUMBER() OVER(
                PARTITION BY indexName
                ORDER BY time DESC
            ) = 1;
        """
        return list(client.query(query).result())
    @staticmethod
    def get_market_breadth(day: int):
        query = f"""
            select
                indexName,
                sum(fluctuationUpIssueCount) AS total_up,
                sum(fluctuationDownIssueCount) AS total_down,
                round(
                    safe_divide(
                        sum(fluctuationUpIssueCount),
                        safe_add(sum(fluctuationUpIssueCount), sum(fluctuationDownIssueCount))) * 100,
                    2
                ) as up_ratio
            from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_market_index`
            where time >= timestamp_sub(current_timestamp(), interval {day} day)
            group by indexName
        """
        return list(client.query(query).result())
    @staticmethod
    def get_market_liquidity(day: int):
        query = f"""
            select
                indexName,
                sum(totalVolumeTraded) as total_volume,
                sum(grossTradeAmount) as total_amount
            from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_market_index`
            where time >= timestamp_sub(current_timestamp(), interval {day} day)
            group by indexName
        """
        return list(client.query(query).result())
class OhlcRepository:
    @staticmethod
    def get_latest_stock_price():
        query = f"""
            with latest as (
                select
                    symbol, time, close,
                    lag(close) over(partition by symbol order by time) as previous_close
                from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_feature`
                where time >= timestamp_sub(current_timestamp(), interval 5 day)
            )
            select
                symbol, time, close as current_price,
                round(
                    safe_divide(close-previous_close, previous_close) * 100,2
                )as change_percent
            from latest
            qualify row_number() over(partition by symbol order by time desc)=1;
        """
        return list(client.query(query).result())
    @staticmethod
    def get_price_range(symbols: list[str], day: int):
        query = f"""
            select
                symbol,
                min(low) as lowest_price,
                max(high) as highest_price,
                avg(close) as average_close
            from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_feature`
            where symbol in unnest (@symbols) and time >= timestamp_sub(current_timestamp(), interval {day} day) group by symbol
        """
        return execute(
            query,
            [bigquery.ArrayQueryParameter("symbols", "STRING", symbols)]
        )
    @staticmethod
    def get_price_volatility(symbols: list[str], day: int):
        query = f"""
            select
                symbol,
                round(stddev(close), 2) as volatility
            from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_feature`
            where symbol in unnest (@symbols) and time >= timestamp_sub(current_timestamp(), interval {day} day) group by symbol
        """
        return execute(
            query,
            [bigquery.ArrayQueryParameter("symbols", "STRING", symbols)]
        )
    @staticmethod
    def get_price_close_to_ma20(symbols: list[str]):
        query = f"""
            select
                symbol,
                time,
                MA2O,
                round(safe_divide(close-MA2O, MA2O)*100, 2) as distance_percent
            from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_feature`
            where symbol in unnest (@symbols) qualify row_number() over(partition by symbol order by time desc)=1
        """
        return execute(
            query,
            [bigquery.ArrayQueryParameter("symbols", "STRING", symbols)]
        )
    @staticmethod
    def get_price_history(symbols: list[str], day: int):
        query = f"""
            select
                symbol,
                time,
                open,
                high,
                low,
                close,
                volume
            from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_feature`
            where symbol in unnest (@symbols) and time >= timestamp_sub(current_timestamp(), interval {day} day) order by symbol, time
        """
        return execute(
            query,
            [bigquery.ArrayQueryParameter("symbols", "STRING", symbols)]
        )
    @staticmethod
    def get_drawdown(symbols: list[str], day: int):
        query = f"""
            with price_data as(
                select
                    symbol,
                    time,
                    close,
                    max(close) over(partition by symbol) as highest_price
                from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_feature`
                where symbol in unnest (@symbols) and time >= timestamp_sub(current_timestamp(), interval {day} day)
            )
            select
                symbol,
                highest_price,
                close as current_price,
                round(safe_divide(close-highest_price,highest_price)*100, 2) as drawdown_percent
            from price_data
            qualify row_number() over(partition by symbol order by time desc) = 1
        """
        return execute(
            query,
            [bigquery.ArrayQueryParameter("symbols", "STRING", symbols)]
        )
    @staticmethod
    def get_price_signal(symbols:list[str]):
        query=f"""
            select
                symbol,
                close,
                MA2O,
                ma50,
                case
                    when close > MA2O and MA2O > ma50
                    then 'STRONG_UPTREND'
                    when close < MA2O and MA2O < ma50
                    then 'STRONG_DOWNTREND'
                    when close > MA2O
                    then 'RECOVERING'
                    else 'WEAK'
                end as signal
            from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_feature`
            where symbol in unnest (@symbols) qualify row_number() over(partition by symbol order by time desc)=1
        """
        return execute(
            query,
            [bigquery.ArrayQueryParameter("symbols", "STRING", symbols)]
        )
    @staticmethod
    def get_stock_trend():
        query = f"""
            select
                symbol, time, close, MA2O, ma50,
                case
                    when MA2O > ma50 then 'UPTREND'
                    when MA2O < ma50 then 'DOWNTREND'
                    else 'SIDEWAY'
                end as trend
            from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_feature`
            where time >= timestamp_sub(current_timestamp(), interval 5 day)
            qualify row_number() over(partition by symbol order by time desc)=1;
        """
        return list(client.query(query).result())
    @staticmethod
    def get_stock_performance(day: int):
        query = f"""
            with price_range as (
                select
                    symbol, time, close
                from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_feature`
                where time >= timestamp_sub(current_timestamp(), interval {day} day)
            ),
            calc as (
                select
                    symbol,
                    first_value(close) over(partition by symbol order by time) as start_price,
                    first_value(close) over(partition by symbol order by time desc) as end_price
                from price_range
            )
            select distinct
                symbol,
                round( safe_divide(end_price - start_price,start_price)*100, 2) as return_percent
            from calc;
        """
        return list(client.query(query).result())
    @staticmethod
    def get_stock_rsi():
        query = f"""
            select
                symbol, close, rsi,
                case
                    when rsi >= 70
                        then 'OVERBOUGHT'
                    when rsi <= 30
                        then 'OVERSOLD'
                    else 'NORMAL'
                end as rsi_signal
            from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_feature`
            where time >= timestamp_sub(current_timestamp(), interval 5 day)
            qualify row_number() over(partition by symbol order by time desc)=1;
        """
        return list(client.query(query).result())
    @staticmethod
    def get_stock_volume(day: int):
        query = f"""
            SELECT
                symbol,
                avg(volume) as avg_volume,
                sum(volume) as total_volume
            from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_feature`
            where time >= timestamp_sub(current_timestamp(), interval {day} day)
            group by symbol;
        """
        return list(client.query(query).result())
class StockCompanyRepository:
    @staticmethod
    def get_company_profile(symbol: str):
        query = f"""
            select
                symbol, company_name_vi, company_name_en, exchange, sector, industry
            from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.dim_company`
            where symbol = '{symbol}'
        """
        return list(client.query(query).result())
class ForeignInvestorRepository:
    @staticmethod
    def get_foreign_investor_latest(symbols: list[str]):
        query = f"""
            SELECT
                symbol, time, buyVolume, sellVolume, buyTradedAmount, sellTradedAmount, netVolume, netAmount,
                case
                    when netAmount > 0 then 'NET_BUY'
                    when netAmount < 0 then 'NET_SELL'
                    else 'NEUTRAL'
                end as foreign_signal
            from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_foreign_investor`
            where symbol in unnest (@symbols) and time >= timestamp_sub(current_timestamp(), interval 5 day)
            qualify row_number() over(partition by symbol order by time desc) = 1
        """
        return execute(
            query,
            [bigquery.ArrayQueryParameter("symbols", "STRING", symbols)]
        )
    @staticmethod
    def get_foreign_investor_flow(symbols: list[str], day: int):
        query = f"""
            select
                symbol,
                sum(buyTradedAmount) as total_buy_amount,
                sum(sellTradedAmount) as total_sell_amount,
                sum(netAmount) as net_foreign_amount,
                case
                    when sum(netAmount) > 0 then 'NET_BUY'
                    when sum(netAmount) < 0 then 'NET_SELL'
                    else 'NEUTRAL'
                end as foreign_trend
            from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_foreign_investor`
            where symbol in unnest (@symbols)
            and time >= timestamp_sub(current_timestamp(), interval {day} day)
            group by symbol
        """
        return execute(
            query,
            [bigquery.ArrayQueryParameter("symbols", "STRING", symbols)]
        )
    @staticmethod
    def get_top_foreign_flow(day: int, limit: int, flow_type: str):
        is_net_buy = flow_type.upper() == 'NET_BUY'
        condition = "total_net_amount > 0" if is_net_buy else "total_net_amount < 0"
        order_direction = "DESC" if is_net_buy else "ASC"
        query = f"""
            with aggregated_flow as (
                select
                    symbol,
                    sum(buyTradedAmount) as total_buy_amount,
                    sum(sellTradedAmount) as total_sell_amount,
                    sum(netAmount) as total_net_amount
                from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_foreign_investor`
                where time >= timestamp_sub(current_timestamp(), interval {day} day) group by symbol
            )
            select
                symbol,
                total_buy_amount,
                total_sell_amount,
                total_net_amount
            from aggregated_flow
            where {condition} order by total_net_amount {order_direction} limit {limit}
        """
        return list(client.query(query).result())
class QuoteRepository:
    @staticmethod
    def get_latest_quote(symbols: list[str]):
        query = f"""
            select
                symbol,
                time,
                bid_price_1,
                bid_volume_1,
                bid_price_2,
                bid_volume_2,
                bid_price_3,
                bid_volume_3
            from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_quote`
            where symbol in unnest (@symbols) qualify row_number() over(partition by symbol  order by time desc) = 1
        """
        return execute(
            query,
            [bigquery.ArrayQueryParameter("symbols", "STRING", symbols)]
        )
    @staticmethod
    def get_quote_history(symbols: list[str], minute: int):
        query = f"""
            select
                symbol,
                time,
                bid_price_1,
                bid_volume_1,
                bid_price_2,
                bid_volume_2,
                bid_price_3,
                bid_volume_3
            from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_quote`
            where symbol in unnest (@symbols) and time >= timestamp_sub(current_timestamp(), interval {minute} minute) order by symbol, time
        """
        return execute(
            query,
            [bigquery.ArrayQueryParameter("symbols", "STRING", symbols)]
        )
    @staticmethod
    def get_bid_depth(symbols: list[str]):
        query = f"""
            select
                symbol,
                time,
                bid_volume_1,
                bid_volume_2,
                bid_volume_3,
                (bid_volume_1 + bid_volume_2 + bid_volume_3) as total_bid_volume
            from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_quote`
            where symbol in unnest (@symbols) qualify row_number() over( partition by symbol order by time desc) = 1
        """
        return execute(
            query,
            [bigquery.ArrayQueryParameter("symbols","STRING", symbols)]
        )
    @staticmethod
    def get_bid_pressure(symbols: list[str]):
        query = f"""
            select
                symbol,
                time,
                safe_divide(bid_volume_1, bid_volume_1 + bid_volume_2 + bid_volume_3) as bid_pressure
            from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_quote`
            where symbol in unnest (@symbols) qualify row_number() over(partition by symbol order by time desc) = 1
        """
        return execute(
            query,
            [bigquery.ArrayQueryParameter("symbols","STRING", symbols)]
        )
    @staticmethod
    def get_bid_volume_change(symbols: list[str], minute: int):
        query = f"""
            with quote_data as(
                select
                    symbol,
                    time,
                    (bid_volume_1 + bid_volume_2 + bid_volume_3) as total_bid_volume,
                    lag(bid_volume_1 +bid_volume_2 + bid_volume_3) over(partition by symbol order by time) as previous_bid_volume
                from `{load_setting.PROJECT_ID}.{load_setting.BIGQUERY_DATASET}.fact_quote`
                where symbol in unnest (@symbols) and time >= timestamp_sub(current_timestamp(), interval {minute} minute)
            )
            select
                symbol,
                time,
                total_bid_volume,
                total_bid_volume - previous_bid_volume as volume_change
            from quote_data order by symbol, time
        """
        return execute(
            query,
            [bigquery.ArrayQueryParameter("symbols","STRING", symbols)]
        )