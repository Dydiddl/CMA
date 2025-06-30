#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 텍스트 추출기 - 통합 버전
PDF에서 텍스트를 추출하고 기본적인 분석을 수행합니다.
"""

import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime
import re

# 설정 모듈 import
try:
    from config.settings import INPUT_DIR, OUTPUT_DIR, ensure_directories
except ImportError:
    INPUT_DIR = Path("input/By_year_Construction_work_standard_price_list")
    OUTPUT_DIR = Path("output")
    
    def ensure_directories():
        INPUT_DIR.mkdir(exist_ok=True)
        OUTPUT_DIR.mkdir(exist_ok=True)

class PDFTextExtractor:
    """PDF 텍스트 추출 클래스"""
    
    def __init__(self):
        """초기화"""
        ensure_directories()
    
    def extract_text_by_pages(self, pdf_path: Path, output_filename: Optional[str] = None) -> str:
        """
        PDF 파일에서 페이지별로 텍스트를 추출하여 TXT 파일로 저장
        
        Args:
            pdf_path: PDF 파일 경로
            output_filename: 출력 파일명 (선택사항)
            
        Returns:
            str: 추출된 텍스트 내용
        """
        try:
            # 1단계: 파일 검증
            if not self._validate_pdf_file(pdf_path):
                return ""
            
            # 2단계: PDF 정보 수집
            pdf_info = self.get_pdf_info(pdf_path)
            print(f"=== PDF 정보 ===")
            print(f"파일명: {pdf_info.get('파일명', 'N/A')}")
            print(f"총 페이지 수: {pdf_info.get('총_페이지_수', 'N/A')}")
            print(f"파일 크기: {pdf_info.get('파일_크기', 'N/A')}")
            print()
            
            # 3단계: 텍스트 추출
            extracted_content = self._extract_text(pdf_path)
            
            # 4단계: 출력 파일명 결정 및 저장
            if output_filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"{pdf_path.stem}_extracted_{timestamp}.txt"
            
            output_path = OUTPUT_DIR / output_filename
            
            # 5단계: 결과 저장
            self._save_extracted_content(output_path, extracted_content, pdf_info)
            
            return extracted_content
            
        except Exception as e:
            print(f"오류: PDF 텍스트 추출 중 오류 발생: {e}")
            return ""
    
    def _validate_pdf_file(self, pdf_path: Path) -> bool:
        """PDF 파일 검증"""
        if not pdf_path.exists():
            print(f"오류: PDF 파일이 존재하지 않습니다: {pdf_path}")
            return False
        
        if pdf_path.stat().st_size == 0:
            print(f"오류: PDF 파일이 비어있습니다: {pdf_path}")
            return False
        
        if pdf_path.suffix.lower() != '.pdf':
            print(f"오류: PDF 파일이 아닙니다: {pdf_path}")
            return False
        
        return True
    
    def _extract_text(self, pdf_path: Path) -> str:
        """텍스트 추출"""
        try:
            doc = fitz.open(str(pdf_path))
            total_pages = len(doc)
            
            extracted_content = []
            
            print("=== 텍스트 추출 시작 ===")
            
            for page_num in range(total_pages):
                print(f"페이지 {page_num + 1}/{total_pages} 처리 중...")
                
                page = doc.load_page(page_num)
                text = page.get_text()
                
                if text.strip():  # 빈 페이지가 아닌 경우만 처리
                    # 페이지 시작 표시
                    extracted_content.append(f"=== {page_num + 1}페이지 ===")
                    
                    # 줄별로 번호 매기기
                    lines = text.strip().split('\n')
                    for line_num, line in enumerate(lines, 1):
                        if line.strip():  # 빈 줄 제외
                            extracted_content.append(f"{line_num}줄: {line}")
                    
                    # 페이지 구분자
                    extracted_content.append("----")
                    extracted_content.append("")  # 빈 줄 추가
            
            doc.close()
            
            return '\n'.join(extracted_content)
            
        except Exception as e:
            print(f"오류: 텍스트 추출 중 오류 발생: {e}")
            return ""
    
    def _save_extracted_content(self, output_path: Path, content: str, pdf_info: Dict[str, Any]):
        """추출된 내용 저장"""
        try:
            # 출력 디렉토리 확인
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 메타데이터 추가
            metadata = self._generate_metadata(pdf_info)
            
            # 전체 내용 구성
            full_content = f"""# PDF 텍스트 추출 결과

## 메타데이터
{metadata}

## 추출된 내용
{content}

