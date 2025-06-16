"""
인증 미들웨어
"""
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Optional

from app.core.config import settings
from app.core.security import ALGORITHM

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = security) -> Optional[str]:
    """
    JWT 토큰 검증
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

class AuthMiddleware:
    """
    인증 미들웨어 클래스
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, request: Request, call_next):
        # 인증이 필요하지 않은 경로는 건너뛰기
        if request.url.path in ["/api/v1/auth/login", "/api/v1/auth/register", "/docs", "/openapi.json"]:
            return await call_next(request)

        try:
            # 토큰 검증
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                raise HTTPException(
                    status_code=401,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload

            response = await call_next(request)
            return response

        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            ) 