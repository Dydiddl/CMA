#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
부문별 추출 모듈 (Section Extractor)

이 모듈은 목차에서 부문(공통부문, 토목부문 등)을 추출하는 기능을 제공합니다.
"""

import re
import logging
from typing import Optional, Tuple
from src.common.types import TOCEntry

logger = logging.getLogger(__name__)

class SectionExtractor:
    """부문별 추출 클래스"""
    
    def __init__(self):
        self.section_patterns = {
            "공통부문": r'공\s*통\s*부\s*문',
            "토목부문": r'토\s*목\s*부\s*문',
            "건축부문": r'건\s*축\s*부\s*문',
            "기계설비부문": r'기\s*계\s*설\s*비\s*부\s*문',
            "유지관리부문": r'유\s*지\s*관\s*리\s*부\s*문'
        }
    
    def extract_section(self, line: str) -> Optional[Tuple[str, TOCEntry]]:
        """라인에서 부문 추출"""
        for section_name, pattern in self.section_patterns.items():
            if re.search(pattern, line):
                section_entry = TOCEntry(
                    number=section_name,
                    title=section_name,
                    level=0,
                    page=0,
                    section=section_name,
                    chapter="",
                    parent=None,
                    children=[],
                    subsection=""
                )
                return section_name, section_entry
        
        return None
    
    def is_section_line(self, line: str) -> bool:
        """부문 라인인지 확인"""
        return any(re.search(pattern, line) for pattern in self.section_patterns.values()) 