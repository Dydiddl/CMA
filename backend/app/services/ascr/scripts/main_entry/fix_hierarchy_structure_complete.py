#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
완전한 계층 구조 수정 스크립트

이 스크립트는 추출된 목차 구조의 계층 레벨, 부문 분류, 장 구조 등을 수정합니다.
모든 레벨(장, 절, 조/항목)을 포함하여 올바른 계층 구조를 생성합니다.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# ASCR 커스텀 로깅 시스템 사용
from src.utils.log import get_logger

# 로거 초기화
logger = get_logger("HierarchyFixer")

class CompleteHierarchyStructureFixer:
    """완전한 계층 구조 수정 클래스"""
    
    def __init__(self):
        # 부문별 페이지 범위 정의 (실제 PDF 기반으로 조정)
        self.section_page_ranges = {
            "공통부문": (3, 298),
            "토목부문": (299, 400), 
            "건축부문": (401, 600),
            "기계설비부문": (601, 800),
            "유지관리부문": (801, 900)
        }
        
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
            logger.info(f"계층 구조 수정 시작: {input_file}")
            
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
            
            # 4. 번호 체계 정규화
            fixed_entries = self._normalize_numbering(fixed_entries)
            logger.info("번호 체계 정규화 완료")
            
            # 5. 부모-자식 관계 수정
            fixed_entries = self._fix_parent_child_relationships(fixed_entries)
            logger.info("부모-자식 관계 수정 완료")
            
            # 6. 결과 저장
            result_data = {
                "entries": fixed_entries,
                "metadata": {
                    "original_file": str(input_file),
                    "fixed_at": datetime.now().isoformat(),
                    "total_entries": len(fixed_entries),
                    "fix_method": "complete_hierarchy_structure_fixer"
                }
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"수정된 구조 저장 완료: {output_file}")
            
            # 7. 통계 출력
            self._print_statistics(fixed_entries)
            
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
            
            # 조/항목 패턴 확인 (level 3) - 절보다 먼저 확인
            elif self._is_item(number, title):
                entry['level'] = 3
                entry['type'] = 'item'
            
            # 절 패턴 확인 (level 2)
            elif self._is_section(number, title):
                entry['level'] = 2
                entry['type'] = 'section'
            
            # 기본값 (level 2로 유지)
            else:
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
        for section, (start, end) in self.section_page_ranges.items():
            if start <= page <= end:
                return section
        return "미분류"
    
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
    
    def _print_statistics(self, entries: List[Dict]) -> None:
        """통계 출력"""
        print("\n=== 계층 구조 수정 통계 ===")
        
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

def main():
    """메인 함수"""
    # 입력/출력 파일 경로
    input_file = Path("output/toc_structure_20250624_220446.json")
    output_file = Path("output/toc_structure_fixed_complete.json")
    
    if not input_file.exists():
        print(f"❌ 입력 파일을 찾을 수 없습니다: {input_file}")
        return
    
    # 계층 구조 수정 실행
    fixer = CompleteHierarchyStructureFixer()
    success = fixer.fix_hierarchy_structure(input_file, output_file)
    
    if success:
        print(f"\n✅ 계층 구조 수정 완료!")
        print(f"📁 수정된 파일: {output_file}")
        
        # 추가 검증
        print(f"\n🔍 추가 검증:")
        with open(output_file, 'r', encoding='utf-8') as f:
            result_data = json.load(f)
        
        entries = result_data.get('entries', [])
        
        # 조/항목 개수 확인
        items = [e for e in entries if e.get('level') == 3]
        print(f"  조/항목 개수: {len(items)}개")
        
        if items:
            print(f"  조/항목 샘플:")
            for item in items[:5]:
                print(f"    {item.get('number')} {item.get('title')}")
        
    else:
        print(f"\n❌ 계층 구조 수정 실패!")

if __name__ == "__main__":
    main() 