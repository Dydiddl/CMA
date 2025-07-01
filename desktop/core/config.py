#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 데스크톱 애플리케이션 설정 관리자
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ConfigManager:
    """설정 관리자 클래스"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.config: Dict[str, Any] = self._load_default_config()
        self._load_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """기본 설정 로드"""
        return {
            "database": {
                "url": "sqlite:///cma_desktop.db",
                "echo": False
            },
            "api": {
                "base_url": "http://localhost:8000",
                "timeout": 30
            },
            "ui": {
                "theme": "light",
                "language": "ko",
                "window_size": [1400, 900]
            },
            "logging": {
                "level": "INFO",
                "file": "cma_desktop.log"
            }
        }
    
    def _load_config(self):
        """설정 파일 로드"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    self.config.update(file_config)
                logger.info("[SUCCESS] 설정 파일 로드 완료")
            else:
                self._save_config()
                logger.info("[INFO] 기본 설정 파일 생성됨")
        except Exception as e:
            logger.error(f"[ERROR] 설정 파일 로드 실패: {e}")
    
    def _save_config(self):
        """설정 파일 저장"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info("[SUCCESS] 설정 파일 저장 완료")
        except Exception as e:
            logger.error(f"[ERROR] 설정 파일 저장 실패: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """설정값 조회"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """설정값 설정"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self._save_config()
    
    def get_database_url(self) -> str:
        """데이터베이스 URL 조회"""
        return self.get("database.url", "sqlite:///cma_desktop.db")
    
    def get_api_base_url(self) -> str:
        """API 기본 URL 조회"""
        return self.get("api.base_url", "http://localhost:8000") 