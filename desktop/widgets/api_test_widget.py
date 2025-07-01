#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 연동 테스트 위젯
백엔드 서버와의 연결을 테스트하고 결과를 표시
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QTextEdit, QLabel, QGroupBox, QGridLayout
)
from PySide6.QtCore import QThread, Signal, Qt
import sys
import os

# API 클라이언트 임포트
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'api'))
from api.api_client import APIClient

class APIWorker(QThread):
    """API 요청을 백그라운드에서 실행하는 워커"""
    
    # 시그널 정의
    health_result = Signal(dict)
    contracts_result = Signal(dict)
    financial_result = Signal(dict)
    labor_result = Signal(dict)
    error_occurred = Signal(str)
    
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api_client = api_client
    
    def run(self):
        """API 테스트 실행"""
        try:
            # 헬스 체크
            health_result = self.api_client.health_check()
            self.health_result.emit(health_result)
            
            # 계약 목록 조회
            contracts_result = self.api_client.get_contracts()
            self.contracts_result.emit(contracts_result)
            
            # 재무 정보 조회
            financial_result = self.api_client.get_financial()
            self.financial_result.emit(financial_result)
            
            # 노무 정보 조회
            labor_result = self.api_client.get_labor()
            self.labor_result.emit(labor_result)
            
        except Exception as e:
            self.error_occurred.emit(str(e))

class APITestWidget(QWidget):
    """API 연동 테스트 위젯"""
    
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.worker = None
        self.setup_ui()
    
    def setup_ui(self):
        """UI 설정"""
        layout = QVBoxLayout(self)
        
        # 제목
        title_label = QLabel("🔗 API 연동 테스트")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        # 서버 상태 그룹
        server_group = QGroupBox("서버 상태")
        server_layout = QGridLayout(server_group)
        
        self.server_status_label = QLabel("서버 상태: 확인 중...")
        self.server_status_label.setStyleSheet("font-weight: bold;")
        server_layout.addWidget(self.server_status_label, 0, 0)
        
        self.test_button = QPushButton("연결 테스트")
        self.test_button.clicked.connect(self.run_api_test)
        server_layout.addWidget(self.test_button, 0, 1)
        
        layout.addWidget(server_group)
        
        # API 엔드포인트 테스트 그룹
        endpoints_group = QGroupBox("API 엔드포인트 테스트")
        endpoints_layout = QVBoxLayout(endpoints_group)
        
        # 결과 표시 영역
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMaximumHeight(300)
        endpoints_layout.addWidget(self.result_text)
        
        layout.addWidget(endpoints_group)
        
        # 개별 테스트 버튼들
        buttons_layout = QHBoxLayout()
        
        self.health_button = QPushButton("헬스 체크")
        self.health_button.clicked.connect(self.test_health)
        buttons_layout.addWidget(self.health_button)
        
        self.contracts_button = QPushButton("계약 목록")
        self.contracts_button.clicked.connect(self.test_contracts)
        buttons_layout.addWidget(self.contracts_button)
        
        self.financial_button = QPushButton("재무 정보")
        self.financial_button.clicked.connect(self.test_financial)
        buttons_layout.addWidget(self.financial_button)
        
        self.labor_button = QPushButton("노무 정보")
        self.labor_button.clicked.connect(self.test_labor)
        buttons_layout.addWidget(self.labor_button)
        
        layout.addLayout(buttons_layout)
        
        # 초기 연결 테스트
        self.run_api_test()
    
    def run_api_test(self):
        """전체 API 테스트 실행"""
        self.test_button.setEnabled(False)
        self.server_status_label.setText("서버 상태: 테스트 중...")
        self.result_text.clear()
        
        # 워커 스레드에서 API 테스트 실행
        self.worker = APIWorker(self.api_client)
        self.worker.health_result.connect(self.on_health_result)
        self.worker.contracts_result.connect(self.on_contracts_result)
        self.worker.financial_result.connect(self.on_financial_result)
        self.worker.labor_result.connect(self.on_labor_result)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.finished.connect(self.on_test_finished)
        self.worker.start()
    
    def test_health(self):
        """헬스 체크만 실행"""
        result = self.api_client.health_check()
        self.display_result("헬스 체크", result)
    
    def test_contracts(self):
        """계약 목록 조회만 실행"""
        result = self.api_client.get_contracts()
        self.display_result("계약 목록 조회", result)
    
    def test_financial(self):
        """재무 정보 조회만 실행"""
        result = self.api_client.get_financial()
        self.display_result("재무 정보 조회", result)
    
    def test_labor(self):
        """노무 정보 조회만 실행"""
        result = self.api_client.get_labor()
        self.display_result("노무 정보 조회", result)
    
    def on_health_result(self, result):
        """헬스 체크 결과 처리"""
        if result.get('status') == 'healthy':
            self.server_status_label.setText("서버 상태: ✅ 연결됨")
            self.server_status_label.setStyleSheet("font-weight: bold; color: green;")
        else:
            self.server_status_label.setText("서버 상태: ❌ 연결 실패")
            self.server_status_label.setStyleSheet("font-weight: bold; color: red;")
        
        self.display_result("헬스 체크", result)
    
    def on_contracts_result(self, result):
        """계약 목록 결과 처리"""
        self.display_result("계약 목록 조회", result)
    
    def on_financial_result(self, result):
        """재무 정보 결과 처리"""
        self.display_result("재무 정보 조회", result)
    
    def on_labor_result(self, result):
        """노무 정보 결과 처리"""
        self.display_result("노무 정보 조회", result)
    
    def on_error(self, error_message):
        """오류 처리"""
        self.server_status_label.setText("서버 상태: ❌ 오류 발생")
        self.server_status_label.setStyleSheet("font-weight: bold; color: red;")
        self.display_result("오류", {"error": error_message})
    
    def on_test_finished(self):
        """테스트 완료 처리"""
        self.test_button.setEnabled(True)
    
    def display_result(self, title: str, result: dict):
        """결과 표시"""
        import json
        
        current_text = self.result_text.toPlainText()
        formatted_result = json.dumps(result, indent=2, ensure_ascii=False)
        
        new_text = f"=== {title} ===\n{formatted_result}\n\n{current_text}"
        self.result_text.setPlainText(new_text) 