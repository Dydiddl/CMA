import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import check_permissions, get_user_permissions
from app.core.permissions import Permissions, PermissionGroups
from app.models.user import User
from app.models.department import Department

def test_superuser_permissions(db_session: Session):
    """슈퍼유저의 권한 테스트"""
    # 슈퍼유저 생성
    superuser = User(
        email="superuser@example.com",
        username="superuser",
        hashed_password="hashed_password",
        is_active=True,
        is_superuser=True
    )
    db_session.add(superuser)
    db_session.commit()
    
    # 모든 권한 검사
    assert check_permissions(superuser, PermissionGroups.SYSTEM_ADMIN)
    assert check_permissions(superuser, PermissionGroups.PROJECT_ADMIN)
    assert check_permissions(superuser, PermissionGroups.CONTRACT_ADMIN)
    assert check_permissions(superuser, PermissionGroups.REGULAR_USER)

def test_regular_user_permissions(db_session: Session):
    """일반 사용자의 권한 테스트"""
    # 일반 사용자 생성
    user = User(
        email="user@example.com",
        username="user",
        hashed_password="hashed_password",
        is_active=True,
        is_superuser=False
    )
    db_session.add(user)
    db_session.commit()
    
    # 기본 권한만 있는지 확인
    assert check_permissions(user, PermissionGroups.REGULAR_USER)
    assert not check_permissions(user, PermissionGroups.PROJECT_ADMIN)
    assert not check_permissions(user, PermissionGroups.CONTRACT_ADMIN)
    assert not check_permissions(user, PermissionGroups.SYSTEM_ADMIN)

def test_department_user_permissions(db_session: Session):
    """부서 소속 사용자의 권한 테스트"""
    # 부서 생성
    department = Department(
        name="테스트 부서",
        code="TEST-DEPT"
    )
    db_session.add(department)
    db_session.commit()
    
    # 부서 소속 사용자 생성
    user = User(
        email="dept_user@example.com",
        username="dept_user",
        hashed_password="hashed_password",
        is_active=True,
        is_superuser=False,
        department_id=department.id
    )
    db_session.add(user)
    db_session.commit()
    
    # 부서 사용자 권한 확인
    permissions = get_user_permissions(user)
    assert "read:project" in permissions
    assert "create:contract" in permissions
    assert "read:contract" in permissions
    assert "update:contract" in permissions
    assert "manage:users" not in permissions
    assert "manage:departments" not in permissions

def test_inactive_user_permissions(db_session: Session):
    """비활성화된 사용자의 권한 테스트"""
    # 비활성화된 사용자 생성
    user = User(
        email="inactive@example.com",
        username="inactive",
        hashed_password="hashed_password",
        is_active=False,
        is_superuser=False
    )
    db_session.add(user)
    db_session.commit()
    
    # 권한이 없는지 확인
    permissions = get_user_permissions(user)
    assert len(permissions) == 0
    assert not check_permissions(user, PermissionGroups.REGULAR_USER)

def test_permission_combinations(db_session: Session):
    """권한 조합 테스트"""
    # 프로젝트 관리자 생성
    project_admin = User(
        email="project_admin@example.com",
        username="project_admin",
        hashed_password="hashed_password",
        is_active=True,
        is_superuser=False
    )
    db_session.add(project_admin)
    db_session.commit()
    
    # 프로젝트 관리자 권한 설정
    project_admin_permissions = [
        Permissions.CREATE_PROJECT,
        Permissions.READ_PROJECT,
        Permissions.UPDATE_PROJECT,
        Permissions.DELETE_PROJECT
    ]
    
    # 권한 조합 검사
    assert check_permissions(project_admin, [Permissions.READ_PROJECT])
    assert check_permissions(project_admin, [Permissions.CREATE_PROJECT, Permissions.READ_PROJECT])
    assert not check_permissions(project_admin, [Permissions.MANAGE_USERS])
    assert not check_permissions(project_admin, [Permissions.CREATE_CONTRACT]) 