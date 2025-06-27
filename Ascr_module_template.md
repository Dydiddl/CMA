# 📁 backend/app/services/ascr/__init__.py
# (빈 파일로 패키지 선언)


# 📁 backend/app/services/ascr/models.py
from pydantic import BaseModel
from typing import List, Optional

class UnitPriceEntry(BaseModel):
    category: str
    item: str
    unit: str
    price: float
    note: Optional[str] = None

class LaborRate(BaseModel):
    occupation: str
    current_rate: float
    previous_rate: Optional[float] = None

class OverheadRatio(BaseModel):
    category: str
    percentage: float


# 📁 backend/app/services/ascr/parser.py
# PDF 또는 한글파일을 읽고 데이터를 추출하여 구조화하는 로직

def parse_standard_cost(pdf_path: str) -> List[dict]:
    # TODO: 표준품셈 PDF를 파싱하여 일위대가 데이터를 리스트로 반환
    pass

def parse_labor_rates(pdf_path: str) -> List[dict]:
    # TODO: 노임단가 PDF를 파싱하여 노동직종별 노임단가 반환
    pass

def parse_overhead_ratios(pdf_path: str) -> List[dict]:
    # TODO: 조달청 제비율표 PDF에서 항목별 비율 추출
    pass


# 📁 backend/app/services/ascr/excel_generator.py
# 엑셀 파일을 기반으로 데이터를 삽입하는 함수들
import openpyxl

def write_unit_prices_to_excel(template_path: str, output_path: str, data: List[dict]):
    # TODO: 일위대가 데이터를 엑셀 서식에 맞게 작성
    pass


def update_labor_rates_in_excel(excel_path: str, rates: List[dict]):
    # TODO: 노임단가 시트 업데이트
    pass


def update_overhead_ratios(excel_path: str, ratios: List[dict]):
    # TODO: 제비율 데이터 삽입
    pass


# 📁 backend/app/services/ascr/service.py
# 전체 자동화 파이프라인을 처리하는 메인 서비스

def generate_estimate_pipeline(
    cost_pdf: str,
    labor_pdf: str,
    overhead_pdf: str,
    template_path: str,
    output_path: str
):
    cost_data = parse_standard_cost(cost_pdf)
    labor_data = parse_labor_rates(labor_pdf)
    ratio_data = parse_overhead_ratios(overhead_pdf)

    write_unit_prices_to_excel(template_path, output_path, cost_data)
    update_labor_rates_in_excel(output_path, labor_data)
    update_overhead_ratios(output_path, ratio_data)

    return output_path
