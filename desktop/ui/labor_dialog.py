#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 노무자 등록/수정 다이얼로그
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QLineEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox,
    QTextEdit, QPushButton, QMessageBox, QFrame, QGroupBox
)
from PySide6.QtCore import Qt, QDate, QThread, Signal
from PySide6.QtGui import QFont
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from api.client import get_api_client, APIError

logger = logging.getLogger(__name__)


class LaborSaveWorker(QThread):
    """노무자 저장을 백그라운드에서 처리하는 워커 스레드"""
    
    save_success = Signal(dict)
    save_failed = Signal(str)
    
    def __init__(self, labor_data: Dict[str, Any], is_update: bool = False, record_id: str = None):
        super().__init__()
        self.labor_data = labor_data
        self.is_update = is_update
        self.record_id = record_id
    
    def run(self):
        """노무자 저장 실행"""
        try:
            api_client = get_api_client()
            
            if self.is_update and self.record_id:
                result = api_client.update_labor_record(self.record_id, self.labor_data)
            else:
                result = api_client.create_labor_record(self.labor_data)
            
            if result.get("status") == "success":
                self.save_success.emit(result.get("data", {}))
            else:
                self.save_failed.emit(result.get("message", "노무자 저장에 실패했습니다."))
                
        except APIError as e:
            self.save_failed.emit(str(e))
        except Exception as e:
            logger.error(f"노무자 저장 중 오류: {e}")
            self.save_failed.emit("노무자 저장 중 오류가 발생했습니다.")


