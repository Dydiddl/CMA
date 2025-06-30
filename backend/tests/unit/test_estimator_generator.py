import pytest
from pathlib import Path
import os
from app.services.estimator.generator import EstimatorGenerator

@pytest.fixture
def generator():
    return EstimatorGenerator()

@pytest.fixture
def sample_work_items():
    return [
        {
            'code': 'A001',
            'name': '토공사',
            'quantity': 100.0,
            'unit': 'm³',
            'amount': 1000000
        },
        {
            'code': 'A002',
            'name': '콘크리트공사',
            'quantity': 50.0,
            'unit': 'm³',
            'amount': 2000000
        }
    ]

@pytest.fixture
def temp_output_dir(tmp_path):
    return tmp_path

def test_generate_estimate(generator, sample_work_items, temp_output_dir):
    """공사내역서 생성 테스트"""
    # 테스트용 템플릿 생성
    template_path = temp_output_dir / 'test_template.xlsx'
    generator.create_template(str(template_path))
    
    # 출력 파일 경로
    output_path = temp_output_dir / 'test_output.xlsx'
    
    # 공사내역서 생성
    result_path = generator.generate_estimate(
        work_items=sample_work_items,
        output_path=str(output_path),
        template_path=str(template_path)
    )
    
    # 결과 검증
    assert Path(result_path).exists()
    assert Path(result_path).suffix == '.xlsx'

def test_generate_estimate_without_template(generator, sample_work_items, temp_output_dir):
    """기본 템플릿으로 공사내역서 생성 테스트"""
    # 기본 템플릿 생성
    generator.create_template(str(generator.default_template))
    
    # 출력 파일 경로
    output_path = temp_output_dir / 'test_output_default.xlsx'
    
    # 공사내역서 생성
    result_path = generator.generate_estimate(
        work_items=sample_work_items,
        output_path=str(output_path)
    )
    
    # 결과 검증
    assert Path(result_path).exists()
    assert Path(result_path).suffix == '.xlsx'

def test_generate_estimate_invalid_template(generator, sample_work_items, temp_output_dir):
    """잘못된 템플릿 파일 테스트"""
    # 존재하지 않는 템플릿 파일 경로
    invalid_template = temp_output_dir / 'invalid_template.xlsx'
    
    # 출력 파일 경로
    output_path = temp_output_dir / 'test_output_invalid.xlsx'
    
    # 예외 발생 확인
    with pytest.raises(FileNotFoundError):
        generator.generate_estimate(
            work_items=sample_work_items,
            output_path=str(output_path),
            template_path=str(invalid_template)
        )

def test_create_template(generator, temp_output_dir):
    """템플릿 생성 테스트"""
    # 템플릿 파일 경로
    template_path = temp_output_dir / 'new_template.xlsx'
    
    # 템플릿 생성
    generator.create_template(str(template_path))
    
    # 결과 검증
    assert Path(template_path).exists()
    assert Path(template_path).suffix == '.xlsx' 