#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
계층 구조 검증 및 수정 스크립트

이 스크립트는 기존 목차 구조의 계층 관계를 검증하고 수정합니다.
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.common.constants import SECTION_MAPPING, COMMON_SECTIONS, CIVIL_SECTIONS, ARCHITECTURE_SECTIONS, MECHANICAL_SECTIONS, MAINTENANCE_SECTIONS
from src.utils.log import get_logger

logger = get_logger(__name__)

class HierarchyValidator:
    """계층 구조 검증 및 수정 클래스"""
    
    def __init__(self):
        self.section_mappings = {
            **COMMON_SECTIONS,
            **CIVIL_SECTIONS,
            **ARCHITECTURE_SECTIONS,
            **MECHANICAL_SECTIONS,
            **MAINTENANCE_SECTIONS
        }
        
        # 장 패턴
        self.chapter_pattern = re.compile(r'^제(\d+)장\s*(.+)$')
        
        # 절 패턴
        self.section_pattern = re.compile(r'^(\d+)-(\d+)\s*(.+)$')
        
        # 조/항목 패턴
        self.item_pattern = re.compile(r'^(\d+)-(\d+)-(\d+)\s*(.+)$')
    
    def validate_and_fix_hierarchy(self, toc_structure: Dict[str, Any]) -> Dict[str, Any]:
        """계층 구조 검증 및 수정"""
        entries = toc_structure.get("entries", [])
        
        print("🔍 계층 구조 검증 시작...")
        
        # 1단계: 기본 검증
        validation_errors = self._validate_basic_structure(entries)
        
        # 2단계: 부문별 분류 수정
        fixed_entries = self._fix_section_classification(entries)
        
        # 3단계: 계층 관계 수정
        fixed_entries = self._fix_hierarchy_relationships(fixed_entries)
        
        # 4단계: 페이지 번호 수정
        fixed_entries = self._fix_page_numbers(fixed_entries)
        
        # 5단계: 부모-자식 관계 재구성
        fixed_entries = self._rebuild_parent_child_relationships(fixed_entries)
        
        # 6단계: 부문별 통계 재생성
        fixed_sections = self._regenerate_section_stats(fixed_entries)
        
        # 수정된 구조 반환
        fixed_structure = {
            "entries": fixed_entries,
            "sections": fixed_sections,
            "metadata": {
                **toc_structure.get("metadata", {}),
                "hierarchy_fixed": True,
                "fix_time": datetime.now().isoformat(),
                "validation_errors": validation_errors
            }
        }
        
        return fixed_structure
    
    def _validate_basic_structure(self, entries: List[Dict]) -> List[str]:
        """기본 구조 검증"""
        errors = []
        
        for entry in entries:
            # 레벨 검증
            if entry.get("level") not in [0, 1, 2, 3]:
                errors.append(f"잘못된 레벨: {entry.get('number')} - 레벨 {entry.get('level')}")
            
            # 페이지 번호 검증
            page = entry.get("page", 0)
            if page > 9999:  # 4자리 이상은 오류
                errors.append(f"잘못된 페이지 번호: {entry.get('number')} - {page}")
            
            # 부모-자식 관계 검증
            parent = entry.get("parent")
            children = entry.get("children", [])
            
            if parent and parent not in [e.get("number") for e in entries]:
                errors.append(f"존재하지 않는 부모: {entry.get('number')} -> {parent}")
            
            for child in children:
                if child not in [e.get("number") for e in entries]:
                    errors.append(f"존재하지 않는 자식: {entry.get('number')} -> {child}")
        
        return errors
    
    def _fix_section_classification(self, entries: List[Dict]) -> List[Dict]:
        """부문별 분류 수정"""
        print("🔧 부문별 분류 수정 중...")
        
        for entry in entries:
            if entry.get("level") == 1:  # 장 레벨
                chapter_title = f"{entry.get('number')} {entry.get('title', '')}"
                
                # 정확한 부문 매핑 적용
                if chapter_title in self.section_mappings:
                    entry["section"] = self.section_mappings[chapter_title]
                else:
                    # 키워드 기반 분류
                    title = entry.get("title", "")
                    if any(keyword in title for keyword in ["적용기준", "가설", "토공", "조경", "기초", "철근콘크리트", "돌공", "건설기계"]):
                        entry["section"] = "공통부문"
                    elif any(keyword in title for keyword in ["도로", "하천", "터널", "궤도", "강구조", "관부설", "항만", "지반", "측량"]):
                        entry["section"] = "토목부문"
                    elif any(keyword in title for keyword in ["철골", "조적", "타일", "목공", "수장", "방수", "지붕", "금속", "미장", "창호", "칠"]):
                        entry["section"] = "건축부문"
                    elif any(keyword in title for keyword in ["배관", "덕트", "보온", "펌프", "밸브", "측정", "위생", "공기조화", "소방", "가스", "자동제어", "플랜트"]):
                        entry["section"] = "기계설비부문"
                    elif any(keyword in title for keyword in ["유지", "관리", "공 통", "토 목", "건 축", "기계설비"]):
                        entry["section"] = "유지관리부문"
                    else:
                        entry["section"] = "미분류"
        
        return entries
    
    def _fix_hierarchy_relationships(self, entries: List[Dict]) -> List[Dict]:
        """계층 관계 수정"""
        print("🔧 계층 관계 수정 중...")
        
        # 레벨별로 정렬
        level_0 = [e for e in entries if e.get("level") == 0]  # 부문
        level_1 = [e for e in entries if e.get("level") == 1]  # 장
        level_2 = [e for e in entries if e.get("level") == 2]  # 절
        level_3 = [e for e in entries if e.get("level") == 3]  # 조/항목
        
        # 부모-자식 관계 재설정
        for entry in entries:
            entry["children"] = []
            entry["parent"] = None
        
        # 부문 → 장 관계
        for chapter in level_1:
            section = chapter.get("section")
            for section_entry in level_0:
                if section_entry.get("title") == section:
                    chapter["parent"] = section_entry.get("number")
                    section_entry["children"].append(chapter.get("number"))
                    break
        
        # 장 → 절 관계
        for section in level_2:
            section_num = section.get("number", "")
            if "-" in section_num:
                chapter_num = section_num.split("-")[0]
                for chapter in level_1:
                    if chapter.get("number") == f"제{chapter_num}장":
                        section["parent"] = chapter.get("number")
                        chapter["children"].append(section.get("number"))
                        break
        
        # 절 → 조/항목 관계
        for item in level_3:
            item_num = item.get("number", "")
            if item_num.count("-") == 2:
                section_num = "-".join(item_num.split("-")[:2])
                for section in level_2:
                    if section.get("number") == section_num:
                        item["parent"] = section.get("number")
                        section["children"].append(item.get("number"))
                        break
        
        return entries
    
    def _fix_page_numbers(self, entries: List[Dict]) -> List[Dict]:
        """페이지 번호 수정"""
        print("🔧 페이지 번호 수정 중...")
        
        for entry in entries:
            page = entry.get("page", 0)
            
            # 4자리 이상인 경우 수정
            if page > 9999:
                # 마지막 3자리를 페이지 번호로 사용
                page_str = str(page)
                if len(page_str) >= 3:
                    fixed_page = int(page_str[-3:])
                    entry["page"] = fixed_page
                    print(f"  페이지 번호 수정: {entry.get('number')} {page} → {fixed_page}")
        
        return entries
    
    def _rebuild_parent_child_relationships(self, entries: List[Dict]) -> List[Dict]:
        """부모-자식 관계 재구성"""
        print("🔧 부모-자식 관계 재구성 중...")
        
        # 기존 관계 초기화
        for entry in entries:
            entry["children"] = []
        
        # 올바른 계층 구조 재구성
        current_section = None
        current_chapter = None
        
        for entry in entries:
            level = entry.get("level", 0)
            
            if level == 0:  # 부문
                current_section = entry
                current_chapter = None
            elif level == 1:  # 장
                if current_section:
                    entry["parent"] = current_section.get("number")
                    current_section["children"].append(entry.get("number"))
                current_chapter = entry
            elif level == 2:  # 절
                if current_chapter:
                    entry["parent"] = current_chapter.get("number")
                    current_chapter["children"].append(entry.get("number"))
            elif level == 3:  # 조/항목
                # 해당 절을 찾아서 부모로 설정
                item_num = entry.get("number", "")
                if item_num.count("-") == 2:
                    section_num = "-".join(item_num.split("-")[:2])
                    for section_entry in entries:
                        if section_entry.get("number") == section_num and section_entry.get("level") == 2:
                            entry["parent"] = section_entry.get("number")
                            section_entry["children"].append(entry.get("number"))
                            break
        
        return entries
    
    def _regenerate_section_stats(self, entries: List[Dict]) -> Dict[str, Any]:
        """부문별 통계 재생성"""
        print("📊 부문별 통계 재생성 중...")
        
        sections = {}
        
        for entry in entries:
            section = entry.get("section", "미분류")
            if section not in sections:
                sections[section] = {
                    "count": 0,
                    "entries": [],
                    "pages": [],
                    "chapters": []
                }
            
            sections[section]["count"] += 1
            sections[section]["entries"].append(entry.get("number"))
            
            if entry.get("page", 0) > 0:
                sections[section]["pages"].append(entry.get("page"))
            
            if entry.get("level") == 1:  # 장 레벨
                sections[section]["chapters"].append(entry.get("number"))
        
        return sections

