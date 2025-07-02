#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
건설업계 표준가격표 목차 추출 스크립트

기능:
1. 표준가격표 PDF에서 목차 구조 분석 및 JSON 생성
2. PDF 구조 검증 및 품질 관리
3. 매핑 설정 자동 생성

주의: 다운로드 자동화 기능은 추후 개발 예정입니다.
현재는 수동으로 다운로드한 PDF 파일을 input 폴더에 넣고 실행하세요.

리팩토링: 통합 목차 추출 모듈 사용
"""

from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import logging

# 통합 모듈 import
from src.utils.toc_interface import TOCExtractorManager, ExtractionConfig, ExtractionMethod
from src.utils.logger import get_logger

# 로거 설정
logger = get_logger(__name__)

class StandardPriceListProcessor:
    """표준가격표 처리 클래스 (목차 추출 전용)"""
    
    def __init__(self):
        # 디렉토리 설정
        self.input_dir = Path("input")
        self.output_dir = Path("output")
        self.input_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # TOC 추출 관리자 초기화
        self.toc_manager = TOCExtractorManager()
    
    def find_standard_price_pdf(self) -> Optional[Path]:
        """
        input 폴더에서 표준가격표 PDF 파일 찾기
        
        Returns:
            찾은 PDF 파일 경로 또는 None
        """
        # 표준가격표 PDF 패턴 검색
        patterns = [
            "*construction_work_standard_price_list*.pdf",
            "*표준가격표*.pdf",
            "*standard_price*.pdf"
        ]
        
        for pattern in patterns:
            files = list(self.input_dir.glob(pattern))
            if files:
                # 가장 최신 파일 반환
                latest_file = max(files, key=lambda x: x.stat().st_mtime)
                logger.info(f"✅ 표준가격표 PDF 발견: {latest_file}")
                return latest_file
        
        logger.warning("❌ 표준가격표 PDF를 찾을 수 없습니다.")
        logger.info("💡 input 폴더에 표준가격표 PDF를 추가한 후 다시 시도해주세요.")
        return None
    
    def extract_toc_from_pdf(self, pdf_path: Path) -> Optional[Dict[str, Any]]:
        """
        PDF에서 목차 추출 (통합 모듈 사용)
        
        Args:
            pdf_path: PDF 파일 경로
            
        Returns:
            목차 구조 또는 None
        """
        try:
            logger.info(f"📋 목차 추출 시작: {pdf_path}")
            
            # 추출 설정
            config = ExtractionConfig(
                method=ExtractionMethod.AUTO,  # 자동 감지
                max_pages=50,  # 목차는 보통 앞쪽에 있음
                include_metadata=True,
                validate_structure=True
            )
            
            # 목차 추출 실행
            result = self.toc_manager.extract_toc(pdf_path, config)
            
            if result.success:
                logger.info("✅ 목차 추출 성공!")
                logger.info(f"📊 추출된 항목 수: {result.metadata.get('total_entries', 0)}")
                
                # 출력 파일 정보
                for output_file in result.output_files:
                    logger.info(f"📁 생성된 파일: {output_file}")
                
                return result.toc_structure
            else:
                logger.error(f"❌ 목차 추출 실패: {result.error_message}")
                return None
                
        except Exception as e:
            logger.error(f"❌ 목차 추출 중 오류: {e}")
            return None
    
    def validate_pdf_structure(self, pdf_path: Path, toc_structure: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        PDF 구조 검증
        
        Args:
            pdf_path: PDF 파일 경로
            toc_structure: 목차 구조 (선택사항)
            
        Returns:
            검증 결과
        """
        validation_result = {
            "file_exists": False,
            "file_size": 0,
            "page_count": 0,
            "toc_extracted": False,
            "toc_entries": 0,
            "sections_found": 0,
            "validation_score": 0
        }
        
        try:
            # 파일 존재 확인
            if pdf_path.exists():
                validation_result["file_exists"] = True
                validation_result["file_size"] = pdf_path.stat().st_size
                
                # 페이지 수 확인
                try:
                    from pypdf import PdfReader
                    reader = PdfReader(pdf_path)
                    validation_result["page_count"] = len(reader.pages)
                except Exception as e:
                    logger.warning(f"페이지 수 확인 실패: {e}")
            
            # 목차 구조 검증
            if toc_structure:
                validation_result["toc_extracted"] = True
                
                if hasattr(toc_structure, 'entries'):
                    validation_result["toc_entries"] = len(toc_structure.entries)
                
                if hasattr(toc_structure, 'sections'):
                    sections_found = len([s for s in toc_structure.sections.values() if s.get('start_page')])
                    validation_result["sections_found"] = sections_found
            
            # 검증 점수 계산
            score = 0
            if validation_result["file_exists"]:
                score += 20
            if validation_result["file_size"] > 1000000:  # 1MB 이상
                score += 20
            if validation_result["page_count"] > 0:
                score += 20
            if validation_result["toc_extracted"]:
                score += 20
            if validation_result["toc_entries"] > 0:
                score += 10
            if validation_result["sections_found"] >= 3:
                score += 10
            
            validation_result["validation_score"] = score
            
            return validation_result
            
        except Exception as e:
            logger.error(f"❌ PDF 구조 검증 실패: {e}")
            return validation_result
    
    def generate_processing_report(self, pdf_path: Path, toc_structure: Optional[Dict[str, Any]] = None, 
                                  validation_result: Optional[Dict[str, Any]] = None) -> str:
        """
        처리 보고서 생성
        
        Args:
            pdf_path: PDF 파일 경로
            toc_structure: 목차 구조
            validation_result: 검증 결과
            
        Returns:
            보고서 내용
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"""# 📋 표준가격표 목차 추출 보고서

