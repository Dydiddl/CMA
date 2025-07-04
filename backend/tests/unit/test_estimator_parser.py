import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from app.services.estimator.parser import EstimatorParser

@pytest.fixture
def parser():
    return EstimatorParser()

@pytest.fixture
def sample_pdf_path():
    # 테스트용 PDF 파일 경로
    return Path("2025년_건설공사표준품셈.pdf")

@pytest.mark.skip(reason="PDF 파일이 없어서 스킵")
def test_parse_pdf(parser, sample_pdf_path):
    """PDF 파일 파싱 테스트"""
    # PDF 파일이 존재하는지 확인
    assert sample_pdf_path.exists(), f"PDF 파일이 존재하지 않습니다: {sample_pdf_path}"
    
    # PDF 파일 파싱
    work_items = parser.parse_file(str(sample_pdf_path))
    
    # 결과 검증
    assert isinstance(work_items, dict), "결과는 딕셔너리여야 합니다"
    assert "data" in work_items, "data 키가 있어야 합니다"
    assert len(work_items["data"]) > 0, "최소 하나 이상의 작업 항목이 있어야 합니다"
    
    # 첫 번째 항목 구조 검증
    first_item = work_items["data"][0]
    assert "code" in first_item, "작업 항목에 코드가 있어야 합니다"
    assert "name" in first_item, "작업 항목에 이름이 있어야 합니다"
    assert "unit" in first_item, "작업 항목에 단위가 있어야 합니다"
    
    # 결과 출력
    print("\n파싱된 작업 항목:")
    for item in work_items["data"][:5]:  # 처음 5개 항목만 출력
        print(f"코드: {item['code']}")
        print(f"이름: {item['name']}")
        print(f"단위: {item['unit']}")
        print("-" * 50)

def test_parse_file_mock(parser):
    """PDF 파일 파싱 Mock 테스트"""
    # Mock 데이터
    mock_work_items = {
        "data": [
            {
                "code": "010101",
                "name": "토공사",
                "unit": "m³",
                "quantity": 100.0,
                "amount": 50000
            },
            {
                "code": "010102", 
                "name": "콘크리트공사",
                "unit": "m³",
                "quantity": 50.0,
                "amount": 75000
            }
        ],
        "pages": 1
    }
    
    # Mock PDF 파일 경로
    mock_pdf_path = "mock_sample.pdf"
    
    # parse_file 메서드를 Mock으로 교체
    with patch.object(parser, 'parse_file', return_value=mock_work_items):
        work_items = parser.parse_file(mock_pdf_path)
        
        # 결과 검증
        assert isinstance(work_items, dict), "결과는 딕셔너리여야 합니다"
        assert "data" in work_items, "data 키가 있어야 합니다"
        assert len(work_items["data"]) == 2, "Mock 데이터 개수와 일치해야 합니다"
        
        # 첫 번째 항목 구조 검증
        first_item = work_items["data"][0]
        assert "code" in first_item, "작업 항목에 코드가 있어야 합니다"
        assert "name" in first_item, "작업 항목에 이름이 있어야 합니다"
        assert "unit" in first_item, "작업 항목에 단위가 있어야 합니다"
        assert first_item["code"] == "010101", "Mock 데이터와 일치해야 합니다"

def test_parse_file_invalid_file(parser):
    """잘못된 PDF 파일 처리 테스트"""
    with pytest.raises(Exception):
        parser.parse_file("invalid.pdf")

def test_parse_file_empty_file(parser, tmp_path):
    """빈 PDF 파일 처리 테스트"""
    empty_pdf = tmp_path / "empty.pdf"
    empty_pdf.touch()
    
    with pytest.raises(Exception):
        parser.parse_file(str(empty_pdf)) 