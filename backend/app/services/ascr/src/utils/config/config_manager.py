#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASCR 설정 관리 시스템
중앙화된 설정 관리와 환경별 설정을 제공합니다.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, Union
from datetime import datetime
import logging

from .exceptions import ConfigError, ConfigFileNotFoundError

class ASCRConfigManager:
    """ASCR 설정 관리자"""
    
    def __init__(self, config_dir: Path = None):
        """
        설정 관리자 초기화
        
        Args:
            config_dir: 설정 파일 디렉토리 (기본값: config/)
        """
        self.config_dir = config_dir or Path("config")
        self.config_dir.mkdir(exist_ok=True)
        
        # 기본 설정 파일들
        self.config_files = {
            'main': self.config_dir / 'config.yaml',
            'mapping': self.config_dir / 'mapping_config.json',
            'logging': self.config_dir / 'logging.yaml'
        }
        
        # 설정 캐시
        self._config_cache = {}
        self._load_default_config()
    
    def _load_default_config(self):
        """기본 설정 로드"""
        self.default_config = {
            'pdf_processing': {
                'max_pages_per_file': 100,
                'supported_formats': ['json', 'csv', 'markdown', 'yaml'],
                'extraction_method': 'auto',
                'split_mode': 'chapter',
                'output_format': 'json'
            },
            'logging': {
                'level': 'INFO',
                'enable_console': True,
                'enable_file': True,
                'max_file_size': '10MB',
                'backup_count': 5
            },
            'output': {
                'create_subdirectories': True,
                'overwrite_existing': False,
                'generate_reports': True,
                'timestamp_format': '%Y%m%d_%H%M%S'
            },
            'sections': {
                'common': '공통부문',
                'civil': '토목부문', 
                'architecture': '건축부문',
                'mechanical': '기계설비부문',
                'maintenance': '유지관리부문'
            },
            'patterns': {
                'chapter': r'제(\d+)장\s*([가-힣A-Za-z0-9\-\(\)\s]+?)\s*[·\-\.]{2,}\s*(\d+)',
                'section': r'(\d+)-(\d+)\s+([가-힣A-Za-z0-9\-\(\)\s]+?)\s*[·\-\.]{2,}\s*(\d+)',
                'subsection': r'(\d+)-(\d+)-(\d+)\s+([가-힣A-Za-z0-9\-\(\)\s]+?)\s*[·\-\.]{2,}\s*(\d+)'
            }
        }
    
    def get_config(self, config_name: str = 'main') -> Dict[str, Any]:
        """
        설정 파일 로드
        
        Args:
            config_name: 설정 파일 이름 ('main', 'mapping', 'logging')
            
        Returns:
            Dict[str, Any]: 설정 데이터
        """
        if config_name in self._config_cache:
            return self._config_cache[config_name]
        
        config_file = self.config_files.get(config_name)
        if not config_file:
            raise ConfigError(f"알 수 없는 설정 파일: {config_name}")
        
        if not config_file.exists():
            # 기본 설정으로 파일 생성
            self._create_default_config_file(config_name)
        
        try:
            if config_file.suffix == '.yaml':
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f) or {}
            elif config_file.suffix == '.json':
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                raise ConfigError(f"지원하지 않는 설정 파일 형식: {config_file.suffix}")
            
            # 기본값과 병합
            if config_name == 'main':
                config = self._merge_with_defaults(config)
            
            self._config_cache[config_name] = config
            return config
            
        except Exception as e:
            raise ConfigError(f"설정 파일 로드 실패: {e}")
    
    def _create_default_config_file(self, config_name: str):
        """기본 설정 파일 생성"""
        config_file = self.config_files[config_name]
        
        if config_name == 'main':
            default_data = self.default_config
        elif config_name == 'logging':
            default_data = self.default_config['logging']
        elif config_name == 'mapping':
            default_data = {'sections': {}, 'metadata': {}}
        else:
            raise ConfigError(f"알 수 없는 설정 파일: {config_name}")
        
        try:
            if config_file.suffix == '.yaml':
                with open(config_file, 'w', encoding='utf-8') as f:
                    yaml.dump(default_data, f, default_flow_style=False, allow_unicode=True)
            elif config_file.suffix == '.json':
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(default_data, f, ensure_ascii=False, indent=2)
            
            logging.info(f"기본 설정 파일 생성: {config_file}")
            
        except Exception as e:
            raise ConfigError(f"기본 설정 파일 생성 실패: {e}")
    
    def _merge_with_defaults(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """사용자 설정과 기본 설정 병합"""
        merged = self.default_config.copy()
        
        def deep_merge(base: Dict, update: Dict):
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    deep_merge(base[key], value)
                else:
                    base[key] = value
        
        deep_merge(merged, config)
        return merged
    
    def save_config(self, config_name: str, config_data: Dict[str, Any]):
        """
        설정 저장
        
        Args:
            config_name: 설정 파일 이름
            config_data: 저장할 설정 데이터
        """
        config_file = self.config_files.get(config_name)
        if not config_file:
            raise ConfigError(f"알 수 없는 설정 파일: {config_name}")
        
        try:
            if config_file.suffix == '.yaml':
                with open(config_file, 'w', encoding='utf-8') as f:
                    yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
            elif config_file.suffix == '.json':
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, ensure_ascii=False, indent=2)
            
            # 캐시 업데이트
            self._config_cache[config_name] = config_data
            logging.info(f"설정 저장 완료: {config_file}")
            
        except Exception as e:
            raise ConfigError(f"설정 저장 실패: {e}")
    
    def get_setting(self, key_path: str, default: Any = None) -> Any:
        """
        중첩된 키 경로로 설정값 조회
        
        Args:
            key_path: 점(.)으로 구분된 키 경로 (예: 'pdf_processing.max_pages_per_file')
            default: 기본값
            
        Returns:
            Any: 설정값
        """
        config = self.get_config('main')
        keys = key_path.split('.')
        
        try:
            value = config
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set_setting(self, key_path: str, value: Any):
        """
        중첩된 키 경로로 설정값 설정
        
        Args:
            key_path: 점(.)으로 구분된 키 경로
            value: 설정할 값
        """
        config = self.get_config('main')
        keys = key_path.split('.')
        
        # 중첩된 딕셔너리 생성
        current = config
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
        self.save_config('main', config)
    
    def validate_config(self) -> Dict[str, Any]:
        """
        설정 유효성 검증
        
        Returns:
            Dict[str, Any]: 검증 결과
        """
        results = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            config = self.get_config('main')
            
            # 필수 설정 확인
            required_settings = [
                'pdf_processing.max_pages_per_file',
                'logging.level',
                'output.create_subdirectories'
            ]
            
            for setting in required_settings:
                if self.get_setting(setting) is None:
                    results['errors'].append(f"필수 설정 누락: {setting}")
                    results['valid'] = False
            
            # 설정값 범위 확인
            max_pages = self.get_setting('pdf_processing.max_pages_per_file')
            if max_pages and (max_pages < 1 or max_pages > 1000):
                results['warnings'].append(f"max_pages_per_file 값이 범위를 벗어남: {max_pages}")
            
            # 로그 레벨 확인
            log_level = self.get_setting('logging.level')
            valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            if log_level and log_level.upper() not in valid_levels:
                results['errors'].append(f"잘못된 로그 레벨: {log_level}")
                results['valid'] = False
            
        except Exception as e:
            results['errors'].append(f"설정 검증 중 오류: {e}")
            results['valid'] = False
        
        return results
    
    def get_environment_config(self) -> Dict[str, Any]:
        """
        환경별 설정 조회
        
        Returns:
            Dict[str, Any]: 환경 설정
        """
        env = os.getenv('ASCR_ENV', 'development')
        env_config_file = self.config_dir / f'config_{env}.yaml'
        
        if env_config_file.exists():
            try:
                with open(env_config_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                logging.warning(f"환경 설정 파일 로드 실패: {e}")
        
        return {}
    
    def reload_config(self):
        """설정 캐시 초기화 및 재로드"""
        self._config_cache.clear()
        logging.info("설정 캐시 초기화 완료")

# 전역 설정 관리자 인스턴스
_config_manager = None

def get_config_manager() -> ASCRConfigManager:
    """전역 설정 관리자 인스턴스 반환"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ASCRConfigManager()
    return _config_manager

def get_setting(key_path: str, default: Any = None) -> Any:
    """설정값 조회 (편의 함수)"""
    return get_config_manager().get_setting(key_path, default)

def set_setting(key_path: str, value: Any):
    """설정값 설정 (편의 함수)"""
    get_config_manager().set_setting(key_path, value) 