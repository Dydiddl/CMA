#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
표준가격표 목차 추출 스크립트

이 스크립트는 input 폴더의 표준가격표 PDF에서 목차 부분을 추출하여 index.pdf로 저장합니다.
기존 src/utils/extract/toc_extractor.py의 TOCExtractor 클래스를 활용합니다.
"""

import sys
from pathlib import Path
import argparse

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.extract.toc_extractor import TOCExtractor
from src.common.utils import validate_pdf_file, ensure_directory
from config.file_paths import FilePathManager

def find_standard_price_pdf(input_dir: Path, target_year: int = None) -> Path:
    """input 폴더에서 표준가격표 PDF 파일을 찾습니다."""
    pdf_files = list(input_dir.glob("*_construction_work_standard_price_list*.pdf"))
    
    if not pdf_files:
        raise FileNotFoundError(f"input 폴더에 PDF 파일이 없습니다: {input_dir}")
    
    # 특정 년도가 지정된 경우
    if target_year:
        target_filename = f"{target_year}_construction_work_standard_price_list.pdf"
        for pdf_file in pdf_files:
            if pdf_file.name == target_filename:
                return pdf_file
        raise FileNotFoundError(f"{target_year}년도 PDF 파일을 찾을 수 없습니다: {target_filename}")
    
    # 년도가 지정되지 않은 경우, 사용 가능한 년도 목록을 보여주고 선택
    available_years = []
    year_files = {}
    
    for pdf_file in pdf_files:
        # 파일명에서 년도 추출
        filename = pdf_file.stem
        if "_construction_work_standard_price_list" in filename:
            year_part = filename.split("_")[0]
            try:
                year = int(year_part)
                available_years.append(year)
                year_files[year] = pdf_file
            except ValueError:
                continue
    
    if not available_years:
        raise FileNotFoundError(f"유효한 년도가 포함된 PDF 파일이 없습니다: {input_dir}")
    
    # 년도 목록을 정렬하여 표시
    available_years.sort()
    print(f"\n📅 사용 가능한 년도: {available_years}")
    
    # 사용자에게 년도 선택 요청
    while True:
        try:
            selected_year = input(f"사용할 년도를 선택하세요 (기본값: {max(available_years)}): ").strip()
            
            if not selected_year:
                selected_year = max(available_years)
            else:
                selected_year = int(selected_year)
            
            if selected_year in available_years:
                selected_file = year_files[selected_year]
                print(f"✅ {selected_year}년도 PDF 파일을 선택했습니다: {selected_file.name}")
                return selected_file
            else:
                print(f"❌ {selected_year}년도는 사용할 수 없습니다. 다시 선택해주세요.")
        except ValueError:
            print("❌ 올바른 년도를 입력해주세요.")
        except KeyboardInterrupt:
            print("\n❌ 사용자가 취소했습니다.")
            sys.exit(1)

def main():
    """메인 실행 함수"""
    try:
        print("=== 표준가격표 목차 추출 시작 ===")
        
        parser = argparse.ArgumentParser(description="표준품셈 PDF에서 목차 인덱스 추출")
        parser.add_argument("--input_dir", type=str, default="input/By_year_Construction_work_standard_price_list", help="입력 PDF 폴더 경로")
        parser.add_argument("--year", type=int, help="사용할 년도 (예: 2025)")
        args = parser.parse_args()
        input_dir = Path(args.input_dir)
        
        # 2. 디렉토리 확인 및 생성
        if not input_dir.exists():
            print(f"❌ input 폴더가 존재하지 않습니다: {input_dir}")
            return False
        
        ensure_directory(input_dir)
        
        # 3. 표준가격표 PDF 파일 찾기
        try:
            pdf_file = find_standard_price_pdf(input_dir, args.year)
            print(f"📄 선택된 PDF 파일: {pdf_file.name}")
        except FileNotFoundError as e:
            print(f"❌ {e}")
            return False
        
        # 4. PDF 파일 검증
        try:
            validate_pdf_file(pdf_file)
            print(f"✅ PDF 파일 검증 완료")
        except Exception as e:
            print(f"❌ PDF 파일 검증 실패: {e}")
            return False
        
        # 5. TOCExtractor 인스턴스 생성
        extractor = TOCExtractor()
        
        # 6. 목차 PDF 추출 (input 폴더에 저장)
        output_path = input_dir / "index.pdf"
        print(f"🔍 목차 추출 중... (최대 100페이지 검색)")
        
        extracted_path = extractor.extract_toc_pdf(
            pdf_path=pdf_file,
            output_path=output_path,
            max_pages=100
        )
        
        if extracted_path and extracted_path.exists():
            print(f"✅ 목차 추출 완료: {extracted_path}")
            print(f"📊 파일 크기: {extracted_path.stat().st_size:,} bytes")
            print(f"💡 이제 '2. 텍스트 추출 및 목차 분석'을 실행할 수 있습니다.")
            return True
        else:
            print("❌ 목차 추출 실패")
            return False
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 표준가격표 목차 추출이 성공적으로 완료되었습니다!")
    else:
        print("\n💥 표준가격표 목차 추출에 실패했습니다.")
        sys.exit(1) 