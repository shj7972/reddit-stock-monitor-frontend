# RedditStockMonitor

레딧에서 최근 많이 언급되는 주식 키워드를 실시간으로 수집, 시각화하고, 클릭 시 상세 리포트를 제공하는 웹 서비스

## 프로젝트 구조

```
RedditStockMonitor/
├── frontend/          # React 프론트엔드
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── InteractiveCloudMap.jsx
│   │   │   └── DetailedReportModal.jsx
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── backend/           # Python 백엔드
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── reddit_collector.py
│   │   ├── gpt_integration.py
│   │   ├── database.py
│   │   └── scheduler.py
│   ├── requirements.txt
│   └── .env
├── docs/              # 문서화
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── SETUP.md
└── README.md
```

## 기능 요구사항

1. **프론트엔드**: React 기반 인터랙티브 클라우드맵, 클릭 시 상세 리포트 모달
2. **백엔드**: Python API 서버, Reddit API 데이터 수집, ChatGPT API 상세 리포트 생성
3. **배포**: 프론트엔드 Vercel, 백엔드 Heroku/AWS
4. **데이터 저장**: MongoDB 캐시 및 저장소
5. **지속적 업데이트**: 1시간 주기로 데이터 갱신

## 기술 스택

- **Frontend**: React, D3.js (워드 클라우드), Axios
- **Backend**: Python, FastAPI, PRAW (Reddit API), OpenAI API
- **Database**: MongoDB
- **Deployment**: Vercel (Frontend), Heroku (Backend)

## 설정 및 실행

자세한 설정 방법은 [SETUP.md](docs/SETUP.md)를 참조하세요.

## API 문서

[API.md](docs/API.md)를 참조하세요.

## 배포 가이드

[DEPLOYMENT.md](docs/DEPLOYMENT.md)를 참조하세요.