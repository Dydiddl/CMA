#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 재무 관리 탭 컴포넌트
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton, QLineEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QDateEdit, QSpinBox, QDoubleSpinBox, QTextEdit, QFormLayout,
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout
)
from PySide6.QtCore import Qt, QDate, QThread, pyqtSignal
from PySide6.QtGui import QFont, QColor
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from api.client import get_api_client, APIError

logger = logging.getLogger(__name__)


class FinancialDataWorker(QThread):
    """재무 데이터를 백그라운드에서 로드하는 워커 스레드"""
    
    data_loaded = pyqtSignal(dict)
    data_failed = pyqtSignal(str)
    
    def __init__(self, search: str = None, type_filter: str = None, skip: int = 0, limit: int = 50):
        super().__init__()
        self.search = search
        self.type_filter = type_filter
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
            if self.type_filter and self.type_filter != "전체":
                params["type"] = self.type_filter
            
            # 재무 데이터 로드
            result = api_client.get_financial_records(**params)
            
            if result.get("status") == "success":
                self.data_loaded.emit(result.get("data", {}))
            else:
                self.data_failed.emit(result.get("message", "재무 데이터 로드에 실패했습니다."))
                
        except APIError as e:
            self.data_failed.emit(str(e))
        except Exception as e:
            logger.error(f"재무 데이터 로드 중 오류: {e}")
            self.data_failed.emit("재무 데이터 로드 중 오류가 발생했습니다.")


class FinancialSummaryWorker(QThread):
    """재무 요약 데이터를 백그라운드에서 로드하는 워커 스레드"""
    
    summary_loaded = pyqtSignal(dict)
    summary_failed = pyqtSignal(str)
    
    def run(self):
        """요약 데이터 로드 실행"""
        try:
            api_client = get_api_client()
            result = api_client.get_financial_summary()
            
            if result.get("status") == "success":
                self.summary_loaded.emit(result.get("data", {}))
            else:
                self.summary_failed.emit(result.get("message", "재무 요약 데이터 로드에 실패했습니다."))
                
        except APIError as e:
            self.summary_failed.emit(str(e))
        except Exception as e:
            logger.error(f"재무 요약 데이터 로드 중 오류: {e}")
            self.summary_failed.emit("재무 요약 데이터 로드 중 오류가 발생했습니다.")


class FinancialSaveWorker(QThread):
    """재무 기록 저장을 백그라운드에서 처리하는 워커 스레드"""
    
    save_success = pyqtSignal(dict)
    save_failed = pyqtSignal(str)
    
    def __init__(self, financial_data: Dict[str, Any], is_update: bool = False, record_id: str = None):
        super().__init__()
        self.financial_data = financial_data
        self.is_update = is_update
        self.record_id = record_id
    
    def run(self):
        """재무 기록 저장 실행"""
        try:
            api_client = get_api_client()
            
            if self.is_update and self.record_id:
                result = api_client.update_financial_record(self.record_id, self.financial_data)
            else:
                result = api_client.create_financial_record(self.financial_data)
            
            if result.get("status") == "success":
                self.save_success.emit(result.get("data", {}))
            else:
                self.save_failed.emit(result.get("message", "재무 기록 저장에 실패했습니다."))
                
        except APIError as e:
            self.save_failed.emit(str(e))
        except Exception as e:
            logger.error(f"재무 기록 저장 중 오류: {e}")
            self.save_failed.emit("재무 기록 저장 중 오류가 발생했습니다.")


class FinancialDeleteWorker(QThread):
    """재무 기록 삭제를 백그라운드에서 처리하는 워커 스레드"""
    
    delete_success = pyqtSignal()
    delete_failed = pyqtSignal(str)
    
    def __init__(self, record_id: str):
        super().__init__()
        self.record_id = record_id
    
    def run(self):
        """재무 기록 삭제 실행"""
        try:
            api_client = get_api_client()
            result = api_client.delete_financial_record(self.record_id)
            
            if result.get("status") == "success":
                self.delete_success.emit()
            else:
                self.delete_failed.emit(result.get("message", "재무 기록 삭제에 실패했습니다."))
                
        except APIError as e:
            self.delete_failed.emit(str(e))
        except Exception as e:
            logger.error(f"재무 기록 삭제 중 오류: {e}")
            self.delete_failed.emit("재무 기록 삭제 중 오류가 발생했습니다.")