def main():
    """메인 함수"""
    try:
        # 최신 JSON 파일 찾기
        output_dir = Path("output")
        json_files = list(output_dir.glob("toc_structure_*.json"))
        
        if not json_files:
            print("❌ 처리할 JSON 파일을 찾을 수 없습니다.")
            return False
        
        # 가장 최신 파일 선택
        latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
        print(f"📄 처리할 파일: {latest_file}")
        
        # JSON 파일 읽기
        with open(latest_file, 'r', encoding='utf-8') as f:
            toc_structure = json.load(f)
        
        # 계층 구조 검증 및 수정
        validator = HierarchyValidator()
        fixed_structure = validator.validate_and_fix_hierarchy(toc_structure)
        
        # 수정된 파일 저장
        output_file = output_dir / f"toc_structure_fixed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(fixed_structure, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 계층 구조 수정 완료")
        print(f"📊 총 항목 수: {len(fixed_structure['entries'])}")
        print(f"📁 부문 수: {len(fixed_structure['sections'])}")
        
        # 부문별 통계 출력
        print("\n📋 부문별 통계:")
        for section_name, stats in fixed_structure["sections"].items():
            print(f"  {section_name}: {stats['count']}개 항목, {len(stats['chapters'])}개 장")
        
        # 검증 오류 출력
        validation_errors = fixed_structure.get("metadata", {}).get("validation_errors", [])
        if validation_errors:
            print(f"\n⚠️ 검증 오류 ({len(validation_errors)}개):")
            for error in validation_errors[:10]:  # 처음 10개만 출력
                print(f"  - {error}")
        
        print(f"\n💾 수정된 파일 저장: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        logger.error(f"계층 구조 수정 실패: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 