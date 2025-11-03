from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
import time
import asyncio
from services.reddit_service import RedditService
from services.openai_service import OpenAIService
from services.database_service import DatabaseService
from services.stock_price_service import StockPriceService
from models.stock_data import StockDataResponse, StockDetailResponse

router = APIRouter()

async def get_db_service():
    db_service = DatabaseService()
    try:
        await db_service.connect()
        yield db_service
    finally:
        await db_service.disconnect()

@router.get("/stocks")
async def get_stock_data(db_service: DatabaseService = Depends(get_db_service)) -> Dict[str, Any]:
    """
    모든 주식 데이터를 반환합니다.
    """
    try:
        stock_data_list = await db_service.get_all_stock_data()

        # 데이터를 적절한 형식으로 변환
        stocks = {}
        total_mentions = 0

        for stock_data in stock_data_list:
            ticker = stock_data['ticker']
            stocks[ticker] = {
                "sentiment": stock_data.get('sentiment', 0.0),
                "mentions": stock_data.get('mentions', 0),
                "price_change_24h": stock_data.get('price_change_24h'),
                "key_words": stock_data.get('key_words', []),
                "posts": stock_data.get('posts', [])
            }
            total_mentions += stock_data.get('mentions', 0)

        return {
            "timestamp": int(time.time()),
            "stocks": stocks,
            "total_mentions": total_mentions,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터 조회 실패: {str(e)}")

@router.post("/stocks/{ticker}/analyze")
async def analyze_stock(ticker: str):
    """
    특정 주식에 대한 실시간 데이터 수집 및 분석을 수행합니다.
    """
    ticker = ticker.upper()

    try:
        # 서비스 인스턴스 생성
        reddit_service = RedditService()
        openai_service = OpenAIService()
        stock_price_service = StockPriceService()
        db_service = DatabaseService()
        await db_service.connect()

        # Reddit 데이터 수집
        posts = reddit_service.search_stock_mentions(ticker, limit=20)

        # OpenAI로 감정 분석 및 키워드 추출
        analyzed_posts = openai_service.analyze_posts_batch(posts)

        # 주식 가격 데이터 가져오기
        price_change = await stock_price_service.get_stock_price_change(ticker)

        # 모든 키워드 수집
        all_keywords = []
        total_sentiment = 0.0

        for post in analyzed_posts:
            all_keywords.extend(post['keywords'])
            total_sentiment += post['sentiment']

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
        await db_service.save_stock_data(ticker, stock_data)

        await db_service.disconnect()

        return {
            "timestamp": int(time.time()),
            "ticker": ticker,
            "status": "success",
            "message": f"{ticker} 데이터 분석 및 저장 완료"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 실패: {str(e)}")

@router.get("/stocks/{ticker}")
async def get_stock_detail(ticker: str, db_service: DatabaseService = Depends(get_db_service)) -> Dict[str, Any]:
    """
    특정 주식의 상세 데이터를 반환합니다.
    """
    ticker = ticker.upper()

    try:
        stock_data = await db_service.get_stock_data(ticker)
        if not stock_data:
            raise HTTPException(status_code=404, detail=f"주식 {ticker}을 찾을 수 없습니다")

        return {
            "timestamp": int(time.time()),
            "ticker": ticker,
            "data": {
                "sentiment": stock_data.get('sentiment', 0.0),
                "mentions": stock_data.get('mentions', 0),
                "price_change_24h": stock_data.get('price_change_24h'),
                "key_words": stock_data.get('key_words', []),
                "posts": stock_data.get('posts', [])
            },
            "status": "success"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터 조회 실패: {str(e)}")