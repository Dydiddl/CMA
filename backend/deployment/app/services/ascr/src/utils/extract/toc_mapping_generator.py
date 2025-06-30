#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
목차 매핑 생성 모듈 (TOC Mapping Generator)

이 모듈은 목차 구조를 기반으로 매핑 정보를 생성하는 기능을 제공합니다.
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

# ASCR 커스텀 로깅 시스템 사용
from ..log import get_logger

# 공통 모듈 import
from src.common.constants import SUPPORTED_FORMATS, SUCCESS_MESSAGES, ERROR_MESSAGES
from src.common.types import TOCStructure
from src.common.exceptions import TOCExtractionError, TOCValidationError

# 로거 초기화
logger = get_logger("TOCMappingGenerator")

class TOCMappingGenerator:
    """목차 매핑 설정 생성 클래스"""
    
    def __init__(self):
        self.supported_formats = SUPPORTED_FORMATS
    
    def generate_mapping_config(self, toc_structure: TOCStructure) -> Dict[str, Any]:
        """
        목차 구조를 기반으로 매핑 설정 생성
        
        Args:
            toc_structure: 목차 구조 객체
            
        Returns:
            매핑 설정 딕셔너리
        """
        logger.info("매핑 설정 생성 시작")
        
        try:
            mapping_config = {
                "metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "version": "2.0",
                    "description": "ASCR 목차 매핑 설정"
                },
                "sections": {},
                "chapters": {},
                "patterns": {},
                "validation_rules": {}
            }
            
            # 섹션별 매핑 생성
            for section_name, section_data in toc_structure.sections.items():
                # section_data가 딕셔너리인지 확인
                if isinstance(section_data, dict):
                    chapters = section_data.get("chapters", [])
                    entries = section_data.get("entries", [])
                else:
                    chapters = []
                    entries = []
                
                mapping_config["sections"][section_name] = {
                    "name": section_name,
                    "chapters": chapters,
                    "total_chapters": len(chapters),
                    "page_range": self._get_page_range(entries)
                }
            
            # 장별 매핑 생성
            for entry in toc_structure.entries:
                if entry.level == 1:  # 장 레벨
                    # children가 문자열 리스트인지 확인
                    if isinstance(entry.children, list):
                        subsections = [child for child in entry.children if isinstance(child, str)]
                        total_subsections = len(subsections)
                    else:
                        subsections = []
                        total_subsections = 0
                    
                    mapping_config["chapters"][entry.number] = {
                        "title": entry.title,
                        "section": entry.section,
                        "page": entry.page,
                        "subsections": subsections,
                        "total_subsections": total_subsections
                    }
            
            # 패턴 매핑 생성
            mapping_config["patterns"] = self._generate_pattern_mappings(toc_structure)
            
            # 검증 규칙 생성
            mapping_config["validation_rules"] = self._generate_validation_rules(toc_structure)
            
            logger.info("매핑 설정 생성 완료")
            return mapping_config
            
        except Exception as e:
            logger.error(f"매핑 설정 생성 실패: {e}")
            raise TOCExtractionError("toc_mapping_generator", "generate_mapping_config", str(e))
    
    def _get_page_range(self, entries: List) -> Dict[str, int]:
        """페이지 범위 계산"""
        if not entries:
            return {"start": 0, "end": 0}
        
        # entries가 TOCEntry 객체인지 확인
        pages = []
        for entry in entries:
            if hasattr(entry, 'page') and entry.page > 0:
                pages.append(entry.page)
            elif isinstance(entry, dict) and 'page' in entry and entry['page'] > 0:
                pages.append(entry['page'])
        
        if not pages:
            return {"start": 0, "end": 0}
        
        return {
            "start": min(pages),
            "end": max(pages)
        }
    
    def _generate_pattern_mappings(self, toc_structure: TOCStructure) -> Dict[str, Any]:
        """패턴 매핑 생성"""
        patterns = {
            "chapter_patterns": [],
            "section_patterns": [],
            "item_patterns": []
        }
        
        for entry in toc_structure.entries:
            if entry.level == 1:  # 장
                patterns["chapter_patterns"].append({
                    "pattern": f"제{entry.number.replace('제', '').replace('장', '')}장",
                    "example": entry.title,
                    "section": entry.section
                })
            elif entry.level == 2:  # 절
                patterns["section_patterns"].append({
                    "pattern": entry.number,
                    "example": entry.title,
                    "chapter": entry.chapter
                })
            elif entry.level == 3:  # 조/항목
                patterns["item_patterns"].append({
                    "pattern": entry.number,
                    "example": entry.title,
                    "subsection": entry.subsection
                })
        
        return patterns
    
    def _generate_validation_rules(self, toc_structure: TOCStructure) -> Dict[str, Any]:
        """검증 규칙 생성"""
        rules = {
            "required_sections": list(toc_structure.sections.keys()),
            "min_chapters_per_section": 1,
            "max_chapters_per_section": 50,
            "page_number_validation": True,
            "hierarchy_validation": True
        }
        
        # 섹션별 장 수 검증 규칙
        for section_name, section_data in toc_structure.sections.items():
            chapter_count = len(section_data.get("chapters", []))
            rules[f"min_chapters_{section_name}"] = max(1, chapter_count // 2)
            rules[f"max_chapters_{section_name}"] = chapter_count * 2
        
        return rules
    
    def save_toc_structure(self, toc_structure: TOCStructure, 
                          output_path: Path, format: str = 'json') -> bool:
        """
        목차 구조를 파일로 저장
        
        Args:
            toc_structure: 목차 구조 객체
            output_path: 출력 파일 경로
            format: 출력 형식 ('json', 'csv', 'markdown', 'yaml')
            
        Returns:
            저장 성공 여부
        """
        try:
            if format == 'json':
                return self._save_json(toc_structure, output_path)
            elif format == 'csv':
                return self._save_csv(toc_structure, output_path)
            elif format == 'markdown':
                return self._save_markdown(toc_structure, output_path)
            elif format == 'yaml':
                return self._save_yaml(toc_structure, output_path)
            else:
                raise ValueError(f"지원하지 않는 형식: {format}")
                
        except Exception as e:
            logger.error(f"목차 구조 저장 실패: {e}")
            return False
    
    def _save_json(self, toc_structure: TOCStructure, output_path: Path) -> bool:
        """JSON 형식으로 저장"""
        try:
            # TOCStructure를 딕셔너리로 변환
            data = {
                "entries": [
                    entry.to_dict() if hasattr(entry, 'to_dict') else {
                        "number": entry.number,
                        "title": entry.title,
                        "level": entry.level,
                        "page": entry.page,
                        "section": entry.section,
                        "chapter": entry.chapter,
                        "subsection": entry.subsection
                    }
                    for entry in toc_structure.entries
                ],
                "sections": toc_structure.sections,
                "metadata": toc_structure.metadata
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"JSON 파일 저장 완료: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"JSON 저장 실패: {e}")
            return False
    
    def _save_csv(self, toc_structure: TOCStructure, output_path: Path) -> bool:
        """CSV 형식으로 저장"""
        try:
            import csv
            
            with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['Number', 'Title', 'Level', 'Page', 'Section', 'Chapter', 'Subsection'])
                
                for entry in toc_structure.entries:
                    writer.writerow([
                        entry.number,
                        entry.title,
                        entry.level,
                        entry.page,
                        entry.section,
                        entry.chapter,
                        entry.subsection
                    ])
            
            logger.info(f"CSV 파일 저장 완료: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"CSV 저장 실패: {e}")
            return False
    
    def _save_markdown(self, toc_structure: TOCStructure, output_path: Path) -> bool:
        """마크다운 형식으로 저장"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("# 목차 구조\n\n")
                
                for entry in toc_structure.entries:
                    indent = "  " * entry.level
                    f.write(f"{indent}- {entry.number} {entry.title} (p.{entry.page})\n")
            
            logger.info(f"마크다운 파일 저장 완료: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"마크다운 저장 실패: {e}")
            return False
    
    def _save_yaml(self, toc_structure: TOCStructure, output_path: Path) -> bool:
        """YAML 형식으로 저장"""
        try:
            import yaml
            
            data = {
                "entries": [
                    {
                        "number": entry.number,
                        "title": entry.title,
                        "level": entry.level,
                        "page": entry.page,
                        "section": entry.section,
                        "chapter": entry.chapter,
                        "subsection": entry.subsection
                    }
                    for entry in toc_structure.entries
                ],
                "sections": toc_structure.sections,
                "metadata": toc_structure.metadata
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            
            logger.info(f"YAML 파일 저장 완료: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"YAML 저장 실패: {e}")
            return False
    
    def validate_toc_structure(self, toc_structure) -> bool:
        """목차 구조 검증"""
        try:
            if not toc_structure.entries:
                logger.warning("목차 항목이 없습니다")
                return False
            
            # 기본 검증
            for entry in toc_structure.entries:
                if not entry.title:
                    logger.warning(f"제목이 없는 항목 발견: {entry.number}")
                    return False
                
                if entry.level < 0 or entry.level > 5:
                    logger.warning(f"잘못된 레벨: {entry.level}")
                    return False
            
            logger.info("목차 구조 검증 통과")
            return True
            
        except Exception as e:
            logger.error(f"목차 구조 검증 실패: {e}")
            return False 