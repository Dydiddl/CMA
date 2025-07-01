#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
인증 서비스 모듈
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from passlib.context import CryptContext
from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.core.exceptions import AuthenticationException

# 비밀번호 해싱 컨텍스트 - bcrypt 대신 sha256_crypt 사용
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


class AuthService:
    """인증 서비스 클래스"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        비밀번호 검증
        
        Args:
            plain_password: 평문 비밀번호
            hashed_password: 해시된 비밀번호
            
        Returns:
            bool: 검증 결과
        """
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return False
    
    def get_password_hash(self, password: str) -> str:
        """
        비밀번호 해싱
        
        Args:
            password: 평문 비밀번호
            
        Returns:
            str: 해시된 비밀번호
        """
        try:
            return pwd_context.hash(password)
        except Exception as e:
            raise ValueError(f"비밀번호 해싱 실패: {e}")
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        사용자 인증
        
        Args:
            email: 이메일
            password: 비밀번호
            
        Returns:
            Optional[User]: 인증된 사용자 또는 None
        """
        try:
            user = self.db.query(User).filter(User.email == email).first()
            if not user:
                return None
            
            if not self.verify_password(password, user.password_hash):
                return None
            
            return user
        except Exception as e:
            print(f"사용자 인증 중 오류: {e}")
            return None
    
    def create_user(self, register_data: RegisterRequest) -> User:
        """
        새 사용자 생성
        
        Args:
            register_data: 회원가입 데이터
            
        Returns:
            User: 생성된 사용자
            
        Raises:
            ValueError: 유효하지 않은 데이터
            IntegrityError: 중복된 이메일
        """
        try:
            # 이메일 중복 확인
            existing_user = self.db.query(User).filter(User.email == register_data.email).first()
            if existing_user:
                raise ValueError("이미 존재하는 이메일입니다.")
            
            # 비밀번호 해싱
            hashed_password = self.get_password_hash(register_data.password)
            
            # 새 사용자 생성
            user = User(
                email=register_data.email,
                password_hash=hashed_password,
                full_name=register_data.name,
                role="user"
            )
            
            # 데이터베이스에 저장
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            
            return user
            
        except ValueError:
            raise
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError("이미 존재하는 이메일입니다.")
        except Exception as e:
            self.db.rollback()
            print(f"사용자 생성 중 오류: {e}")
            raise ValueError("사용자 생성 중 오류가 발생했습니다.")
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        이메일로 사용자 조회
        
        Args:
            email: 이메일
            
        Returns:
            Optional[User]: 사용자 또는 None
        """
        try:
            return self.db.query(User).filter(User.email == email).first()
        except Exception as e:
            print(f"사용자 조회 중 오류: {e}")
            return None
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        ID로 사용자 조회
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            Optional[User]: 사용자 또는 None
        """
        try:
            return self.db.query(User).filter(User.id == user_id).first()
        except Exception as e:
            print(f"사용자 조회 중 오류: {e}")
            return None
    
    def update_user_password(self, user_id: str, new_password: str) -> bool:
        """
        사용자 비밀번호 업데이트
        
        Args:
            user_id: 사용자 ID
            new_password: 새 비밀번호
            
        Returns:
            bool: 업데이트 성공 여부
        """
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False
            
            # 새 비밀번호 해싱
            hashed_password = self.get_password_hash(new_password)
            user.password_hash = hashed_password
            
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"비밀번호 업데이트 중 오류 발생: {e}")
    
    def deactivate_user(self, user_id: str) -> bool:
        """
        사용자 비활성화
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            bool: 비활성화 성공 여부
        """
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False
            
            user.is_active = False
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"사용자 비활성화 중 오류 발생: {e}")
    
    def activate_user(self, user_id: str) -> bool:
        """
        사용자 활성화
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            bool: 활성화 성공 여부
        """
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False
            
            user.is_active = True
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"사용자 활성화 중 오류 발생: {e}") 