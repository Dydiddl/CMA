#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
장 정보 추출 모듈

이 모듈은 JSON 데이터에서 장 정보를 추출하고 페이지 범위를 계산하는 기능을 제공합니다.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# ASCR 커스텀 로깅 시스템 사용
from ..log import get_logger

# 공통 모듈 import
from src.common.constants import SECTION_MAPPING
from src.common.utils import get_section_for_chapter

# 로거 초기화
logger = get_logger("ChapterExtractor")

class ChapterExtractor:
    """장 정보 추출 클래스"""
    
    def __init__(self, toc_data: Dict[str, Any]):
        """초기화"""
        self.toc_data = toc_data
        self.sections = ["공통부문", "토목부문", "건축부문", "기계설비부문", "유지관리부문"]
    
    def extract_chapters_by_section(self) -> Dict[str, List[Dict[str, Any]]]:
        """JSON에서 부문별 장 정보 추출"""
        if not self.toc_data:
            logger.error("목차 데이터가 없습니다")
            return {}
        
        chapters_by_section = {section: [] for section in self.sections}
        
        # entries에서 장 정보 추출 (level=1인 항목들)
        entries = self.toc_data.get('entries', [])
        
        for entry in entries:
            if entry.get('level') == 1:  # 장 단위 항목
                title = entry.get('title', '')
                page = entry.get('page', 0)
                section = entry.get('section', '공통부문')
                
                # 부문이 정의된 목록에 있는지 확인
                if section in self.sections:
                    chapters_by_section[section].append({
                        'title': title,
                        'page': page,
                        'number': entry.get('number', ''),
                        'source_page': page
                    })
        
        # 각 부문 내에서 페이지 순으로 정렬
        for section in chapters_by_section:
            chapters_by_section[section].sort(key=lambda x: x['page'])
        
        # 디버깅 정보 출력
        total_chapters = sum(len(chapters) for chapters in chapters_by_section.values())
        print(f"📊 추출된 장 정보: 총 {total_chapters}개")
        for section, chapters in chapters_by_section.items():
            if chapters:
                print(f"   📂 {section}: {len(chapters)}개 장")
        
        return chapters_by_section
    
    def calculate_page_ranges(self, chapters: List[Dict], total_pages: int) -> List[Dict]:
        """페이지 범위 계산"""
        print("📊 페이지 범위 계산 중...")
        
        # skip 플래그가 있는 장 제외
        valid_chapters = [ch for ch in chapters if not ch.get('skip', False)]
        
        for i, chapter in enumerate(valid_chapters):
            start_page = chapter.get('start_page', 0)
            end_page = chapter.get('end_page', 0)
            
            if start_page > 0 and end_page > 0:
                chapter['page_range'] = (start_page, end_page)
                print(f"  📄 {chapter['title']}: {start_page}-{end_page}")
            else:
                print(f"  ⚠️ {chapter['title']}: 페이지 범위 계산 실패")
        
        return valid_chapters
    
    def find_chapter_start_page(self, chapter_title: str, chapter_number: str) -> int:
        """장 시작 페이지 찾기"""
        try:
            # 장 번호에서 숫자 추출
            if chapter_number:
                chapter_num = int(chapter_number.replace('제', '').replace('장', ''))
            else:
                # 제목에서 장 번호 추출
                match = re.search(r'제(\d+)장', chapter_title)
                if match:
                    chapter_num = int(match.group(1))
                else:
                    return 0
            
            # 해당 장의 시작 페이지 찾기
            entries = self.toc_data.get('entries', [])
            for entry in entries:
                if entry.get('level') == 1:  # 장 단위
                    entry_title = entry.get('title', '')
                    if f"제{chapter_num}장" in entry_title:
                        return entry.get('page', 0)
            
            return 0
            
        except Exception as e:
            logger.error(f"장 시작 페이지 찾기 실패: {e}")
            return 0
    
    def _find_next_chapter_start(self, current_start: int, chapters: List[Dict]) -> int:
        """다음 장 시작 페이지 찾기"""
        try:
            # 현재 장 이후의 장들 중 가장 가까운 장 찾기
            next_chapters = [ch for ch in chapters if ch.get('page', 0) > current_start]
            if next_chapters:
                return min(ch.get('page', 0) for ch in next_chapters)
            return 0
        except Exception as e:
            logger.error(f"다음 장 시작 페이지 찾기 실패: {e}")
            return 0
    
    def validate_and_correct_page_ranges(self, chapters: List[Dict], total_pages: int) -> List[Dict]:
        """페이지 범위 검증 및 수정"""
        print("🔍 페이지 범위 검증 및 수정 중...")
        
        corrected_chapters = []
        
        for i, chapter in enumerate(chapters):
            start_page = chapter.get('start_page', 0)
            end_page = chapter.get('end_page', 0)
            
            # 기본 검증
            if start_page <= 0 or end_page <= 0:
                print(f"  ⚠️ {chapter['title']}: 유효하지 않은 페이지 범위 ({start_page}-{end_page})")
                continue
            
            if start_page > end_page:
                print(f"  ⚠️ {chapter['title']}: 시작 페이지가 끝 페이지보다 큽니다 ({start_page} > {end_page})")
                continue
            
            if end_page > total_pages:
                print(f"  ⚠️ {chapter['title']}: 끝 페이지가 총 페이지 수를 초과합니다 ({end_page} > {total_pages})")
                end_page = total_pages
                chapter['end_page'] = end_page
            
            # 수정된 장 정보 추가
            chapter['page_range'] = (start_page, end_page)
            corrected_chapters.append(chapter)
            
            print(f"  ✅ {chapter['title']}: {start_page}-{end_page}")
        
        return corrected_chapters
    
    def get_section_for_chapter_title(self, chapter_title: str) -> str:
        """장 제목으로부터 부문 결정"""
        return get_section_for_chapter(chapter_title)
    
    def analyze_chapter_structure(self, chapters_by_section: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """장 구조 분석"""
        analysis = {
            "total_chapters": 0,
            "sections_with_chapters": 0,
            "average_chapters_per_section": 0,
            "section_distribution": {},
            "page_range_analysis": {}
        }
        
        total_chapters = 0
        sections_with_chapters = 0
        
        for section, chapters in chapters_by_section.items():
            if chapters:
                sections_with_chapters += 1
                total_chapters += len(chapters)
                analysis["section_distribution"][section] = len(chapters)
                
                # 페이지 범위 분석
                if chapters:
                    pages = [ch.get('page', 0) for ch in chapters]
                    analysis["page_range_analysis"][section] = {
                        "min_page": min(pages),
                        "max_page": max(pages),
                        "page_count": len(pages)
                    }
        
        analysis["total_chapters"] = total_chapters
        analysis["sections_with_chapters"] = sections_with_chapters
        analysis["average_chapters_per_section"] = (
            total_chapters / sections_with_chapters if sections_with_chapters > 0 else 0
        )
        
        return analysis 