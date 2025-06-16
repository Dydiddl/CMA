import os
from pathlib import Path
from typing import Optional
import logging
from datetime import datetime
import time
import shutil
from pdf2docx import Converter

logger = logging.getLogger(__name__)

class PDFConverter:
    """PDF 파일을 Word 문서로 변환하는 클래스"""
    
    def __init__(self):
        """초기화"""
        self.supported_formats = ['.docx', '.doc']
        self.temp_dir = Path('temp')
        self.temp_dir.mkdir(exist_ok=True)
    
    def convert_to_word(self, pdf_path: str, output_path: Optional[str] = None) -> str:
        """
        PDF 파일을 Word 문서로 변환합니다.
        
        Args:
            pdf_path (str): 변환할 PDF 파일 경로
            output_path (Optional[str]): 출력 파일 경로 (지정하지 않으면 자동 생성)
            
        Returns:
            str: 생성된 Word 파일 경로
            
        Raises:
            FileNotFoundError: PDF 파일이 존재하지 않는 경우
            ValueError: 지원하지 않는 파일 형식인 경우
            RuntimeError: 변환 실패 시
        """
        # 입력 파일 검증
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")
        
        if pdf_path.suffix.lower() != '.pdf':
            raise ValueError("PDF 파일만 변환이 가능합니다.")
        
        # 출력 경로 설정
        if output_path is None:
            output_path = self._generate_output_path(pdf_path)
        else:
            output_path = Path(output_path)
            if output_path.suffix.lower() not in self.supported_formats:
                raise ValueError(f"지원하지 않는 출력 형식입니다. 지원 형식: {', '.join(self.supported_formats)}")
        
        try:
            logger.info(f"PDF 변환 시작: {pdf_path} -> {output_path}")
            
            # 변환 시작 시간
            start_time = time.time()
            
            # PDF를 Word로 변환
            cv = Converter(str(pdf_path))
            cv.convert(str(output_path))
            cv.close()
            
            logger.info(f"PDF 변환 완료 (소요 시간: {time.time() - start_time:.2f}초): {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"PDF 변환 중 오류 발생: {str(e)}")
            raise RuntimeError(f"PDF 변환 실패: {str(e)}")
    
    def _generate_output_path(self, pdf_path: Path) -> Path:
        """
        출력 파일 경로를 생성합니다.
        
        Args:
            pdf_path (Path): 원본 PDF 파일 경로
            
        Returns:
            Path: 생성된 출력 파일 경로
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{pdf_path.stem}_{timestamp}.docx"
        return self.temp_dir / output_filename
    
    def cleanup(self):
        """임시 파일들을 정리합니다."""
        try:
            for file in self.temp_dir.glob("*"):
                if file.is_file():
                    file.unlink()
            logger.info("임시 파일 정리 완료")
        except Exception as e:
            logger.error(f"임시 파일 정리 중 오류 발생: {str(e)}") 