import asyncio
from datetime import datetime, time
import logging
from typing import List
from services.reddit_service import RedditService
from services.openai_service import OpenAIService
from services.database_service import DatabaseService
from services.stock_price_service import StockPriceService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self, tickers: List[str] = None):
        self.tickers = tickers or ["AAPL", "TSLA", "GOOGL", "MSFT", "NVDA"]
        self.reddit_service = RedditService()
        self.openai_service = OpenAIService()
        self.stock_price_service = StockPriceService()
        self.db_service = DatabaseService()
        self.is_running = False

    async def initialize_database(self):
        """데이터베이스 연결 초기화"""
        await self.db_service.connect()

    async def analyze_single_stock(self, ticker: str):
        """단일 주식 분석"""
        try:
            logger.info(f"Analyzing {ticker}...")

            # Reddit 데이터 수집
            posts = self.reddit_service.search_stock_mentions(ticker, limit=20)

            if not posts:
                logger.info(f"No posts found for {ticker}")
                return

            # OpenAI로 감정 분석 및 키워드 추출
            analyzed_posts = self.openai_service.analyze_posts_batch(posts)

            # 주식 가격 데이터 가져오기
            price_change = await self.stock_price_service.get_stock_price_change(ticker)

            # 모든 키워드 수집
            all_keywords = []
            total_sentiment = 0.0

            for post in analyzed_posts:
                all_keywords.extend(post.get('keywords', []))
                total_sentiment += post.get('sentiment', 0.0)

            # 평균 감정 점수 계산
            avg_sentiment = total_sentiment / len(analyzed_posts) if analyzed_posts else 0.0

            # 상위 키워드 추출 (빈도 기준)
            from collections import Counter
            keyword_counts = Counter(all_keywords)
            top_keywords = [k for k, v in keyword_counts.most_common(5)]

            # 데이터 구조화
            stock_data = {
                "ticker": ticker,
                "sentiment": round(avg_sentiment, 3),
                "mentions": len(analyzed_posts),
                "price_change_24h": price_change,
                "key_words": top_keywords,
                "posts": analyzed_posts
            }

            # 데이터베이스에 저장
            await self.db_service.save_stock_data(ticker, stock_data)

            logger.info(f"Successfully analyzed and saved data for {ticker}")

        except Exception as e:
            logger.error(f"Error analyzing {ticker}: {str(e)}")

    async def analyze_all_stocks(self):
        """모든 주식 분석"""
        logger.info("Starting batch analysis of all stocks...")
        tasks = []

        for ticker in self.tickers:
            tasks.append(self.analyze_single_stock(ticker))

        await asyncio.gather(*tasks)
        logger.info("Batch analysis completed")

    async def scheduled_task(self):
        """주기적으로 실행되는 작업"""
        while self.is_running:
            try:
                now = datetime.now()
                logger.info(f"Scheduled task running at {now}")

                await self.analyze_all_stocks()

                # 다음 실행까지 대기 (1시간)
                await asyncio.sleep(3600)

            except Exception as e:
                logger.error(f"Error in scheduled task: {str(e)}")
                await asyncio.sleep(60)  # 오류 시 1분 대기

    async def start_scheduler(self):
        """스케줄러 시작"""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return

        await self.initialize_database()
        self.is_running = True
        logger.info("Starting scheduler service")

        # 백그라운드에서 스케줄러 실행
        asyncio.create_task(self.scheduled_task())

    async def stop_scheduler(self):
        """스케줄러 중지"""
        self.is_running = False
        await self.db_service.disconnect()
        logger.info("Scheduler stopped")

    async def manual_run(self):
        """수동 실행"""
        await self.initialize_database()
        await self.analyze_all_stocks()
        await self.db_service.disconnect()