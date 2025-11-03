import aiohttp
import os
from typing import Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockPriceService:
    def __init__(self):
        # 무료 주식 API 사용 (Alpha Vantage 등)
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')  # demo 키로 제한적 사용 가능
        self.base_url = "https://www.alphavantage.co/query"

    async def get_stock_price_change(self, ticker: str) -> Optional[float]:
        """
        주식의 24시간 가격 변동을 퍼센트로 반환합니다.
        실제 구현에서는 유료 주식 API를 사용하는 것이 좋습니다.
        """
        try:
            # 현재는 시뮬레이션된 데이터 반환
            # 실제로는 Alpha Vantage나 다른 주식 API를 사용
            import random
            price_change = round(random.uniform(-5.0, 5.0), 2)
            return price_change

        except Exception as e:
            logger.error(f"Error getting stock price for {ticker}: {str(e)}")
            return None

    async def get_intraday_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        주식의 인트라데이 데이터를 가져옵니다.
        """
        try:
            params = {
                'function': 'TIME_SERIES_INTRADAY',
                'symbol': ticker,
                'interval': '5min',
                'apikey': self.api_key
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        logger.warning(f"Alpha Vantage API returned status {response.status}")
                        return None

        except Exception as e:
            logger.error(f"Error fetching intraday data for {ticker}: {str(e)}")
            return None

    async def get_batch_price_changes(self, tickers: list) -> Dict[str, float]:
        """
        여러 티커의 가격 변동을 일괄 조회합니다.
        """
        results = {}
        for ticker in tickers:
            change = await self.get_stock_price_change(ticker)
            if change is not None:
                results[ticker] = change
        return results