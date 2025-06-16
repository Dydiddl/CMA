from app.services.estimator import PDFConverter
import os
from pathlib import Path
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # 현재 스크립트의 디렉토리 경로
    current_dir = Path(__file__).parent
    
    # 변환할 PDF 파일 경로 (같은 디렉토리에 있는 PDF 파일)
    pdf_path = current_dir / "2025_Construction_Work_Standard_Price_List.pdf"
    
    if not pdf_path.exists():
        logger.error(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return
    
    # PDFConverter 인스턴스 생성
    converter = PDFConverter()
    
    try:
        logger.info(f"PDF 변환 시작: {pdf_path}")
        # PDF를 Word로 변환
        word_path = converter.convert_to_word(str(pdf_path))
        logger.info(f"변환 성공! Word 파일 위치: {word_path}")
        
    except Exception as e:
        logger.error(f"변환 실패: {str(e)}")

if __name__ == "__main__":
    main() 