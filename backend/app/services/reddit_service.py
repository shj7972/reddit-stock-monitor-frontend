import praw
import os
from typing import List, Dict, Any
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedditService:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT', 'RedditStockMonitor/1.0')
        )

    def search_stock_mentions(self, ticker: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        특정 주식 티커와 관련된 Reddit 포스트를 검색합니다.
        """
        try:
            posts = []
            subreddits = ['stocks', 'investing', 'wallstreetbets', 'StockMarket']

            for subreddit_name in subreddits:
                subreddit = self.reddit.subreddit(subreddit_name)

                # 최근 24시간 내 포스트 검색
                for post in subreddit.search(f"{ticker}", limit=limit//len(subreddits), time_filter='day'):
                    if hasattr(post, 'title') and hasattr(post, 'score'):
                        posts.append({
                            'title': post.title,
                            'score': post.score,
                            'comments': post.num_comments,
                            'url': f"https://reddit.com{post.permalink}",
                            'created_utc': post.created_utc,
                            'subreddit': subreddit_name,
                            'selftext': getattr(post, 'selftext', '')[:500]  # 텍스트 일부만 저장
                        })

            logger.info(f"Found {len(posts)} posts for {ticker}")
            return posts

        except Exception as e:
            logger.error(f"Error searching Reddit for {ticker}: {str(e)}")
            return []

    def get_top_posts_by_mentions(self, tickers: List[str], limit: int = 10) -> Dict[str, List[Dict[str, Any]]]:
        """
        여러 티커에 대한 최고 점수 포스트들을 반환합니다.
        """
        results = {}
        for ticker in tickers:
            posts = self.search_stock_mentions(ticker, limit)
            # 점수 내림차순 정렬
            sorted_posts = sorted(posts, key=lambda x: x['score'], reverse=True)
            results[ticker] = sorted_posts[:limit]

        return results