from typing import List, Callable
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import get_current_user, check_permissions
from app.models.user import User
from app.db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def require_permissions(required_permissions: List[str]):
    """
    권한 검사 데코레이터
    """
    async def permission_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        if not check_permissions(current_user, required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="권한이 없습니다"
            )
        return current_user
    return permission_checker

# 권한 상수 정의
class Permissions:
    # 프로젝트 관련 권한
    CREATE_PROJECT = "create:project"
    READ_PROJECT = "read:project"
    UPDATE_PROJECT = "update:project"
    DELETE_PROJECT = "delete:project"
    
    # 계약 관련 권한
    CREATE_CONTRACT = "create:contract"
    READ_CONTRACT = "read:contract"
    UPDATE_CONTRACT = "update:contract"
    DELETE_CONTRACT = "delete:contract"
    
    # 사용자 관련 권한
    MANAGE_USERS = "manage:users"
    READ_OWN_PROFILE = "read:own_profile"
    UPDATE_OWN_PROFILE = "update:own_profile"
    
    # 부서 관련 권한
    MANAGE_DEPARTMENTS = "manage:departments"

# 권한 그룹 정의
class PermissionGroups:
    # 프로젝트 관리자 권한
    PROJECT_ADMIN = [
        Permissions.CREATE_PROJECT,
        Permissions.READ_PROJECT,
        Permissions.UPDATE_PROJECT,
        Permissions.DELETE_PROJECT
    ]
    
    # 계약 관리자 권한
    CONTRACT_ADMIN = [
        Permissions.CREATE_CONTRACT,
        Permissions.READ_CONTRACT,
        Permissions.UPDATE_CONTRACT,
        Permissions.DELETE_CONTRACT
    ]
    
    # 시스템 관리자 권한
    SYSTEM_ADMIN = [
        *PROJECT_ADMIN,
        *CONTRACT_ADMIN,
        Permissions.MANAGE_USERS,
        Permissions.MANAGE_DEPARTMENTS
    ]
    
    # 일반 사용자 권한
    REGULAR_USER = [
        Permissions.READ_PROJECT,
        Permissions.READ_CONTRACT,
        Permissions.READ_OWN_PROFILE,
        Permissions.UPDATE_OWN_PROFILE
    ] 