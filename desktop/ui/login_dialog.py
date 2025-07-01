#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 로그인 다이얼로그
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox, QCheckBox, QFrame, QGridLayout
)
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QFont, QIcon, QPixmap
import logging
from typing import Optional, Dict, Any
from api.client import get_api_client, APIError

logger = logging.getLogger(__name__)


class LoginWorker(QThread):
    """로그인 작업을 백그라운드에서 처리하는 워커 스레드"""
    
    login_success = Signal(dict)
    login_failed = Signal(str)
    
    def __init__(self, email: str, password: str):
        super().__init__()
        self.email = email
        self.password = password
    
    def run(self):
        """로그인 실행"""
        try:
            api_client = get_api_client()
            result = api_client.login(self.email, self.password)
            
            if result.get("status") == "success":
                # 토큰 설정
                access_token = result.get("data", {}).get("access_token")
                if access_token:
                    api_client.set_auth_token(access_token)
                
                self.login_success.emit(result)
            else:
                self.login_failed.emit(result.get("message", "로그인에 실패했습니다."))
                
        except APIError as e:
            self.login_failed.emit(str(e))
        except Exception as e:
            logger.error(f"로그인 중 오류 발생: {e}")
            self.login_failed.emit("로그인 중 오류가 발생했습니다.")


class RegisterWorker(QThread):
    """회원가입 작업을 백그라운드에서 처리하는 워커 스레드"""
    
    register_success = Signal(dict)
    register_failed = Signal(str)
    
    def __init__(self, email: str, password: str, name: str):
        super().__init__()
        self.email = email
        self.password = password
        self.name = name
    
    def run(self):
        """회원가입 실행"""
        try:
            api_client = get_api_client()
            result = api_client.register(self.email, self.password, self.name)
            
            if result.get("status") == "success":
                self.register_success.emit(result)
            else:
                self.register_failed.emit(result.get("message", "회원가입에 실패했습니다."))
                
        except APIError as e:
            self.register_failed.emit(str(e))
        except Exception as e:
            logger.error(f"회원가입 중 오류 발생: {e}")
            self.register_failed.emit("회원가입 중 오류가 발생했습니다.")


class LoginDialog(QDialog):
    """로그인 다이얼로그"""
    
    login_successful = Signal(dict)  # 로그인 성공 시그널
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CMA - 로그인")
        self.setFixedSize(400, 500)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        # UI 초기화
        self.init_ui()
        
        # 워커 스레드
        self.login_worker = None
        self.register_worker = None
    
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout()
        
        # 로고 및 제목
        title_label = QLabel("CMA 건설관리시스템")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin: 20px;")
        layout.addWidget(title_label)
        
        # 구분선
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        # 로그인 폼
        form_layout = QGridLayout()
        
        # 이메일 입력
        email_label = QLabel("이메일:")
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("이메일을 입력하세요")
        self.email_edit.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        form_layout.addWidget(email_label, 0, 0)
        form_layout.addWidget(self.email_edit, 0, 1)
        
        # 비밀번호 입력
        password_label = QLabel("비밀번호:")
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("비밀번호를 입력하세요")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        form_layout.addWidget(password_label, 1, 0)
        form_layout.addWidget(self.password_edit, 1, 1)
        
        # 자동 로그인 체크박스
        self.auto_login_checkbox = QCheckBox("자동 로그인")
        form_layout.addWidget(self.auto_login_checkbox, 2, 1)
        
        layout.addLayout(form_layout)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        
        # 로그인 버튼
        self.login_button = QPushButton("로그인")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.login_button.clicked.connect(self.login)
        button_layout.addWidget(self.login_button)
        
        # 회원가입 버튼
        self.register_button = QPushButton("회원가입")
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        self.register_button.clicked.connect(self.show_register_dialog)
        button_layout.addWidget(self.register_button)
        
        layout.addLayout(button_layout)
        
        # 상태 메시지
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #e74c3c; font-size: 12px;")
        layout.addWidget(self.status_label)
        
        # 엔터 키 이벤트 연결
        self.email_edit.returnPressed.connect(self.login)
        self.password_edit.returnPressed.connect(self.login)
        
        self.setLayout(layout)
    
    def login(self):
        """로그인 실행"""
        email = self.email_edit.text().strip()
        password = self.password_edit.text().strip()
        
        # 입력 검증
        if not email:
            self.show_error("이메일을 입력해주세요.")
            self.email_edit.setFocus()
            return
        
        if not password:
            self.show_error("비밀번호를 입력해주세요.")
            self.password_edit.setFocus()
            return
        
        # UI 상태 변경
        self.set_loading_state(True)
        self.clear_error()
        
        # 백그라운드에서 로그인 실행
        self.login_worker = LoginWorker(email, password)
        self.login_worker.login_success.connect(self.on_login_success)
        self.login_worker.login_failed.connect(self.on_login_failed)
        self.login_worker.finished.connect(self.on_worker_finished)
        self.login_worker.start()
    
    def on_login_success(self, result: Dict[str, Any]):
        """로그인 성공 처리"""
        self.login_successful.emit(result)
        self.accept()
    
    def on_login_failed(self, error_message: str):
        """로그인 실패 처리"""
        self.show_error(error_message)
        self.set_loading_state(False)
    
    def on_worker_finished(self):
        """워커 스레드 완료 처리"""
        if self.login_worker:
            self.login_worker.deleteLater()
            self.login_worker = None
    
    def show_register_dialog(self):
        """회원가입 다이얼로그 표시"""
        dialog = RegisterDialog(self)
        if dialog.exec() == QDialog.Accepted:
            # 회원가입 성공 시 이메일 자동 입력
            self.email_edit.setText(dialog.email_edit.text())
            self.password_edit.setFocus()
    
    def set_loading_state(self, loading: bool):
        """로딩 상태 설정"""
        self.login_button.setEnabled(not loading)
        self.register_button.setEnabled(not loading)
        self.email_edit.setEnabled(not loading)
        self.password_edit.setEnabled(not loading)
        
        if loading:
            self.login_button.setText("로그인 중...")
        else:
            self.login_button.setText("로그인")
    
    def show_error(self, message: str):
        """오류 메시지 표시"""
        self.status_label.setText(message)
    
    def clear_error(self):
        """오류 메시지 제거"""
        self.status_label.setText("")


