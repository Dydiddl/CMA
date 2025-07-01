#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 시스템 설정 관리
애플리케이션의 모든 설정을 중앙에서 관리
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # 기본 설정
    APP_NAME: str = "CMA - Construction Management System"
    APP_VERSION: str = "3.1.0"
    DEBUG: bool = False
    
    # 서버 설정
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS 설정
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # 데이터베이스 설정 (SQLite로 변경)
    DATABASE_URL: str = "sqlite:///./cma_backend.db"
    
    # 보안 설정
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 파일 업로드 설정
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [".pdf", ".xlsx", ".xls", ".doc", ".docx"]
    
    # 로깅 설정
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/cma.log"
    
    # ASCR 모듈 설정
    ASCR_UPLOAD_DIR: str = "./uploads/ascr"
    ASCR_TEMP_DIR: str = "./temp"
    
    # 성능 설정
    MAX_WORKERS: int = 4
    CACHE_TTL: int = 3600  # 1시간
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# 전역 설정 인스턴스
settings = Settings() 