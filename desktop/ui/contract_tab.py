#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 계약 관리 탭 컴포넌트
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
from typing import Dict, Any, List, Optional
from datetime import datetime
from api.client import get_api_client, APIError

logger = logging.getLogger(__name__)


class ContractDataWorker(QThread):
    """계약 데이터를 백그라운드에서 로드하는 워커 스레드"""
    
    data_loaded = pyqtSignal(dict)
    data_failed = pyqtSignal(str)
    
    def __init__(self, search: str = None, status: str = None, skip: int = 0, limit: int = 50):
        super().__init__()
        self.search = search
        self.status = status
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
            if self.status and self.status != "전체":
                params["status"] = self.status
            
            # 계약 데이터 로드
            result = api_client.get_contracts(**params)
            
            if result.get("status") == "success":
                self.data_loaded.emit(result.get("data", {}))
            else:
                self.data_failed.emit(result.get("message", "계약 데이터 로드에 실패했습니다."))
                
        except APIError as e:
            self.data_failed.emit(str(e))
        except Exception as e:
            logger.error(f"계약 데이터 로드 중 오류: {e}")
            self.data_failed.emit("계약 데이터 로드 중 오류가 발생했습니다.")


class ContractSaveWorker(QThread):
    """계약 저장을 백그라운드에서 처리하는 워커 스레드"""
    
    save_success = pyqtSignal(dict)
    save_failed = pyqtSignal(str)
    
    def __init__(self, contract_data: Dict[str, Any], is_update: bool = False, contract_id: str = None):
        super().__init__()
        self.contract_data = contract_data
        self.is_update = is_update
        self.contract_id = contract_id
    
    def run(self):
        """계약 저장 실행"""
        try:
            api_client = get_api_client()
            
            if self.is_update and self.contract_id:
                result = api_client.update_contract(self.contract_id, self.contract_data)
            else:
                result = api_client.create_contract(self.contract_data)
            
            if result.get("status") == "success":
                self.save_success.emit(result.get("data", {}))
            else:
                self.save_failed.emit(result.get("message", "계약 저장에 실패했습니다."))
                
        except APIError as e:
            self.save_failed.emit(str(e))
        except Exception as e:
            logger.error(f"계약 저장 중 오류: {e}")
            self.save_failed.emit("계약 저장 중 오류가 발생했습니다.")


class ContractDeleteWorker(QThread):
    """계약 삭제를 백그라운드에서 처리하는 워커 스레드"""
    
    delete_success = pyqtSignal()
    delete_failed = pyqtSignal(str)
    
    def __init__(self, contract_id: str):
        super().__init__()
        self.contract_id = contract_id
    
    def run(self):
        """계약 삭제 실행"""
        try:
            api_client = get_api_client()
            result = api_client.delete_contract(self.contract_id)
            
            if result.get("status") == "success":
                self.delete_success.emit()
            else:
                self.delete_failed.emit(result.get("message", "계약 삭제에 실패했습니다."))
                
        except APIError as e:
            self.delete_failed.emit(str(e))
        except Exception as e:
            logger.error(f"계약 삭제 중 오류: {e}")
            self.delete_failed.emit("계약 삭제 중 오류가 발생했습니다.")


