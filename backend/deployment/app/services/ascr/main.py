#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASCR - 건설업계 표준 문서 자동화 처리 시스템
메인 프로그램

기능:
- PDF 텍스트 추출 및 목차 분석
- 장별/부문별 PDF 분할
- 자동화된 워크플로우
- 품질 검증 및 보고서 생성

개발자: ASCR Team
버전: 2.0
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# CLI 메뉴 핸들러 import
from src.cli.menu_handler import show_main_menu, ensure_directories

def main():
    """메인 함수"""
    try:
        # 필요한 디렉토리 생성
        ensure_directories()
        
        # 메인 메뉴 실행
        show_main_menu()
        
    except KeyboardInterrupt:
        print("\n\n👋 프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 프로그램 실행 중 오류가 발생했습니다: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()