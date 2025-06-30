#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
파일 경로 관리 설정 모듈
년도별 표준품셈 PDF 및 ground truth 파일 경로를 동적으로 관리
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class FilePathManager:
    """파일 경로 관리 클래스"""
    
    def __init__(self, base_dir: str = None):
        """초기화"""
        if base_dir is None:
            self.base_dir = Path(__file__).parent.parent
        else:
            self.base_dir = Path(base_dir)
        
        # 기본 경로 설정
        self.input_dir = self.base_dir / "input"
        self.output_dir = self.base_dir / "output"
        self.data_dir = self.base_dir / "data"
        self.ground_truth_dir = self.data_dir / "ground truth"
        self.standard_price_dir = self.input_dir / "By_year_Construction_work_standard_price_list"
        
        # 사용 가능한 년도 목록 (자동 감지)
        self.available_years = self._detect_available_years()
        
        # 기본 년도 설정 (가장 최신 년도)
        self.default_year = max(self.available_years) if self.available_years else 2025
    
    def _detect_available_years(self) -> List[int]:
        """사용 가능한 년도 자동 감지"""
        years = []
        
        if self.standard_price_dir.exists():
            for pdf_file in self.standard_price_dir.glob("*_construction_work_standard_price_list*.pdf"):
                # 파일명에서 년도 추출
                filename = pdf_file.stem
                if "_construction_work_standard_price_list" in filename:
                    year_part = filename.split("_")[0]
                    try:
                        year = int(year_part)
                        years.append(year)
                    except ValueError:
                        continue
        
        return sorted(years)
    
    def get_standard_price_pdf_path(self, year: int = None) -> Optional[Path]:
        """표준품셈 PDF 파일 경로 반환"""
        if year is None:
            year = self.default_year
        
        # 기본 파일명 패턴
        filename = f"{year}_construction_work_standard_price_list.pdf"
        pdf_path = self.standard_price_dir / filename
        
        # 수정본이 있는지 확인
        revised_filename = f"{year}_construction_work_standard_price_list_revised.pdf"
        revised_path = self.standard_price_dir / revised_filename
        
        # 적용본이 있는지 확인
        applied_filename = f"{year}_construction_work_standard_price_list_applied.pdf"
        applied_path = self.standard_price_dir / applied_filename
        
        # 우선순위: 적용본 > 수정본 > 기본본
        if applied_path.exists():
            return applied_path
        elif revised_path.exists():
            return revised_path
        elif pdf_path.exists():
            return pdf_path
        else:
            return None
    
    def get_ground_truth_path(self, year: int = None) -> Optional[Path]:
        """Ground truth 파일 경로 반환"""
        if year is None:
            year = self.default_year
        
        # 기본 파일명 패턴
        filename = f"toc_ground_truth_{year}.md"
        gt_path = self.ground_truth_dir / filename
        
        if gt_path.exists():
            return gt_path
        else:
            return None
    
    def get_available_standard_price_years(self) -> List[int]:
        """사용 가능한 표준품셈 년도 목록 반환"""
        return self.available_years.copy()
    
    def get_available_ground_truth_years(self) -> List[int]:
        """사용 가능한 ground truth 년도 목록 반환"""
        years = []
        
        if self.ground_truth_dir.exists():
            for gt_file in self.ground_truth_dir.glob("toc_ground_truth_*.md"):
                filename = gt_file.stem
                if filename.startswith("toc_ground_truth_"):
                    year_part = filename.replace("toc_ground_truth_", "")
                    try:
                        year = int(year_part)
                        years.append(year)
                    except ValueError:
                        continue
        
        return sorted(years)
    
    def validate_year(self, year: int) -> bool:
        """년도 유효성 검증"""
        return year in self.available_years
    
    def get_latest_year(self) -> int:
        """최신 년도 반환"""
        return max(self.available_years) if self.available_years else 2025
    
    def get_file_info(self, year: int = None) -> Dict[str, any]:
        """파일 정보 반환"""
        if year is None:
            year = self.default_year
        
        pdf_path = self.get_standard_price_pdf_path(year)
        gt_path = self.get_ground_truth_path(year)
        
        return {
            "year": year,
            "standard_price_pdf": {
                "path": str(pdf_path) if pdf_path else None,
                "exists": pdf_path.exists() if pdf_path else False,
                "size": pdf_path.stat().st_size if pdf_path and pdf_path.exists() else 0
            },
            "ground_truth": {
                "path": str(gt_path) if gt_path else None,
                "exists": gt_path.exists() if gt_path else False,
                "size": gt_path.stat().st_size if gt_path and gt_path.exists() else 0
            }
        }
    
    def list_all_files(self) -> Dict[str, List[str]]:
        """모든 파일 목록 반환"""
        files = {
            "standard_price_pdfs": [],
            "ground_truth_files": [],
            "available_years": self.available_years
        }
        
        # 표준품셈 PDF 파일들
        if self.standard_price_dir.exists():
            for pdf_file in self.standard_price_dir.glob("*_construction_work_standard_price_list*.pdf"):
                files["standard_price_pdfs"].append(pdf_file.name)
        
        # Ground truth 파일들
        if self.ground_truth_dir.exists():
            for gt_file in self.ground_truth_dir.glob("toc_ground_truth_*.md"):
                files["ground_truth_files"].append(gt_file.name)
        
        return files