class ContractTab(QWidget):
    """계약 관리 탭 클래스"""
    
    def __init__(self):
        super().__init__()
        self.api_client = get_api_client()
        self.contracts_data = []
        self.current_page = 0
        self.page_size = 50
        
        # 워커 스레드
        self.data_worker = None
        self.save_worker = None
        self.delete_worker = None
        
        self.init_ui()
        self.load_contract_data()
    
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 제목
        title = QLabel("계약 관리")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # 검색 및 필터 영역
        self.setup_search_area(layout)
        
        # 버튼 영역
        self.setup_button_area(layout)
        
        # 계약 목록 테이블
        self.setup_contract_table(layout)
        
        # 페이지네이션
        self.setup_pagination(layout)
    
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
        self.search_input.setPlaceholderText("계약명, 계약번호, 발주처명으로 검색...")
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
        self.search_input.returnPressed.connect(self.search_contracts)
        search_layout.addWidget(self.search_input)
        
        # 상태 필터
        status_label = QLabel("상태:")
        status_label.setStyleSheet("font-weight: bold; color: #495057;")
        search_layout.addWidget(status_label)
        
        self.status_filter = QComboBox()
        self.status_filter.addItems(["전체", "진행중", "완료", "중단", "취소"])
        self.status_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
                min-width: 100px;
            }
        """)
        self.status_filter.currentTextChanged.connect(self.on_filter_changed)
        search_layout.addWidget(self.status_filter)
        
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
        search_button.clicked.connect(self.search_contracts)
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
        refresh_button.clicked.connect(self.load_contract_data)
        search_layout.addWidget(refresh_button)
        
        search_layout.addStretch()
        layout.addWidget(search_frame)
    
    def setup_button_area(self, layout):
        """버튼 영역 설정"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # 새 계약 등록 버튼
        add_button = QPushButton("새 계약 등록")
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
        add_button.clicked.connect(self.add_new_contract)
        button_layout.addWidget(add_button)
        
        # 계약 수정 버튼
        edit_button = QPushButton("계약 수정")
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
        edit_button.clicked.connect(self.edit_contract)
        button_layout.addWidget(edit_button)
        
        # 계약 삭제 버튼
        delete_button = QPushButton("계약 삭제")
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
        delete_button.clicked.connect(self.delete_contract)
        button_layout.addWidget(delete_button)
        
        button_layout.addStretch()
        
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
        export_button.clicked.connect(self.export_contracts)
        button_layout.addWidget(export_button)
        
        layout.addLayout(button_layout)
    
    def setup_contract_table(self, layout):
        """계약 목록 테이블 설정"""
        self.contract_table = QTableWidget()
        self.contract_table.setColumnCount(8)
        self.contract_table.setHorizontalHeaderLabels([
            "계약번호", "계약명", "발주처", "계약금액", "계약일", "시작일", "종료일", "상태"
        ])
        
        # 테이블 스타일 설정
        self.contract_table.setStyleSheet("""
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
        header = self.contract_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 계약번호
        header.setSectionResizeMode(1, QHeaderView.Stretch)           # 계약명
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # 발주처
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # 계약금액
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # 계약일
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # 시작일
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # 종료일
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # 상태
        
        # 더블클릭 이벤트 연결
        self.contract_table.itemDoubleClicked.connect(self.on_contract_double_clicked)
        
        layout.addWidget(self.contract_table)
    
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
    
    def load_contract_data(self):
        """계약 데이터 로드"""
        if self.data_worker and self.data_worker.isRunning():
            return
        
        self.data_worker = ContractDataWorker(
            search=self.search_input.text().strip() or None,
            status=self.status_filter.currentText() if self.status_filter.currentText() != "전체" else None,
            skip=self.current_page * self.page_size,
            limit=self.page_size
        )
        self.data_worker.data_loaded.connect(self.on_data_loaded)
        self.data_worker.data_failed.connect(self.on_data_failed)
        self.data_worker.finished.connect(self.on_worker_finished)
        self.data_worker.start()
    
    def on_data_loaded(self, data: Dict[str, Any]):
        """데이터 로드 성공 처리"""
        self.contracts_data = data.get("contracts", [])
        total = data.get("total", 0)
        
        self.update_contract_table()
        self.update_pagination(total)
    
    def on_data_failed(self, error_message: str):
        """데이터 로드 실패 처리"""
        QMessageBox.warning(self, "데이터 로드 실패", error_message)
    
    def on_worker_finished(self):
        """워커 스레드 완료 처리"""
        if self.data_worker:
            self.data_worker.deleteLater()
            self.data_worker = None
    
    def update_contract_table(self):
        """계약 테이블 업데이트"""
        self.contract_table.setRowCount(len(self.contracts_data))
        
        for row, contract in enumerate(self.contracts_data):
            # 계약번호
            self.contract_table.setItem(row, 0, QTableWidgetItem(contract.get("contract_number", "")))
            
            # 계약명
            self.contract_table.setItem(row, 1, QTableWidgetItem(contract.get("name", "")))
            
            # 발주처
            self.contract_table.setItem(row, 2, QTableWidgetItem(contract.get("client_name", "")))
            
            # 계약금액
            amount = contract.get("contract_amount", 0)
            self.contract_table.setItem(row, 3, QTableWidgetItem(f"{amount:,}원"))
            
            # 계약일
            contract_date = contract.get("contract_date", "")
            if contract_date:
                try:
                    date_obj = datetime.fromisoformat(contract_date.replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime("%Y-%m-%d")
                except:
                    formatted_date = contract_date
            else:
                formatted_date = ""
            self.contract_table.setItem(row, 4, QTableWidgetItem(formatted_date))
            
            # 시작일
            start_date = contract.get("start_date", "")
            if start_date:
                try:
                    date_obj = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime("%Y-%m-%d")
                except:
                    formatted_date = start_date
            else:
                formatted_date = ""
            self.contract_table.setItem(row, 5, QTableWidgetItem(formatted_date))
            
            # 종료일
            end_date = contract.get("end_date", "")
            if end_date:
                try:
                    date_obj = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime("%Y-%m-%d")
                except:
                    formatted_date = end_date
            else:
                formatted_date = ""
            self.contract_table.setItem(row, 6, QTableWidgetItem(formatted_date))
            
            # 상태
            status = contract.get("status", "")
            status_item = QTableWidgetItem(status)
            
            # 상태별 색상 설정
            if status == "진행중":
                status_item.setBackground(QColor("#d4edda"))
                status_item.setForeground(QColor("#155724"))
            elif status == "완료":
                status_item.setBackground(QColor("#cce5ff"))
                status_item.setForeground(QColor("#004085"))
            elif status == "중단":
                status_item.setBackground(QColor("#fff3cd"))
                status_item.setForeground(QColor("#856404"))
            elif status == "취소":
                status_item.setBackground(QColor("#f8d7da"))
                status_item.setForeground(QColor("#721c24"))
            
            self.contract_table.setItem(row, 7, status_item)
    
    def update_pagination(self, total: int):
        """페이지네이션 업데이트"""
        total_pages = (total + self.page_size - 1) // self.page_size
        
        self.page_info.setText(f"페이지 {self.current_page + 1} / {total_pages} (총 {total}건)")
        
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < total_pages - 1)
    
    def search_contracts(self):
        """계약 검색"""
        self.current_page = 0
        self.load_contract_data()
    
    def on_filter_changed(self):
        """필터 변경 처리"""
        self.current_page = 0
        self.load_contract_data()
    
    def previous_page(self):
        """이전 페이지"""
        if self.current_page > 0:
            self.current_page -= 1
            self.load_contract_data()
    
    def next_page(self):
        """다음 페이지"""
        self.current_page += 1
        self.load_contract_data()
    
    def on_contract_double_clicked(self, item):
        """계약 더블클릭 처리"""
        row = item.row()
        if row < len(self.contracts_data):
            contract = self.contracts_data[row]
            self.edit_contract_with_data(contract)
    
    def add_new_contract(self):
        """새 계약 등록"""
        dialog = ContractDialog(self)
        if dialog.exec() == QDialog.Accepted:
            contract_data = dialog.get_contract_data()
            self.save_contract(contract_data)
    
    def edit_contract(self):
        """계약 수정"""
        current_row = self.contract_table.currentRow()
        if current_row >= 0 and current_row < len(self.contracts_data):
            contract = self.contracts_data[current_row]
            self.edit_contract_with_data(contract)
        else:
            QMessageBox.warning(self, "선택 오류", "수정할 계약을 선택해주세요.")
    
    def edit_contract_with_data(self, contract: Dict[str, Any]):
        """계약 데이터로 수정 다이얼로그 열기"""
        dialog = ContractDialog(self, contract)
        if dialog.exec() == QDialog.Accepted:
            contract_data = dialog.get_contract_data()
            self.save_contract(contract_data, is_update=True, contract_id=contract.get("id"))
    
    def save_contract(self, contract_data: Dict[str, Any], is_update: bool = False, contract_id: str = None):
        """계약 저장"""
        if self.save_worker and self.save_worker.isRunning():
            return
        
        self.save_worker = ContractSaveWorker(contract_data, is_update, contract_id)
        self.save_worker.save_success.connect(self.on_save_success)
        self.save_worker.save_failed.connect(self.on_save_failed)
        self.save_worker.finished.connect(self.on_save_worker_finished)
        self.save_worker.start()
    
    def on_save_success(self, contract_data: Dict[str, Any]):
        """저장 성공 처리"""
        QMessageBox.information(self, "성공", "계약이 성공적으로 저장되었습니다.")
        self.load_contract_data()
    
    def on_save_failed(self, error_message: str):
        """저장 실패 처리"""
        QMessageBox.warning(self, "저장 실패", error_message)
    
    def on_save_worker_finished(self):
        """저장 워커 스레드 완료 처리"""
        if self.save_worker:
            self.save_worker.deleteLater()
            self.save_worker = None
    
    def delete_contract(self):
        """계약 삭제"""
        current_row = self.contract_table.currentRow()
        if current_row >= 0 and current_row < len(self.contracts_data):
            contract = self.contracts_data[current_row]
            
            reply = QMessageBox.question(
                self, "삭제 확인",
                f"계약 '{contract.get('name', '')}'을(를) 삭제하시겠습니까?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.delete_contract_by_id(contract.get("id"))
        else:
            QMessageBox.warning(self, "선택 오류", "삭제할 계약을 선택해주세요.")
    
    def delete_contract_by_id(self, contract_id: str):
        """계약 ID로 삭제"""
        if self.delete_worker and self.delete_worker.isRunning():
            return
        
        self.delete_worker = ContractDeleteWorker(contract_id)
        self.delete_worker.delete_success.connect(self.on_delete_success)
        self.delete_worker.delete_failed.connect(self.on_delete_failed)
        self.delete_worker.finished.connect(self.on_delete_worker_finished)
        self.delete_worker.start()
    
    def on_delete_success(self):
        """삭제 성공 처리"""
        QMessageBox.information(self, "성공", "계약이 성공적으로 삭제되었습니다.")
        self.load_contract_data()
    
    def on_delete_failed(self, error_message: str):
        """삭제 실패 처리"""
        QMessageBox.warning(self, "삭제 실패", error_message)
    
    def on_delete_worker_finished(self):
        """삭제 워커 스레드 완료 처리"""
        if self.delete_worker:
            self.delete_worker.deleteLater()
            self.delete_worker = None
    
    def export_contracts(self):
        """계약 내보내기"""
        QMessageBox.information(self, "내보내기", "Excel 내보내기 기능은 추후 구현 예정입니다.")


class ContractDialog(QDialog):
    """계약 등록/수정 다이얼로그"""
    
    def __init__(self, parent=None, contract_data: Dict[str, Any] = None):
        super().__init__(parent)
        self.contract_data = contract_data
        self.is_edit_mode = contract_data is not None
        
        self.setWindowTitle("계약 등록" if not self.is_edit_mode else "계약 수정")
        self.setFixedSize(600, 500)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        self.init_ui()
        if self.is_edit_mode:
            self.load_contract_data()
    
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # 폼 레이아웃
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # 계약명
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("계약명을 입력하세요")
        form_layout.addRow("계약명:", self.name_edit)
        
        # 계약번호
        self.contract_number_edit = QLineEdit()
        self.contract_number_edit.setPlaceholderText("계약번호를 입력하세요")
        form_layout.addRow("계약번호:", self.contract_number_edit)
        
        # 계약금액
        self.amount_edit = QDoubleSpinBox()
        self.amount_edit.setRange(0, 999999999999)
        self.amount_edit.setSuffix(" 원")
        self.amount_edit.setGroupSeparatorShown(True)
        form_layout.addRow("계약금액:", self.amount_edit)
        
        # 발주처명
        self.client_name_edit = QLineEdit()
        self.client_name_edit.setPlaceholderText("발주처명을 입력하세요")
        form_layout.addRow("발주처명:", self.client_name_edit)
        
        # 계약일
        self.contract_date_edit = QDateEdit()
        self.contract_date_edit.setDate(QDate.currentDate())
        self.contract_date_edit.setCalendarPopup(True)
        form_layout.addRow("계약일:", self.contract_date_edit)
        
        # 시작일
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate())
        self.start_date_edit.setCalendarPopup(True)
        form_layout.addRow("시작일:", self.start_date_edit)
        
        # 종료일
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDate(QDate.currentDate().addMonths(1))
        self.end_date_edit.setCalendarPopup(True)
        form_layout.addRow("종료일:", self.end_date_edit)
        
        # 상태
        self.status_combo = QComboBox()
        self.status_combo.addItems(["진행중", "완료", "중단", "취소"])
        form_layout.addRow("상태:", self.status_combo)
        
        # 설명
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        self.description_edit.setPlaceholderText("계약에 대한 설명을 입력하세요")
        form_layout.addRow("설명:", self.description_edit)
        
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
    
    def load_contract_data(self):
        """계약 데이터 로드"""
        if not self.contract_data:
            return
        
        self.name_edit.setText(self.contract_data.get("name", ""))
        self.contract_number_edit.setText(self.contract_data.get("contract_number", ""))
        self.amount_edit.setValue(self.contract_data.get("contract_amount", 0))
        self.client_name_edit.setText(self.contract_data.get("client_name", ""))
        
        # 날짜 설정
        contract_date = self.contract_data.get("contract_date", "")
        if contract_date:
            try:
                date_obj = datetime.fromisoformat(contract_date.replace('Z', '+00:00'))
                self.contract_date_edit.setDate(QDate(date_obj.year, date_obj.month, date_obj.day))
            except:
                pass
        
        start_date = self.contract_data.get("start_date", "")
        if start_date:
            try:
                date_obj = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                self.start_date_edit.setDate(QDate(date_obj.year, date_obj.month, date_obj.day))
            except:
                pass
        
        end_date = self.contract_data.get("end_date", "")
        if end_date:
            try:
                date_obj = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                self.end_date_edit.setDate(QDate(date_obj.year, date_obj.month, date_obj.day))
            except:
                pass
        
        # 상태 설정
        status = self.contract_data.get("status", "진행중")
        index = self.status_combo.findText(status)
        if index >= 0:
            self.status_combo.setCurrentIndex(index)
        
        self.description_edit.setPlainText(self.contract_data.get("description", ""))
    
    def get_contract_data(self) -> Dict[str, Any]:
        """계약 데이터 반환"""
        return {
            "name": self.name_edit.text().strip(),
            "contract_number": self.contract_number_edit.text().strip(),
            "contract_amount": self.amount_edit.value(),
            "client_name": self.client_name_edit.text().strip(),
            "contract_date": self.contract_date_edit.date().toString("yyyy-MM-dd"),
            "start_date": self.start_date_edit.date().toString("yyyy-MM-dd"),
            "end_date": self.end_date_edit.date().toString("yyyy-MM-dd"),
            "status": self.status_combo.currentText(),
            "description": self.description_edit.toPlainText().strip()
        } 