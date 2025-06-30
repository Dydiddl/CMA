#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
범용 계층 구조 수정 스크립트

이 스크립트는 모든 버전의 장점을 통합한 범용적인 계층 구조 수정 도구입니다.
설정 가능한 옵션과 다양한 문서 형식에 대응할 수 있습니다.
"""

import json
import re
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# ASCR 커스텀 로깅 시스템 사용
from src.utils.log import get_logger

# 로거 초기화
logger = get_logger("UniversalHierarchyFixer")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

@dataclass
class FixerConfig:
    """계층 구조 수정 설정"""
    # 부문별 페이지 범위 (기본값)
    section_page_ranges: Dict[str, Tuple[int, int]] = None
    
    # 패턴 우선순위 (True: 조/항목 우선, False: 절 우선)
    item_priority: bool = True
    
    # 장 구조 별도 관리 여부
    separate_chapter_structure: bool = False
    
    # 상세 통계 출력 여부
    detailed_statistics: bool = True
    
    # 추가 검증 수행 여부
    additional_validation: bool = True
    
    def __post_init__(self):
        if self.section_page_ranges is None:
            self.section_page_ranges = {
                "공통부문": (3, 298),
                "토목부문": (299, 400), 
                "건축부문": (401, 600),
                "기계설비부문": (601, 800),
                "유지관리부문": (801, 900)
            }

class UniversalHierarchyStructureFixer:
    """범용 계층 구조 수정 클래스"""
    
    def __init__(self, config: FixerConfig = None):
        self.config = config or FixerConfig()
        
        # 장 패턴 정의
        self.chapter_patterns = [
            r'^제(\d+)장\s*([가-힣A-Za-z0-9\-\s]+)',
            r'^(\d+)장\s*([가-힣A-Za-z0-9\-\s]+)',
            r'^제(\d+)장$',
            r'^(\d+)장$'
        ]
        
        # 절 패턴 정의 (n-n 형태)
        self.section_patterns = [
            r'^(\d+)-(\d+)\s*([가-힣A-Za-z0-9\-\s]+)',
            r'^(\d+)-(\d+)$'
        ]
        
        # 조/항목 패턴 정의 (n-n-n 형태)
        self.item_patterns = [
            r'^(\d+)-(\d+)-(\d+)\s*([가-힣A-Za-z0-9\-\s]+)',
            r'^(\d+)-(\d+)-(\d+)$'
        ]
    
    def fix_hierarchy_structure(self, input_file: Path, output_file: Path) -> bool:
        """계층 구조 수정 메인 함수"""
        try:
            logger.info(f"범용 계층 구조 수정 시작: {input_file}")
            
            # 1. JSON 파일 로드
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            entries = data.get('entries', [])
            logger.info(f"총 {len(entries)}개 항목 로드")
            
            # 2. 계층 레벨 수정
            fixed_entries = self._fix_levels(entries)
            logger.info("계층 레벨 수정 완료")
            
            # 3. 부문 분류 수정
            fixed_entries = self._fix_sections(fixed_entries)
            logger.info("부문 분류 수정 완료")
            
            # 4. 장 구조 추가 (설정에 따라)
            if self.config.separate_chapter_structure:
                fixed_entries = self._add_chapter_structure(fixed_entries)
                logger.info("장 구조 추가 완료")
            
            # 5. 번호 체계 정규화
            fixed_entries = self._normalize_numbering(fixed_entries)
            logger.info("번호 체계 정규화 완료")
            
            # 6. 부모-자식 관계 수정
            fixed_entries = self._fix_parent_child_relationships(fixed_entries)
            logger.info("부모-자식 관계 수정 완료")
            
            # 7. 결과 저장
            result_data = {
                "entries": fixed_entries,
                "metadata": {
                    "original_file": str(input_file),
                    "fixed_at": datetime.now().isoformat(),
                    "total_entries": len(fixed_entries),
                    "fix_method": "universal_hierarchy_structure_fixer",
                    "config": {
                        "item_priority": self.config.item_priority,
                        "separate_chapter_structure": self.config.separate_chapter_structure,
                        "section_page_ranges": self.config.section_page_ranges
                    }
                }
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"수정된 구조 저장 완료: {output_file}")
            
            # 8. 통계 출력
            if self.config.detailed_statistics:
                self._print_detailed_statistics(fixed_entries)
            else:
                self._print_basic_statistics(fixed_entries)
            
            # 9. 추가 검증 (설정에 따라)
            if self.config.additional_validation:
                self._perform_additional_validation(fixed_entries)
            
            return True
            
        except Exception as e:
            logger.error(f"계층 구조 수정 실패: {e}")
            return False
    
    def _fix_levels(self, entries: List[Dict]) -> List[Dict]:
        """계층 레벨 수정"""
        fixed_entries = []
        
        for entry in entries:
            number = entry.get('number', '')
            title = entry.get('title', '')
            
            # 부문 헤더 (level 0)
            if number in ["공통부문", "토목부문", "건축부문", "기계설비부문", "유지관리부문"]:
                entry['level'] = 0
                entry['type'] = 'section_header'
            
            # 장 패턴 확인 (level 1)
            elif self._is_chapter(number, title):
                entry['level'] = 1
                entry['type'] = 'chapter'
            
            # 조/항목과 절 패턴 확인 (설정에 따라 우선순위 결정)
            elif self.config.item_priority:
                # 조/항목 우선 확인
                if self._is_item(number, title):
                    entry['level'] = 3
                    entry['type'] = 'item'
                elif self._is_section(number, title):
                    entry['level'] = 2
                    entry['type'] = 'section'
            else:
                # 절 우선 확인
                if self._is_section(number, title):
                    entry['level'] = 2
                    entry['type'] = 'section'
                elif self._is_item(number, title):
                    entry['level'] = 3
                    entry['type'] = 'item'
            
            # 기본값 (level 2로 유지)
            if 'level' not in entry:
                entry['level'] = 2
                entry['type'] = 'unknown'
            
            fixed_entries.append(entry)
        
        return fixed_entries
    
    def _is_chapter(self, number: str, title: str) -> bool:
        """장 패턴 확인"""
        for pattern in self.chapter_patterns:
            if re.match(pattern, number) or re.match(pattern, title):
                return True
        return False
    
    def _is_section(self, number: str, title: str) -> bool:
        """절 패턴 확인 (n-n 형태)"""
        for pattern in self.section_patterns:
            if re.match(pattern, number) or re.match(pattern, title):
                return True
        return False
    
    def _is_item(self, number: str, title: str) -> bool:
        """조/항목 패턴 확인 (n-n-n 형태)"""
        for pattern in self.item_patterns:
            if re.match(pattern, number) or re.match(pattern, title):
                return True
        return False
    
    def _fix_sections(self, entries: List[Dict]) -> List[Dict]:
        """부문 분류 수정"""
        for entry in entries:
            page = entry.get('page', 0)
            entry['section'] = self._determine_section_by_page(page)
        
        return entries
    
    def _determine_section_by_page(self, page: int) -> str:
        """페이지 번호로 부문 결정"""
        for section, (start, end) in self.config.section_page_ranges.items():
            if start <= page <= end:
                return section
        return "미분류"
    
    def _add_chapter_structure(self, entries: List[Dict]) -> List[Dict]:
        """장 구조 추가 (기본 버전의 기능)"""
        chapters = []
        current_chapter = None
        chapter_entries = []
        
        for entry in entries:
            if entry['level'] == 1 and entry['type'] == 'chapter':
                # 이전 장이 있으면 저장
                if current_chapter:
                    current_chapter['children'] = chapter_entries
                    chapters.append(current_chapter)
                
                # 새 장 시작
                current_chapter = entry.copy()
                chapter_entries = []
            else:
                # 장의 하위 항목
                if current_chapter:
                    chapter_entries.append(entry)
                else:
                    # 장이 없는 경우 직접 추가
                    chapters.append(entry)
        
        # 마지막 장 처리
        if current_chapter:
            current_chapter['children'] = chapter_entries
            chapters.append(current_chapter)
        
        return chapters
    
    def _normalize_numbering(self, entries: List[Dict]) -> List[Dict]:
        """번호 체계 정규화"""
        for entry in entries:
            number = entry.get('number', '')
            
            # 장 번호 정규화: "제1장" → "1"
            if entry['type'] == 'chapter':
                entry['number'] = re.sub(r'^제?(\d+)장', r'\1', number)
            
            # 절 번호: "1-1" 유지
            elif entry['type'] == 'section':
                pass  # 이미 올바른 형식
            
            # 조 번호: "1-1-1" 유지
            elif entry['type'] == 'item':
                pass  # 이미 올바른 형식
        
        return entries
    
    def _fix_parent_child_relationships(self, entries: List[Dict]) -> List[Dict]:
        """부모-자식 관계 수정"""
        # 부모-자식 관계를 재구성
        for entry in entries:
            entry['parent'] = None
            entry['children'] = []
        
        # 계층 구조에 따라 부모-자식 관계 설정
        for i, entry in enumerate(entries):
            current_level = entry.get('level', 0)
            
            # 상위 레벨의 항목을 부모로 찾기
            for j in range(i-1, -1, -1):
                parent_level = entries[j].get('level', 0)
                if parent_level < current_level:
                    entry['parent'] = entries[j].get('number', '')
                    entries[j]['children'].append(entry.get('number', ''))
                    break
        
        return entries
    
    def _print_detailed_statistics(self, entries: List[Dict]) -> None:
        """상세 통계 출력"""
        print("\n=== 범용 계층 구조 수정 상세 통계 ===")
        
        # 레벨별 통계
        level_stats = {}
        for entry in entries:
            level = entry.get('level', 0)
            level_stats[level] = level_stats.get(level, 0) + 1
        
        print("레벨별 항목 수:")
        for level in sorted(level_stats.keys()):
            level_name = {0: "부문헤더", 1: "장", 2: "절", 3: "조/항목"}.get(level, f"레벨{level}")
            print(f"  {level_name} (레벨 {level}): {level_stats[level]}개")
        
        # 부문별 통계
        section_stats = {}
        for entry in entries:
            section = entry.get('section', '미분류')
            section_stats[section] = section_stats.get(section, 0) + 1
        
        print("\n부문별 항목 수:")
        for section in sorted(section_stats.keys()):
            print(f"  {section}: {section_stats[section]}개")
        
        # 타입별 통계
        type_stats = {}
        for entry in entries:
            entry_type = entry.get('type', 'unknown')
            type_stats[entry_type] = type_stats.get(entry_type, 0) + 1
        
        print("\n타입별 항목 수:")
        for entry_type in sorted(type_stats.keys()):
            print(f"  {entry_type}: {type_stats[entry_type]}개")
        
        # 페이지 범위 확인
        pages = [entry.get('page', 0) for entry in entries if entry.get('page', 0) > 0]
        if pages:
            print(f"\n페이지 범위: {min(pages)} ~ {max(pages)}")
        
        # 샘플 출력
        print("\n=== 샘플 구조 ===")
        sample_count = 0
        for entry in entries[:30]:  # 처음 30개만 출력
            level = entry.get('level', 0)
            indent = "  " * level
            number = entry.get('number', '')
            title = entry.get('title', '')
            section = entry.get('section', '')
            entry_type = entry.get('type', '')
            print(f"{indent}{number} {title} ({section}) [{entry_type}]")
            sample_count += 1
            if sample_count >= 30:
                break
    
    def _print_basic_statistics(self, entries: List[Dict]) -> None:
        """기본 통계 출력"""
        print(f"\n=== 기본 통계 ===")
        print(f"총 항목 수: {len(entries)}개")
        
        # 레벨별 개수만 출력
        level_stats = {}
        for entry in entries:
            level = entry.get('level', 0)
            level_stats[level] = level_stats.get(level, 0) + 1
        
        for level in sorted(level_stats.keys()):
            level_name = {0: "부문헤더", 1: "장", 2: "절", 3: "조/항목"}.get(level, f"레벨{level}")
            print(f"{level_name}: {level_stats[level]}개")
    
    def _perform_additional_validation(self, entries: List[Dict]) -> None:
        """추가 검증 수행"""
        print(f"\n🔍 추가 검증:")
        
        # 조/항목 개수 확인
        items = [e for e in entries if e.get('level') == 3]
        print(f"  조/항목 개수: {len(items)}개")
        
        if items:
            print(f"  조/항목 샘플:")
            for item in items[:5]:
                print(f"    {item.get('number')} {item.get('title')}")
        
        # 부문별 조/항목 분포 확인
        section_items = {}
        for item in items:
            section = item.get('section', '미분류')
            section_items[section] = section_items.get(section, 0) + 1
        
        print(f"  부문별 조/항목 분포:")
        for section, count in sorted(section_items.items()):
            print(f"    {section}: {count}개")

def main():
    """메인 함수"""
    # 입력/출력 파일 경로
    input_file = Path("output/toc_structure_20250625_115242.json")
    output_file = Path("output/toc_structure_universal.json")
    
    if not input_file.exists():
        print(f"❌ 입력 파일을 찾을 수 없습니다: {input_file}")
        return
    
    # 설정 예시들
    configs = {
        "기본": FixerConfig(
            item_priority=True,
            separate_chapter_structure=False,
            detailed_statistics=True,
            additional_validation=True
        ),
        "장구조별도": FixerConfig(
            item_priority=True,
            separate_chapter_structure=True,
            detailed_statistics=True,
            additional_validation=True
        ),
        "절우선": FixerConfig(
            item_priority=False,
            separate_chapter_structure=False,
            detailed_statistics=True,
            additional_validation=True
        ),
        "간단": FixerConfig(
            item_priority=True,
            separate_chapter_structure=False,
            detailed_statistics=False,
            additional_validation=False
        )
    }
    
    # 기본 설정으로 실행
    config = configs["기본"]
    print(f"🔧 설정: {config}")
    
    # 범용 계층 구조 수정 실행
    fixer = UniversalHierarchyStructureFixer(config)
    success = fixer.fix_hierarchy_structure(input_file, output_file)
    
    if success:
        print(f"\n✅ 범용 계층 구조 수정 완료!")
        print(f"📁 수정된 파일: {output_file}")
        print(f"⚙️ 사용된 설정: {config}")
    else:
        print(f"\n❌ 범용 계층 구조 수정 실패!")

if __name__ == "__main__":
    main() 