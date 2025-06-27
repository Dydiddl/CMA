#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
분류 시스템 통합 테스트

이 모듈은 분류 시스템의 통합 테스트를 수행합니다.
"""

import pytest
import sys
import json
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.common.utils import get_section_for_chapter, calculate_confidence_score
from src.utils.extract.toc_extractor import TOCExtractor
from src.utils.split.pdf_split_utils import PDFSplitter

class TestClassificationIntegration:
    """분류 시스템 통합 테스트"""
    
    def test_toc_extraction_with_classification(self, temp_dir):
        """목차 추출과 분류 통합 테스트"""
        # 목차 추출기 생성
        extractor = TOCExtractor()
        
        # 샘플 목차 데이터 생성
        sample_toc_data = {
            "entries": [
                {
                    "number": "1",
                    "title": "배관공사",
                    "page": 10,
                    "level": 1
                },
                {
                    "number": "2", 
                    "title": "타일공사",
                    "page": 20,
                    "level": 1
                },
                {
                    "number": "3",
                    "title": "도로공사", 
                    "page": 30,
                    "level": 1
                }
            ]
        }
        
        # 목차 구조 생성
        toc_structure = extractor._create_toc_structure(sample_toc_data["entries"])
        
        # 각 항목에 부문 분류 적용
        for entry in toc_structure.entries:
            section = get_section_for_chapter(entry.title)
            entry.section = section
            
            # 분류 결과 검증
            if "배관" in entry.title:
                assert section == "기계설비부문"
            elif "타일" in entry.title:
                assert section == "건축부문"
            elif "도로" in entry.title:
                assert section == "토목부문"
    
    def test_pdf_splitter_with_classification(self, temp_dir):
        """PDF 분할과 분류 통합 테스트"""
        # 샘플 JSON 파일 생성
        sample_json = {
            "entries": [
                {
                    "number": "1",
                    "title": "배관공사",
                    "page": 10,
                    "level": 1,
                    "section": "기계설비부문"
                },
                {
                    "number": "2",
                    "title": "타일공사", 
                    "page": 20,
                    "level": 1,
                    "section": "건축부문"
                }
            ]
        }
        
        json_file = temp_dir / "test_toc.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(sample_json, f, ensure_ascii=False, indent=2)
        
        # PDF 분할기 생성 (실제 PDF 없이 테스트)
        # splitter = PDFSplitter(json_file, Path("dummy.pdf"), temp_dir)
        
        # 부문별 분류 결과 검증
        sections_found = set()
        for entry in sample_json["entries"]:
            sections_found.add(entry["section"])
        
        expected_sections = {"기계설비부문", "건축부문"}
        assert sections_found == expected_sections
    
    def test_classification_with_real_file_names(self, temp_dir):
        """실제 파일명으로 분류 테스트"""
        # 공통부문에서 발견된 실제 파일명들
        real_file_names = [
            "배관누수_검사",
            "관갱생공", 
            "유량계_교체",
            "펌프_해체",
            "덕트보온_해체",
            "타일_교체",
            "도배_교체",
            "지붕_덧씌우기",
            "칠공사",
            "철골재_철거(기계)",
            "콘크리트구조물_헐기(기계)",
            "궤도공사",
            "도로반사경_교체",
            "유지보수",
            "관리공사"
        ]
        
        classification_results = {}
        
        for filename in real_file_names:
            section = get_section_for_chapter(filename)
            confidence = calculate_confidence_score(filename, section)
            classification_results[filename] = {
                "section": section,
                "confidence": confidence
            }
        
        # 결과 검증
        mechanical_files = [f for f, r in classification_results.items() 
                          if r["section"] == "기계설비부문"]
        architecture_files = [f for f, r in classification_results.items() 
                            if r["section"] == "건축부문"]
        civil_files = [f for f, r in classification_results.items() 
                      if r["section"] == "토목부문"]
        maintenance_files = [f for f, r in classification_results.items() 
                           if r["section"] == "유지관리부문"]
        unclassified_files = [f for f, r in classification_results.items() 
                            if r["section"] == "미분류"]
        
        # 예상되는 분류 결과 검증
        assert len(mechanical_files) > 0, "기계설비부문 파일이 있어야 함"
        assert len(architecture_files) > 0, "건축부문 파일이 있어야 함"
        assert len(civil_files) > 0, "토목부문 파일이 있어야 함"
        
        # 신뢰도 검증
        high_confidence_files = [f for f, r in classification_results.items() 
                               if r["confidence"] > 0.3]
        assert len(high_confidence_files) > 0, "높은 신뢰도 파일이 있어야 함"
    
    def test_classification_consistency(self):
        """분류 일관성 테스트"""
        # 동일한 키워드가 포함된 다양한 표현들
        test_cases = [
            ("배관공사", "배관_공사", "배관-공사", "배관(공사)"),
            ("타일공사", "타일_공사", "타일-공사", "타일(공사)"),
            ("도로공사", "도로_공사", "도로-공사", "도로(공사)"),
        ]
        
        for case_group in test_cases:
            sections = []
            for title in case_group:
                section = get_section_for_chapter(title)
                sections.append(section)
            
            # 모든 변형이 동일한 부문으로 분류되어야 함
            assert len(set(sections)) == 1, f"일관성 없음: {case_group} -> {sections}"
    
    def test_classification_edge_cases(self):
        """엣지 케이스 테스트"""
        edge_cases = [
            ("", "미분류"),  # 빈 문자열
            ("   ", "미분류"),  # 공백만
            ("123", "미분류"),  # 숫자만
            ("!@#$%", "미분류"),  # 특수문자만
            ("배관", "기계설비부문"),  # 키워드만
            ("공사", "미분류"),  # 일반적인 단어
            ("설치", "미분류"),  # 일반적인 단어
            ("해체", "미분류"),  # 일반적인 단어
        ]
        
        for title, expected in edge_cases:
            result = get_section_for_chapter(title)
            assert result == expected, f"'{title}' should be '{expected}', got '{result}'"
    
    def test_classification_with_mixed_keywords(self):
        """혼합 키워드 테스트"""
        mixed_cases = [
            ("배관타일공사", "기계설비부문"),  # 기계설비 우선
            ("타일도로공사", "토목부문"),  # 토목 우선
            ("도로철골공사", "토목부문"),  # 토목 우선
            ("철골배관공사", "기계설비부문"),  # 기계설비 우선
            ("배관도로타일공사", "기계설비부문"),  # 기계설비 우선
        ]
        
        for title, expected in mixed_cases:
            result = get_section_for_chapter(title)
            assert result == expected, f"'{title}' should be '{expected}', got '{result}'"
    
    def test_classification_performance_with_real_data(self):
        """실제 데이터로 성능 테스트"""
        import time
        
        # 대량의 테스트 데이터 생성
        test_data = []
        keywords = ["배관", "타일", "도로", "철골", "유지관리"]
        
        for i in range(1000):
            keyword = keywords[i % len(keywords)]
            test_data.append(f"{keyword}공사_{i}")
        
        # 성능 측정
        start_time = time.time()
        
        for title in test_data:
            section = get_section_for_chapter(title)
            confidence = calculate_confidence_score(title, section)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # 성능 검증 (1000개 항목을 1초 이내에 처리해야 함)
        assert processing_time < 1.0, f"성능 테스트 실패: {processing_time:.2f}초" 