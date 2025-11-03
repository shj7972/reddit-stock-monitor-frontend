# 배포 가이드

## 개요

RedditStockMonitor는 프론트엔드(Vercel)와 백엔드(Heroku/AWS)를 분리하여 배포합니다.

## 프론트엔드 배포 (Vercel)

### 1. Vercel 계정 생성
- https://vercel.com 에서 계정 생성

### 2. 프로젝트 연결
```bash
cd frontend
vercel login
vercel
```

### 3. 환경 변수 설정
Vercel 대시보드에서 다음 환경 변수를 설정:
- `REACT_APP_API_BASE_URL`: 백엔드 API URL

### 4. 배포
```bash
vercel --prod
```

## 백엔드 배포 (Heroku)

### 1. Heroku CLI 설치 및 로그인
```bash
heroku login
```

### 2. 앱 생성
```bash
cd backend
heroku create reddit-stock-monitor-api
```

### 3. 환경 변수 설정
```bash
heroku config:set REDDIT_CLIENT_ID=your_reddit_client_id
heroku config:set REDDIT_CLIENT_SECRET=your_reddit_client_secret
heroku config:set REDDIT_USER_AGENT=RedditStockMonitor/1.0
heroku config:set OPENAI_API_KEY=your_openai_api_key
heroku config:set MONGODB_URL=your_mongodb_url
```

### 4. 배포
```bash
git push heroku main
```

### 5. 로그 확인
```bash
heroku logs --tail -a reddit-stock-monitor-api
```

## 백엔드 배포 (Docker)

### 1. Docker 및 Docker Compose 설치
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

### 2. 환경 변수 파일 생성
```bash
cd backend
cp .env.example .env
# .env 파일을 실제 값으로 수정
```

### 3. Docker Compose로 배포
```bash
docker-compose up -d
```

### 4. 로그 확인
```bash
docker-compose logs -f reddit-stock-api
```

### 5. 서비스 중지
```bash
docker-compose down
```

## 백엔드 배포 (AWS)

### 1. AWS 계정 및 서비스 설정
- EC2 인스턴스 생성
- RDS MongoDB 또는 DocumentDB 설정

### 2. 애플리케이션 배포
```bash
# EC2에 접속 후
cd /var/www
git clone <repository-url>
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Systemd 서비스 생성
`/etc/systemd/system/reddit-monitor.service`:
```ini
[Unit]
Description=Reddit Stock Monitor API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/var/www/backend
ExecStart=/var/www/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable reddit-monitor
sudo systemctl start reddit-monitor
```

## MongoDB 설정

### MongoDB Atlas (권장)
1. https://cloud.mongodb.com 에서 클러스터 생성
2. IP 화이트리스트 설정 (0.0.0.0/0 for initial)
3. 데이터베이스 사용자 생성
4. 연결 문자열 복사

### 로컬 MongoDB
```bash
# MongoDB 설치 (Ubuntu)
sudo apt update
sudo apt install -y mongodb

# 서비스 시작
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

## 모니터링 및 로깅

### Heroku 로그
```bash
heroku logs --tail -a reddit-stock-monitor-api
```

### AWS CloudWatch
- EC2 인스턴스에 CloudWatch 에이전트 설치
- 로그 그룹 및 스트림 설정

## 도메인 및 SSL

### Vercel (프론트엔드)
- Vercel에서 자동 SSL 제공
- 커스텀 도메인 설정 가능

### Heroku (백엔드)
- 자동 SSL 제공
- 커스텀 도메인 추가 가능

### AWS
- Route 53으로 도메인 관리
- Certificate Manager로 SSL 인증서 발급
- CloudFront + API Gateway로 CDN 및 API 게이트웨이 구성

## 환경별 설정

### 개발 환경
- 로컬 MongoDB 또는 MongoDB Atlas 개발 클러스터
- 로컬 Redis (선택사항)

### 스테이징 환경
- 별도 Heroku 앱 또는 AWS 스테이징 인스턴스
- 스테이징용 데이터베이스

### 프로덕션 환경
- 프로덕션 Heroku 앱 또는 AWS 프로덕션 인스턴스
- 프로덕션 데이터베이스
- 백업 및 모니터링 설정