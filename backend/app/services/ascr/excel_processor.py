#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASCR Excel 문서 처리 모듈
Excel 문서(.xlsx, .xls) 분석 및 구조화
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import json
import pandas as pd
import openpyxl
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import numpy as np

logger = logging.getLogger(__name__)

@dataclass
class ExcelSheetStructure:
    """Excel 시트 구조 데이터 클래스"""
    sheet_name: str
    rows: int
    columns: int
    data_range: str
    headers: List[str]
    data_types: Dict[str, str]
    empty_cells: int
    formulas: List[str]

@dataclass
class ExcelWorkbookStructure:
    """Excel 워크북 구조 데이터 클래스"""
    file_name: str
    sheets: List[ExcelSheetStructure]
    total_sheets: int
    total_rows: int
    total_columns: int

class ExcelDocumentProcessor:
    """Excel 문서 처리 클래스"""
    
    def __init__(self):
        self.supported_extensions = ['.xlsx', '.xls']
        self.construction_keywords = {
            "공통부문": ["공통", "일반", "기본", "표준", "규정"],
            "토목부문": ["토목", "도로", "교량", "터널", "댐", "제방"],
            "건축부문": ["건축", "건물", "시설", "구조", "마감"],
            "기계설비부문": ["기계", "설비", "전기", "통신", "소방"],
            "유지관리부문": ["유지", "관리", "보수", "점검", "정비"]
        }
    
    def can_process(self, file_path: Path) -> bool:
        """파일 처리 가능 여부 확인"""
        return file_path.suffix.lower() in self.supported_extensions
    
    def extract_text_from_excel(self, file_path: Path) -> str:
        """Excel 문서에서 텍스트 추출"""
        try:
            # pandas를 사용하여 모든 시트의 데이터 읽기
            excel_file = pd.ExcelFile(str(file_path))
            text_content = []
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                text_content.append(f"=== {sheet_name} ===")
                
                # 헤더 추가
                if not df.empty:
                    headers = df.columns.tolist()
                    text_content.append("헤더: " + " | ".join(str(h) for h in headers))
                    
                    # 데이터 추가 (처음 10행만)
                    for idx, row in df.head(10).iterrows():
                        row_text = " | ".join(str(val) for val in row.values if pd.notna(val))
                        if row_text.strip():
                            text_content.append(row_text)
            
            return '\n'.join(text_content)
            
        except Exception as e:
            logger.error(f"Excel 문서 텍스트 추출 실패: {e}")
            raise
    
    def analyze_workbook_structure(self, file_path: Path) -> ExcelWorkbookStructure:
        """Excel 워크북 구조 분석"""
        try:
            workbook = load_workbook(str(file_path), data_only=True)
            sheets = []
            total_rows = 0
            total_columns = 0
            
            for sheet_name in workbook.sheetnames:
                sheet = workbook[sheet_name]
                sheet_structure = self._analyze_sheet_structure(sheet, sheet_name)
                sheets.append(sheet_structure)
                
                total_rows = max(total_rows, sheet_structure.rows)
                total_columns = max(total_columns, sheet_structure.columns)
            
            return ExcelWorkbookStructure(
                file_name=file_path.name,
                sheets=sheets,
                total_sheets=len(sheets),
                total_rows=total_rows,
                total_columns=total_columns
            )
            
        except Exception as e:
            logger.error(f"Excel 워크북 구조 분석 실패: {e}")
            raise
    
    def _analyze_sheet_structure(self, sheet, sheet_name: str) -> ExcelSheetStructure:
        """시트 구조 분석"""
        # 데이터 범위 찾기
        max_row = sheet.max_row
        max_col = sheet.max_column
        
        # 헤더 추출 (첫 번째 행)
        headers = []
        for col in range(1, max_col + 1):
            cell_value = sheet.cell(row=1, column=col).value
            headers.append(str(cell_value) if cell_value is not None else f"Column_{col}")
        
        # 데이터 타입 분석
        data_types = {}
        empty_cells = 0
        formulas = []
        
        for row in range(2, min(max_row + 1, 100)):  # 처음 100행만 분석
            for col in range(1, max_col + 1):
                cell = sheet.cell(row=row, column=col)
                
                if cell.value is None:
                    empty_cells += 1
                else:
                    col_letter = get_column_letter(col)
                    if col_letter not in data_types:
                        data_types[col_letter] = type(cell.value).__name__
                
                # 수식 확인
                if cell.data_type == 'f':  # formula
                    formulas.append(f"{col_letter}{row}: {cell.value}")
        
        return ExcelSheetStructure(
            sheet_name=sheet_name,
            rows=max_row,
            columns=max_col,
            data_range=f"A1:{get_column_letter(max_col)}{max_row}",
            headers=headers,
            data_types=data_types,
            empty_cells=empty_cells,
            formulas=formulas
        )
    
    def extract_structured_data(self, file_path: Path) -> Dict[str, Any]:
        """구조화된 데이터 추출"""
        try:
            workbook_structure = self.analyze_workbook_structure(file_path)
            text_content = self.extract_text_from_excel(file_path)
            
            # 각 시트별 상세 데이터 추출
            sheets_data = []
            for sheet_structure in workbook_structure.sheets:
                sheet_data = self._extract_sheet_data(file_path, sheet_structure)
                sheets_data.append(sheet_data)
            
            return {
                "file_path": str(file_path),
                "file_type": "excel",
                "workbook_name": workbook_structure.file_name,
                "sheets": sheets_data,
                "text_content": text_content,
                "statistics": {
                    "total_sheets": workbook_structure.total_sheets,
                    "total_rows": workbook_structure.total_rows,
                    "total_columns": workbook_structure.total_columns
                },
                "categories": self._extract_categories(sheets_data)
            }
            
        except Exception as e:
            logger.error(f"Excel 문서 구조화 데이터 추출 실패: {e}")
            raise
    
    def _extract_sheet_data(self, file_path: Path, sheet_structure: ExcelSheetStructure) -> Dict[str, Any]:
        """시트별 상세 데이터 추출"""
        try:
            df = pd.read_excel(str(file_path), sheet_name=sheet_structure.sheet_name)
            
            # 데이터 분석
            data_analysis = {
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "missing_values": df.isnull().sum().to_dict(),
                "data_types": df.dtypes.astype(str).to_dict(),
                "numeric_columns": df.select_dtypes(include=[np.number]).columns.tolist(),
                "text_columns": df.select_dtypes(include=['object']).columns.tolist()
            }
            
            # 테이블 유형 분류
            table_type = self._classify_excel_table(df, sheet_structure)
            
            # 샘플 데이터 (처음 5행)
            sample_data = df.head(5).to_dict('records')
            
            return {
                "sheet_name": sheet_structure.sheet_name,
                "structure": {
                    "rows": sheet_structure.rows,
                    "columns": sheet_structure.columns,
                    "data_range": sheet_structure.data_range,
                    "headers": sheet_structure.headers,
                    "data_types": sheet_structure.data_types,
                    "empty_cells": sheet_structure.empty_cells,
                    "formulas": sheet_structure.formulas
                },
                "analysis": data_analysis,
                "table_type": table_type,
                "sample_data": sample_data,
                "category": self._classify_sheet(sheet_structure.sheet_name, df)
            }
            
        except Exception as e:
            logger.error(f"시트 데이터 추출 실패: {sheet_structure.sheet_name} - {e}")
            return {
                "sheet_name": sheet_structure.sheet_name,
                "error": str(e)
            }
    
    def _classify_excel_table(self, df: pd.DataFrame, sheet_structure: ExcelSheetStructure) -> str:
        """Excel 테이블 유형 분류"""
        if df.empty:
            return "빈 시트"
        
        headers_text = " ".join(str(h) for h in df.columns)
        headers_lower = headers_text.lower()
        
        # 건설업계 특화 분류
        if any(keyword in headers_lower for keyword in ["단가", "금액", "비용", "가격"]):
            return "단가표"
        elif any(keyword in headers_lower for keyword in ["수량", "개수", "면적", "부피"]):
            return "수량표"
        elif any(keyword in headers_lower for keyword in ["공종", "세부항목", "내역", "공사"]):
            return "내역서"
        elif any(keyword in headers_lower for keyword in ["일정", "계획", "스케줄"]):
            return "일정표"
        elif any(keyword in headers_lower for keyword in ["인력", "직원", "작업자"]):
            return "인력표"
        else:
            return "일반표"
    
    def _classify_sheet(self, sheet_name: str, df: pd.DataFrame) -> str:
        """시트 분류"""
        sheet_name_lower = sheet_name.lower()
        headers_text = " ".join(str(h) for h in df.columns).lower()
        
        for category, keywords in self.construction_keywords.items():
            for keyword in keywords:
                if keyword in sheet_name_lower or keyword in headers_text:
                    return category
        
        return "기타"
    
    def _extract_categories(self, sheets_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """카테고리별 통계 추출"""
        categories = {}
        for sheet_data in sheets_data:
            if "category" in sheet_data:
                category = sheet_data["category"]
                categories[category] = categories.get(category, 0) + 1
        return categories
    
    def create_excel_template(self, template_data: Dict[str, Any], output_path: Path) -> Path:
        """Excel 템플릿 생성"""
        try:
            # ExcelWriter 사용하여 여러 시트 생성
            with pd.ExcelWriter(str(output_path), engine='openpyxl') as writer:
                
                # 기본 정보 시트
                basic_info = pd.DataFrame({
                    "항목": ["프로젝트명", "작성일", "작성자", "버전"],
                    "내용": [
                        template_data.get("project_name", "건설 프로젝트"),
                        template_data.get("created_date", "2024-01-23"),
                        template_data.get("author", "시스템"),
                        template_data.get("version", "1.0")
                    ]
                })
                basic_info.to_excel(writer, sheet_name="기본정보", index=False)
                
                # 내역서 시트
                if "items" in template_data:
                    items_df = pd.DataFrame(template_data["items"])
                    items_df.to_excel(writer, sheet_name="내역서", index=False)
                
                # 단가표 시트
                if "prices" in template_data:
                    prices_df = pd.DataFrame(template_data["prices"])
                    prices_df.to_excel(writer, sheet_name="단가표", index=False)
                
                # 수량표 시트
                if "quantities" in template_data:
                    quantities_df = pd.DataFrame(template_data["quantities"])
                    quantities_df.to_excel(writer, sheet_name="수량표", index=False)
            
            logger.info(f"Excel 템플릿 생성 완료: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Excel 템플릿 생성 실패: {e}")
            raise
    
    def convert_to_pdf_format(self, excel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Excel 데이터를 PDF 형식으로 변환"""
        return {
            "pdf_info": {
                "total_pages": excel_data["statistics"]["total_sheets"],
                "file_size": 0,
                "file_name": excel_data["workbook_name"],
                "creation_date": 0
            },
            "toc_structure": {
                "sections": [sheet["sheet_name"] for sheet in excel_data["sheets"]],
                "chapters": [],
                "subsections": []
            },
            "split_results": [],
            "excel_specific": {
                "sheets": excel_data["sheets"],
                "categories": excel_data["categories"]
            }
        }
    
    def extract_tables_from_excel(self, file_path: Path) -> List[Dict[str, Any]]:
        """Excel에서 테이블 데이터 추출"""
        try:
            tables = []
            excel_file = pd.ExcelFile(str(file_path))
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                if not df.empty:
                    table_data = {
                        "sheet_name": sheet_name,
                        "table_type": self._classify_excel_table(df, None),
                        "headers": df.columns.tolist(),
                        "data": df.to_dict('records'),
                        "statistics": {
                            "rows": len(df),
                            "columns": len(df.columns),
                            "missing_values": df.isnull().sum().sum()
                        }
                    }
                    tables.append(table_data)
            
            return tables
            
        except Exception as e:
            logger.error(f"Excel 테이블 추출 실패: {e}")
            raise

# 사용 예시
def main():
    """Excel 문서 처리 예시"""
    processor = ExcelDocumentProcessor()
    
    # 샘플 Excel 파일 생성
    sample_data = {
        "기본정보": pd.DataFrame({
            "항목": ["프로젝트명", "작성일", "작성자"],
            "내용": ["도로공사", "2024-01-23", "시스템"]
        }),
        "내역서": pd.DataFrame({
            "공종": ["도로포장", "교량공사", "터널공사"],
            "단위": ["m²", "m", "m"],
            "수량": [1000, 500, 200],
            "단가": [50000, 100000, 200000]
        }),
        "단가표": pd.DataFrame({
            "자재": ["아스팔트", "콘크리트", "철근"],
            "단위": ["톤", "m³", "톤"],
            "단가": [80000, 120000, 150000]
        })
    }
    
    # Excel 파일 생성
    sample_path = Path("sample_workbook.xlsx")
    with pd.ExcelWriter(str(sample_path), engine='openpyxl') as writer:
        for sheet_name, df in sample_data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    # 문서 분석
    if processor.can_process(sample_path):
        result = processor.extract_structured_data(sample_path)
        print("Excel 문서 분석 결과:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        # 테이블 추출
        tables = processor.extract_tables_from_excel(sample_path)
        print(f"\n추출된 테이블 수: {len(tables)}")
    
    # 샘플 파일 정리
    sample_path.unlink()

if __name__ == "__main__":
    main() 