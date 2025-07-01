from typing import List, Dict, Any, Optional
import os
from pathlib import Path
import pandas as pd
import re
import tabula
import logging

logger = logging.getLogger(__name__)

class EstimatorParser:
    """품셈 PDF 파일을 파싱하는 클래스"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
        self.column_mappings = {
            '품목코드': 'code',
            '품목명': 'name',
            '수량': 'quantity',
            '단위': 'unit',
            '금액': 'amount'
        }
        
        # 데이터 정제를 위한 패턴
        self.patterns = {
            'code': r'^[A-Z0-9-]+$',  # 품목코드 패턴
            'quantity': r'^\d+(\.\d+)?$',  # 수량 패턴
            'amount': r'^\d+(,\d+)*$'  # 금액 패턴
        }
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        품셈 PDF 파일을 파싱하여 구조화된 데이터로 변환
        
        Args:
            file_path (str): 품셈 PDF 파일 경로
            
        Returns:
            Dict[str, Any]: 파싱된 품셈 데이터
        """
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext not in self.supported_formats:
            raise ValueError(f"지원하지 않는 파일 형식입니다: {file_ext}")
            
        return self._parse_pdf(file_path)
    
    def _parse_pdf(self, file_path: str) -> Dict[str, Any]:
        """PDF 파일 파싱"""
        try:
            # 모든 페이지에서 테이블 추출
            tables = tabula.read_pdf(
                file_path,
                pages='all',  # 모든 페이지 처리
                multiple_tables=True,  # 여러 테이블 처리
                guess=False,  # 자동 감지 비활성화
                lattice=True,  # 격자형 테이블 처리
                pandas_options={'header': 0}
            )
            
            if not tables:
                raise ValueError("PDF에서 테이블을 찾을 수 없습니다.")
            
            # 모든 테이블의 데이터를 하나로 합치기
            all_items = []
            for table in tables:
                items = self._process_table(table)
                all_items.extend(items)
            
            # 데이터 정제 및 중복 제거
            cleaned_items = self._clean_data(all_items)
            
            return {
                "data": cleaned_items,
                "pages": len(tables)
            }
        except Exception as e:
            logger.error(f"PDF 파싱 중 오류 발생: {str(e)}")
            raise
    
    def _process_table(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        DataFrame을 처리하여 작업 항목 목록을 생성합니다.
        
        Args:
            df: pandas DataFrame
            
        Returns:
            List[Dict[str, Any]]: 작업 항목 목록
        """
        items = []
        
        # 컬럼명 정규화
        df.columns = [self._normalize_column_name(col) for col in df.columns]
        
        # 필수 컬럼 확인
        required_columns = ['code', 'name', 'quantity', 'unit', 'amount']
        if not all(col in df.columns for col in required_columns):
            logger.warning(f"필수 컬럼 누락: {df.columns}")
            return items
        
        # 데이터 처리
        for _, row in df.iterrows():
            try:
                item = {
                    'code': str(row['code']).strip(),
                    'name': str(row['name']).strip(),
                    'quantity': self._parse_quantity(row['quantity']),
                    'unit': str(row['unit']).strip(),
                    'amount': self._parse_amount(row['amount'])
                }
                
                # 유효한 데이터만 추가
                if self._is_valid_item(item):
                    items.append(item)
                    
            except Exception as e:
                logger.warning(f"행 처리 중 오류 발생: {str(e)}")
                continue
        
        return items

    def _normalize_column_name(self, column: str) -> str:
        """
        컬럼명을 정규화합니다.
        
        Args:
            column: 원본 컬럼명
            
        Returns:
            str: 정규화된 컬럼명
        """
        column = str(column).strip()
        for key, value in self.column_mappings.items():
            if key in column:
                return value
        return column.lower()

    def _parse_quantity(self, value: Any) -> float:
        """
        수량을 파싱합니다.
        
        Args:
            value: 수량 값
            
        Returns:
            float: 파싱된 수량
        """
        if pd.isna(value):
            return 0.0
        
        value = str(value).strip()
        # 쉼표 제거 및 숫자만 추출
        value = re.sub(r'[^\d.]', '', value)
        try:
            return float(value)
        except ValueError:
            return 0.0

    def _parse_amount(self, value: Any) -> int:
        """
        금액을 파싱합니다.
        
        Args:
            value: 금액 값
            
        Returns:
            int: 파싱된 금액
        """
        if pd.isna(value):
            return 0
        
        value = str(value).strip()
        # 쉼표 제거 및 숫자만 추출
        value = re.sub(r'[^\d]', '', value)
        try:
            return int(value)
        except ValueError:
            return 0

    def _is_valid_item(self, item: Dict[str, Any]) -> bool:
        """
        작업 항목의 유효성을 검사합니다.
        
        Args:
            item: 작업 항목
            
        Returns:
            bool: 유효성 여부
        """
        # 필수 필드 검사
        if not all(item.values()):
            return False
        
        # 패턴 검사
        if not re.match(self.patterns['code'], item['code']):
            return False
        
        if not re.match(self.patterns['quantity'], str(item['quantity'])):
            return False
        
        if not re.match(self.patterns['amount'], str(item['amount'])):
            return False
        
        return True

    def _clean_data(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        데이터를 정제하고 중복을 제거합니다.
        
        Args:
            items: 작업 항목 목록
            
        Returns:
            List[Dict[str, Any]]: 정제된 작업 항목 목록
        """
        # 중복 제거를 위한 임시 딕셔너리
        unique_items = {}
        
        for item in items:
            key = (item['code'], item['name'])
            if key not in unique_items:
                unique_items[key] = item
            else:
                # 동일한 항목이 있는 경우 수량과 금액을 합산
                existing = unique_items[key]
                existing['quantity'] += item['quantity']
                existing['amount'] += item['amount']
        
        return list(unique_items.values())
    
    def extract_work_items(self, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        파싱된 데이터에서 공사 항목 추출
        
        Args:
            parsed_data (Dict[str, Any]): 파싱된 품셈 데이터
            
        Returns:
            List[Dict[str, Any]]: 추출된 공사 항목 목록
        """
        return parsed_data.get('data', [])
    
    def validate_data(self, parsed_data: Dict[str, Any]) -> bool:
        """
        파싱된 데이터의 유효성 검증
        
        Args:
            parsed_data (Dict[str, Any]): 파싱된 품셈 데이터
            
        Returns:
            bool: 유효성 검증 결과
        """
        data = parsed_data.get('data', [])
        if not data:
            return False
            
        # 필수 필드 확인
        required_fields = ['code', 'name', 'quantity', 'unit', 'amount']
        for item in data:
            if not all(field in item for field in required_fields):
                return False
                
        return True