# 전역 인스턴스 생성
file_path_manager = FilePathManager()


def get_standard_price_pdf_path(year: int = None) -> Optional[Path]:
    """표준품셈 PDF 파일 경로 반환 (편의 함수)"""
    return file_path_manager.get_standard_price_pdf_path(year)


def get_ground_truth_path(year: int = None) -> Optional[Path]:
    """Ground truth 파일 경로 반환 (편의 함수)"""
    return file_path_manager.get_ground_truth_path(year)


def get_available_years() -> List[int]:
    """사용 가능한 년도 목록 반환 (편의 함수)"""
    return file_path_manager.get_available_standard_price_years()


def validate_year(year: int) -> bool:
    """년도 유효성 검증 (편의 함수)"""
    return file_path_manager.validate_year(year)


if __name__ == "__main__":
    """테스트 및 정보 출력"""
    print("📁 파일 경로 관리 시스템 정보")
    print("=" * 50)
    
    # 사용 가능한 년도 출력
    available_years = file_path_manager.get_available_standard_price_years()
    print(f"📅 사용 가능한 표준품셈 년도: {available_years}")
    
    # Ground truth 년도 출력
    gt_years = file_path_manager.get_available_ground_truth_years()
    print(f"📋 사용 가능한 Ground Truth 년도: {gt_years}")
    
    # 최신 년도 정보 출력
    latest_year = file_path_manager.get_latest_year()
    print(f"🆕 최신 년도: {latest_year}")
    
    # 파일 정보 출력
    print(f"\n📊 {latest_year}년 파일 정보:")
    file_info = file_path_manager.get_file_info(latest_year)
    
    pdf_info = file_info["standard_price_pdf"]
    if pdf_info["exists"]:
        print(f"  📄 표준품셈 PDF: {Path(pdf_info['path']).name} ({pdf_info['size']:,} bytes)")
    else:
        print(f"  ❌ 표준품셈 PDF: 없음")
    
    gt_info = file_info["ground_truth"]
    if gt_info["exists"]:
        print(f"  📋 Ground Truth: {Path(gt_info['path']).name} ({gt_info['size']:,} bytes)")
    else:
        print(f"  ❌ Ground Truth: 없음")
    
    # 모든 파일 목록 출력
    print(f"\n📂 전체 파일 목록:")
    all_files = file_path_manager.list_all_files()
    
    print(f"  📄 표준품셈 PDF ({len(all_files['standard_price_pdfs'])}개):")
    for pdf_file in all_files["standard_price_pdfs"]:
        print(f"    - {pdf_file}")
    
    print(f"  📋 Ground Truth ({len(all_files['ground_truth_files'])}개):")
    for gt_file in all_files["ground_truth_files"]:
        print(f"    - {gt_file}") 