#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
사용자 서비스 모듈
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Tuple
from passlib.context import CryptContext
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.exceptions import NotFoundException, ValidationException

# 비밀번호 해싱 컨텍스트
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """사용자 서비스 클래스"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_password_hash(self, password: str) -> str:
        """
        비밀번호 해싱
        
        Args:
            password: 평문 비밀번호
            
        Returns:
            str: 해시된 비밀번호
        """
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        비밀번호 검증
        
        Args:
            plain_password: 평문 비밀번호
            hashed_password: 해시된 비밀번호
            
        Returns:
            bool: 검증 결과
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_users(
        self, 
        skip: int = 0, 
        limit: int = 10, 
        search: Optional[str] = None
    ) -> Tuple[List[UserResponse], int]:
        """
        사용자 목록 조회
        
        Args:
            skip: 건너뛸 레코드 수
            limit: 가져올 레코드 수
            search: 검색어
            
        Returns:
            Tuple[List[UserResponse], int]: 사용자 목록과 전체 개수
        """
        try:
            query = self.db.query(User)
            
            # 검색 조건 적용
            if search:
                query = query.filter(
                    User.email.contains(search) | 
                    User.full_name.contains(search) |
                    User.department.contains(search)
                )
            
            # 전체 개수 조회
            total = query.count()
            
            # 페이징 적용
            users = query.offset(skip).limit(limit).all()
            
            # 응답 스키마로 변환
            user_responses = [
                UserResponse(
                    id=str(user.id),
                    email=user.email,
                    full_name=user.full_name,
                    role=user.role,
                    department=user.department,
                    phone=user.phone,
                    is_active=user.is_active,
                    created_at=user.created_at,
                    updated_at=user.updated_at
                ) for user in users
            ]
            
            return user_responses, total
            
        except Exception as e:
            raise ValidationException(f"사용자 목록 조회 중 오류 발생: {e}")
    
    def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        """
        ID로 사용자 조회
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            Optional[UserResponse]: 사용자 정보 또는 None
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return None
            
            return UserResponse(
                id=str(user.id),
                email=user.email,
                full_name=user.full_name,
                role=user.role,
                department=user.department,
                phone=user.phone,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            
        except Exception as e:
            raise ValidationException(f"사용자 조회 중 오류 발생: {e}")
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        이메일로 사용자 조회
        
        Args:
            email: 사용자 이메일
            
        Returns:
            Optional[User]: 사용자 또는 None
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def create_user(self, user_data: UserCreate) -> UserResponse:
        """
        새 사용자 생성
        
        Args:
            user_data: 사용자 생성 데이터
            
        Returns:
            UserResponse: 생성된 사용자 정보
            
        Raises:
            ValidationException: 유효하지 않은 데이터
        """
        try:
            # 이메일 중복 확인
            existing_user = self.get_user_by_email(user_data.email)
            if existing_user:
                raise ValidationException("이미 존재하는 이메일입니다.")
            
            # 비밀번호 해싱
            hashed_password = self.get_password_hash(user_data.password)
            
            # 새 사용자 생성
            user = User(
                email=user_data.email,
                password_hash=hashed_password,
                full_name=user_data.full_name,
                role=user_data.role,
                department=user_data.department,
                phone=user_data.phone,
                is_active=user_data.is_active
            )
            
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            
            return UserResponse(
                id=str(user.id),
                email=user.email,
                full_name=user.full_name,
                role=user.role,
                department=user.department,
                phone=user.phone,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            
        except IntegrityError:
            self.db.rollback()
            raise ValidationException("이미 존재하는 이메일입니다.")
        except Exception as e:
            self.db.rollback()
            raise ValidationException(f"사용자 생성 중 오류 발생: {e}")
    
    def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[UserResponse]:
        """
        사용자 정보 수정
        
        Args:
            user_id: 사용자 ID
            user_data: 수정할 사용자 데이터
            
        Returns:
            Optional[UserResponse]: 수정된 사용자 정보 또는 None
            
        Raises:
            ValidationException: 유효하지 않은 데이터
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return None
            
            # 업데이트할 데이터만 추출
            update_data = user_data.dict(exclude_unset=True)
            
            # 이메일 변경 시 중복 확인
            if 'email' in update_data:
                existing_user = self.get_user_by_email(update_data['email'])
                if existing_user and existing_user.id != user_id:
                    raise ValidationException("이미 존재하는 이메일입니다.")
            
            # 사용자 정보 업데이트
            for field, value in update_data.items():
                setattr(user, field, value)
            
            self.db.commit()
            self.db.refresh(user)
            
            return UserResponse(
                id=str(user.id),
                email=user.email,
                full_name=user.full_name,
                role=user.role,
                department=user.department,
                phone=user.phone,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            
        except IntegrityError:
            self.db.rollback()
            raise ValidationException("이미 존재하는 이메일입니다.")
        except Exception as e:
            self.db.rollback()
            raise ValidationException(f"사용자 수정 중 오류 발생: {e}")
    
    def delete_user(self, user_id: str) -> bool:
        """
        사용자 삭제
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            bool: 삭제 성공 여부
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return False
            
            self.db.delete(user)
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            raise ValidationException(f"사용자 삭제 중 오류 발생: {e}")
    
    def activate_user(self, user_id: str) -> bool:
        """
        사용자 활성화
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            bool: 활성화 성공 여부
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return False
            
            user.is_active = True
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            raise ValidationException(f"사용자 활성화 중 오류 발생: {e}")
    
    def deactivate_user(self, user_id: str) -> bool:
        """
        사용자 비활성화
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            bool: 비활성화 성공 여부
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return False
            
            user.is_active = False
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            raise ValidationException(f"사용자 비활성화 중 오류 발생: {e}")
    
    def update_user_password(self, user_id: str, current_password: str, new_password: str) -> bool:
        """
        사용자 비밀번호 변경
        
        Args:
            user_id: 사용자 ID
            current_password: 현재 비밀번호
            new_password: 새 비밀번호
            
        Returns:
            bool: 비밀번호 변경 성공 여부
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return False
            
            # 현재 비밀번호 검증
            if not self.verify_password(current_password, user.password_hash):
                raise ValidationException("현재 비밀번호가 올바르지 않습니다.")
            
            # 새 비밀번호 해싱
            hashed_password = self.get_password_hash(new_password)
            user.password_hash = hashed_password
            
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            raise ValidationException(f"비밀번호 변경 중 오류 발생: {e}")
    
    def get_user_stats(self) -> dict:
        """
        사용자 통계 조회
        
        Returns:
            dict: 사용자 통계 정보
        """
        try:
            total_users = self.db.query(User).count()
            active_users = self.db.query(User).filter(User.is_active == True).count()
            inactive_users = total_users - active_users
            
            # 역할별 사용자 수
            users_by_role = {}
            roles = self.db.query(User.role).distinct().all()
            for role in roles:
                count = self.db.query(User).filter(User.role == role[0]).count()
                users_by_role[role[0]] = count
            
            return {
                "total_users": total_users,
                "active_users": active_users,
                "inactive_users": inactive_users,
                "users_by_role": users_by_role
            }
            
        except Exception as e:
            raise ValidationException(f"사용자 통계 조회 중 오류 발생: {e}") 