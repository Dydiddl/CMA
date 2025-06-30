#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
년도 선택 인터페이스
사용자가 표준품셈 PDF 및 ground truth 파일의 년도를 선택할 수 있는 도구
"""

import sys
from pathlib import Path
from typing import Optional, List

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.file_paths import FilePathManager, get_available_years, validate_year


class YearSelector:
    """년도 선택 클래스"""
    
    def __init__(self):
        self.file_manager = FilePathManager()
    
    def show_available_years(self) -> None:
        """사용 가능한 년도 목록 표시"""
        available_years = self.file_manager.get_available_standard_price_years()
        gt_years = self.file_manager.get_available_ground_truth_years()
        
        print("📅 사용 가능한 년도 목록")
        print("=" * 40)
        
        print("📄 표준품셈 PDF:")
        if available_years:
            for year in available_years:
                pdf_path = self.file_manager.get_standard_price_pdf_path(year)
                status = "✅" if pdf_path and pdf_path.exists() else "❌"
                print(f"  {status} {year}년")
        else:
            print("  ❌ 사용 가능한 PDF 파일이 없습니다")
        
        print("\n📋 Ground Truth:")
        if gt_years:
            for year in gt_years:
                gt_path = self.file_manager.get_ground_truth_path(year)
                status = "✅" if gt_path and gt_path.exists() else "❌"
                print(f"  {status} {year}년")
        else:
            print("  ❌ 사용 가능한 Ground Truth 파일이 없습니다")
        
        print(f"\n🆕 최신 년도: {self.file_manager.get_latest_year()}")
    
    def select_year_interactive(self) -> Optional[int]:
        """대화형 년도 선택"""
        available_years = self.file_manager.get_available_standard_price_years()
        
        if not available_years:
            print("❌ 사용 가능한 년도가 없습니다")
            return None
        
        print("\n🎯 년도를 선택하세요:")
        print("=" * 30)
        
        for i, year in enumerate(available_years, 1):
            pdf_path = self.file_manager.get_standard_price_pdf_path(year)
            status = "✅" if pdf_path and pdf_path.exists() else "❌"
            print(f"  {i}. {status} {year}년")
        
        print(f"  {len(available_years) + 1}. 🆕 최신 년도 ({self.file_manager.get_latest_year()})")
        print(f"  {len(available_years) + 2}. ❌ 취소")
        
        while True:
            try:
                choice = input(f"\n선택 (1-{len(available_years) + 2}): ").strip()
                
                if not choice:
                    continue
                
                choice_num = int(choice)
                
                if choice_num == len(available_years) + 1:
                    # 최신 년도 선택
                    selected_year = self.file_manager.get_latest_year()
                    print(f"✅ 최신 년도 {selected_year}년을 선택했습니다")
                    return selected_year
                
                elif choice_num == len(available_years) + 2:
                    # 취소
                    print("❌ 년도 선택을 취소했습니다")
                    return None
                
                elif 1 <= choice_num <= len(available_years):
                    # 년도 선택
                    selected_year = available_years[choice_num - 1]
                    print(f"✅ {selected_year}년을 선택했습니다")
                    return selected_year
                
                else:
                    print(f"❌ 1-{len(available_years) + 2} 사이의 숫자를 입력하세요")
                    
            except ValueError:
                print("❌ 올바른 숫자를 입력하세요")
            except KeyboardInterrupt:
                print("\n❌ 년도 선택을 취소했습니다")
                return None
    
    def validate_selection(self, year: int) -> bool:
        """선택된 년도 유효성 검증"""
        if not validate_year(year):
            print(f"❌ {year}년은 사용할 수 없습니다")
            return False
        
        pdf_path = self.file_manager.get_standard_price_pdf_path(year)
        if not pdf_path or not pdf_path.exists():
            print(f"❌ {year}년 표준품셈 PDF 파일이 없습니다")
            return False
        
        print(f"✅ {year}년 파일 검증 완료")
        return True
    
    def get_file_paths(self, year: int) -> dict:
        """선택된 년도의 파일 경로 반환"""
        pdf_path = self.file_manager.get_standard_price_pdf_path(year)
        gt_path = self.file_manager.get_ground_truth_path(year)
        
        return {
            "year": year,
            "standard_price_pdf": pdf_path,
            "ground_truth": gt_path,
            "pdf_exists": pdf_path and pdf_path.exists(),
            "gt_exists": gt_path and gt_path.exists()
        }


def main():
    """메인 함수"""
    print("🎯 년도 선택 도구")
    print("=" * 30)
    
    selector = YearSelector()
    
    # 사용 가능한 년도 표시
    selector.show_available_years()
    
    # 년도 선택
    selected_year = selector.select_year_interactive()
    
    if selected_year is None:
        return
    
    # 선택된 년도 검증
    if not selector.validate_selection(selected_year):
        return
    
    # 파일 경로 정보 출력
    file_paths = selector.get_file_paths(selected_year)
    
    print(f"\n📊 {selected_year}년 파일 정보:")
    print("=" * 30)
    
    pdf_path = file_paths["standard_price_pdf"]
    if file_paths["pdf_exists"]:
        print(f"📄 표준품셈 PDF: {pdf_path.name}")
        print(f"   경로: {pdf_path}")
        print(f"   크기: {pdf_path.stat().st_size:,} bytes")
    else:
        print("❌ 표준품셈 PDF: 없음")
    
    gt_path = file_paths["ground_truth"]
    if file_paths["gt_exists"]:
        print(f"📋 Ground Truth: {gt_path.name}")
        print(f"   경로: {gt_path}")
        print(f"   크기: {gt_path.stat().st_size:,} bytes")
    else:
        print("❌ Ground Truth: 없음")
    
    print(f"\n💡 이 년도를 사용하려면:")
    print(f"   - PDF 경로: {pdf_path}")
    if gt_path:
        print(f"   - Ground Truth 경로: {gt_path}")


if __name__ == "__main__":
    main() 