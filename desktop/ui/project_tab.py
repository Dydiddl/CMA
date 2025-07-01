#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 프로젝트 관리 탭 컴포넌트
"""

import logging
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton, QLineEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QDateEdit, QSpinBox, QDoubleSpinBox, QTextEdit, QFormLayout,
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout
)
from PySide6.QtCore import Qt, QDate, QThread, Signal
from PySide6.QtGui import QFont, QColor
from typing import Dict, Any, List, Optional
from datetime import datetime
from api.client import get_api_client, APIError

logger = logging.getLogger(__name__)


class ProjectDataWorker(QThread):
    """프로젝트 데이터를 백그라운드에서 로드하는 워커 스레드"""
    
    data_loaded = Signal(dict)
    data_failed = Signal(str)
    
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
            
            # 프로젝트 데이터 로드
            result = api_client.get_projects(**params)
            
            if result.get("status") == "success":
                self.data_loaded.emit(result.get("data", {}))
            else:
                self.data_failed.emit(result.get("message", "프로젝트 데이터 로드에 실패했습니다."))
                
        except APIError as e:
            self.data_failed.emit(str(e))
        except Exception as e:
            logger.error(f"프로젝트 데이터 로드 중 오류: {e}")
            self.data_failed.emit("프로젝트 데이터 로드 중 오류가 발생했습니다.")


class ProjectSaveWorker(QThread):
    """프로젝트 저장을 백그라운드에서 처리하는 워커 스레드"""
    
    save_success = Signal(dict)
    save_failed = Signal(str)
    
    def __init__(self, project_data: Dict[str, Any], is_update: bool = False, project_id: str = None):
        super().__init__()
        self.project_data = project_data
        self.is_update = is_update
        self.project_id = project_id
    
    def run(self):
        """프로젝트 저장 실행"""
        try:
            api_client = get_api_client()
            
            if self.is_update and self.project_id:
                result = api_client.update_project(self.project_id, self.project_data)
            else:
                result = api_client.create_project(self.project_data)
            
            if result.get("status") == "success":
                self.save_success.emit(result.get("data", {}))
            else:
                self.save_failed.emit(result.get("message", "프로젝트 저장에 실패했습니다."))
                
        except APIError as e:
            self.save_failed.emit(str(e))
        except Exception as e:
            logger.error(f"프로젝트 저장 중 오류: {e}")
            self.save_failed.emit("프로젝트 저장 중 오류가 발생했습니다.")


class ProjectDeleteWorker(QThread):
    """프로젝트 삭제를 백그라운드에서 처리하는 워커 스레드"""
    
    delete_success = Signal()
    delete_failed = Signal(str)
    
    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
    
    def run(self):
        """프로젝트 삭제 실행"""
        try:
            api_client = get_api_client()
            result = api_client.delete_project(self.project_id)
            
            if result.get("status") == "success":
                self.delete_success.emit()
            else:
                self.delete_failed.emit(result.get("message", "프로젝트 삭제에 실패했습니다."))
                
        except APIError as e:
            self.delete_failed.emit(str(e))
        except Exception as e:
            logger.error(f"프로젝트 삭제 중 오류: {e}")
            self.delete_failed.emit("프로젝트 삭제 중 오류가 발생했습니다.")


class ProjectTab(QWidget):
    """프로젝트 관리 탭 클래스"""
    
    def __init__(self):
        super().__init__()
        self.api_client = get_api_client()
        self.projects_data = []
        self.current_page = 0
        self.page_size = 50
        
        # 워커 스레드
        self.data_worker = None
        self.save_worker = None
        self.delete_worker = None
        
        self.init_ui()
        self.load_project_data()
    
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 제목
        title = QLabel("프로젝트 관리")
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
        
        # 프로젝트 목록 테이블
        self.setup_project_table(layout)
        
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
        self.search_input.setPlaceholderText("프로젝트명, 프로젝트번호, 발주처명으로 검색...")
        self.search_input.setMinimumWidth(300)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
                outline: none;
            }
        """)
        self.search_input.returnPressed.connect(self.search_projects)
        search_layout.addWidget(self.search_input)
        
        # 상태 필터
        status_label = QLabel("상태:")
        status_label.setStyleSheet("font-weight: bold; color: #495057;")
        search_layout.addWidget(status_label)
        
        self.status_filter = QComboBox()
        self.status_filter.addItems(["전체", "계획", "진행중", "완료", "중단"])
        self.status_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
                min-width: 120px;
            }
        """)
        self.status_filter.currentTextChanged.connect(self.on_filter_changed)
        search_layout.addWidget(self.status_filter)
        
        # 검색 버튼
        search_button = QPushButton("검색")
        search_button.setStyleSheet("""
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
        search_button.clicked.connect(self.search_projects)
        search_layout.addWidget(search_button)
        
        search_layout.addStretch()
        layout.addWidget(search_frame)
    
    def setup_button_area(self, layout):
        """버튼 영역 설정"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # 새 프로젝트 버튼
        add_button = QPushButton("새 프로젝트")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        add_button.clicked.connect(self.add_new_project)
        button_layout.addWidget(add_button)
        
        # 편집 버튼
        edit_button = QPushButton("편집")
        edit_button.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)
        edit_button.clicked.connect(self.edit_project)
        button_layout.addWidget(edit_button)
        
        # 삭제 버튼
        delete_button = QPushButton("삭제")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        delete_button.clicked.connect(self.delete_project)
        button_layout.addWidget(delete_button)
        
        button_layout.addStretch()
        
        # 내보내기 버튼
        export_button = QPushButton("내보내기")
        export_button.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        export_button.clicked.connect(self.export_projects)
        button_layout.addWidget(export_button)
        
        layout.addLayout(button_layout)
    
    def setup_project_table(self, layout):
        """프로젝트 목록 테이블 설정"""
        self.project_table = QTableWidget()
        self.project_table.setColumnCount(8)
        self.project_table.setHorizontalHeaderLabels([
            "프로젝트 ID", "프로젝트명", "발주처", "시작일", "종료일", 
            "예산", "진행률", "상태"
        ])
        
        # 테이블 스타일 설정
        self.project_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                gridline-color: #dee2e6;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
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
                background-color: #e3f2fd;
                color: #1976d2;
            }
        """)
        
        # 컬럼 너비 설정
        header = self.project_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.Stretch)           # 프로젝트명
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # 발주처
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # 시작일
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # 종료일
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # 예산
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # 진행률
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # 상태
        
        # 더블클릭 이벤트 연결
        self.project_table.itemDoubleClicked.connect(self.on_project_double_clicked)
        
        layout.addWidget(self.project_table)
    
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
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:disabled {
                background-color: #dee2e6;
                color: #6c757d;
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
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:disabled {
                background-color: #dee2e6;
                color: #6c757d;
            }
        """)
        self.next_button.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.next_button)
        
        layout.addLayout(pagination_layout)
    
    def load_project_data(self):
        """프로젝트 데이터 로드"""
        if self.data_worker and self.data_worker.isRunning():
            return
        
        self.data_worker = ProjectDataWorker(
            search=self.search_input.text(),
            status=self.status_filter.currentText(),
            skip=self.current_page * self.page_size,
            limit=self.page_size
        )
        self.data_worker.data_loaded.connect(self.on_data_loaded)
        self.data_worker.data_failed.connect(self.on_data_failed)
        self.data_worker.finished.connect(self.on_worker_finished)
        self.data_worker.start()
    
    def on_data_loaded(self, data: Dict[str, Any]):
        """데이터 로드 완료 처리"""
        self.projects_data = data.get("data", [])
        total = data.get("total", 0)
        
        self.update_project_table()
        self.update_pagination(total)
    
    def on_data_failed(self, error_message: str):
        """데이터 로드 실패 처리"""
        QMessageBox.warning(self, "오류", error_message)
    
    def on_worker_finished(self):
        """워커 스레드 완료 처리"""
        self.data_worker = None
    
    def update_project_table(self):
        """프로젝트 테이블 업데이트"""
        self.project_table.setRowCount(len(self.projects_data))
        
        for row, project in enumerate(self.projects_data):
            # 프로젝트 ID
            id_item = QTableWidgetItem(str(project.get("id", "")))
            id_item.setData(Qt.UserRole, project.get("id"))
            self.project_table.setItem(row, 0, id_item)
            
            # 프로젝트명
            name_item = QTableWidgetItem(project.get("name", ""))
            self.project_table.setItem(row, 1, name_item)
            
            # 발주처
            client_item = QTableWidgetItem(project.get("client_name", ""))
            self.project_table.setItem(row, 2, client_item)
            
            # 시작일
            start_date = project.get("start_date")
            if start_date:
                start_item = QTableWidgetItem(start_date[:10])
            else:
                start_item = QTableWidgetItem("")
            self.project_table.setItem(row, 3, start_item)
            
            # 종료일
            end_date = project.get("end_date")
            if end_date:
                end_item = QTableWidgetItem(end_date[:10])
            else:
                end_item = QTableWidgetItem("")
            self.project_table.setItem(row, 4, end_item)
            
            # 예산
            budget = project.get("budget", 0)
            budget_item = QTableWidgetItem(f"{budget:,}원")
            self.project_table.setItem(row, 5, budget_item)
            
            # 진행률
            progress = project.get("progress", 0)
            progress_item = QTableWidgetItem(f"{progress}%")
            self.project_table.setItem(row, 6, progress_item)
            
            # 상태
            status = project.get("status", "")
            status_item = QTableWidgetItem(status)
            
            # 상태별 색상 설정
            if status == "완료":
                status_item.setBackground(QColor("#d4edda"))
                status_item.setForeground(QColor("#155724"))
            elif status == "진행중":
                status_item.setBackground(QColor("#d1ecf1"))
                status_item.setForeground(QColor("#0c5460"))
            elif status == "중단":
                status_item.setBackground(QColor("#f8d7da"))
                status_item.setForeground(QColor("#721c24"))
            else:
                status_item.setBackground(QColor("#fff3cd"))
                status_item.setForeground(QColor("#856404"))
            
            self.project_table.setItem(row, 7, status_item)
    
    def update_pagination(self, total: int):
        """페이지네이션 업데이트"""
        total_pages = (total + self.page_size - 1) // self.page_size
        current_page = self.current_page + 1
        
        self.page_info.setText(f"페이지 {current_page} / {total_pages} (총 {total}개)")
        
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(current_page < total_pages)
    
    def search_projects(self):
        """프로젝트 검색"""
        self.current_page = 0
        self.load_project_data()
    
    def on_filter_changed(self):
        """필터 변경 처리"""
        self.current_page = 0
        self.load_project_data()
    
    def previous_page(self):
        """이전 페이지"""
        if self.current_page > 0:
            self.current_page -= 1
            self.load_project_data()
    
    def next_page(self):
        """다음 페이지"""
        self.current_page += 1
        self.load_project_data()
    
    def on_project_double_clicked(self, item):
        """프로젝트 더블클릭 처리"""
        row = item.row()
        if row < len(self.projects_data):
            project = self.projects_data[row]
            self.edit_project_with_data(project)
    
    def add_new_project(self):
        """새 프로젝트 추가"""
        dialog = ProjectDialog(self)
        if dialog.exec() == QDialog.Accepted:
            project_data = dialog.get_project_data()
            self.save_project(project_data)
    
    def edit_project(self):
        """프로젝트 편집"""
        current_row = self.project_table.currentRow()
        if current_row >= 0 and current_row < len(self.projects_data):
            project = self.projects_data[current_row]
            self.edit_project_with_data(project)
        else:
            QMessageBox.warning(self, "알림", "편집할 프로젝트를 선택해주세요.")
    
    def edit_project_with_data(self, project: Dict[str, Any]):
        """데이터와 함께 프로젝트 편집"""
        dialog = ProjectDialog(self, project)
        if dialog.exec() == QDialog.Accepted:
            project_data = dialog.get_project_data()
            self.save_project(project_data, is_update=True, project_id=project.get("id"))
    
    def save_project(self, project_data: Dict[str, Any], is_update: bool = False, project_id: str = None):
        """프로젝트 저장"""
        if self.save_worker and self.save_worker.isRunning():
            return
        
        self.save_worker = ProjectSaveWorker(project_data, is_update, project_id)
        self.save_worker.save_success.connect(self.on_save_success)
        self.save_worker.save_failed.connect(self.on_save_failed)
        self.save_worker.finished.connect(self.on_save_worker_finished)
        self.save_worker.start()
    
    def on_save_success(self, project_data: Dict[str, Any]):
        """저장 성공 처리"""
        QMessageBox.information(self, "성공", "프로젝트가 성공적으로 저장되었습니다.")
        self.load_project_data()
    
    def on_save_failed(self, error_message: str):
        """저장 실패 처리"""
        QMessageBox.warning(self, "오류", error_message)
    
    def on_save_worker_finished(self):
        """저장 워커 스레드 완료 처리"""
        self.save_worker = None
    
    def delete_project(self):
        """프로젝트 삭제"""
        current_row = self.project_table.currentRow()
        if current_row >= 0 and current_row < len(self.projects_data):
            project = self.projects_data[current_row]
            project_id = project.get("id")
            project_name = project.get("name", "")
            
            reply = QMessageBox.question(
                self, "확인", 
                f"프로젝트 '{project_name}'을(를) 삭제하시겠습니까?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.delete_project_by_id(project_id)
        else:
            QMessageBox.warning(self, "알림", "삭제할 프로젝트를 선택해주세요.")
    
    def delete_project_by_id(self, project_id: str):
        """ID로 프로젝트 삭제"""
        if self.delete_worker and self.delete_worker.isRunning():
            return
        
        self.delete_worker = ProjectDeleteWorker(project_id)
        self.delete_worker.delete_success.connect(self.on_delete_success)
        self.delete_worker.delete_failed.connect(self.on_delete_failed)
        self.delete_worker.finished.connect(self.on_delete_worker_finished)
        self.delete_worker.start()
    
    def on_delete_success(self):
        """삭제 성공 처리"""
        QMessageBox.information(self, "성공", "프로젝트가 성공적으로 삭제되었습니다.")
        self.load_project_data()
    
    def on_delete_failed(self, error_message: str):
        """삭제 실패 처리"""
        QMessageBox.warning(self, "오류", error_message)
    
    def on_delete_worker_finished(self):
        """삭제 워커 스레드 완료 처리"""
        self.delete_worker = None
    
    def export_projects(self):
        """프로젝트 내보내기"""
        QMessageBox.information(self, "알림", "프로젝트 내보내기 기능은 추후 구현 예정입니다.")


class ProjectDialog(QDialog):
    """프로젝트 편집 다이얼로그"""
    
    def __init__(self, parent=None, project_data: Dict[str, Any] = None):
        super().__init__(parent)
        self.project_data = project_data
        self.is_edit_mode = project_data is not None
        
        self.setWindowTitle("프로젝트 편집" if self.is_edit_mode else "새 프로젝트")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        self.init_ui()
        if self.is_edit_mode:
            self.load_project_data()
    
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 폼 레이아웃
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # 프로젝트명
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("프로젝트명을 입력하세요")
        form_layout.addRow("프로젝트명 *:", self.name_input)
        
        # 발주처명
        self.client_input = QLineEdit()
        self.client_input.setPlaceholderText("발주처명을 입력하세요")
        form_layout.addRow("발주처명 *:", self.client_input)
        
        # 시작일
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        form_layout.addRow("시작일:", self.start_date)
        
        # 종료일
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate().addMonths(1))
        form_layout.addRow("종료일:", self.end_date)
        
        # 예산
        self.budget_input = QDoubleSpinBox()
        self.budget_input.setRange(0, 999999999999)
        self.budget_input.setSuffix("원")
        self.budget_input.setDecimals(0)
        form_layout.addRow("예산:", self.budget_input)
        
        # 진행률
        self.progress_input = QSpinBox()
        self.progress_input.setRange(0, 100)
        self.progress_input.setSuffix("%")
        form_layout.addRow("진행률:", self.progress_input)
        
        # 상태
        self.status_combo = QComboBox()
        self.status_combo.addItems(["계획", "진행중", "완료", "중단"])
        form_layout.addRow("상태:", self.status_combo)
        
        # 설명
        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(100)
        self.description_input.setPlaceholderText("프로젝트 설명을 입력하세요")
        form_layout.addRow("설명:", self.description_input)
        
        layout.addLayout(form_layout)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_button = QPushButton("취소")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        save_button = QPushButton("저장")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        save_button.clicked.connect(self.accept)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
    
    def load_project_data(self):
        """프로젝트 데이터 로드"""
        if not self.project_data:
            return
        
        self.name_input.setText(self.project_data.get("name", ""))
        self.client_input.setText(self.project_data.get("client_name", ""))
        
        # 날짜 설정
        start_date_str = self.project_data.get("start_date")
        if start_date_str:
            start_date = QDate.fromString(start_date_str[:10], "yyyy-MM-dd")
            self.start_date.setDate(start_date)
        
        end_date_str = self.project_data.get("end_date")
        if end_date_str:
            end_date = QDate.fromString(end_date_str[:10], "yyyy-MM-dd")
            self.end_date.setDate(end_date)
        
        self.budget_input.setValue(self.project_data.get("budget", 0))
        self.progress_input.setValue(self.project_data.get("progress", 0))
        
        status = self.project_data.get("status", "")
        index = self.status_combo.findText(status)
        if index >= 0:
            self.status_combo.setCurrentIndex(index)
        
        self.description_input.setPlainText(self.project_data.get("description", ""))
    
    def get_project_data(self) -> Dict[str, Any]:
        """프로젝트 데이터 반환"""
        return {
            "name": self.name_input.text(),
            "client_name": self.client_input.text(),
            "start_date": self.start_date.date().toString("yyyy-MM-dd"),
            "end_date": self.end_date.date().toString("yyyy-MM-dd"),
            "budget": self.budget_input.value(),
            "progress": self.progress_input.value(),
            "status": self.status_combo.currentText(),
            "description": self.description_input.toPlainText()
        } 