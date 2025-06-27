#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
텍스트 처리 유틸리티 모듈

이 모듈은 텍스트 처리와 관련된 유틸리티 함수들을 제공합니다.
"""

import re
import logging
import unicodedata
from typing import Dict, List, Any, Optional, Union, Tuple
from functools import wraps
import time

from .constants import SECTION_MAPPING, SECTION_KEYWORDS, TOC_PATTERNS
from .types import ChapterInfo, ValidationResult, SectionName, ChapterTitle

def clean_text(text: str) -> str:
    """텍스트를 정리합니다."""
    if not text:
        return ""
    
    # 공백 정리
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # 특수 문자 제거 (한글, 영문, 숫자, 기본 문장부호만 유지)
    text = re.sub(r'[^\w\s가-힣\-\.\,\;\:\!\?\(\)\[\]\{\}]', '', text)
    
    return text

def extract_page_number(text: str) -> Optional[int]:
    """텍스트에서 페이지 번호를 추출합니다."""
    if not text:
        return None
    
    # 다양한 페이지 번호 패턴
    patterns = [
        r'(\d+)\s*$',  # 끝에 숫자
        r'(\d+)\s*페이지',  # 숫자 + 페이지
        r'(\d+)\s*page',  # 숫자 + page
        r'[·\-\.]{2,}\s*(\d+)',  # 점선 + 숫자
        r'\s+(\d+)\s*$',  # 공백 + 숫자 + 끝
        r'p\.\s*(\d+)',  # p. 숫자
        r'page\s*(\d+)'  # page 숫자
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                continue
    
    return None

def determine_section(title: str) -> str:
    """제목을 기반으로 부문을 결정합니다."""
    return get_section_for_chapter(title)

def normalize_text(text: str) -> str:
    """텍스트를 정규화합니다."""
    if not text:
        return ""
    
    # 유니코드 정규화
    text = unicodedata.normalize('NFKC', text)
    
    # 공백 정리
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # 소문자 변환 (영문만)
    text = re.sub(r'[A-Z]', lambda m: m.group(0).lower(), text)
    
    return text

def find_toc_page_range(text: str, max_pages: int = 100) -> Optional[int]:
    """목차 페이지 범위를 찾습니다."""
    if not text:
        return None
    
    # 목차 관련 키워드 검색
    toc_keywords = ['목차', '차례', 'INDEX', 'CONTENTS', 'Table of Contents']
    
    lines = text.split('\n')
    for i, line in enumerate(lines[:max_pages]):
        line_lower = line.lower()
        for keyword in toc_keywords:
            if keyword.lower() in line_lower:
                return i
    
    return None

def validate_toc_structure(toc_data: Dict[str, Any]) -> bool:
    """목차 구조를 검증합니다."""
    if not isinstance(toc_data, dict):
        return False
    
    required_keys = ['entries', 'sections', 'metadata']
    for key in required_keys:
        if key not in toc_data:
            return False
    
    if not isinstance(toc_data['entries'], list):
        return False
    
    return True

def validate_section_name(section_name: str) -> bool:
    """부문명을 검증합니다."""
    valid_sections = [
        "공통부문", "토목부문", "건축부문", 
        "기계설비부문", "유지관리부문", "미분류"
    ]
    return section_name in valid_sections

def is_valid_page_number(page_num: int) -> bool:
    """페이지 번호가 유효한지 확인합니다."""
    return isinstance(page_num, int) and page_num > 0

def get_section_for_chapter(chapter_title: ChapterTitle) -> SectionName:
    """장 제목을 기반으로 부문을 결정합니다."""
    if not chapter_title:
        return "미분류"
    
    chapter_lower = chapter_title.lower()
    
    # 공통부문 키워드
    common_keywords = ['적용기준', '가설공사', '토공사', '조경공사', '기초공사', 
                      '철근콘크리트공사', '돌공사', '건설기계']
    
    # 토목부문 키워드
    civil_keywords = ['도로포장', '하천', '터널', '궤도', '강구조', '관부설', 
                     '항만', '지반조사', '측량']
    
    # 건축부문 키워드
    architecture_keywords = ['철골', '조적', '타일', '목공사', '수장', '방수', 
                           '지붕', '홈통', '금속', '미장', '창호', '유리', '칠공사']
    
    # 기계설비부문 키워드
    mechanical_keywords = ['배관', '덕트', '보온', '펌프', '공기설비', '밸브', 
                          '측정기기', '위생기구', '공기조화', '소방설비', '가스설비', 
                          '자동제어', '플랜트설비']
    
    # 유지관리부문 키워드
    maintenance_keywords = ['유지관리', '보수', '점검', '정비']
    
    # 키워드 매칭
    for keyword in common_keywords:
        if keyword in chapter_lower:
            return "공통부문"
    
    for keyword in civil_keywords:
        if keyword in chapter_lower:
            return "토목부문"
    
    for keyword in architecture_keywords:
        if keyword in chapter_lower:
            return "건축부문"
    
    for keyword in mechanical_keywords:
        if keyword in chapter_lower:
            return "기계설비부문"
    
    for keyword in maintenance_keywords:
        if keyword in chapter_lower:
            return "유지관리부문"
    
    return "미분류"

def calculate_confidence_score(chapter_title: ChapterTitle, section: SectionName) -> float:
    """장 제목과 부문 간의 신뢰도를 계산합니다."""
    if not chapter_title or not section:
        return 0.0
    
    chapter_lower = chapter_title.lower()
    section_lower = section.lower()
    
    # 키워드 매칭 점수 계산
    score = 0.0
    
    # 정확한 부문명 매칭 (높은 점수)
    if section_lower in chapter_lower:
        score += 0.8
    
    # 키워드 매칭
    section_keywords = {
        "공통부문": ['적용기준', '가설공사', '토공사', '조경공사', '기초공사', '철근콘크리트공사', '돌공사', '건설기계'],
        "토목부문": ['도로포장', '하천', '터널', '궤도', '강구조', '관부설', '항만', '지반조사', '측량'],
        "건축부문": ['철골', '조적', '타일', '목공사', '수장', '방수', '지붕', '홈통', '금속', '미장', '창호', '유리', '칠공사'],
        "기계설비부문": ['배관', '덕트', '보온', '펌프', '공기설비', '밸브', '측정기기', '위생기구', '공기조화', '소방설비', '가스설비', '자동제어', '플랜트설비'],
        "유지관리부문": ['유지관리', '보수', '점검', '정비']
    }
    
    keywords = section_keywords.get(section, [])
    matched_keywords = 0
    
    for keyword in keywords:
        if keyword in chapter_lower:
            matched_keywords += 1
            score += 0.4  # 키워드 매칭당 0.4점
    
    # 여러 키워드가 매칭되면 추가 점수
    if matched_keywords > 1:
        score += 0.2
    
    # 미분류인 경우 낮은 점수
    if section == "미분류":
        score = min(score, 0.1)
    
    return min(score, 1.0)

def extract_chapter_info(text: str) -> List[Dict[str, Any]]:
    """
    텍스트에서 장 정보 추출
    
    Args:
        text: 추출할 텍스트
        
    Returns:
        장 정보 리스트
    """
    chapters = []
    
    # 장 패턴 매칭
    chapter_pattern = TOC_PATTERNS["chapter"]
    matches = re.finditer(chapter_pattern, text)
    
    for match in matches:
        chapter_info = {
            'number': match.group(1),
            'title': match.group(2).strip(),
            'page': int(match.group(3)) if match.group(3) else 0,
            'start_pos': match.start(),
            'end_pos': match.end()
        }
        chapters.append(chapter_info)
    
    return chapters

def performance_monitor(func):
    """함수 성능을 모니터링하는 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        logging.info(f"{func.__name__} 실행 시간: {execution_time:.4f}초")
        
        return result
    return wrapper

