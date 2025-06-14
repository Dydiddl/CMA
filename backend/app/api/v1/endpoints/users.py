from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.core.permissions import check_permissions
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, User as UserSchema
from app.crud import user as user_crud

router = APIRouter()

@router.post("/", response_model=UserSchema)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
    current_user: User = Depends(deps.get_current_user)
) -> User:
    """
    새로운 사용자를 생성합니다.
    """
    if not check_permissions(current_user, ["manage:users"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="사용자 생성 권한이 없습니다"
        )
    
    user = user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다"
        )
    
    user = user_crud.create(db, obj_in=user_in)
    return user

@router.get("/", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> List[User]:
    """
    사용자 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["manage:users"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="사용자 조회 권한이 없습니다"
        )
    
    users = user_crud.get_multi(db, skip=skip, limit=limit)
    return users

@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(deps.get_current_user)
) -> User:
    """
    현재 로그인한 사용자의 정보를 조회합니다.
    """
    return current_user

@router.get("/{user_id}", response_model=UserSchema)
def read_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> User:
    """
    특정 사용자의 정보를 조회합니다.
    """
    if not check_permissions(current_user, ["manage:users"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="사용자 조회 권한이 없습니다"
        )
    
    user = user_crud.get(db=db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    return user

@router.put("/me", response_model=UserSchema)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> User:
    """
    현재 로그인한 사용자의 정보를 수정합니다.
    """
    user = user_crud.update(db=db, db_obj=current_user, obj_in=user_in)
    return user

@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> User:
    """
    사용자 정보를 업데이트합니다.
    """
    if not check_permissions(current_user, ["manage:users"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="사용자 수정 권한이 없습니다"
        )
    
    user = user_crud.get(db=db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    
    user = user_crud.update(db=db, db_obj=user, obj_in=user_in)
    return user

@router.delete("/{user_id}")
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    """
    사용자를 삭제합니다.
    """
    if not check_permissions(current_user, ["manage:users"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="사용자 삭제 권한이 없습니다"
        )
    
    user = user_crud.get(db=db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    
    user_crud.remove(db=db, id=user_id)
    return {"status": "success"} 