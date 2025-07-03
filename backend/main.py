# CMA 백엔드 실행 안내 파일
# 실제 FastAPI 진입점은 app/main.py 입니다.
#
# 개발 서버 실행:
#   cd backend
#   source venv/bin/activate
#   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
#
# 이 파일은 더 이상 사용되지 않습니다.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import project, task

app = FastAPI(title="Construction Management API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 환경에서만 사용. 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project.router)
app.include_router(task.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)