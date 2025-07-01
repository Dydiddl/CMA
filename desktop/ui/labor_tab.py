#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 노무 관리 탭 컴포넌트
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton, QLineEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QDateEdit, QSpinBox, QDoubleSpinBox, QTextEdit, QFormLayout,
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout
)
from PySide6.QtCore import Qt, QDate, QThread, Signal
from PySide6.QtGui import QFont, QColor
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from api.client import get_api_client, APIError

logger = logging.getLogger(__name__)


class LaborDataWorker(QThread):
    """노무 데이터를 백그라운드에서 로드하는 워커 스레드"""
    
    data_loaded = Signal(dict)
    data_failed = Signal(str)
    
    def __init__(self, search: str = None, worker_id: str = None, skip: int = 0, limit: int = 50):
        super().__init__()
        self.search = search
        self.worker_id = worker_id
        self.skip = skip
        self.limit = limit
    
    def run(self):
        """데이터 로드 실행"""
        try:
            api_client = get_api_client()
            
            # API 파라미터 준비
            params = {"skip": self.skip, "limit": self.limit}
            if self.search:
                params["search"] = self.search
            if self.worker_id:
                params["worker_id"] = self.worker_id
            
            # 노무 데이터 로드
            result = api_client.get_labor_records(**params)
            
            if result.get("status") == "success":
                self.data_loaded.emit(result.get("data", {}))
            else:
                self.data_failed.emit(result.get("message", "노무 데이터 로드에 실패했습니다."))
                
        except APIError as e:
            self.data_failed.emit(str(e))
        except Exception as e:
            logger.error(f"노무 데이터 로드 중 오류: {e}")
            self.data_failed.emit("노무 데이터 로드 중 오류가 발생했습니다.")


class LaborSummaryWorker(QThread):
    """노무 요약 데이터를 백그라운드에서 로드하는 워커 스레드"""
    
    summary_loaded = Signal(dict)
    summary_failed = Signal(str)
    
    def run(self):
        """요약 데이터 로드 실행"""
        try:
            api_client = get_api_client()
            result = api_client.get_labor_summary()
            
            if result.get("status") == "success":
                self.summary_loaded.emit(result.get("data", {}))
            else:
                self.summary_failed.emit(result.get("message", "노무 요약 데이터 로드에 실패했습니다."))
                
        except APIError as e:
            self.summary_failed.emit(str(e))
        except Exception as e:
            logger.error(f"노무 요약 데이터 로드 중 오류: {e}")
            self.summary_failed.emit("노무 요약 데이터 로드 중 오류가 발생했습니다.")


class LaborSaveWorker(QThread):
    """노무 기록 저장을 백그라운드에서 처리하는 워커 스레드"""
    
    save_success = Signal(dict)
    save_failed = Signal(str)
    
    def __init__(self, labor_data: Dict[str, Any], is_update: bool = False, record_id: str = None):
        super().__init__()
        self.labor_data = labor_data
        self.is_update = is_update
        self.record_id = record_id
    
    def run(self):
        """노무 기록 저장 실행"""
        try:
            api_client = get_api_client()
            
            if self.is_update and self.record_id:
                result = api_client.update_labor_record(self.record_id, self.labor_data)
            else:
                result = api_client.create_labor_record(self.labor_data)
            
            if result.get("status") == "success":
                self.save_success.emit(result.get("data", {}))
            else:
                self.save_failed.emit(result.get("message", "노무 기록 저장에 실패했습니다."))
                
        except APIError as e:
            self.save_failed.emit(str(e))
        except Exception as e:
            logger.error(f"노무 기록 저장 중 오류: {e}")
            self.save_failed.emit("노무 기록 저장 중 오류가 발생했습니다.")


class LaborDeleteWorker(QThread):
    """노무 기록 삭제를 백그라운드에서 처리하는 워커 스레드"""
    
    delete_success = Signal()
    delete_failed = Signal(str)
    
    def __init__(self, record_id: str):
        super().__init__()
        self.record_id = record_id
    
    def run(self):
        """노무 기록 삭제 실행"""
        try:
            api_client = get_api_client()
            result = api_client.delete_labor_record(self.record_id)
            
            if result.get("status") == "success":
                self.delete_success.emit()
            else:
                self.delete_failed.emit(result.get("message", "노무 기록 삭제에 실패했습니다."))
                
        except APIError as e:
            self.delete_failed.emit(str(e))
        except Exception as e:
            logger.error(f"노무 기록 삭제 중 오류: {e}")
            self.delete_failed.emit("노무 기록 삭제 중 오류가 발생했습니다.")