class FinancialTab(QWidget):
    """재무 관리 탭 클래스"""
    
    def __init__(self):
        super().__init__()
        self.api_client = get_api_client()
        self.financial_data = []
        self.current_page = 0
        self.page_size = 50
        
        # 워커 스레드
        self.data_worker = None
        self.summary_worker = None
        self.save_worker = None
        self.delete_worker = None
        
        self.init_ui()
        self.load_financial_data()
        self.load_summary_data()
    
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 제목
        title = QLabel("재무 관리")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # 재무 요약 카드
        self.setup_summary_cards(layout)
        
        # 검색 및 필터 영역
        self.setup_search_area(layout)
        
        # 버튼 영역
        self.setup_button_area(layout)
        
        # 재무 데이터 테이블
        self.setup_financial_table(layout)
        
        # 페이지네이션
        self.setup_pagination(layout)
    
    def setup_summary_cards(self, layout):
        """재무 요약 카드 설정"""
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(15)
        
        # 총 수입 카드
        self.income_card = self.create_summary_card(
            "총 수입", "0", "원", "#27ae60",
            "이번 달: 0원", "0%"
        )
        summary_layout.addWidget(self.income_card)
        
        # 총 지출 카드
        self.expense_card = self.create_summary_card(
            "총 지출", "0", "원", "#e74c3c",
            "이번 달: 0원", "0%"
        )
        summary_layout.addWidget(self.expense_card)
        
        # 순이익 카드
        self.profit_card = self.create_summary_card(
            "순이익", "0", "원", "#3498db",
            "이번 달: 0원", "0%"
        )
        summary_layout.addWidget(self.profit_card)
        
        # 미수금 카드
        self.receivable_card = self.create_summary_card(
            "미수금", "0", "원", "#f39c12",
            "30일 이상: 0원", "0%"
        )
        summary_layout.addWidget(self.receivable_card)
        
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
        if "+" in trend:
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
            if "+" in trend:
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
        self.search_input.setPlaceholderText("거래처명, 거래내역으로 검색...")
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
        self.search_input.returnPressed.connect(self.search_financial_data)
        search_layout.addWidget(self.search_input)
        
        # 거래 유형 필터
        type_label = QLabel("거래유형:")
        type_label.setStyleSheet("font-weight: bold; color: #495057;")
        search_layout.addWidget(type_label)
        
        self.type_filter = QComboBox()
        self.type_filter.addItems(["전체", "수입", "지출", "이체"])
        self.type_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
                min-width: 100px;
            }
        """)
        self.type_filter.currentTextChanged.connect(self.on_filter_changed)
        search_layout.addWidget(self.type_filter)
        
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
        search_button.clicked.connect(self.search_financial_data)
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
        refresh_button.clicked.connect(self.load_financial_data)
        search_layout.addWidget(refresh_button)
        
        search_layout.addStretch()
        layout.addWidget(search_frame)
    
    def setup_button_area(self, layout):
        """버튼 영역 설정"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # 새 거래 등록 버튼
        add_button = QPushButton("새 거래 등록")
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
        add_button.clicked.connect(self.add_new_transaction)
        button_layout.addWidget(add_button)
        
        # 거래 수정 버튼
        edit_button = QPushButton("거래 수정")
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
        edit_button.clicked.connect(self.edit_transaction)
        button_layout.addWidget(edit_button)
        
        # 거래 삭제 버튼
        delete_button = QPushButton("거래 삭제")
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
        delete_button.clicked.connect(self.delete_transaction)
        button_layout.addWidget(delete_button)
        
        button_layout.addStretch()
        
        # 재무 보고서 생성 버튼
        report_button = QPushButton("재무 보고서")
        report_button.setStyleSheet("""
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
        report_button.clicked.connect(self.generate_financial_report)
        button_layout.addWidget(report_button)
        
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
        export_button.clicked.connect(self.export_financial_data)
        button_layout.addWidget(export_button)
        
        layout.addLayout(button_layout)
    
    def setup_financial_table(self, layout):
        """재무 데이터 테이블 설정"""
        self.financial_table = QTableWidget()
        self.financial_table.setColumnCount(8)
        self.financial_table.setHorizontalHeaderLabels([
            "거래일", "거래유형", "거래처", "거래내역", "금액", "잔액", "분류", "비고"
        ])
        
        # 테이블 스타일 설정
        self.financial_table.setStyleSheet("""
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
        header = self.financial_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 거래일
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 거래유형
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # 거래처
        header.setSectionResizeMode(3, QHeaderView.Stretch)           # 거래내역
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # 금액
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # 잔액
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # 분류
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # 비고
        
        # 더블클릭 이벤트 연결
        self.financial_table.itemDoubleClicked.connect(self.on_transaction_double_clicked)
        
        layout.addWidget(self.financial_table)
    
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
    
    def load_financial_data(self):
        """재무 데이터 로드"""
        if self.data_worker and self.data_worker.isRunning():
            return
        
        self.data_worker = FinancialDataWorker(
            search=self.search_input.text().strip() or None,
            type_filter=self.type_filter.currentText() if self.type_filter.currentText() != "전체" else None,
            skip=self.current_page * self.page_size,
            limit=self.page_size
        )
        self.data_worker.data_loaded.connect(self.on_data_loaded)
        self.data_worker.data_failed.connect(self.on_data_failed)
        self.data_worker.finished.connect(self.on_worker_finished)
        self.data_worker.start()
    
    def load_summary_data(self):
        """재무 요약 데이터 로드"""
        if self.summary_worker and self.summary_worker.isRunning():
            return
        
        self.summary_worker = FinancialSummaryWorker()
        self.summary_worker.summary_loaded.connect(self.on_summary_loaded)
        self.summary_worker.summary_failed.connect(self.on_summary_failed)
        self.summary_worker.finished.connect(self.on_summary_worker_finished)
        self.summary_worker.start()
    
    def on_data_loaded(self, data: Dict[str, Any]):
        """데이터 로드 성공 처리"""
        self.financial_data = data.get("records", [])
        total = data.get("total", 0)
        
        self.update_financial_table()
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
        # 총 수입
        total_income = summary.get("total_income", 0)
        monthly_income = summary.get("monthly_income", 0)
        income_trend = summary.get("income_trend", "0%")
        
        self.update_summary_card(
            self.income_card,
            f"{total_income:,}",
            f"이번 달: {monthly_income:,}원",
            f"{income_trend}"
        )
        
        # 총 지출
        total_expense = summary.get("total_expense", 0)
        monthly_expense = summary.get("monthly_expense", 0)
        expense_trend = summary.get("expense_trend", "0%")
        
        self.update_summary_card(
            self.expense_card,
            f"{total_expense:,}",
            f"이번 달: {monthly_expense:,}원",
            f"{expense_trend}"
        )
        
        # 순이익
        net_profit = summary.get("net_profit", 0)
        monthly_profit = summary.get("monthly_profit", 0)
        profit_trend = summary.get("profit_trend", "0%")
        
        self.update_summary_card(
            self.profit_card,
            f"{net_profit:,}",
            f"이번 달: {monthly_profit:,}원",
            f"{profit_trend}"
        )
        
        # 미수금
        receivables = summary.get("receivables", 0)
        overdue_receivables = summary.get("overdue_receivables", 0)
        receivables_trend = summary.get("receivables_trend", "0%")
        
        self.update_summary_card(
            self.receivable_card,
            f"{receivables:,}",
            f"30일 이상: {overdue_receivables:,}원",
            f"{receivables_trend}"
        )
    
    def on_summary_failed(self, error_message: str):
        """요약 데이터 로드 실패 처리"""
        logger.warning(f"재무 요약 데이터 로드 실패: {error_message}")
    
    def on_summary_worker_finished(self):
        """요약 워커 스레드 완료 처리"""
        if self.summary_worker:
            self.summary_worker.deleteLater()
            self.summary_worker = None
    
    def update_financial_table(self):
        """재무 테이블 업데이트"""
        self.financial_table.setRowCount(len(self.financial_data))
        
        for row, record in enumerate(self.financial_data):
            # 거래일
            transaction_date = record.get("transaction_date", "")
            if transaction_date:
                try:
                    date_obj = datetime.fromisoformat(transaction_date.replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime("%Y-%m-%d")
                except:
                    formatted_date = transaction_date
            else:
                formatted_date = ""
            self.financial_table.setItem(row, 0, QTableWidgetItem(formatted_date))
            
            # 거래유형
            transaction_type = record.get("type", "")
            type_item = QTableWidgetItem(transaction_type)
            
            # 거래유형별 색상 설정
            if transaction_type == "수입":
                type_item.setBackground(QColor("#d4edda"))
                type_item.setForeground(QColor("#155724"))
            elif transaction_type == "지출":
                type_item.setBackground(QColor("#f8d7da"))
                type_item.setForeground(QColor("#721c24"))
            elif transaction_type == "이체":
                type_item.setBackground(QColor("#cce5ff"))
                type_item.setForeground(QColor("#004085"))
            
            self.financial_table.setItem(row, 1, type_item)
            
            # 거래처
            self.financial_table.setItem(row, 2, QTableWidgetItem(record.get("vendor_name", "")))
            
            # 거래내역
            self.financial_table.setItem(row, 3, QTableWidgetItem(record.get("description", "")))
            
            # 금액
            amount = record.get("amount", 0)
            amount_item = QTableWidgetItem(f"{amount:,}원")
            if transaction_type == "수입":
                amount_item.setForeground(QColor("#27ae60"))
            elif transaction_type == "지출":
                amount_item.setForeground(QColor("#e74c3c"))
            self.financial_table.setItem(row, 4, amount_item)
            
            # 잔액
            balance = record.get("balance", 0)
            self.financial_table.setItem(row, 5, QTableWidgetItem(f"{balance:,}원"))
            
            # 분류
            self.financial_table.setItem(row, 6, QTableWidgetItem(record.get("category", "")))
            
            # 비고
            self.financial_table.setItem(row, 7, QTableWidgetItem(record.get("notes", "")))
    
    def update_pagination(self, total: int):
        """페이지네이션 업데이트"""
        total_pages = (total + self.page_size - 1) // self.page_size
        
        self.page_info.setText(f"페이지 {self.current_page + 1} / {total_pages} (총 {total}건)")
        
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < total_pages - 1)
    
    def search_financial_data(self):
        """재무 데이터 검색"""
        self.current_page = 0
        self.load_financial_data()
    
    def on_filter_changed(self):
        """필터 변경 처리"""
        self.current_page = 0
        self.load_financial_data()
    
    def previous_page(self):
        """이전 페이지"""
        if self.current_page > 0:
            self.current_page -= 1
            self.load_financial_data()
    
    def next_page(self):
        """다음 페이지"""
        self.current_page += 1
        self.load_financial_data()
    
    def on_transaction_double_clicked(self, item):
        """거래 더블클릭 처리"""
        row = item.row()
        if row < len(self.financial_data):
            record = self.financial_data[row]
            self.edit_transaction_with_data(record)
    
    def add_new_transaction(self):
        """새 거래 등록"""
        dialog = FinancialDialog(self)
        if dialog.exec() == QDialog.Accepted:
            transaction_data = dialog.get_transaction_data()
            self.save_transaction(transaction_data)
    
    def edit_transaction(self):
        """거래 수정"""
        current_row = self.financial_table.currentRow()
        if current_row >= 0 and current_row < len(self.financial_data):
            record = self.financial_data[current_row]
            self.edit_transaction_with_data(record)
        else:
            QMessageBox.warning(self, "선택 오류", "수정할 거래를 선택해주세요.")
    
    def edit_transaction_with_data(self, record: Dict[str, Any]):
        """거래 데이터로 수정 다이얼로그 열기"""
        dialog = FinancialDialog(self, record)
        if dialog.exec() == QDialog.Accepted:
            transaction_data = dialog.get_transaction_data()
            self.save_transaction(transaction_data, is_update=True, record_id=record.get("id"))
    
    def save_transaction(self, transaction_data: Dict[str, Any], is_update: bool = False, record_id: str = None):
        """거래 저장"""
        if self.save_worker and self.save_worker.isRunning():
            return
        
        self.save_worker = FinancialSaveWorker(transaction_data, is_update, record_id)
        self.save_worker.save_success.connect(self.on_save_success)
        self.save_worker.save_failed.connect(self.on_save_failed)
        self.save_worker.finished.connect(self.on_save_worker_finished)
        self.save_worker.start()
    
    def on_save_success(self, transaction_data: Dict[str, Any]):
        """저장 성공 처리"""
        QMessageBox.information(self, "성공", "거래가 성공적으로 저장되었습니다.")
        self.load_financial_data()
        self.load_summary_data()
    
    def on_save_failed(self, error_message: str):
        """저장 실패 처리"""
        QMessageBox.warning(self, "저장 실패", error_message)
    
    def on_save_worker_finished(self):
        """저장 워커 스레드 완료 처리"""
        if self.save_worker:
            self.save_worker.deleteLater()
            self.save_worker = None
    
    def delete_transaction(self):
        """거래 삭제"""
        current_row = self.financial_table.currentRow()
        if current_row >= 0 and current_row < len(self.financial_data):
            record = self.financial_data[current_row]
            
            reply = QMessageBox.question(
                self, "삭제 확인",
                f"거래 '{record.get('description', '')}'을(를) 삭제하시겠습니까?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.delete_transaction_by_id(record.get("id"))
        else:
            QMessageBox.warning(self, "선택 오류", "삭제할 거래를 선택해주세요.")
    
    def delete_transaction_by_id(self, record_id: str):
        """거래 ID로 삭제"""
        if self.delete_worker and self.delete_worker.isRunning():
            return
        
        self.delete_worker = FinancialDeleteWorker(record_id)
        self.delete_worker.delete_success.connect(self.on_delete_success)
        self.delete_worker.delete_failed.connect(self.on_delete_failed)
        self.delete_worker.finished.connect(self.on_delete_worker_finished)
        self.delete_worker.start()
    
    def on_delete_success(self):
        """삭제 성공 처리"""
        QMessageBox.information(self, "성공", "거래가 성공적으로 삭제되었습니다.")
        self.load_financial_data()
        self.load_summary_data()
    
    def on_delete_failed(self, error_message: str):
        """삭제 실패 처리"""
        QMessageBox.warning(self, "삭제 실패", error_message)
    
    def on_delete_worker_finished(self):
        """삭제 워커 스레드 완료 처리"""
        if self.delete_worker:
            self.delete_worker.deleteLater()
            self.delete_worker = None
    
    def generate_financial_report(self):
        """재무 보고서 생성"""
        QMessageBox.information(self, "보고서 생성", "재무 보고서 생성 기능은 추후 구현 예정입니다.")
    
    def export_financial_data(self):
        """재무 데이터 내보내기"""
        QMessageBox.information(self, "내보내기", "Excel 내보내기 기능은 추후 구현 예정입니다.")


class FinancialDialog(QDialog):
    """재무 거래 등록/수정 다이얼로그"""
    
    def __init__(self, parent=None, record_data: Dict[str, Any] = None):
        super().__init__(parent)
        self.record_data = record_data
        self.is_edit_mode = record_data is not None
        
        self.setWindowTitle("거래 등록" if not self.is_edit_mode else "거래 수정")
        self.setFixedSize(500, 400)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        self.init_ui()
        if self.is_edit_mode:
            self.load_record_data()
    
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # 폼 레이아웃
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # 거래일
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        form_layout.addRow("거래일:", self.date_edit)
        
        # 거래유형
        self.type_combo = QComboBox()
        self.type_combo.addItems(["수입", "지출", "이체"])
        form_layout.addRow("거래유형:", self.type_combo)
        
        # 거래처
        self.vendor_edit = QLineEdit()
        self.vendor_edit.setPlaceholderText("거래처명을 입력하세요")
        form_layout.addRow("거래처:", self.vendor_edit)
        
        # 거래내역
        self.description_edit = QLineEdit()
        self.description_edit.setPlaceholderText("거래내역을 입력하세요")
        form_layout.addRow("거래내역:", self.description_edit)
        
        # 금액
        self.amount_edit = QDoubleSpinBox()
        self.amount_edit.setRange(0, 999999999999)
        self.amount_edit.setSuffix(" 원")
        self.amount_edit.setGroupSeparatorShown(True)
        form_layout.addRow("금액:", self.amount_edit)
        
        # 분류
        self.category_edit = QLineEdit()
        self.category_edit.setPlaceholderText("분류를 입력하세요 (예: 건축자재, 인건비)")
        form_layout.addRow("분류:", self.category_edit)
        
        # 비고
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(80)
        self.notes_edit.setPlaceholderText("추가 메모를 입력하세요")
        form_layout.addRow("비고:", self.notes_edit)
        
        layout.addLayout(form_layout)
        
        # 버튼
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_button = QPushButton("저장")
        save_button.clicked.connect(self.accept)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton("취소")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
    
    def load_record_data(self):
        """거래 데이터 로드"""
        if not self.record_data:
            return
        
        # 거래일 설정
        transaction_date = self.record_data.get("transaction_date", "")
        if transaction_date:
            try:
                date_obj = datetime.fromisoformat(transaction_date.replace('Z', '+00:00'))
                self.date_edit.setDate(QDate(date_obj.year, date_obj.month, date_obj.day))
            except:
                pass
        
        # 거래유형 설정
        transaction_type = self.record_data.get("type", "수입")
        index = self.type_combo.findText(transaction_type)
        if index >= 0:
            self.type_combo.setCurrentIndex(index)
        
        self.vendor_edit.setText(self.record_data.get("vendor_name", ""))
        self.description_edit.setText(self.record_data.get("description", ""))
        self.amount_edit.setValue(self.record_data.get("amount", 0))
        self.category_edit.setText(self.record_data.get("category", ""))
        self.notes_edit.setPlainText(self.record_data.get("notes", ""))
    
    def get_transaction_data(self) -> Dict[str, Any]:
        """거래 데이터 반환"""
        return {
            "transaction_date": self.date_edit.date().toString("yyyy-MM-dd"),
            "type": self.type_combo.currentText(),
            "vendor_name": self.vendor_edit.text().strip(),
            "description": self.description_edit.text().strip(),
            "amount": self.amount_edit.value(),
            "category": self.category_edit.text().strip(),
            "notes": self.notes_edit.toPlainText().strip()
        } 