#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 설정 탭 컴포넌트
"""

import logging
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton, QLineEdit, QComboBox,
    QSpinBox, QCheckBox, QTextEdit, QFormLayout,
    QGroupBox, QTabWidget, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QFont, QColor
from typing import Dict, Any, List, Optional
import json
import os

logger = logging.getLogger(__name__)


class SettingsTab(QWidget):
    """설정 탭 클래스"""
    
    def __init__(self):
        super().__init__()
        self.settings = QSettings("CMA", "ConstructionManagementSystem")
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 제목
        title = QLabel("설정")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # 설정 탭 위젯
        self.settings_tabs = QTabWidget()
        self.settings_tabs.setStyleSheet("""
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
        
        # 일반 설정 탭
        self.setup_general_tab()
        
        # 데이터베이스 설정 탭
        self.setup_database_tab()
        
        # API 설정 탭
        self.setup_api_tab()
        
        # 백업 설정 탭
        self.setup_backup_tab()
        
        layout.addWidget(self.settings_tabs)
        
        # 버튼 영역
        self.setup_button_area(layout)
    
    def setup_general_tab(self):
        """일반 설정 탭"""
        general_widget = QWidget()
        general_layout = QVBoxLayout(general_widget)
        general_layout.setSpacing(20)
        
        # 애플리케이션 설정
        app_group = QGroupBox("애플리케이션 설정")
        app_layout = QFormLayout(app_group)
        
        # 언어 설정
        self.language_combo = QComboBox()
        self.language_combo.addItems(["한국어", "English", "日本語"])
        app_layout.addRow("언어:", self.language_combo)
        
        # 테마 설정
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["라이트", "다크", "시스템"])
        app_layout.addRow("테마:", self.theme_combo)
        
        # 자동 저장
        self.auto_save_check = QCheckBox("자동 저장 사용")
        app_layout.addRow("", self.auto_save_check)
        
        # 자동 저장 간격
        self.auto_save_interval = QSpinBox()
        self.auto_save_interval.setRange(1, 60)
        self.auto_save_interval.setSuffix(" 분")
        app_layout.addRow("자동 저장 간격:", self.auto_save_interval)
        
        general_layout.addWidget(app_group)
        
        # 알림 설정
        notification_group = QGroupBox("알림 설정")
        notification_layout = QFormLayout(notification_group)
        
        # 이메일 알림
        self.email_notification_check = QCheckBox("이메일 알림 사용")
        notification_layout.addRow("", self.email_notification_check)
        
        # 푸시 알림
        self.push_notification_check = QCheckBox("푸시 알림 사용")
        notification_layout.addRow("", self.push_notification_check)
        
        # 알림 소리
        self.notification_sound_check = QCheckBox("알림 소리 사용")
        notification_layout.addRow("", self.notification_sound_check)
        
        general_layout.addWidget(notification_group)
        
        general_layout.addStretch()
        self.settings_tabs.addTab(general_widget, "일반")
    
    def setup_database_tab(self):
        """데이터베이스 설정 탭"""
        db_widget = QWidget()
        db_layout = QVBoxLayout(db_widget)
        db_layout.setSpacing(20)
        
        # 데이터베이스 연결 설정
        connection_group = QGroupBox("데이터베이스 연결")
        connection_layout = QFormLayout(connection_group)
        
        # 데이터베이스 타입
        self.db_type_combo = QComboBox()
        self.db_type_combo.addItems(["PostgreSQL", "MySQL", "SQLite"])
        connection_layout.addRow("데이터베이스 타입:", self.db_type_combo)
        
        # 호스트
        self.db_host_input = QLineEdit()
        self.db_host_input.setPlaceholderText("localhost")
        connection_layout.addRow("호스트:", self.db_host_input)
        
        # 포트
        self.db_port_input = QSpinBox()
        self.db_port_input.setRange(1, 65535)
        self.db_port_input.setValue(5432)
        connection_layout.addRow("포트:", self.db_port_input)
        
        # 데이터베이스명
        self.db_name_input = QLineEdit()
        self.db_name_input.setPlaceholderText("cma_db")
        connection_layout.addRow("데이터베이스명:", self.db_name_input)
        
        # 사용자명
        self.db_user_input = QLineEdit()
        self.db_user_input.setPlaceholderText("사용자명")
        connection_layout.addRow("사용자명:", self.db_user_input)
        
        # 비밀번호
        self.db_password_input = QLineEdit()
        self.db_password_input.setEchoMode(QLineEdit.Password)
        self.db_password_input.setPlaceholderText("비밀번호")
        connection_layout.addRow("비밀번호:", self.db_password_input)
        
        db_layout.addWidget(connection_group)
        
        # 연결 테스트 버튼
        test_button = QPushButton("연결 테스트")
        test_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        test_button.clicked.connect(self.test_database_connection)
        db_layout.addWidget(test_button)
        
        db_layout.addStretch()
        self.settings_tabs.addTab(db_widget, "데이터베이스")
    
    def setup_api_tab(self):
        """API 설정 탭"""
        api_widget = QWidget()
        api_layout = QVBoxLayout(api_widget)
        api_layout.setSpacing(20)
        
        # API 서버 설정
        server_group = QGroupBox("API 서버 설정")
        server_layout = QFormLayout(server_group)
        
        # API 서버 URL
        self.api_url_input = QLineEdit()
        self.api_url_input.setPlaceholderText("http://localhost:8000")
        server_layout.addRow("API 서버 URL:", self.api_url_input)
        
        # API 버전
        self.api_version_input = QLineEdit()
        self.api_version_input.setPlaceholderText("v1")
        server_layout.addRow("API 버전:", self.api_version_input)
        
        # 타임아웃 설정
        self.api_timeout_input = QSpinBox()
        self.api_timeout_input.setRange(5, 300)
        self.api_timeout_input.setValue(30)
        self.api_timeout_input.setSuffix(" 초")
        server_layout.addRow("타임아웃:", self.api_timeout_input)
        
        api_layout.addWidget(server_group)
        
        # 인증 설정
        auth_group = QGroupBox("인증 설정")
        auth_layout = QFormLayout(auth_group)
        
        # 자동 로그인
        self.auto_login_check = QCheckBox("자동 로그인 사용")
        auth_layout.addRow("", self.auto_login_check)
        
        # 토큰 만료 알림
        self.token_expiry_check = QCheckBox("토큰 만료 알림")
        auth_layout.addRow("", self.token_expiry_check)
        
        api_layout.addWidget(auth_group)
        
        # 연결 테스트 버튼
        test_api_button = QPushButton("API 연결 테스트")
        test_api_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        test_api_button.clicked.connect(self.test_api_connection)
        api_layout.addWidget(test_api_button)
        
        api_layout.addStretch()
        self.settings_tabs.addTab(api_widget, "API")
    
    def setup_backup_tab(self):
        """백업 설정 탭"""
        backup_widget = QWidget()
        backup_layout = QVBoxLayout(backup_widget)
        backup_layout.setSpacing(20)
        
        # 백업 설정
        backup_group = QGroupBox("백업 설정")
        backup_layout_form = QFormLayout(backup_group)
        
        # 자동 백업
        self.auto_backup_check = QCheckBox("자동 백업 사용")
        backup_layout_form.addRow("", self.auto_backup_check)
        
        # 백업 주기
        self.backup_interval_combo = QComboBox()
        self.backup_interval_combo.addItems(["매일", "매주", "매월"])
        backup_layout_form.addRow("백업 주기:", self.backup_interval_combo)
        
        # 백업 경로
        backup_path_layout = QHBoxLayout()
        self.backup_path_input = QLineEdit()
        self.backup_path_input.setPlaceholderText("백업 파일 저장 경로")
        backup_path_layout.addWidget(self.backup_path_input)
        
        browse_button = QPushButton("찾아보기")
        browse_button.clicked.connect(self.browse_backup_path)
        backup_path_layout.addWidget(browse_button)
        
        backup_layout_form.addRow("백업 경로:", backup_path_layout)
        
        # 백업 보관 기간
        self.backup_retention_input = QSpinBox()
        self.backup_retention_input.setRange(1, 365)
        self.backup_retention_input.setValue(30)
        self.backup_retention_input.setSuffix(" 일")
        backup_layout_form.addRow("백업 보관 기간:", self.backup_retention_input)
        
        backup_layout.addWidget(backup_group)
        
        # 백업 버튼
        backup_button_layout = QHBoxLayout()
        
        manual_backup_button = QPushButton("수동 백업")
        manual_backup_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        manual_backup_button.clicked.connect(self.manual_backup)
        backup_button_layout.addWidget(manual_backup_button)
        
        restore_button = QPushButton("복원")
        restore_button.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)
        restore_button.clicked.connect(self.restore_backup)
        backup_button_layout.addWidget(restore_button)
        
        backup_layout.addLayout(backup_button_layout)
        backup_layout.addStretch()
        self.settings_tabs.addTab(backup_widget, "백업")
    
    def setup_button_area(self, layout):
        """버튼 영역 설정"""
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 기본값으로 복원 버튼
        reset_button = QPushButton("기본값으로 복원")
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        reset_button.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(reset_button)
        
        # 저장 버튼
        save_button = QPushButton("저장")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
    
    def load_settings(self):
        """설정 로드"""
        try:
            # 일반 설정
            language = self.settings.value("general/language", "한국어")
            index = self.language_combo.findText(language)
            if index >= 0:
                self.language_combo.setCurrentIndex(index)
            
            theme = self.settings.value("general/theme", "라이트")
            index = self.theme_combo.findText(theme)
            if index >= 0:
                self.theme_combo.setCurrentIndex(index)
            
            self.auto_save_check.setChecked(self.settings.value("general/auto_save", True, type=bool))
            self.auto_save_interval.setValue(self.settings.value("general/auto_save_interval", 5, type=int))
            
            # 알림 설정
            self.email_notification_check.setChecked(self.settings.value("notifications/email", False, type=bool))
            self.push_notification_check.setChecked(self.settings.value("notifications/push", True, type=bool))
            self.notification_sound_check.setChecked(self.settings.value("notifications/sound", True, type=bool))
            
            # 데이터베이스 설정
            db_type = self.settings.value("database/type", "PostgreSQL")
            index = self.db_type_combo.findText(db_type)
            if index >= 0:
                self.db_type_combo.setCurrentIndex(index)
            
            self.db_host_input.setText(self.settings.value("database/host", "localhost"))
            self.db_port_input.setValue(self.settings.value("database/port", 5432, type=int))
            self.db_name_input.setText(self.settings.value("database/name", "cma_db"))
            self.db_user_input.setText(self.settings.value("database/user", ""))
            self.db_password_input.setText(self.settings.value("database/password", ""))
            
            # API 설정
            self.api_url_input.setText(self.settings.value("api/url", "http://localhost:8000"))
            self.api_version_input.setText(self.settings.value("api/version", "v1"))
            self.api_timeout_input.setValue(self.settings.value("api/timeout", 30, type=int))
            
            self.auto_login_check.setChecked(self.settings.value("api/auto_login", True, type=bool))
            self.token_expiry_check.setChecked(self.settings.value("api/token_expiry_notification", True, type=bool))
            
            # 백업 설정
            self.auto_backup_check.setChecked(self.settings.value("backup/auto_backup", True, type=bool))
            
            backup_interval = self.settings.value("backup/interval", "매일")
            index = self.backup_interval_combo.findText(backup_interval)
            if index >= 0:
                self.backup_interval_combo.setCurrentIndex(index)
            
            self.backup_path_input.setText(self.settings.value("backup/path", ""))
            self.backup_retention_input.setValue(self.settings.value("backup/retention", 30, type=int))
            
        except Exception as e:
            logger.error(f"설정 로드 실패: {e}")
            QMessageBox.warning(self, "오류", "설정을 로드하는 중 오류가 발생했습니다.")
    
    def save_settings(self):
        """설정 저장"""
        try:
            # 일반 설정
            self.settings.setValue("general/language", self.language_combo.currentText())
            self.settings.setValue("general/theme", self.theme_combo.currentText())
            self.settings.setValue("general/auto_save", self.auto_save_check.isChecked())
            self.settings.setValue("general/auto_save_interval", self.auto_save_interval.value())
            
            # 알림 설정
            self.settings.setValue("notifications/email", self.email_notification_check.isChecked())
            self.settings.setValue("notifications/push", self.push_notification_check.isChecked())
            self.settings.setValue("notifications/sound", self.notification_sound_check.isChecked())
            
            # 데이터베이스 설정
            self.settings.setValue("database/type", self.db_type_combo.currentText())
            self.settings.setValue("database/host", self.db_host_input.text())
            self.settings.setValue("database/port", self.db_port_input.value())
            self.settings.setValue("database/name", self.db_name_input.text())
            self.settings.setValue("database/user", self.db_user_input.text())
            self.settings.setValue("database/password", self.db_password_input.text())
            
            # API 설정
            self.settings.setValue("api/url", self.api_url_input.text())
            self.settings.setValue("api/version", self.api_version_input.text())
            self.settings.setValue("api/timeout", self.api_timeout_input.value())
            self.settings.setValue("api/auto_login", self.auto_login_check.isChecked())
            self.settings.setValue("api/token_expiry_notification", self.token_expiry_check.isChecked())
            
            # 백업 설정
            self.settings.setValue("backup/auto_backup", self.auto_backup_check.isChecked())
            self.settings.setValue("backup/interval", self.backup_interval_combo.currentText())
            self.settings.setValue("backup/path", self.backup_path_input.text())
            self.settings.setValue("backup/retention", self.backup_retention_input.value())
            
            self.settings.sync()
            QMessageBox.information(self, "성공", "설정이 성공적으로 저장되었습니다.")
            
        except Exception as e:
            logger.error(f"설정 저장 실패: {e}")
            QMessageBox.warning(self, "오류", "설정을 저장하는 중 오류가 발생했습니다.")
    
    def reset_to_defaults(self):
        """기본값으로 복원"""
        reply = QMessageBox.question(
            self, "확인", 
            "모든 설정을 기본값으로 복원하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.settings.clear()
            self.load_settings()
            QMessageBox.information(self, "완료", "설정이 기본값으로 복원되었습니다.")
    
    def test_database_connection(self):
        """데이터베이스 연결 테스트"""
        QMessageBox.information(self, "알림", "데이터베이스 연결 테스트 기능은 추후 구현 예정입니다.")
    
    def test_api_connection(self):
        """API 연결 테스트"""
        QMessageBox.information(self, "알림", "API 연결 테스트 기능은 추후 구현 예정입니다.")
    
    def browse_backup_path(self):
        """백업 경로 찾아보기"""
        path = QFileDialog.getExistingDirectory(self, "백업 경로 선택")
        if path:
            self.backup_path_input.setText(path)
    
    def manual_backup(self):
        """수동 백업"""
        QMessageBox.information(self, "알림", "수동 백업 기능은 추후 구현 예정입니다.")
    
    def restore_backup(self):
        """백업 복원"""
        QMessageBox.information(self, "알림", "백업 복원 기능은 추후 구현 예정입니다.") 