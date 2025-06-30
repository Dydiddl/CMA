#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pytest 설정 파일
"""

import pytest
import sys
import time
import logging
import json
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture
def sample_pdf_path():
    """테스트용 샘플 PDF 파일 경로"""
    return project_root / "tests" / "fixtures" / "sample.pdf"

@pytest.fixture
def temp_dir():
    """임시 디렉토리"""
    temp_path = project_root / "temp" / "test"
    temp_path.mkdir(parents=True, exist_ok=True)
    yield temp_path
    # 테스트 후 정리 (Windows 호환성 개선)
    import shutil
    if temp_path.exists():
        try:
            # 로그 핸들러들을 정리
            for logger_name in logging.root.manager.loggerDict:
                logger = logging.getLogger(logger_name)
                for handler in logger.handlers[:]:
                    handler.close()
                    logger.removeHandler(handler)
            
            # 잠시 대기 후 삭제 시도
            time.sleep(0.1)
            shutil.rmtree(temp_path)
        except PermissionError:
            # Windows에서 파일이 사용 중인 경우 무시
            pass

@pytest.fixture
def test_config():
    """테스트용 설정"""
    return {
        "input_dir": "tests/fixtures",
        "output_dir": "temp/test_output",
        "log_level": "DEBUG"
    }

@pytest.fixture
def classification_test_data():
    """분류 시스템 테스트용 데이터"""
    return {
        "mechanical_keywords": [
            "배관공사", "덕트설치", "보온공사", "펌프설치", "밸브교체",
            "위생설비", "소방설비", "가스설비", "자동제어설비", "플랜트설비"
        ],
        "architecture_keywords": [
            "타일공사", "지붕공사", "칠공사", "철골공사", "조적공사",
            "목공사", "수장공사", "방수공사", "미장공사", "창호공사"
        ],
        "civil_keywords": [
            "도로공사", "하천공사", "터널공사", "궤도공사", "강구조공사",
            "관부설공사", "항만공사", "지반조사", "측량"
        ],
        "maintenance_keywords": [
            "유지보수", "관리공사", "시설관리", "설비관리"
        ],
        "common_keywords": [
            "적용기준", "가설공사", "토공사", "조경공사", "기초공사",
            "철근콘크리트공사", "돌공사", "건설기계"
        ],
        "unclassified_keywords": [
            "기타공사", "특수공사", "보조공사", "알수없는공사"
        ]
    }

@pytest.fixture
def sample_toc_structure():
    """샘플 목차 구조"""
    return {
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
            },
            {
                "number": "3",
                "title": "도로공사",
                "page": 30,
                "level": 1,
                "section": "토목부문"
            },
            {
                "number": "4",
                "title": "유지보수",
                "page": 40,
                "level": 1,
                "section": "유지관리부문"
            }
        ],
        "sections": {
            "기계설비부문": {"chapters": [{"title": "배관공사", "page": 10}]},
            "건축부문": {"chapters": [{"title": "타일공사", "page": 20}]},
            "토목부문": {"chapters": [{"title": "도로공사", "page": 30}]},
            "유지관리부문": {"chapters": [{"title": "유지보수", "page": 40}]}
        }
    }

@pytest.fixture
def real_file_names():
    """실제 파일명 샘플"""
    return [
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

@pytest.fixture
def classification_expected_results():
    """분류 예상 결과"""
    return {
        "배관누수_검사": "기계설비부문",
        "관갱생공": "미분류",
        "유량계_교체": "미분류",
        "펌프_해체": "기계설비부문",
        "덕트보온_해체": "기계설비부문",
        "타일_교체": "건축부문",
        "도배_교체": "미분류",
        "지붕_덧씌우기": "건축부문",
        "칠공사": "건축부문",
        "철골재_철거(기계)": "건축부문",
        "콘크리트구조물_헐기(기계)": "공통부문",
        "궤도공사": "토목부문",
        "도로반사경_교체": "토목부문",
        "유지보수": "유지관리부문",
        "관리공사": "유지관리부문"
    }

@pytest.fixture
def test_output_dir():
    """테스트 출력 디렉토리"""
    output_path = project_root / "temp" / "test_output"
    output_path.mkdir(parents=True, exist_ok=True)
    yield output_path
    # 테스트 후 정리
    import shutil
    if output_path.exists():
        try:
            shutil.rmtree(output_path)
        except PermissionError:
            pass 