class LaborDialog(QDialog):
    """노무자 등록/수정 다이얼로그"""
    
    def __init__(self, parent=None, labor_data: Dict[str, Any] = None):
        super().__init__(parent)
        self.labor_data = labor_data
        self.is_update = labor_data is not None
        self.record_id = labor_data.get("id") if labor_data else None
        
        # 워커 스레드
        self.save_worker = None
        
        self.init_ui()
        if self.is_update:
            self.load_labor_data()
    
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("노무자 등록" if not self.is_update else "노무자 수정")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 제목
        title = QLabel("노무자 등록" if not self.is_update else "노무자 수정")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # 기본 정보 그룹
        self.setup_basic_info_group(layout)
        
        # 근무 정보 그룹
        self.setup_work_info_group(layout)
        
        # 연락처 정보 그룹
        self.setup_contact_info_group(layout)
        
        # 메모 그룹
        self.setup_memo_group(layout)
        
        # 버튼 영역
        self.setup_button_area(layout)
    
    def setup_basic_info_group(self, layout):
        """기본 정보 그룹 설정"""
        group = QGroupBox("기본 정보")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        form_layout = QFormLayout(group)
        form_layout.setSpacing(15)
        
        # 이름
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("노무자 이름을 입력하세요")
        self.name_input.setStyleSheet("""
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
        form_layout.addRow("이름 *:", self.name_input)
        
        # 주민등록번호
        self.ssn_input = QLineEdit()
        self.ssn_input.setPlaceholderText("000000-0000000")
        self.ssn_input.setMaxLength(14)
        self.ssn_input.setStyleSheet("""
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
        form_layout.addRow("주민등록번호:", self.ssn_input)
        
        # 생년월일
        self.birth_date = QDateEdit()
        self.birth_date.setCalendarPopup(True)
        self.birth_date.setDate(QDate.currentDate().addYears(-25))
        self.birth_date.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
            }
            QDateEdit:focus {
                border-color: #007bff;
            }
        """)
        form_layout.addRow("생년월일:", self.birth_date)
        
        # 성별
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["남성", "여성"])
        self.gender_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
            }
            QComboBox:focus {
                border-color: #007bff;
            }
        """)
        form_layout.addRow("성별:", self.gender_combo)
        
        layout.addWidget(group)
    
    def setup_work_info_group(self, layout):
        """근무 정보 그룹 설정"""
        group = QGroupBox("근무 정보")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        form_layout = QFormLayout(group)
        form_layout.setSpacing(15)
        
        # 직종
        self.job_type_combo = QComboBox()
        self.job_type_combo.addItems(["기술자", "일반노무자", "관리자", "안전관리자"])
        self.job_type_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
            }
            QComboBox:focus {
                border-color: #007bff;
            }
        """)
        form_layout.addRow("직종 *:", self.job_type_combo)
        
        # 입사일
        self.hire_date = QDateEdit()
        self.hire_date.setCalendarPopup(True)
        self.hire_date.setDate(QDate.currentDate())
        self.hire_date.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
            }
            QDateEdit:focus {
                border-color: #007bff;
            }
        """)
        form_layout.addRow("입사일 *:", self.hire_date)
        
        # 시급
        self.hourly_wage = QDoubleSpinBox()
        self.hourly_wage.setRange(0, 100000)
        self.hourly_wage.setSuffix(" 원")
        self.hourly_wage.setValue(15000)
        self.hourly_wage.setStyleSheet("""
            QDoubleSpinBox {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
            }
            QDoubleSpinBox:focus {
                border-color: #007bff;
            }
        """)
        form_layout.addRow("시급 *:", self.hourly_wage)
        
        # 근무시간
        self.work_hours = QSpinBox()
        self.work_hours.setRange(0, 24)
        self.work_hours.setSuffix(" 시간")
        self.work_hours.setValue(8)
        self.work_hours.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
            }
            QSpinBox:focus {
                border-color: #007bff;
            }
        """)
        form_layout.addRow("일일 근무시간:", self.work_hours)
        
        # 상태
        self.status_combo = QComboBox()
        self.status_combo.addItems(["재직", "휴직", "퇴직"])
        self.status_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
            }
            QComboBox:focus {
                border-color: #007bff;
            }
        """)
        form_layout.addRow("상태 *:", self.status_combo)
        
        layout.addWidget(group)
    
    def setup_contact_info_group(self, layout):
        """연락처 정보 그룹 설정"""
        group = QGroupBox("연락처 정보")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        form_layout = QFormLayout(group)
        form_layout.setSpacing(15)
        
        # 전화번호
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("010-0000-0000")
        self.phone_input.setStyleSheet("""
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
        form_layout.addRow("전화번호 *:", self.phone_input)
        
        # 주소
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("주소를 입력하세요")
        self.address_input.setStyleSheet("""
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
        form_layout.addRow("주소:", self.address_input)
        
        # 비상연락처
        self.emergency_contact = QLineEdit()
        self.emergency_contact.setPlaceholderText("비상연락처를 입력하세요")
        self.emergency_contact.setStyleSheet("""
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
        form_layout.addRow("비상연락처:", self.emergency_contact)
        
        layout.addWidget(group)
    
    def setup_memo_group(self, layout):
        """메모 그룹 설정"""
        group = QGroupBox("메모")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        group_layout = QVBoxLayout(group)
        
        self.memo_input = QTextEdit()
        self.memo_input.setPlaceholderText("노무자에 대한 메모를 입력하세요...")
        self.memo_input.setMaximumHeight(100)
        self.memo_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
            }
            QTextEdit:focus {
                border-color: #007bff;
            }
        """)
        group_layout.addWidget(self.memo_input)
        
        layout.addWidget(group)
    
    def setup_button_area(self, layout):
        """버튼 영역 설정"""
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 취소 버튼
        cancel_button = QPushButton("취소")
        cancel_button.setStyleSheet("""
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
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        # 저장 버튼
        save_button = QPushButton("저장")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #adb5bd;
            }
        """)
        save_button.clicked.connect(self.save_labor)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
    
    def load_labor_data(self):
        """기존 노무자 데이터 로드"""
        if not self.labor_data:
            return
        
        # 기본 정보
        self.name_input.setText(self.labor_data.get("worker_name", ""))
        self.ssn_input.setText(self.labor_data.get("ssn", ""))
        
        # 생년월일
        birth_date = self.labor_data.get("birth_date")
        if birth_date:
            try:
                date_obj = datetime.fromisoformat(birth_date.replace('Z', '+00:00'))
                self.birth_date.setDate(QDate(date_obj.year, date_obj.month, date_obj.day))
            except:
                pass
        
        # 성별
        gender = self.labor_data.get("gender", "")
        if gender == "남성":
            self.gender_combo.setCurrentIndex(0)
        elif gender == "여성":
            self.gender_combo.setCurrentIndex(1)
        
        # 근무 정보
        job_type = self.labor_data.get("job_type", "")
        job_types = ["기술자", "일반노무자", "관리자", "안전관리자"]
        if job_type in job_types:
            self.job_type_combo.setCurrentIndex(job_types.index(job_type))
        
        # 입사일
        hire_date = self.labor_data.get("hire_date")
        if hire_date:
            try:
                date_obj = datetime.fromisoformat(hire_date.replace('Z', '+00:00'))
                self.hire_date.setDate(QDate(date_obj.year, date_obj.month, date_obj.day))
            except:
                pass
        
        self.hourly_wage.setValue(self.labor_data.get("hourly_wage", 15000))
        self.work_hours.setValue(self.labor_data.get("work_hours", 8))
        
        # 상태
        status = self.labor_data.get("status", "")
        statuses = ["재직", "휴직", "퇴직"]
        if status in statuses:
            self.status_combo.setCurrentIndex(statuses.index(status))
        
        # 연락처 정보
        self.phone_input.setText(self.labor_data.get("contact", ""))
        self.address_input.setText(self.labor_data.get("address", ""))
        self.emergency_contact.setText(self.labor_data.get("emergency_contact", ""))
        
        # 메모
        self.memo_input.setPlainText(self.labor_data.get("memo", ""))
    
    def validate_form(self) -> bool:
        """폼 검증"""
        errors = []
        
        # 필수 필드 검증
        if not self.name_input.text().strip():
            errors.append("이름을 입력해주세요.")
        
        if not self.phone_input.text().strip():
            errors.append("전화번호를 입력해주세요.")
        
        if self.hourly_wage.value() <= 0:
            errors.append("시급은 0보다 커야 합니다.")
        
        # 전화번호 형식 검증
        phone = self.phone_input.text().strip()
        if phone and not self.is_valid_phone(phone):
            errors.append("올바른 전화번호 형식을 입력해주세요. (예: 010-0000-0000)")
        
        # 주민등록번호 형식 검증
        ssn = self.ssn_input.text().strip()
        if ssn and not self.is_valid_ssn(ssn):
            errors.append("올바른 주민등록번호 형식을 입력해주세요. (예: 000000-0000000)")
        
        if errors:
            QMessageBox.warning(self, "입력 오류", "\n".join(errors))
            return False
        
        return True
    
    def is_valid_phone(self, phone: str) -> bool:
        """전화번호 형식 검증"""
        import re
        pattern = r'^01[0-9]-\d{3,4}-\d{4}$'
        return bool(re.match(pattern, phone))
    
    def is_valid_ssn(self, ssn: str) -> bool:
        """주민등록번호 형식 검증"""
        import re
        pattern = r'^\d{6}-\d{7}$'
        return bool(re.match(pattern, ssn))
    
    def get_form_data(self) -> Dict[str, Any]:
        """폼 데이터 수집"""
        return {
            "worker_name": self.name_input.text().strip(),
            "ssn": self.ssn_input.text().strip(),
            "birth_date": self.birth_date.date().toString("yyyy-MM-dd"),
            "gender": self.gender_combo.currentText(),
            "job_type": self.job_type_combo.currentText(),
            "hire_date": self.hire_date.date().toString("yyyy-MM-dd"),
            "hourly_wage": self.hourly_wage.value(),
            "work_hours": self.work_hours.value(),
            "status": self.status_combo.currentText(),
            "contact": self.phone_input.text().strip(),
            "address": self.address_input.text().strip(),
            "emergency_contact": self.emergency_contact.text().strip(),
            "memo": self.memo_input.toPlainText().strip()
        }
    
    def save_labor(self):
        """노무자 저장"""
        if not self.validate_form():
            return
        
        # 폼 데이터 수집
        labor_data = self.get_form_data()
        
        # 워커 스레드로 저장 실행
        self.save_worker = LaborSaveWorker(
            labor_data=labor_data,
            is_update=self.is_update,
            record_id=self.record_id
        )
        self.save_worker.save_success.connect(self.on_save_success)
        self.save_worker.save_failed.connect(self.on_save_failed)
        self.save_worker.finished.connect(self.on_save_worker_finished)
        self.save_worker.start()
    
    def on_save_success(self, data: Dict[str, Any]):
        """저장 성공 처리"""
        QMessageBox.information(
            self, 
            "저장 완료", 
            "노무자 정보가 성공적으로 저장되었습니다."
        )
        self.accept()
    
    def on_save_failed(self, error_message: str):
        """저장 실패 처리"""
        QMessageBox.critical(self, "저장 실패", error_message)
    
    def on_save_worker_finished(self):
        """저장 워커 스레드 완료 처리"""
        if self.save_worker:
            self.save_worker.deleteLater()
            self.save_worker = None 