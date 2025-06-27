#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
파일 처리 유틸리티 모듈

이 모듈은 파일 처리와 관련된 유틸리티 함수들을 제공합니다.
"""

import os
import re
import json
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

from .constants import MAX_FILENAME_LENGTH
from .types import FilePath, JSONData
from .exceptions import FileValidationError

def validate_pdf_file(file_path: FilePath) -> bool:
    """PDF 파일 유효성을 검증합니다."""
    path = Path(file_path)
    
    if not path.exists():
        raise FileValidationError(str(path), "파일이 존재하지 않습니다")
    
    if not path.is_file():
        raise FileValidationError(str(path), "파일이 아닙니다")
    
    if path.suffix.lower() != '.pdf':
        raise FileValidationError(str(path), "PDF 파일이 아닙니다")
    
    if path.stat().st_size == 0:
        raise FileValidationError(str(path), "빈 파일입니다")
    
    return True

def get_file_hash(file_path: FilePath, algorithm: str = 'md5') -> str:
    """파일의 해시값을 계산합니다."""
    path = Path(file_path)
    
    if algorithm == 'md5':
        hash_func = hashlib.md5()
    elif algorithm == 'sha1':
        hash_func = hashlib.sha1()
    elif algorithm == 'sha256':
        hash_func = hashlib.sha256()
    else:
        raise ValueError(f"지원하지 않는 해시 알고리즘: {algorithm}")
    
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()

def ensure_directory(directory: FilePath) -> Path:
    """디렉토리가 존재하는지 확인하고 없으면 생성합니다."""
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_safe_filename(filename: str) -> str:
    """안전한 파일명으로 변환합니다."""
    # 위험한 문자들을 제거하거나 대체
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # 연속된 언더스코어를 하나로
    safe_name = re.sub(r'_+', '_', safe_name)
    # 앞뒤 공백 제거
    safe_name = safe_name.strip('._')
    return safe_name

def format_file_size(size_bytes: int) -> str:
    """파일 크기를 읽기 쉬운 형태로 변환합니다."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def get_current_timestamp() -> str:
    """현재 타임스탬프를 문자열로 반환합니다."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def load_json_data(file_path: FilePath) -> JSONData:
    """JSON 파일을 로드합니다."""
    path = Path(file_path)
    
    if not path.exists():
        raise FileValidationError(str(path), "JSON 파일이 존재하지 않습니다")
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise FileValidationError(str(path), f"JSON 파싱 오류: {e}")
    except Exception as e:
        raise FileValidationError(str(path), f"파일 읽기 오류: {e}")

def save_json_data(data: JSONData, file_path: FilePath, indent: int = 2) -> None:
    """데이터를 JSON 파일로 저장합니다."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)

def merge_dictionaries(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """두 딕셔너리를 병합합니다."""
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dictionaries(result[key], value)
        else:
            result[key] = value
    
    return result

def create_section_directory(base_dir: Path, section_name: str) -> Path:
    """부문별 디렉토리를 생성합니다."""
    section_dir = base_dir / section_name
    section_dir.mkdir(parents=True, exist_ok=True)
    return section_dir

def get_output_path(base_dir: Path, filename: str, extension: str = "") -> Path:
    """출력 파일 경로를 생성합니다."""
    # 파일명 길이 제한
    if len(filename) > MAX_FILENAME_LENGTH:
        name_part = filename[:MAX_FILENAME_LENGTH//2]
        ext_part = filename[filename.rfind('.'):] if '.' in filename else ""
        filename = name_part + ext_part
    
    # 안전한 파일명으로 변환
    safe_filename = get_safe_filename(filename)
    
    # 확장자 추가
    if extension and not safe_filename.endswith(extension):
        safe_filename += extension
    
    return base_dir / safe_filename

def show_progress(current: int, total: int, message: str = "") -> None:
    """진행률을 표시합니다."""
    if total == 0:
        return
    
    percentage = (current / total) * 100
    bar_length = 30
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    
    print(f"\r{message} |{bar}| {percentage:.1f}% ({current}/{total})", end='')
    
    if current == total:
        print()  # 줄바꿈 