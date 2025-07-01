#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 데스크톱 애플리케이션 메인 모듈
PySide6 기반 건설 관리 시스템
"""

import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtCore import Qt, QThread, pyqtSignal
from PySide6.QtGui import QIcon, QFont

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from desktop.ui.main_window import MainWindow
from desktop.core.database import DatabaseManager
from desktop.core.config import ConfigManager
from desktop.utils.logger import setup_logger

class CMAApplication(QApplication):
    """CMA 데스크톱 애플리케이션 클래스"""
    
    def __init__(self, argv):
        super().__init__(argv)
        
        # 애플리케이션 정보 설정
        self.setApplicationName("CMA - Construction Management System")
        self.setApplicationVersion("1.0.0")
        self.setOrganizationName("CMA Development Team")
        
        # 로거 설정
        self.logger = setup_logger()
        
        # 설정 관리자 초기화
        self.config = ConfigManager()
        
        # 데이터베이스 관리자 초기화
        self.db_manager = DatabaseManager()
        
        # 메인 윈도우 생성
        self.main_window = MainWindow(self)
        
    def initialize(self):
        """애플리케이션 초기화"""
        try:
            self.logger.info("[INFO] CMA 데스크톱 애플리케이션 초기화 시작")
            
            # 데이터베이스 연결
            self.db_manager.connect()
            
            # 메인 윈도우 표시
            self.main_window.show()
            
            self.logger.info("[SUCCESS] CMA 데스크톱 애플리케이션 초기화 완료")
            
        except Exception as e:
            self.logger.error(f"[ERROR] 애플리케이션 초기화 실패: {e}")
            raise
    
    def cleanup(self):
        """애플리케이션 정리"""
        try:
            self.logger.info("[INFO] 애플리케이션 정리 시작")
            
            # 데이터베이스 연결 종료
            self.db_manager.disconnect()
            
            self.logger.info("[SUCCESS] 애플리케이션 정리 완료")
            
        except Exception as e:
            self.logger.error(f"[ERROR] 애플리케이션 정리 실패: {e}")

def main():
    """메인 함수"""
    try:
        # 애플리케이션 생성
        app = CMAApplication(sys.argv)
        
        # 애플리케이션 초기화
        app.initialize()
        
        # 이벤트 루프 시작
        exit_code = app.exec()
        
        # 애플리케이션 정리
        app.cleanup()
        
        sys.exit(exit_code)
        
    except Exception as e:
        print(f"[ERROR] 애플리케이션 실행 실패: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 