from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.crud import user as user_crud
from app.core.redis import is_blacklisted

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    JWT 액세스 토큰을 생성합니다.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def create_refresh_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    JWT 리프레시 토큰을 생성합니다.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    비밀번호를 검증합니다.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    비밀번호를 해시화합니다.
    """
    return pwd_context.hash(password)

def verify_token(token: str) -> dict:
    """
    JWT 토큰을 검증합니다.
    """
    try:
        # 블랙리스트 체크
        if is_blacklisted(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="로그아웃된 토큰입니다",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰이 만료되었습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    현재 인증된 사용자를 가져옵니다.
    """
    payload = verify_token(token)
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 인증 정보입니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = user_crud.get_user(db, user_id=int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비활성화된 사용자입니다"
        )
    
    return user

def check_permissions(user: User, required_permissions: list[str]) -> bool:
    """
    사용자의 권한을 검사합니다.
    """
    if user.is_superuser:
        return True
    
    user_permissions = get_user_permissions(user)
    return all(perm in user_permissions for perm in required_permissions)

def get_user_permissions(user: User) -> list[str]:
    """
    사용자의 권한 목록을 가져옵니다.
    """
    permissions = []
    
    # 기본 권한
    permissions.extend(["read:own_profile", "update:own_profile"])
    
    # 역할 기반 권한
    if user.is_superuser:
        permissions.extend([
            "create:project",
            "read:project",
            "update:project",
            "delete:project",
            "create:contract",
            "read:contract",
            "update:contract",
            "delete:contract",
            "manage:users",
            "manage:departments"
        ])
    elif user.department:
        permissions.extend([
            "read:project",
            "create:contract",
            "read:contract",
            "update:contract"
        ])
    
    return permissions 