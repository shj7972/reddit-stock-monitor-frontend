# 설정 및 실행 가이드

## 환경 요구사항

- Node.js 18.x 이상
- Python 3.9 이상
- MongoDB Atlas 계정 (또는 로컬 MongoDB)
- Reddit API 키 (PRAW)
- OpenAI API 키

## 설치 단계

### 1. 저장소 클론

```bash
git clone <repository-url>
cd RedditStockMonitor
```

### 2. 백엔드 설정

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env` 파일을 생성하고 다음 변수를 설정하세요:

```
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=RedditStockMonitor/1.0
OPENAI_API_KEY=your_openai_api_key
MONGODB_URL=mongodb+srv://your_mongodb_connection_string
```

### 4. 프론트엔드 설정

```bash
cd ../frontend
npm install
```

### 5. MongoDB 설정

MongoDB Atlas에서 데이터베이스를 생성하거나 로컬 MongoDB를 설치하세요.

## 실행 방법

### 백엔드 실행

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### 프론트엔드 실행

```bash
cd frontend
npm start
```

## 테스트

프론트엔드: http://localhost:3000
백엔드 API: http://localhost:8000

API 문서: http://localhost:8000/docs