class RegisterDialog(QDialog):
    """회원가입 다이얼로그"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CMA - 회원가입")
        self.setFixedSize(400, 400)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        self.init_ui()
        self.register_worker = None
    
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout()
        
        # 제목
        title_label = QLabel("회원가입")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin: 20px;")
        layout.addWidget(title_label)
        
        # 폼
        form_layout = QGridLayout()
        
        # 이름 입력
        name_label = QLabel("이름:")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("이름을 입력하세요")
        form_layout.addWidget(name_label, 0, 0)
        form_layout.addWidget(self.name_edit, 0, 1)
        
        # 이메일 입력
        email_label = QLabel("이메일:")
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("이메일을 입력하세요")
        form_layout.addWidget(email_label, 1, 0)
        form_layout.addWidget(self.email_edit, 1, 1)
        
        # 비밀번호 입력
        password_label = QLabel("비밀번호:")
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("비밀번호를 입력하세요 (6자 이상)")
        self.password_edit.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(password_label, 2, 0)
        form_layout.addWidget(self.password_edit, 2, 1)
        
        # 비밀번호 확인
        confirm_label = QLabel("비밀번호 확인:")
        self.confirm_edit = QLineEdit()
        self.confirm_edit.setPlaceholderText("비밀번호를 다시 입력하세요")
        self.confirm_edit.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(confirm_label, 3, 0)
        form_layout.addWidget(self.confirm_edit, 3, 1)
        
        layout.addLayout(form_layout)
        
        # 버튼
        button_layout = QHBoxLayout()
        
        self.register_button = QPushButton("회원가입")
        self.register_button.clicked.connect(self.register)
        button_layout.addWidget(self.register_button)
        
        self.cancel_button = QPushButton("취소")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        # 상태 메시지
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #e74c3c; font-size: 12px;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def register(self):
        """회원가입 실행"""
        name = self.name_edit.text().strip()
        email = self.email_edit.text().strip()
        password = self.password_edit.text().strip()
        confirm = self.confirm_edit.text().strip()
        
        # 입력 검증
        if not name:
            self.show_error("이름을 입력해주세요.")
            return
        
        if not email:
            self.show_error("이메일을 입력해주세요.")
            return
        
        if not password:
            self.show_error("비밀번호를 입력해주세요.")
            return
        
        if password != confirm:
            self.show_error("비밀번호가 일치하지 않습니다.")
            return
        
        if len(password) < 6:
            self.show_error("비밀번호는 6자 이상이어야 합니다.")
            return
        
        # 회원가입 실행
        self.register_worker = RegisterWorker(email, password, name)
        self.register_worker.register_success.connect(self.on_register_success)
        self.register_worker.register_failed.connect(self.on_register_failed)
        self.register_worker.start()
    
    def on_register_success(self, result: Dict[str, Any]):
        """회원가입 성공 처리"""
        QMessageBox.information(self, "회원가입 성공", "회원가입이 완료되었습니다.")
        self.accept()
    
    def on_register_failed(self, error_message: str):
        """회원가입 실패 처리"""
        self.show_error(error_message)
    
    def show_error(self, message: str):
        """오류 메시지 표시"""
        self.status_label.setText(message) 