def cache_result(ttl_seconds: int = 3600):
    """결과를 캐시하는 데코레이터"""
    cache = {}
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 캐시 키 생성
            import hashlib
            key_data = str(args) + str(sorted(kwargs.items()))
            cache_key = hashlib.md5(key_data.encode()).hexdigest()
            
            current_time = time.time()
            
            # 캐시에서 결과 확인
            if cache_key in cache:
                result, timestamp = cache[cache_key]
                if current_time - timestamp < ttl_seconds:
                    return result
            
            # 함수 실행 및 결과 캐시
            result = func(*args, **kwargs)
            cache[cache_key] = (result, current_time)
            
            return result
        return wrapper
    return decorator

def batch_process(items: List[Any], batch_size: int = 100) -> List[List[Any]]:
    """아이템들을 배치로 나눕니다."""
    return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]

def determine_section_with_confidence(chapter_title: ChapterTitle) -> Tuple[SectionName, float]:
    """장 제목을 기반으로 부문을 결정하고 신뢰도를 반환합니다."""
    if not chapter_title:
        return "미분류", 0.0
    
    # 부문 결정
    section = get_section_for_chapter(chapter_title)
    
    # 신뢰도 계산
    confidence = calculate_confidence_score(chapter_title, section)
    
    return section, confidence

def validate_section_classification(chapter_title: ChapterTitle, expected_section: SectionName) -> Tuple[bool, float]:
    """장 제목의 부문 분류 검증"""
    if not chapter_title or not expected_section:
        return False, 0.0
    
    # 실제 부문 결정
    actual_section, confidence = determine_section_with_confidence(chapter_title)
    
    # 예상 부문과 실제 부문 비교
    is_correct = actual_section == expected_section
    
    return is_correct, confidence 