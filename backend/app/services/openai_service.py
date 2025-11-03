import openai
import os
import json
from typing import List, Dict, Any, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def analyze_sentiment(self, text: str) -> float:
        """
        텍스트의 감정을 분석하여 -1(부정)에서 1(긍정) 사이의 점수를 반환합니다.
        """
        try:
            prompt = f"""
            다음 텍스트의 감정을 분석하여 -1(매우 부정)에서 1(매우 긍정) 사이의 점수로 평가해주세요.
            응답은 JSON 형식으로만 반환하세요: {{"sentiment": 0.5}}

            텍스트: {text}
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50,
                temperature=0.3
            )

            result = response.choices[0].message.content.strip()
            sentiment_data = json.loads(result)
            sentiment_score = float(sentiment_data.get('sentiment', 0))

            # 범위 제한
            sentiment_score = max(-1, min(1, sentiment_score))

            return sentiment_score

        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return 0.0

    def extract_keywords(self, text: str, max_keywords: int = 5) -> List[str]:
        """
        텍스트에서 주요 키워드를 추출합니다.
        """
        try:
            prompt = f"""
            다음 텍스트에서 최대 {max_keywords}개의 주요 키워드를 추출해주세요.
            주식과 투자 관련 키워드를 우선적으로 선택하세요.
            응답은 JSON 형식으로만 반환하세요: {{"keywords": ["keyword1", "keyword2"]}}

            텍스트: {text}
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.3
            )

            result = response.choices[0].message.content.strip()
            keyword_data = json.loads(result)
            keywords = keyword_data.get('keywords', [])

            return keywords[:max_keywords]

        except Exception as e:
            logger.error(f"Error extracting keywords: {str(e)}")
            return []

    def analyze_posts_batch(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        여러 포스트에 대한 감정 분석과 키워드 추출을 일괄 수행합니다.
        """
        analyzed_posts = []

        for post in posts:
            text = f"{post['title']} {post.get('selftext', '')}"
            sentiment = self.analyze_sentiment(text)
            keywords = self.extract_keywords(text)

            analyzed_post = post.copy()
            analyzed_post['sentiment'] = sentiment
            analyzed_post['keywords'] = keywords

            analyzed_posts.append(analyzed_post)

        return analyzed_posts