## 📋 작업 개요
- **작업 시간**: {timestamp}
- **원본 파일**: {pdf_path.name}
- **파일 경로**: {pdf_path}

## 📊 파일 정보
"""
        
        if validation_result:
            report += f"""
- **파일 존재**: {'✅' if validation_result['file_exists'] else '❌'}
- **파일 크기**: {validation_result['file_size']:,} bytes ({validation_result['file_size'] / 1024 / 1024:.1f} MB)
- **페이지 수**: {validation_result['page_count']}페이지
- **검증 점수**: {validation_result['validation_score']}/100점
"""
        
        if toc_structure:
            report += f"""
## 📋 목차 구조 정보
- **목차 추출**: ✅ 성공
- **총 항목 수**: {validation_result.get('toc_entries', 0) if validation_result else 'N/A'}
- **발견된 부문**: {validation_result.get('sections_found', 0) if validation_result else 'N/A'}
"""
            
            if hasattr(toc_structure, 'metadata'):
                method = toc_structure.metadata.get('extraction_method', 'unknown')
                report += f"- **추출 방법**: {method}\n"
        else:
            report += """
## 📋 목차 구조 정보
- **목차 추출**: ❌ 실패
"""
        
        report += f"""
## 🔍 품질 평가
"""
        
        if validation_result:
            score = validation_result['validation_score']
            if score >= 80:
                report += "- **등급**: 🟢 우수\n"
            elif score >= 60:
                report += "- **등급**: 🟡 양호\n"
            elif score >= 40:
                report += "- **등급**: 🟠 보통\n"
            else:
                report += "- **등급**: 🔴 미흡\n"
            
            report += f"- **점수**: {score}/100점\n"
        
        report += f"""
## 💡 다음 단계
1. **PDF 분할**: `python scripts/pdf_split_by_chapters.py`
2. **부문별 분할**: `python scripts/pdf_split_by_sections.py`
3. **장 정보 분석**: `python scripts/analyze_chapters.py`
4. **매핑 설정 생성**: `python -m src.utils.pdf_to_lookup_table --action convert --lookup-table output/lookup_table_xxx.csv`

## 📁 생성된 파일들
"""
        
        # 생성된 파일 목록
        output_files = list(self.output_dir.glob("*"))
        for file in output_files:
            if file.is_file():
                file_size = file.stat().st_size
                report += f"- **{file.name}**: {file_size:,} bytes\n"
        
        report += f"""
## 🔮 향후 개발 예정 기능
- **자동 다운로드**: 표준가격표 PDF 자동 다운로드 기능
- **버전 관리**: 연도별 표준가격표 버전 관리
- **업데이트 알림**: 새로운 표준가격표 출시 알림
"""
        
        return report
    
    def run_processing_workflow(self) -> bool:
        """
        목차 추출 워크플로우 실행
        
        Returns:
            성공 여부
        """
        logger.info("🚀 목차 추출 워크플로우 시작")
        
        try:
            # 1. PDF 파일 찾기
            pdf_path = self.find_standard_price_pdf()
            if not pdf_path:
                logger.error("❌ 표준가격표 PDF를 찾을 수 없습니다")
                return False
            
            # 2. 목차 추출
            toc_structure = self.extract_toc_from_pdf(pdf_path)
            
            # 3. 구조 검증
            validation_result = self.validate_pdf_structure(pdf_path, toc_structure)
            
            # 4. 보고서 생성
            report = self.generate_processing_report(pdf_path, toc_structure, validation_result)
            
            # 보고서 저장
            report_file = self.output_dir / f"processing_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            with open(report_file, 'w', encoding='utf-8', newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
                f.write(report)
            
            logger.info(f"📄 보고서 저장: {report_file}")
            
            # 결과 출력
            print("\n" + "="*60)
            print("🎉 목차 추출 워크플로우 완료!")
            print("="*60)
            print(f"📄 처리 파일: {pdf_path.name}")
            print(f"📋 목차 추출: {'성공' if toc_structure else '실패'}")
            print(f"🔍 검증 점수: {validation_result['validation_score']}/100점")
            print(f"📄 보고서: {report_file.name}")
            print("="*60)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ 워크플로우 실행 실패: {e}")
            return False

def main():
    """메인 함수 (목차 추출 전용)"""
    import argparse
    
    parser = argparse.ArgumentParser(description="표준가격표 목차 추출")
    parser.add_argument("--pdf", type=str, default=None,
                       help="처리할 PDF 파일 경로 (기본값: input 폴더에서 자동 검색)")
    parser.add_argument("--validate", action="store_true", 
                       help="결과 검증 수행")
    
    args = parser.parse_args()
    
    print("🚀 ASCR - 표준가격표 목차 추출 시스템")
    print("=" * 60)
    print("💡 다운로드 자동화 기능은 추후 개발 예정입니다.")
    print("📁 input 폴더에 표준가격표 PDF를 추가한 후 실행하세요.")
    print("=" * 60)
    
    processor = StandardPriceListProcessor()
    
    if args.pdf:
        # 지정된 PDF 파일 처리
        pdf_path = Path(args.pdf)
        if pdf_path.exists():
            toc_structure = processor.extract_toc_from_pdf(pdf_path)
            if toc_structure:
                print(f"✅ 목차 추출 완료: {pdf_path}")
            else:
                print("❌ 목차 추출 실패")
        else:
            print(f"❌ 파일을 찾을 수 없습니다: {pdf_path}")
    else:
        # 자동 검색 및 처리
        success = processor.run_processing_workflow()
        if not success:
            print("❌ 워크플로우 실행 실패")

if __name__ == "__main__":
    main() 