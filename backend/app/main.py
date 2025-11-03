from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from services.scheduler_service import SchedulerService

scheduler = SchedulerService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 애플리케이션 시작 시
    await scheduler.start_scheduler()
    yield
    # 애플리케이션 종료 시
    await scheduler.stop_scheduler()

app = FastAPI(
    title="Reddit Stock Monitor API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 환경에서는 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 포함
from api.endpoints import stock_data
app.include_router(stock_data.router, prefix="/api/v1", tags=["stocks"])

@app.get("/")
async def root():
    return {"message": "Reddit Stock Monitor API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 수동 분석을 위한 엔드포인트
@app.post("/api/v1/analyze")
async def manual_analyze():
    """모든 주식에 대한 수동 분석 실행"""
    try:
        await scheduler.manual_run()
        return {"status": "success", "message": "수동 분석이 완료되었습니다"}
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"분석 실패: {str(e)}")