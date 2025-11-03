from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging
from models.stock_data import StockData, RedditPost

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.database = None
        self.stock_collection = None

    async def connect(self):
        """MongoDB 연결"""
        try:
            mongodb_url = os.getenv('MONGODB_URL')
            self.client = AsyncIOMotorClient(mongodb_url)
            # 연결 테스트
            await self.client.admin.command('ping')
            self.database = self.client['reddit_stock_monitor']
            self.stock_collection = self.database['stock_data']
            logger.info("Connected to MongoDB")
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    async def disconnect(self):
        """MongoDB 연결 해제"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")

    async def save_stock_data(self, ticker: str, data: Dict[str, Any]):
        """주식 데이터를 MongoDB에 저장"""
        try:
            # 마지막 업데이트 시간 추가
            data['last_updated'] = datetime.utcnow()
            data['ticker'] = ticker.upper()

            # upsert: 존재하면 업데이트, 없으면 삽입
            result = await self.stock_collection.replace_one(
                {'ticker': ticker.upper()},
                data,
                upsert=True
            )
            logger.info(f"Saved data for {ticker}: {result.modified_count if result.modified_count > 0 else 'inserted'}")
            return result
        except Exception as e:
            logger.error(f"Error saving stock data for {ticker}: {str(e)}")
            raise

    async def get_stock_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        """특정 주식 데이터를 조회"""
        try:
            data = await self.stock_collection.find_one({'ticker': ticker.upper()})
            return data
        except Exception as e:
            logger.error(f"Error retrieving stock data for {ticker}: {str(e)}")
            raise

    async def get_all_stock_data(self) -> List[Dict[str, Any]]:
        """모든 주식 데이터를 조회"""
        try:
            cursor = self.stock_collection.find({})
            data = await cursor.to_list(length=None)
            return data
        except Exception as e:
            logger.error(f"Error retrieving all stock data: {str(e)}")
            raise

    async def delete_old_data(self, days: int = 7):
        """지정된 일수보다 오래된 데이터를 삭제"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            result = await self.stock_collection.delete_many(
                {'last_updated': {'$lt': cutoff_date}}
            )
            logger.info(f"Deleted {result.deleted_count} old records")
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error deleting old data: {str(e)}")
            raise

    async def get_recent_mentions(self, ticker: str, hours: int = 24) -> List[Dict[str, Any]]:
        """최근 N시간 내의 멘션 데이터를 조회"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            cursor = self.stock_collection.find({
                'ticker': ticker.upper(),
                'last_updated': {'$gte': cutoff_time}
            })
            data = await cursor.to_list(length=None)
            return data
        except Exception as e:
            logger.error(f"Error retrieving recent mentions for {ticker}: {str(e)}")
            raise