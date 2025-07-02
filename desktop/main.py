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
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon, QFont, QFontDatabase
import platform

# 플랫폼별 GUI 실행 환경 설정
if platform.system() == "Darwin":  # macOS
    # Mac 특화 설정
    os.environ['QT_QPA_PLATFORM'] = 'cocoa'  # Cocoa 플랫폼 사용
    os.environ['QT_MAC_WANTS_LAYER'] = '1'   # Metal 렌더링 사용
    print("[INFO] macOS 환경에서 Cocoa 플랫폼으로 실행합니다.")
    
elif platform.system() == "Linux":
    # WSL2 환경 감지
    is_wsl = Path('/proc/version').exists() and 'microsoft' in open('/proc/version').read().lower()
    
    if is_wsl:
        # WSL2에서는 X 서버 연결 시도
        if 'DISPLAY' in os.environ and os.environ['DISPLAY'] != ':0':
            os.environ['QT_QPA_PLATFORM'] = 'xcb'
            print(f"[INFO] WSL2 X 서버 연결: {os.environ['DISPLAY']}")
        else:
            # X 서버가 없으면 offscreen 사용
            os.environ['QT_QPA_PLATFORM'] = 'offscreen'
            print("[WARNING] WSL2에서 X 서버가 연결되지 않았습니다. offscreen 모드로 실행합니다.")
    else:
        # 일반 Linux
        os.environ['QT_QPA_PLATFORM'] = 'xcb'
        print("[INFO] Linux 환경에서 XCB 플랫폼으로 실행합니다.")
        
elif platform.system() == "Windows":
    # Windows 환경
    os.environ['QT_QPA_PLATFORM'] = 'windows'
    print("[INFO] Windows 환경에서 Windows 플랫폼으로 실행합니다.")
    
else:
    # 기타 환경
    os.environ['QT_QPA_PLATFORM'] = 'xcb'
    print(f"[INFO] {platform.system()} 환경에서 XCB 플랫폼으로 실행합니다.")

os.environ['LANG'] = 'ko_KR.UTF-8'     # 한글 로케일 설정

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
        
        # 한글 폰트 설정
        self.setup_korean_font()
        
        # 로거 설정
        self.logger = setup_logger()
        
        # 설정 관리자 초기화
        self.config = ConfigManager()
        
        # 데이터베이스 관리자 초기화
        self.db_manager = DatabaseManager()
        
        # 메인 윈도우 생성
        self.main_window = MainWindow()
    
    def setup_korean_font(self):
        """한글 폰트 설정"""
        try:
            # Cursor에서 사용하는 폰트 설정
            # 영어: JetBrains Mono, 한글: D2Coding
            english_fonts = ["JetBrains Mono", "JetBrains Mono NL"]
            korean_fonts = ["D2Coding", "D2Coding ligature"]
            
            # 사용 가능한 폰트 찾기
            available_fonts = QFontDatabase().families()
            
            # 영어 폰트 선택
            selected_english_font = None
            for font in english_fonts:
                if font in available_fonts:
                    selected_english_font = font
                    break
            
            # 한글 폰트 선택
            selected_korean_font = None
            for font in korean_fonts:
                if font in available_fonts:
                    selected_korean_font = font
                    break
            
            if selected_english_font and selected_korean_font:
                # 기본 폰트로 JetBrains Mono 설정
                self.setFont(QFont(selected_english_font, 9))
                print(f"[SUCCESS] 폰트 설정 완료 - 영어: {selected_english_font}, 한글: {selected_korean_font}")
            elif selected_english_font:
                self.setFont(QFont(selected_english_font, 9))
                print(f"[SUCCESS] 영어 폰트 설정 완료: {selected_english_font}")
            elif selected_korean_font:
                self.setFont(QFont(selected_korean_font, 9))
                print(f"[SUCCESS] 한글 폰트 설정 완료: {selected_korean_font}")
            else:
                print(f"[WARNING] JetBrains Mono 또는 D2Coding 폰트를 찾을 수 없습니다.")
                print(f"[INFO] 사용 가능한 폰트: {available_fonts[:10]}")
                
        except Exception as e:
            print(f"[ERROR] 폰트 설정 실패: {e}")
        
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
        # 콘솔 모드 확인
        console_mode = '--console' in sys.argv or '--headless' in sys.argv
        
        if console_mode:
            print("[INFO] 콘솔 모드로 실행합니다.")
            # 콘솔 모드에서는 GUI 없이 백엔드 기능만 실행
            run_console_mode()
        else:
            # GUI 모드 실행
            app = CMAApplication(sys.argv)
            app.initialize()
            exit_code = app.exec()
            app.cleanup()
            sys.exit(exit_code)
        
    except Exception as e:
        print(f"[ERROR] 애플리케이션 실행 실패: {e}")
        sys.exit(1)

def run_console_mode():
    """콘솔 모드 실행"""
    try:
        print("[INFO] CMA 콘솔 모드 시작")
        
        # 설정 관리자 초기화
        config = ConfigManager()
        print(f"[INFO] 설정 로드 완료: {config.config_file}")
        
        # 데이터베이스 관리자 초기화
        db_manager = DatabaseManager()
        db_manager.connect()
        print("[SUCCESS] 데이터베이스 연결 완료")
        
        # 로거 설정
        logger = setup_logger()
        logger.info("[SUCCESS] 콘솔 모드 초기화 완료")
        
        print("[SUCCESS] CMA 콘솔 모드가 성공적으로 시작되었습니다.")
        print("[INFO] GUI 모드로 실행하려면: python main.py")
        print("[INFO] 종료하려면 Ctrl+C를 누르세요.")
        
        # 무한 루프로 실행 (Ctrl+C로 종료)
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[INFO] 사용자에 의해 종료되었습니다.")
        
    except Exception as e:
        print(f"[ERROR] 콘솔 모드 실행 실패: {e}")
        raise

if __name__ == "__main__":
    main() 