class WorkersDataWorker(QThread):
    """근로자 목록을 백그라운드에서 로드하는 워커 스레드"""
    
    workers_loaded = Signal(dict)
    workers_failed = Signal(str)
    
    def __init__(self, search: str = None, skip: int = 0, limit: int = 100):
        super().__init__()
        self.search = search
        self.skip = skip
        self.limit = limit
    
    def run(self):
        """근로자 데이터 로드 실행"""
        try:
            api_client = get_api_client()
            
            # API 파라미터 준비
            params = {"skip": self.skip, "limit": self.limit}
            if self.search:
                params["search"] = self.search
            
            # 근로자 데이터 로드
            result = api_client.get_workers(**params)
            
            if result.get("status") == "success":
                self.workers_loaded.emit(result.get("data", {}))
            else:
                self.workers_failed.emit(result.get("message", "근로자 데이터 로드에 실패했습니다."))
                
        except APIError as e:
            self.workers_failed.emit(str(e))
        except Exception as e:
            logger.error(f"근로자 데이터 로드 중 오류: {e}")
            self.workers_failed.emit("근로자 데이터 로드 중 오류가 발생했습니다.")


class LaborTab(QWidget):
    """노무 관리 탭 클래스"""
    
    def __init__(self):
        super().__init__()
        self.api_client = get_api_client()
        self.labor_data = []
        self.workers_data = []
        self.current_page = 0
        self.page_size = 50
        
        # 워커 스레드
        self.data_worker = None
        self.summary_worker = None
        self.save_worker = None
        self.delete_worker = None
        self.workers_worker = None
        
        self.init_ui()
        self.load_labor_data()
        self.load_summary_data()
        self.load_workers_data()
    
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 제목
        title = QLabel("노무 관리")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # 노무 요약 카드
        self.setup_summary_cards(layout)
        
        # 검색 및 필터 영역
        self.setup_search_area(layout)
        
        # 버튼 영역
        self.setup_button_area(layout)
        
        # 노무 데이터 테이블
        self.setup_labor_table(layout)
        
        # 페이지네이션
        self.setup_pagination(layout)
    
    def setup_summary_cards(self, layout):
        """노무 요약 카드 설정"""
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(15)
        
        # 총 인력 수 카드
        self.total_card = self.create_summary_card(
            "총 인력 수", "0", "명", "#3498db",
            "현재 투입: 0명", "가동률 0%"
        )
        summary_layout.addWidget(self.total_card)
        
        # 총 인건비 카드
        self.cost_card = self.create_summary_card(
            "총 인건비", "0", "원", "#e74c3c",
            "이번 달: 0원", "0%"
        )
        summary_layout.addWidget(self.cost_card)
        
        # 평균 임금 카드
        self.avg_wage_card = self.create_summary_card(
            "평균 임금", "0", "원", "#27ae60",
            "월 평균", "0%"
        )
        summary_layout.addWidget(self.avg_wage_card)
        
        # 근무 시간 카드
        self.hours_card = self.create_summary_card(
            "총 근무시간", "0", "시간", "#f39c12",
            "이번 주: 0시간", "목표 대비 0%"
        )
        summary_layout.addWidget(self.hours_card)
        
        layout.addLayout(summary_layout)
    
    def create_summary_card(self, title, value, unit, color, subtitle, trend):
        """요약 카드 생성"""
        card = QFrame()
        card.setFrameStyle(QFrame.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
            }}
            QFrame:hover {{
                border-color: {color};
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(8)
        
        # 제목
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #6c757d; font-size: 14px; font-weight: bold;")
        card_layout.addWidget(title_label)
        
        # 값
        value_layout = QHBoxLayout()
        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
        value_label.setObjectName("value_label")
        value_layout.addWidget(value_label)
        
        unit_label = QLabel(unit)
        unit_label.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold;")
        unit_label.setObjectName("unit_label")
        value_layout.addWidget(unit_label)
        value_layout.addStretch()
        
        card_layout.addLayout(value_layout)
        
        # 부제목
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("color: #495057; font-size: 12px;")
        subtitle_label.setObjectName("subtitle_label")
        card_layout.addWidget(subtitle_label)
        
        # 트렌드
        trend_label = QLabel(trend)
        trend_label.setObjectName("trend_label")
        if "+" in trend or "95%" in trend or "0%" not in trend:
            trend_label.setStyleSheet("color: #27ae60; font-size: 12px; font-weight: bold;")
        else:
            trend_label.setStyleSheet("color: #e74c3c; font-size: 12px; font-weight: bold;")
        card_layout.addWidget(trend_label)
        
        return card
    
    def update_summary_card(self, card, value, subtitle, trend):
        """요약 카드 업데이트"""
        value_label = card.findChild(QLabel, "value_label")
        subtitle_label = card.findChild(QLabel, "subtitle_label")
        trend_label = card.findChild(QLabel, "trend_label")
        
        if value_label:
            value_label.setText(str(value))
        if subtitle_label:
            subtitle_label.setText(subtitle)
        if trend_label:
            trend_label.setText(trend)
            if "+" in trend or "95%" in trend or "0%" not in trend:
                trend_label.setStyleSheet("color: #27ae60; font-size: 12px; font-weight: bold;")
            else:
                trend_label.setStyleSheet("color: #e74c3c; font-size: 12px; font-weight: bold;")
    
    def setup_search_area(self, layout):
        """검색 영역 설정"""
        search_frame = QFrame()
        search_frame.setFrameStyle(QFrame.StyledPanel)
        search_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        search_layout = QHBoxLayout(search_frame)
        search_layout.setSpacing(15)
        
        # 검색어 입력
        search_label = QLabel("검색:")
        search_label.setStyleSheet("font-weight: bold; color: #495057;")
        search_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("이름, 직종, 프로젝트로 검색...")
        self.search_input.setMinimumWidth(300)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #007bff;
            }
        """)
        self.search_input.returnPressed.connect(self.search_labor_data)
        search_layout.addWidget(self.search_input)
        
        # 직종 필터
        job_label = QLabel("직종:")
        job_label.setStyleSheet("font-weight: bold; color: #495057;")
        search_layout.addWidget(job_label)
        
        self.job_filter = QComboBox()
        self.job_filter.addItems(["전체", "기술자", "일반노무자", "관리자", "안전관리자"])
        self.job_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
                min-width: 120px;
            }
        """)
        self.job_filter.currentTextChanged.connect(self.on_filter_changed)
        search_layout.addWidget(self.job_filter)
        
        # 검색 버튼
        search_button = QPushButton("검색")
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        search_button.clicked.connect(self.search_labor_data)
        search_layout.addWidget(search_button)
        
        # 새로고침 버튼
        refresh_button = QPushButton("새로고침")
        refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)
        refresh_button.clicked.connect(self.load_labor_data)
        search_layout.addWidget(refresh_button)
        
        search_layout.addStretch()
        layout.addWidget(search_frame)
    
    def setup_button_area(self, layout):
        """버튼 영역 설정"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # 새 노무자 등록 버튼
        add_button = QPushButton("새 노무자 등록")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        add_button.clicked.connect(self.add_new_labor)
        button_layout.addWidget(add_button)
        
        # 노무자 수정 버튼
        edit_button = QPushButton("노무자 수정")
        edit_button.setStyleSheet("""
            QPushButton {
                background-color: #ffc107;
                color: #212529;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)
        edit_button.clicked.connect(self.edit_labor)
        button_layout.addWidget(edit_button)
        
        # 노무자 삭제 버튼
        delete_button = QPushButton("노무자 삭제")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        delete_button.clicked.connect(self.delete_labor)
        button_layout.addWidget(delete_button)
        
        button_layout.addStretch()
        
        # 근무시간 관리 버튼
        hours_button = QPushButton("근무시간 관리")
        hours_button.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        hours_button.clicked.connect(self.manage_work_hours)
        button_layout.addWidget(hours_button)
        
        # 임금 계산 버튼
        salary_button = QPushButton("임금 계산")
        salary_button.setStyleSheet("""
            QPushButton {
                background-color: #6f42c1;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a32a3;
            }
        """)
        salary_button.clicked.connect(self.calculate_salary)
        button_layout.addWidget(salary_button)
        
        # 내보내기 버튼
        export_button = QPushButton("Excel 내보내기")
        export_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)
        export_button.clicked.connect(self.export_labor_data)
        button_layout.addWidget(export_button)
        
        layout.addLayout(button_layout)
    
    def setup_labor_table(self, layout):
        """노무 데이터 테이블 설정"""
        self.labor_table = QTableWidget()
        self.labor_table.setColumnCount(8)
        self.labor_table.setHorizontalHeaderLabels([
            "이름", "직종", "연락처", "입사일", "시급", "근무시간", "프로젝트", "상태"
        ])
        
        # 테이블 스타일 설정
        self.labor_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
                gridline-color: #dee2e6;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 10px;
                border: none;
                border-bottom: 1px solid #dee2e6;
                font-weight: bold;
                color: #495057;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f8f9fa;
            }
            QTableWidget::item:selected {
                background-color: #007bff;
                color: white;
            }
        """)
        
        # 컬럼 너비 설정
        header = self.labor_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 이름
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 직종
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # 연락처
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # 입사일
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # 시급
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # 근무시간
        header.setSectionResizeMode(6, QHeaderView.Stretch)           # 프로젝트
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # 상태
        
        # 더블클릭 이벤트 연결
        self.labor_table.itemDoubleClicked.connect(self.on_labor_double_clicked)
        
        layout.addWidget(self.labor_table)
    
    def setup_pagination(self, layout):
        """페이지네이션 설정"""
        pagination_layout = QHBoxLayout()
        pagination_layout.addStretch()
        
        # 이전 페이지 버튼
        self.prev_button = QPushButton("이전")
        self.prev_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
            QPushButton:disabled {
                background-color: #adb5bd;
            }
        """)
        self.prev_button.clicked.connect(self.previous_page)
        pagination_layout.addWidget(self.prev_button)
        
        # 페이지 정보
        self.page_info = QLabel("페이지 1")
        self.page_info.setStyleSheet("color: #495057; font-size: 12px; margin: 0 10px;")
        pagination_layout.addWidget(self.page_info)
        
        # 다음 페이지 버튼
        self.next_button = QPushButton("다음")
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
            QPushButton:disabled {
                background-color: #adb5bd;
            }
        """)
        self.next_button.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.next_button)
        
        layout.addLayout(pagination_layout)
    
    def load_labor_data(self):
        """노무 데이터 로드"""
        if self.data_worker and self.data_worker.isRunning():
            return
        
        self.data_worker = LaborDataWorker(
            search=self.search_input.text().strip() or None,
            skip=self.current_page * self.page_size,
            limit=self.page_size
        )
        self.data_worker.data_loaded.connect(self.on_data_loaded)
        self.data_worker.data_failed.connect(self.on_data_failed)
        self.data_worker.finished.connect(self.on_worker_finished)
        self.data_worker.start()
    
    def load_summary_data(self):
        """노무 요약 데이터 로드"""
        if self.summary_worker and self.summary_worker.isRunning():
            return
        
        self.summary_worker = LaborSummaryWorker()
        self.summary_worker.summary_loaded.connect(self.on_summary_loaded)
        self.summary_worker.summary_failed.connect(self.on_summary_failed)
        self.summary_worker.finished.connect(self.on_summary_worker_finished)
        self.summary_worker.start()
    
    def load_workers_data(self):
        """근로자 목록 데이터 로드"""
        if self.workers_worker and self.workers_worker.isRunning():
            return
        
        self.workers_worker = WorkersDataWorker()
        self.workers_worker.workers_loaded.connect(self.on_workers_loaded)
        self.workers_worker.workers_failed.connect(self.on_workers_failed)
        self.workers_worker.finished.connect(self.on_workers_worker_finished)
        self.workers_worker.start()
    
    def on_data_loaded(self, data: Dict[str, Any]):
        """데이터 로드 성공 처리"""
        self.labor_data = data.get("records", [])
        total = data.get("total", 0)
        
        self.update_labor_table()
        self.update_pagination(total)
    
    def on_data_failed(self, error_message: str):
        """데이터 로드 실패 처리"""
        QMessageBox.warning(self, "데이터 로드 실패", error_message)
    
    def on_worker_finished(self):
        """워커 스레드 완료 처리"""
        if self.data_worker:
            self.data_worker.deleteLater()
            self.data_worker = None
    
    def on_summary_loaded(self, summary: Dict[str, Any]):
        """요약 데이터 로드 성공 처리"""
        # 총 인력 수
        total_workers = summary.get("total_workers", 0)
        active_workers = summary.get("active_workers", 0)
        utilization_rate = summary.get("utilization_rate", 0)
        
        self.update_summary_card(
            self.total_card,
            total_workers,
            f"현재 투입: {active_workers}명",
            f"가동률 {utilization_rate}%"
        )
        
        # 총 인건비
        total_labor_cost = summary.get("total_labor_cost", 0)
        monthly_labor_cost = summary.get("monthly_labor_cost", 0)
        labor_cost_trend = summary.get("labor_cost_trend", "0%")
        
        self.update_summary_card(
            self.cost_card,
            f"{total_labor_cost:,}",
            f"이번 달: {monthly_labor_cost:,}원",
            f"{labor_cost_trend}"
        )
        
        # 평균 임금
        avg_wage = summary.get("average_wage", 0)
        wage_trend = summary.get("wage_trend", "0%")
        
        self.update_summary_card(
            self.avg_wage_card,
            f"{avg_wage:,}",
            "월 평균",
            f"{wage_trend}"
        )
        
        # 총 근무시간
        total_hours = summary.get("total_hours", 0)
        weekly_hours = summary.get("weekly_hours", 0)
        hours_target = summary.get("hours_target", 0)
        
        self.update_summary_card(
            self.hours_card,
            f"{total_hours:,}",
            f"이번 주: {weekly_hours}시간",
            f"목표 대비 {hours_target}%"
        )
    
    def on_summary_failed(self, error_message: str):
        """요약 데이터 로드 실패 처리"""
        logger.warning(f"노무 요약 데이터 로드 실패: {error_message}")
    
    def on_summary_worker_finished(self):
        """요약 워커 스레드 완료 처리"""
        if self.summary_worker:
            self.summary_worker.deleteLater()
            self.summary_worker = None
    
    def on_workers_loaded(self, data: Dict[str, Any]):
        """근로자 데이터 로드 성공 처리"""
        self.workers_data = data.get("workers", [])
    
    def on_workers_failed(self, error_message: str):
        """근로자 데이터 로드 실패 처리"""
        logger.warning(f"근로자 데이터 로드 실패: {error_message}")
    
    def on_workers_worker_finished(self):
        """근로자 워커 스레드 완료 처리"""
        if self.workers_worker:
            self.workers_worker.deleteLater()
            self.workers_worker = None
    
    def update_labor_table(self):
        """노무 테이블 업데이트"""
        self.labor_table.setRowCount(len(self.labor_data))
        
        for row, record in enumerate(self.labor_data):
            # 이름
            self.labor_table.setItem(row, 0, QTableWidgetItem(record.get("worker_name", "")))
            
            # 직종
            job_type = record.get("job_type", "")
            job_item = QTableWidgetItem(job_type)
            
            # 직종별 색상 설정
            if job_type == "기술자":
                job_item.setBackground(QColor("#d4edda"))
                job_item.setForeground(QColor("#155724"))
            elif job_type == "일반노무자":
                job_item.setBackground(QColor("#cce5ff"))
                job_item.setForeground(QColor("#004085"))
            elif job_type == "관리자":
                job_item.setBackground(QColor("#fff3cd"))
                job_item.setForeground(QColor("#856404"))
            elif job_type == "안전관리자":
                job_item.setBackground(QColor("#f8d7da"))
                job_item.setForeground(QColor("#721c24"))
            
            self.labor_table.setItem(row, 1, job_item)
            
            # 연락처
            self.labor_table.setItem(row, 2, QTableWidgetItem(record.get("contact", "")))
            
            # 입사일
            hire_date = record.get("hire_date", "")
            if hire_date:
                try:
                    date_obj = datetime.fromisoformat(hire_date.replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime("%Y-%m-%d")
                except:
                    formatted_date = hire_date
            else:
                formatted_date = ""
            self.labor_table.setItem(row, 3, QTableWidgetItem(formatted_date))
            
            # 시급
            hourly_wage = record.get("hourly_wage", 0)
            self.labor_table.setItem(row, 4, QTableWidgetItem(f"{hourly_wage:,}원"))
            
            # 근무시간
            work_hours = record.get("work_hours", 0)
            self.labor_table.setItem(row, 5, QTableWidgetItem(f"{work_hours}시간"))
            
            # 프로젝트
            self.labor_table.setItem(row, 6, QTableWidgetItem(record.get("project", "")))
            
            # 상태
            status = record.get("status", "")
            status_item = QTableWidgetItem(status)
            
            # 상태별 색상 설정
            if status == "재직":
                status_item.setBackground(QColor("#d4edda"))
                status_item.setForeground(QColor("#155724"))
            elif status == "휴직":
                status_item.setBackground(QColor("#fff3cd"))
                status_item.setForeground(QColor("#856404"))
            elif status == "퇴직":
                status_item.setBackground(QColor("#f8d7da"))
                status_item.setForeground(QColor("#721c24"))
            
            self.labor_table.setItem(row, 7, status_item)
    
    def update_pagination(self, total: int):
        """페이지네이션 업데이트"""
        total_pages = (total + self.page_size - 1) // self.page_size
        
        self.page_info.setText(f"페이지 {self.current_page + 1} / {total_pages} (총 {total}건)")
        
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < total_pages - 1)
    
    def search_labor_data(self):
        """노무 데이터 검색"""
        self.current_page = 0
        self.load_labor_data()
    
    def on_filter_changed(self):
        """필터 변경 처리"""
        self.current_page = 0
        self.load_labor_data()
    
    def previous_page(self):
        """이전 페이지"""
        if self.current_page > 0:
            self.current_page -= 1
            self.load_labor_data()
    
    def next_page(self):
        """다음 페이지"""
        self.current_page += 1
        self.load_labor_data()
    
    def on_labor_double_clicked(self, item):
        """노무자 더블클릭 처리"""
        row = item.row()
        if row < len(self.labor_data):
            record = self.labor_data[row]
            self.edit_labor_with_data(record)
    
    def add_new_labor(self):
        """새 노무자 등록"""
        from .labor_dialog import LaborDialog
        
        dialog = LaborDialog(self)
        if dialog.exec() == QDialog.Accepted:
            # 새로고침
            self.load_labor_data()
            self.load_summary_data()
    
    def edit_labor(self):
        """노무자 수정"""
        current_row = self.labor_table.currentRow()
        if current_row >= 0 and current_row < len(self.labor_data):
            record = self.labor_data[current_row]
            self.edit_labor_with_data(record)
        else:
            QMessageBox.warning(self, "선택 오류", "수정할 노무자를 선택해주세요.")
    
    def edit_labor_with_data(self, record: Dict[str, Any]):
        """노무자 데이터로 수정 다이얼로그 열기"""
        from .labor_dialog import LaborDialog
        
        dialog = LaborDialog(self, record)
        if dialog.exec() == QDialog.Accepted:
            # 새로고침
            self.load_labor_data()
            self.load_summary_data()
    
    def delete_labor(self):
        """노무자 삭제"""
        current_row = self.labor_table.currentRow()
        if current_row >= 0 and current_row < len(self.labor_data):
            record = self.labor_data[current_row]
            
            reply = QMessageBox.question(
                self, "삭제 확인",
                f"노무자 '{record.get('worker_name', '')}'을(를) 삭제하시겠습니까?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.perform_delete_labor(record.get("id"))
        else:
            QMessageBox.warning(self, "선택 오류", "삭제할 노무자를 선택해주세요.")
    
    def perform_delete_labor(self, record_id: str):
        """노무자 삭제 실행"""
        if self.delete_worker and self.delete_worker.isRunning():
            return
        
        self.delete_worker = LaborDeleteWorker(record_id)
        self.delete_worker.delete_success.connect(self.on_delete_success)
        self.delete_worker.delete_failed.connect(self.on_delete_failed)
        self.delete_worker.finished.connect(self.on_delete_worker_finished)
        self.delete_worker.start()
    
    def on_delete_success(self):
        """삭제 성공 처리"""
        QMessageBox.information(self, "삭제 완료", "노무자가 성공적으로 삭제되었습니다.")
        # 새로고침
        self.load_labor_data()
        self.load_summary_data()
    
    def on_delete_failed(self, error_message: str):
        """삭제 실패 처리"""
        QMessageBox.critical(self, "삭제 실패", error_message)
    
    def on_delete_worker_finished(self):
        """삭제 워커 스레드 완료 처리"""
        if self.delete_worker:
            self.delete_worker.deleteLater()
            self.delete_worker = None
    
    def manage_work_hours(self):
        """근무시간 관리"""
        QMessageBox.information(self, "근무시간 관리", "근무시간 관리 기능은 추후 구현 예정입니다.")
    
    def calculate_salary(self):
        """임금 계산"""
        QMessageBox.information(self, "임금 계산", "임금 계산 기능은 추후 구현 예정입니다.")
    
    def export_labor_data(self):
        """노무 데이터 내보내기"""
        QMessageBox.information(self, "내보내기", "Excel 내보내기 기능은 추후 구현 예정입니다.") 