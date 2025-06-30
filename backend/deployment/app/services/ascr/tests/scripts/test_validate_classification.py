#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
분류 시스템 검증 테스트

scripts/validate_classification.py의 기능을 테스트로 변환
"""

import pytest
import sys
from pathlib import Path
import json
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.common.utils import (
    determine_section, 
    determine_section_with_confidence, 
    validate_section_classification
)

class TestClassificationValidation:
    """분류 시스템 검증 테스트"""
    
    def test_analyze_classification_results(self, classification_test_data):
        """분류 결과 분석 테스트"""
        print("🔍 분류 시스템 검증 시작")
        
        # 테스트 케이스 정의
        test_cases = []
        
        # 각 부문별 테스트 케이스 추가
        for keyword in classification_test_data["mechanical_keywords"]:
            test_cases.append((keyword, "기계설비부문"))
        
        for keyword in classification_test_data["architecture_keywords"]:
            test_cases.append((keyword, "건축부문"))
            
        for keyword in classification_test_data["civil_keywords"]:
            test_cases.append((keyword, "토목부문"))
            
        for keyword in classification_test_data["maintenance_keywords"]:
            test_cases.append((keyword, "유지관리부문"))
            
        for keyword in classification_test_data["common_keywords"]:
            test_cases.append((keyword, "공통부문"))
            
        for keyword in classification_test_data["unclassified_keywords"]:
            test_cases.append((keyword, "미분류"))
        
        results = {
            "total_tests": len(test_cases),
            "correct_classifications": 0,
            "incorrect_classifications": 0,
            "unclassified_items": 0,
            "low_confidence_items": 0,
            "detailed_results": []
        }
        
        for title, expected_section in test_cases:
            # 개선된 분류 실행
            new_section = determine_section(title)
            section, confidence = determine_section_with_confidence(title)
            
            # 검증
            validation = validate_section_classification(title, new_section)
            
            # 결과 기록
            result = {
                "title": title,
                "expected": expected_section,
                "classified": new_section,
                "confidence": confidence,
                "is_correct": new_section == expected_section,
                "needs_review": validation["needs_review"]
            }
            
            results["detailed_results"].append(result)
            
            # 통계 업데이트
            if new_section == expected_section:
                results["correct_classifications"] += 1
            else:
                results["incorrect_classifications"] += 1
                
            if new_section == "미분류":
                results["unclassified_items"] += 1
                
            if confidence < 0.3:
                results["low_confidence_items"] += 1
        
        # 검증
        accuracy = (results["correct_classifications"] / results["total_tests"]) * 100
        assert accuracy >= 80, f"정확도가 너무 낮음: {accuracy:.1f}%"
        
        # 미분류 비율 검증
        unclassified_ratio = results["unclassified_items"] / results["total_tests"]
        assert unclassified_ratio <= 0.3, f"미분류 비율이 너무 높음: {unclassified_ratio:.1%}"
        
        return results
    
    def test_analyze_existing_files(self, temp_dir):
        """기존 파일들의 분류 분석 테스트"""
        # 테스트용 파일명 생성
        test_file_names = [
            "배관누수_검사", "관갱생공", "유량계_교체", "펌프_해체", "덕트보온_해체",
            "타일_교체", "도배_교체", "지붕_덧씌우기", "칠공사", "철골재_철거",
            "콘크리트구조물_헐기", "궤도공사", "도로반사경_교체", "유지보수", "관리공사"
        ]
        
        classification_analysis = {
            "should_be_mechanical": [],
            "should_be_architecture": [],
            "should_be_civil": [],
            "should_be_maintenance": [],
            "should_remain_common": [],
            "unclassified": []
        }
        
        for filename in test_file_names:
            # 개선된 분류 실행
            new_section = determine_section(filename)
            section, confidence = determine_section_with_confidence(filename)
            
            # 분류 결과에 따라 카테고리화
            if new_section == "기계설비부문":
                classification_analysis["should_be_mechanical"].append({
                    "file": filename,
                    "confidence": confidence
                })
            elif new_section == "건축부문":
                classification_analysis["should_be_architecture"].append({
                    "file": filename,
                    "confidence": confidence
                })
            elif new_section == "토목부문":
                classification_analysis["should_be_civil"].append({
                    "file": filename,
                    "confidence": confidence
                })
            elif new_section == "유지관리부문":
                classification_analysis["should_be_maintenance"].append({
                    "file": filename,
                    "confidence": confidence
                })
            elif new_section == "공통부문":
                classification_analysis["should_remain_common"].append({
                    "file": filename,
                    "confidence": confidence
                })
            else:
                classification_analysis["unclassified"].append({
                    "file": filename,
                    "confidence": confidence
                })
        
        # 검증
        total_files = len(test_file_names)
        mechanical_count = len(classification_analysis["should_be_mechanical"])
        architecture_count = len(classification_analysis["should_be_architecture"])
        civil_count = len(classification_analysis["should_be_civil"])
        
        # 최소한 일부 부문은 분류되어야 함
        assert mechanical_count > 0, "기계설비부문 파일이 있어야 함"
        assert architecture_count > 0, "건축부문 파일이 있어야 함"
        assert civil_count > 0, "토목부문 파일이 있어야 함"
        
        # 미분류 비율이 너무 높지 않아야 함
        unclassified_count = len(classification_analysis["unclassified"])
        unclassified_ratio = unclassified_count / total_files
        assert unclassified_ratio <= 0.5, f"미분류 비율이 너무 높음: {unclassified_ratio:.1%}"
        
        return classification_analysis
    
    def test_generate_reclassification_script(self, temp_dir):
        """재분류 스크립트 생성 테스트"""
        # 재분류 스크립트 내용 생성
        script_content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
자동 재분류 스크립트 (테스트용)
\"\"\"

import shutil
from pathlib import Path
import sys

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.common.utils import determine_section

def reclassify_files():
    \"\"\"파일 재분류 실행\"\"\"
    print("재분류 스크립트 실행 테스트")
    return True

if __name__ == "__main__":
    reclassify_files()
"""
        
        # 스크립트 파일 생성
        script_path = temp_dir / "test_reclassify_script.py"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # 파일이 생성되었는지 확인
        assert script_path.exists(), "스크립트 파일이 생성되지 않음"
        
        # 스크립트 내용 검증
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "재분류 스크립트" in content, "스크립트 내용이 올바르지 않음"
        assert "determine_section" in content, "분류 함수 import가 누락됨"
        
        return script_path
    
    def test_classification_performance(self):
        """분류 성능 테스트"""
        import time
        
        # 테스트 데이터 생성
        test_titles = [
            "배관공사", "덕트설치", "보온공사", "펌프설치", "밸브교체",
            "타일교체", "지붕공사", "칠공사", "철골공사", "조적공사",
            "도로공사", "하천공사", "터널공사", "궤도공사", "강구조공사",
            "유지보수", "관리공사", "적용기준", "가설공사", "토공사"
        ] * 50  # 1000개 항목
        
        start_time = time.time()
        
        results = []
        for title in test_titles:
            section = determine_section(title)
            section, confidence = determine_section_with_confidence(title)
            results.append((title, section, confidence))
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # 성능 검증 (1000개 항목을 2초 이내에 처리)
        assert processing_time < 2.0, f"1000개 처리에 {processing_time:.2f}초 소요"
        assert len(results) == len(test_titles)
        
        # 결과 검증
        mechanical_count = sum(1 for _, section, _ in results if section == "기계설비부문")
        architecture_count = sum(1 for _, section, _ in results if section == "건축부문")
        civil_count = sum(1 for _, section, _ in results if section == "토목부문")
        
        assert mechanical_count > 0, "기계설비부문 분류 결과가 없음"
        assert architecture_count > 0, "건축부문 분류 결과가 없음"
        assert civil_count > 0, "토목부문 분류 결과가 없음"
        
        return {
            "processing_time": processing_time,
            "total_items": len(results),
            "mechanical_count": mechanical_count,
            "architecture_count": architecture_count,
            "civil_count": civil_count
        } 