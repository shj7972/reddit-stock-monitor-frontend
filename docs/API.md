# API 문서

## 개요

RedditStockMonitor 백엔드 API는 FastAPI를 기반으로 구축되었으며, Reddit 데이터 수집, 분석, 및 보고서 생성을 제공합니다.

## 기본 엔드포인트

### GET /health
서버 상태 확인

**응답:**
```json
{
  "status": "healthy",
  "timestamp": "2023-11-02T06:00:00Z"
}
```

### GET /api/stock-data
현재 주식 키워드 데이터 가져오기

**응답:**
```json
{
  "data": [
    {
      "keyword": "AAPL",
      "mentions": 150,
      "sentiment": 0.8,
      "last_updated": "2023-11-02T05:00:00Z"
    }
  ],
  "timestamp": "2023-11-02T06:00:00Z"
}
```

### POST /api/reports/{keyword}
특정 키워드에 대한 상세 보고서 생성

**요청 본문:**
```json
{
  "period": "24h",
  "include_sentiment": true
}
```

**응답:**
```json
{
  "keyword": "AAPL",
  "report": "상세 분석 내용...",
  "generated_at": "2023-11-02T06:00:00Z"
}
```

### GET /api/history/{keyword}
키워드의 히스토리 데이터 가져오기

**쿼리 파라미터:**
- days: 조회할 일수 (기본값: 7)

**응답:**
```json
{
  "keyword": "AAPL",
  "history": [
    {
      "date": "2023-11-01",
      "mentions": 120,
      "sentiment": 0.7
    }
  ]
}
```

## 인증

현재 API는 공개 엔드포인트로, 별도 인증이 필요하지 않습니다.

## 에러 응답

모든 API는 표준 HTTP 상태 코드를 사용하며, 에러 시 다음과 같은 응답을 반환합니다:

```json
{
  "detail": "에러 메시지",
  "error_code": "ERROR_CODE"
}
```

## 속도 제한

- 무료 티어: 100 요청/시간
- 프리미엄 티어: 1000 요청/시간