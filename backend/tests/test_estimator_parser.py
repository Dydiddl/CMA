import pytest
from pathlib import Path
from app.services.estimator.parser import EstimatorParser

@pytest.fixture
def parser():
    return EstimatorParser()

@pytest.fixture
def sample_pdf_path():
    # 테스트용 PDF 파일 경로
    return Path("2025년_건설공사표준품셈.pdf")

def test_parse_pdf(parser, sample_pdf_path):
    """PDF 파일 파싱 테스트"""
    # PDF 파일이 존재하는지 확인
    assert sample_pdf_path.exists(), f"PDF 파일이 존재하지 않습니다: {sample_pdf_path}"
    
    # PDF 파일 파싱
    work_items = parser.parse_pdf(sample_pdf_path)
    
    # 결과 검증
    assert isinstance(work_items, list), "결과는 리스트여야 합니다"
    assert len(work_items) > 0, "최소 하나 이상의 작업 항목이 있어야 합니다"
    
    # 첫 번째 항목 구조 검증
    first_item = work_items[0]
    assert "code" in first_item, "작업 항목에 코드가 있어야 합니다"
    assert "name" in first_item, "작업 항목에 이름이 있어야 합니다"
    assert "unit" in first_item, "작업 항목에 단위가 있어야 합니다"
    
    # 결과 출력
    print("\n파싱된 작업 항목:")
    for item in work_items[:5]:  # 처음 5개 항목만 출력
        print(f"코드: {item['code']}")
        print(f"이름: {item['name']}")
        print(f"단위: {item['unit']}")
        print("-" * 50)

def test_parse_pdf_invalid_file(parser):
    """잘못된 PDF 파일 처리 테스트"""
    with pytest.raises(Exception):
        parser.parse_pdf(Path("invalid.pdf"))

def test_parse_pdf_empty_file(parser, tmp_path):
    """빈 PDF 파일 처리 테스트"""
    empty_pdf = tmp_path / "empty.pdf"
    empty_pdf.touch()
    
    with pytest.raises(Exception):
        parser.parse_pdf(empty_pdf) 