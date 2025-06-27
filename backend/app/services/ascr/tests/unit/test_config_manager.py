#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
설정 관리자 테스트
"""

import pytest
from pathlib import Path
from src.utils.config.config_manager import ConfigManager, get_config_manager
from src.utils.config.exceptions import ConfigurationError

class TestConfigManager:
    """설정 관리자 테스트"""
    
    def test_config_manager_creation(self, temp_dir):
        """설정 관리자 생성 테스트"""
        config_manager = ConfigManager(temp_dir)
        assert config_manager.config_dir == temp_dir
    
    def test_get_config_manager(self, temp_dir):
        """get_config_manager 함수 테스트"""
        config_manager = get_config_manager(temp_dir)
        assert isinstance(config_manager, ConfigManager)
        assert config_manager.config_dir == temp_dir
    
    def test_yaml_config_operations(self, temp_dir):
        """YAML 설정 파일 작업 테스트"""
        config_manager = ConfigManager(temp_dir)
        
        # 테스트 설정 데이터
        test_config = {
            "pdf_processing": {
                "max_pages_per_file": 1000,
                "supported_formats": [".pdf"]
            },
            "logging": {
                "level": "INFO"
            }
        }
        
        # 설정 저장
        config_manager.save_yaml_config(test_config, "test_config.yaml")
        
        # 설정 로드
        loaded_config = config_manager.load_yaml_config("test_config.yaml")
        
        assert loaded_config["pdf_processing"]["max_pages_per_file"] == 1000
        assert loaded_config["logging"]["level"] == "INFO"
    
    def test_json_config_operations(self, temp_dir):
        """JSON 설정 파일 작업 테스트"""
        config_manager = ConfigManager(temp_dir)
        
        # 테스트 설정 데이터
        test_config = {
            "chapter_patterns": [
                {"pattern": "제1장", "chapter": "1"}
            ],
            "section_patterns": [
                {"pattern": "01부문", "section": "01"}
            ]
        }
        
        # 설정 저장
        config_manager.save_json_config(test_config, "test_mapping.json")
        
        # 설정 로드
        loaded_config = config_manager.load_json_config("test_mapping.json")
        
        assert len(loaded_config["chapter_patterns"]) == 1
        assert len(loaded_config["section_patterns"]) == 1
    
    def test_config_value_operations(self, temp_dir):
        """설정 값 작업 테스트"""
        config_manager = ConfigManager(temp_dir)
        
        test_config = {
            "pdf_processing": {
                "max_pages_per_file": 1000
            },
            "logging": {
                "level": "INFO"
            }
        }
        
        # 값 가져오기
        max_pages = config_manager.get_config_value(test_config, "pdf_processing.max_pages_per_file")
        assert max_pages == 1000
        
        # 기본값 테스트
        default_value = config_manager.get_config_value(test_config, "nonexistent.key", "default")
        assert default_value == "default"
        
        # 값 설정
        config_manager.set_config_value(test_config, "pdf_processing.batch_size", 50)
        batch_size = config_manager.get_config_value(test_config, "pdf_processing.batch_size")
        assert batch_size == 50
    
    def test_config_validation(self, temp_dir):
        """설정 검증 테스트"""
        config_manager = ConfigManager(temp_dir)
        
        # 유효한 설정
        valid_config = {
            "pdf_processing": {
                "max_pages_per_file": 1000,
                "supported_formats": [".pdf"]
            },
            "logging": {
                "level": "INFO"
            }
        }
        assert config_manager.validate_config(valid_config) == True
        
        # 유효하지 않은 설정
        invalid_config = {
            "pdf_processing": {
                "max_pages_per_file": 1000
                # supported_formats 누락
            }
            # logging 섹션 누락
        }
        assert config_manager.validate_config(invalid_config) == False
    
    def test_config_merge(self, temp_dir):
        """설정 병합 테스트"""
        config_manager = ConfigManager(temp_dir)
        
        base_config = {
            "pdf_processing": {
                "max_pages_per_file": 1000,
                "supported_formats": [".pdf"]
            },
            "logging": {
                "level": "INFO"
            }
        }
        
        override_config = {
            "pdf_processing": {
                "max_pages_per_file": 2000  # 덮어쓰기
            },
            "performance": {
                "max_workers": 4  # 새 섹션 추가
            }
        }
        
        merged_config = config_manager.merge_configs(base_config, override_config)
        
        assert merged_config["pdf_processing"]["max_pages_per_file"] == 2000
        assert merged_config["pdf_processing"]["supported_formats"] == [".pdf"]
        assert merged_config["logging"]["level"] == "INFO"
        assert merged_config["performance"]["max_workers"] == 4
    
    def test_file_not_found_error(self, temp_dir):
        """파일을 찾을 수 없는 경우 테스트"""
        config_manager = ConfigManager(temp_dir)
        
        with pytest.raises(ConfigurationError):
            config_manager.load_yaml_config("nonexistent.yaml")
        
        with pytest.raises(ConfigurationError):
            config_manager.load_json_config("nonexistent.json") 