#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 데스크톱 애플리케이션 메인 윈도우
PySide6 기반 건설 관리 시스템 UI
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QMenuBar, QStatusBar, QToolBar,
    QLabel, QPushButton, QSplitter, QFrame, QMessageBox,
    QApplication, QDialog
)
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QIcon, QFont, QAction, QFontDatabase
import logging
from typing import Optional, Dict, Any
import platform

from .contract_tab import ContractTab
from .financial_tab import FinancialTab
from .labor_tab import LaborTab
from .dashboard_tab import DashboardTab
from .project_tab import ProjectTab
from .settings_tab import SettingsTab
from .help_tab import HelpTab
from .login_dialog import LoginDialog
from api.client import get_api_client, APIError
from widgets.api_test_widget import APITestWidget

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """CMA 메인 윈도우 클래스"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CMA - Construction Management System")
        self.setGeometry(100, 100, 1400, 900)
        
        # 한글 폰트 설정
        self.setup_korean_font()
        
        # API 클라이언트 초기화
        self.api_client = get_api_client()
        self.current_user = None
        
        # 로그인 상태 확인
        if not self.check_login():
            self.show_login_dialog()
        
        # UI 초기화
        self.init_ui()
        self.setup_menu_bar()
        self.setup_tool_bar()
        self.setup_status_bar()
        
        # 스타일 설정
        self.setup_styles()
        
        # 타이머 설정 (주기적 상태 업데이트)
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(30000)  # 30초마다 업데이트
    
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
                app = QApplication.instance()
                if app:
                    app.setFont(QFont(selected_english_font, 9))
                    logger.info(f"[SUCCESS] 폰트 설정 완료 - 영어: {selected_english_font}, 한글: {selected_korean_font}")
                else:
                    logger.warning("[WARNING] QApplication 인스턴스를 찾을 수 없습니다")
            elif selected_english_font:
                app = QApplication.instance()
                if app:
                    app.setFont(QFont(selected_english_font, 9))
                    logger.info(f"[SUCCESS] 영어 폰트 설정 완료: {selected_english_font}")
            elif selected_korean_font:
                app = QApplication.instance()
                if app:
                    app.setFont(QFont(selected_korean_font, 9))
                    logger.info(f"[SUCCESS] 한글 폰트 설정 완료: {selected_korean_font}")
            else:
                logger.warning(f"[WARNING] JetBrains Mono 또는 D2Coding 폰트를 찾을 수 없습니다.")
                logger.info(f"[INFO] 사용 가능한 폰트: {available_fonts[:10]}")
                
        except Exception as e:
            logger.error(f"[ERROR] 폰트 설정 실패: {e}")
    
    def check_login(self) -> bool:
        """로그인 상태 확인"""
        try:
            # 저장된 토큰이 있는지 확인
            if self.api_client.access_token:
                # 토큰 유효성 검증
                result = self.api_client.get_current_user()
                if result.get("status") == "success":
                    self.current_user = result.get("data")
                    return True
        except Exception as e:
            logger.warning(f"로그인 상태 확인 실패: {e}")
        
        return False
    
    def show_login_dialog(self):
        """로그인 다이얼로그 표시"""
        login_dialog = LoginDialog(self)
        login_dialog.login_successful.connect(self.on_login_success)
        
        result = login_dialog.exec()
        if result != QDialog.DialogCode.Accepted:
            # 로그인 취소 또는 실패 시 앱 완전 종료
            logger.info("로그인 취소 또는 실패로 인한 애플리케이션 종료")
            # 즉시 애플리케이션 종료
            QApplication.instance().quit()
            # 강제 종료를 위한 sys.exit 추가
            import sys
            sys.exit(0)
            return
        
        # 로그인 성공 시에만 계속 진행
        if not self.current_user:
            logger.warning("로그인 성공했지만 사용자 정보가 없습니다. 애플리케이션을 종료합니다.")
            QApplication.instance().quit()
            import sys
            sys.exit(0)
            return
    
    def on_login_success(self, result: Dict[str, Any]):
        """로그인 성공 처리"""
        try:
            user_data = result.get("data", {})
            self.current_user = user_data
            
            # 사용자 정보 업데이트
            self.update_user_info()
            
            # 대시보드 데이터 로드
            self.load_dashboard_data()
            
            logger.info(f"사용자 로그인 성공: {user_data.get('email', 'Unknown')}")
            
        except Exception as e:
            logger.error(f"로그인 성공 처리 중 오류: {e}")
            QMessageBox.critical(self, "오류", "로그인 처리 중 오류가 발생했습니다.")
    
    def update_user_info(self):
        """사용자 정보 업데이트"""
        if self.current_user:
            user_info_text = f"사용자: {self.current_user.get('name', 'Unknown')} | 로그인 시간: {self.current_user.get('login_time', 'Unknown')}"
            if hasattr(self, 'user_info_label'):
                self.user_info_label.setText(user_info_text)
    
    def load_dashboard_data(self):
        """대시보드 데이터 로드"""
        try:
            if hasattr(self, 'dashboard_tab'):
                self.dashboard_tab.load_data()
        except Exception as e:
            logger.error(f"대시보드 데이터 로드 실패: {e}")
    
    def init_ui(self):
        """UI 초기화"""
        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # 헤더 영역
        self.setup_header(main_layout)
        
        # 탭 위젯 설정
        self.setup_tab_widget(main_layout)
        
        # 상태 영역
        self.setup_status_area(main_layout)
    
    def setup_header(self, layout):
        """헤더 영역 설정"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.StyledPanel)
        header_frame.setMaximumHeight(80)
        
        header_layout = QHBoxLayout(header_frame)
        
        # 로고 및 제목
        title_label = QLabel("CMA - Construction Management System")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # 사용자 정보
        self.user_info_label = QLabel("사용자: 로그인 필요")
        self.user_info_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        header_layout.addWidget(self.user_info_label)
        
        # 로그아웃 버튼
        logout_button = QPushButton("로그아웃")
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        logout_button.clicked.connect(self.logout)
        header_layout.addWidget(logout_button)
        
        layout.addWidget(header_frame)
    
    def setup_tab_widget(self, layout):
        """탭 위젯 설정"""
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                background: white;
            }
            QTabBar::tab {
                background: #ecf0f1;
                padding: 8px 16px;
                margin-right: 2px;
                border: 1px solid #bdc3c7;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 1px solid white;
            }
            QTabBar::tab:hover {
                background: #d5dbdb;
            }
        """)
        
        # 대시보드 탭
        self.dashboard_tab = DashboardTab()
        self.tab_widget.addTab(self.dashboard_tab, "대시보드")
        
        # 계약 관리 탭
        self.contract_tab = ContractTab()
        self.tab_widget.addTab(self.contract_tab, "계약 관리")
        
        # 재무 관리 탭
        self.financial_tab = FinancialTab()
        self.tab_widget.addTab(self.financial_tab, "재무 관리")
        
        # 노무 관리 탭
        self.labor_tab = LaborTab()
        self.tab_widget.addTab(self.labor_tab, "노무 관리")
        
        # 프로젝트 관리 탭
        self.project_tab = ProjectTab()
        self.tab_widget.addTab(self.project_tab, "프로젝트 관리")
        
        # 설정 탭
        self.settings_tab = SettingsTab()
        self.tab_widget.addTab(self.settings_tab, "설정")
        
        # 도움말 탭
        self.help_tab = HelpTab()
        self.tab_widget.addTab(self.help_tab, "도움말")
        
        # API 테스트 탭
        self.api_test_tab = APITestWidget()
        self.tab_widget.addTab(self.api_test_tab, "API 테스트")
        
        layout.addWidget(self.tab_widget)
    
    def setup_status_area(self, layout):
        """상태 영역 설정"""
        status_frame = QFrame()
        status_frame.setFrameStyle(QFrame.StyledPanel)
        status_frame.setMaximumHeight(60)
        
        status_layout = QHBoxLayout(status_frame)
        
        # 시스템 상태
        self.system_status_label = QLabel("시스템 상태: 확인 중...")
        self.system_status_label.setStyleSheet("color: #f39c12; font-weight: bold;")
        status_layout.addWidget(self.system_status_label)
        
        status_layout.addStretch()
        
        # 데이터베이스 연결 상태
        self.db_status_label = QLabel("데이터베이스: 확인 중...")
        self.db_status_label.setStyleSheet("color: #f39c12;")
        status_layout.addWidget(self.db_status_label)
        
        # 마지막 업데이트
        self.last_update_label = QLabel("마지막 업데이트: -")
        self.last_update_label.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        status_layout.addWidget(self.last_update_label)
        
        layout.addWidget(status_frame)
    
    def update_status(self):
        """상태 정보 업데이트"""
        try:
            # 시스템 상태 확인
            system_status = self.api_client.get_system_status()
            if system_status.get("status") == "success":
                health = system_status.get("data", {}).get("health", "unknown")
                if health == "healthy":
                    self.system_status_label.setText("시스템 상태: 정상")
                    self.system_status_label.setStyleSheet("color: #27ae60; font-weight: bold;")
                elif health == "warning":
                    self.system_status_label.setText("시스템 상태: 주의")
                    self.system_status_label.setStyleSheet("color: #f39c12; font-weight: bold;")
                else:
                    self.system_status_label.setText("시스템 상태: 오류")
                    self.system_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
                
                # 데이터베이스 상태
                db_status = system_status.get("data", {}).get("database_status", "unknown")
                if db_status == "connected":
                    self.db_status_label.setText("데이터베이스: 연결됨")
                    self.db_status_label.setStyleSheet("color: #27ae60;")
                else:
                    self.db_status_label.setText("데이터베이스: 연결 실패")
                    self.db_status_label.setStyleSheet("color: #e74c3c;")
                
                # 마지막 업데이트 시간
                from datetime import datetime
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.last_update_label.setText(f"마지막 업데이트: {current_time}")
                
        except Exception as e:
            logger.error(f"상태 업데이트 실패: {e}")
            self.system_status_label.setText("시스템 상태: 오류")
            self.system_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
    
    def logout(self):
        """로그아웃"""
        try:
            # API 토큰 제거
            self.api_client.clear_auth_token()
            self.current_user = None
            
            # UI 초기화
            self.user_info_label.setText("사용자: 로그인 필요")
            
            # 로그인 다이얼로그 표시
            self.show_login_dialog()
            
        except Exception as e:
            logger.error(f"로그아웃 중 오류: {e}")
    
    def setup_menu_bar(self):
        """메뉴바 설정"""
        menubar = self.menuBar()
        
        # 파일 메뉴
        file_menu = menubar.addMenu("파일")
        
        new_action = QAction("새로 만들기", self)
        new_action.setShortcut("Ctrl+N")
        file_menu.addAction(new_action)
        
        open_action = QAction("열기", self)
        open_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_action)
        
        save_action = QAction("저장", self)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("종료", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 편집 메뉴
        edit_menu = menubar.addMenu("편집")
        
        undo_action = QAction("실행 취소", self)
        undo_action.setShortcut("Ctrl+Z")
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("다시 실행", self)
        redo_action.setShortcut("Ctrl+Y")
        edit_menu.addAction(redo_action)
        
        # 도구 메뉴
        tools_menu = menubar.addMenu("도구")
        
        settings_action = QAction("설정", self)
        tools_menu.addAction(settings_action)
        
        # 도움말 메뉴
        help_menu = menubar.addMenu("도움말")
        
        about_action = QAction("정보", self)
        help_menu.addAction(about_action)
    
    def setup_tool_bar(self):
        """툴바 설정"""
        toolbar = self.addToolBar("메인 툴바")
        toolbar.setMovable(False)
        
        # 새로 만들기
        new_action = QAction("새로 만들기", self)
        new_action.setStatusTip("새 문서 만들기")
        toolbar.addAction(new_action)
        
        toolbar.addSeparator()
        
        # 저장
        save_action = QAction("저장", self)
        save_action.setStatusTip("현재 문서 저장")
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # 인쇄
        print_action = QAction("인쇄", self)
        print_action.setStatusTip("현재 문서 인쇄")
        toolbar.addAction(print_action)
    
    def setup_status_bar(self):
        """상태바 설정"""
        status_bar = self.statusBar()
        status_bar.showMessage("준비")
    
    def setup_styles(self):
        """스타일 설정"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
    
    def closeEvent(self, event):
        """앱 종료 이벤트"""
        try:
            # API 클라이언트 정리
            if self.api_client:
                self.api_client.close()
            
            # 타이머 정지
            if hasattr(self, 'status_timer'):
                self.status_timer.stop()
            
            logger.info("CMA 애플리케이션 종료")
            event.accept()
            
        except Exception as e:
            logger.error(f"앱 종료 중 오류: {e}")
            event.accept() 