## 분석 완료 시간
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
            
            # 파일 저장
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            print(f"✅ 텍스트 추출 완료: {output_path}")
            print(f"📊 파일 크기: {output_path.stat().st_size:,} bytes")
            
        except Exception as e:
            print(f"오류: 파일 저장 중 오류 발생: {e}")
    
    def _generate_metadata(self, pdf_info: Dict[str, Any]) -> str:
        """메타데이터 생성"""
        metadata_lines = []
        
        # 기본 정보
        metadata_lines.append(f"- 파일명: {pdf_info.get('파일명', 'N/A')}")
        metadata_lines.append(f"- 총 페이지 수: {pdf_info.get('총_페이지_수', 'N/A')}")
        metadata_lines.append(f"- 파일 크기: {pdf_info.get('파일_크기', 'N/A')}")
        metadata_lines.append(f"- 추출 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return '\n'.join(metadata_lines)
    
    def get_pdf_info(self, pdf_path: Path) -> Dict[str, Any]:
        """PDF 파일 정보 수집"""
        try:
            doc = fitz.open(str(pdf_path))
            
            info = {
                "파일명": pdf_path.name,
                "총_페이지_수": len(doc),
                "파일_크기": f"{pdf_path.stat().st_size:,} bytes",
                "메타데이터": doc.metadata
            }
            
            doc.close()
            return info
            
        except Exception as e:
            print(f"오류: PDF 정보 수집 중 오류 발생: {e}")
            return {}
    
    def extract_text_with_options(self, pdf_path: Path, include_page_numbers: bool = True, 
                                 include_line_numbers: bool = True, page_separator: str = "----",
                                 output_filename: Optional[str] = None) -> str:
        """
        옵션을 지정하여 PDF 텍스트 추출
        
        Args:
            pdf_path: PDF 파일 경로
            include_page_numbers: 페이지 번호 포함 여부
            include_line_numbers: 줄 번호 포함 여부
            page_separator: 페이지 구분자
            output_filename: 출력 파일명
            
        Returns:
            str: 추출된 텍스트 내용
        """
        try:
            if not self._validate_pdf_file(pdf_path):
                return ""
            
            doc = fitz.open(str(pdf_path))
            total_pages = len(doc)
            
            extracted_content = []
            
            for page_num in range(total_pages):
                page = doc.load_page(page_num)
                text = page.get_text()
                
                if text.strip():
                    # 페이지 번호 포함
                    if include_page_numbers:
                        extracted_content.append(f"=== {page_num + 1}페이지 ===")
                    
                    # 줄별 처리
                    lines = text.strip().split('\n')
                    for line_num, line in enumerate(lines, 1):
                        if line.strip():
                            if include_line_numbers:
                                extracted_content.append(f"{line_num}줄: {line}")
                            else:
                                extracted_content.append(line)
                    
                    # 페이지 구분자
                    if page_num < total_pages - 1:  # 마지막 페이지가 아닌 경우
                        extracted_content.append(page_separator)
                        extracted_content.append("")
            
            doc.close()
            
            content = '\n'.join(extracted_content)
            
            # 파일 저장
            if output_filename:
                output_path = OUTPUT_DIR / output_filename
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ 텍스트 추출 완료: {output_path}")
            
            return content
            
        except Exception as e:
            print(f"오류: 텍스트 추출 중 오류 발생: {e}")
            return ""
    
    def analyze_content(self, content: str) -> Dict[str, Any]:
        """추출된 내용 분석"""
        try:
            analysis = {
                "content_length": len(content),
                "line_count": len(content.split('\n')),
                "page_count": len(re.findall(r"=== \d+페이지 ===", content)),
                "patterns_found": self._find_patterns(content),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            return analysis
            
        except Exception as e:
            print(f"오류: 내용 분석 중 오류 발생: {e}")
            return {}
    
    def _find_patterns(self, content: str) -> Dict[str, list]:
        """내용에서 패턴 찾기"""
        patterns = {
            "부문": re.findall(r"([가-힣]+부문)", content),
            "장": re.findall(r"(제[0-9]+장\s*[가-힣]+)", content),
            "절": re.findall(r"([0-9]+-[0-9]+[가-힣]*)", content),
            "페이지": re.findall(r"(=== [0-9]+페이지 ===)", content)
        }
        
        return patterns

def main():
    """메인 함수"""
    import sys
    
    if len(sys.argv) < 2:
        print("사용법: python pdf_text_extractor.py <PDF_파일_경로>")
        sys.exit(1)
    
    pdf_path = Path(sys.argv[1])
    extractor = PDFTextExtractor()
    
    # 기본 추출
    content = extractor.extract_text_by_pages(pdf_path)
    
    if content:
        print("✅ 텍스트 추출이 완료되었습니다.")
        
        # 내용 분석
        analysis = extractor.analyze_content(content)
        print(f"\n=== 분석 결과 ===")
        print(f"총 문자 수: {analysis.get('content_length', 0):,}")
        print(f"총 줄 수: {analysis.get('line_count', 0):,}")
        print(f"페이지 수: {analysis.get('page_count', 0)}")
        
        patterns = analysis.get('patterns_found', {})
        for pattern_name, matches in patterns.items():
            print(f"{pattern_name}: {len(matches)}개 발견")
    else:
        print("❌ 텍스트 추출에 실패했습니다.")

if __name__ == "__main__":
    main() 