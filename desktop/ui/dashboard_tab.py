#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 대시보드 탭 컴포넌트
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton, QProgressBar,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QFont, QColor
import logging
from typing import Dict, Any, List
from api.client import get_api_client, APIError

logger = logging.getLogger(__name__)


class DashboardDataWorker(QThread):
    """대시보드 데이터를 백그라운드에서 로드하는 워커 스레드"""
    
    data_loaded = Signal(dict)
    data_failed = Signal(str)
    
    def run(self):
        """데이터 로드 실행"""
        try:
            api_client = get_api_client()
            
            # 대시보드 데이터 로드
            dashboard_data = api_client.get_dashboard_data()
            
            if dashboard_data.get("status") == "success":
                self.data_loaded.emit(dashboard_data.get("data", {}))
            else:
                self.data_failed.emit(dashboard_data.get("message", "데이터 로드에 실패했습니다."))
                
        except APIError as e:
            self.data_failed.emit(str(e))
        except Exception as e:
            logger.error(f"대시보드 데이터 로드 중 오류: {e}")
            self.data_failed.emit("데이터 로드 중 오류가 발생했습니다.")


class DashboardTab(QWidget):
    """대시보드 탭 클래스"""
    
    def __init__(self):
        super().__init__()
        self.api_client = get_api_client()
        self.dashboard_data = {}
        self.data_worker = None
        
        self.init_ui()
        self.setup_timer()
    
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 제목
        title = QLabel("대시보드")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # 새로고침 버튼
        refresh_layout = QHBoxLayout()
        refresh_layout.addStretch()
        
        refresh_button = QPushButton("새로고침")
        refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        refresh_button.clicked.connect(self.load_data)
        refresh_layout.addWidget(refresh_button)
        
        layout.addLayout(refresh_layout)
        
        # 통계 카드 영역
        self.setup_statistics_cards(layout)
        
        # 차트 및 그래프 영역
        self.setup_charts_area(layout)
        
        # 최근 활동 영역
        self.setup_recent_activities(layout)
        
        # 초기 데이터 로드
        self.load_data()
    
    def setup_statistics_cards(self, layout):
        """통계 카드 설정"""
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        
        # 계약 통계 카드
        self.contract_card = self.create_stat_card(
            "총 계약 수", "0", "건", "#3498db",
            "이번 달 계약: 0건", "전월 대비 0%"
        )
        stats_layout.addWidget(self.contract_card)
        
        # 재무 통계 카드
        self.financial_card = self.create_stat_card(
            "총 계약 금액", "0", "원", "#27ae60",
            "이번 달: 0원", "전월 대비 0%"
        )
        stats_layout.addWidget(self.financial_card)
        
        # 노무 통계 카드
        self.labor_card = self.create_stat_card(
            "총 인력 수", "0", "명", "#e74c3c",
            "현재 투입: 0명", "가동률 0%"
        )
        stats_layout.addWidget(self.labor_card)
        
        # 진행률 통계 카드
        self.progress_card = self.create_stat_card(
            "전체 진행률", "0", "%", "#f39c12",
            "목표 대비", "예정 대비 0%"
        )
        stats_layout.addWidget(self.progress_card)
        
        layout.addLayout(stats_layout)
    
    def create_stat_card(self, title, value, unit, color, subtitle, trend):
        """통계 카드 생성"""
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
        value_label.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold;")
        value_label.setObjectName("value_label")
        value_layout.addWidget(value_label)
        
        unit_label = QLabel(unit)
        unit_label.setStyleSheet(f"color: {color}; font-size: 16px; font-weight: bold;")
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
    
    def update_stat_card(self, card, value, subtitle, trend):
        """통계 카드 업데이트"""
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
    
    def setup_charts_area(self, layout):
        """차트 영역 설정"""
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(15)
        
        # 진행률 차트
        self.progress_chart = self.create_progress_chart()
        charts_layout.addWidget(self.progress_chart)
        
        # 월별 계약 현황
        self.contract_chart = self.create_contract_chart()
        charts_layout.addWidget(self.contract_chart)
        
        layout.addLayout(charts_layout)
    
    def create_progress_chart(self):
        """진행률 차트 생성"""
        chart_frame = QFrame()
        chart_frame.setFrameStyle(QFrame.StyledPanel)
        chart_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        chart_layout = QVBoxLayout(chart_frame)
        
        # 제목
        title = QLabel("프로젝트 진행률")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        chart_layout.addWidget(title)
        
        # 진행률 바들
        self.progress_bars = {}
        projects = [
            ("A동 건축공사", 0, "#3498db"),
            ("B동 토목공사", 0, "#27ae60"),
            ("C동 기계설비", 0, "#e74c3c"),
            ("D동 전기공사", 0, "#f39c12")
        ]
        
        for project_name, progress, color in projects:
            project_layout = QHBoxLayout()
            
            # 프로젝트명
            name_label = QLabel(project_name)
            name_label.setStyleSheet("font-size: 12px; color: #495057;")
            name_label.setMinimumWidth(120)
            project_layout.addWidget(name_label)
            
            # 진행률 바
            progress_bar = QProgressBar()
            progress_bar.setValue(progress)
            progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    border: 1px solid #dee2e6;
                    border-radius: 4px;
                    text-align: center;
                    background-color: #f8f9fa;
                }}
                QProgressBar::chunk {{
                    background-color: {color};
                    border-radius: 3px;
                }}
            """)
            project_layout.addWidget(progress_bar)
            
            # 진행률 텍스트
            progress_text = QLabel(f"{progress}%")
            progress_text.setStyleSheet("font-size: 12px; color: #495057; font-weight: bold;")
            progress_text.setMinimumWidth(40)
            project_layout.addWidget(progress_text)
            
            chart_layout.addLayout(project_layout)
            self.progress_bars[project_name] = progress_bar
        
        chart_layout.addStretch()
        return chart_frame
    
    def create_contract_chart(self):
        """계약 현황 차트 생성"""
        chart_frame = QFrame()
        chart_frame.setFrameStyle(QFrame.StyledPanel)
        chart_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        chart_layout = QVBoxLayout(chart_frame)
        
        # 제목
        title = QLabel("월별 계약 현황")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        chart_layout.addWidget(title)
        
        # 계약 현황 테이블
        self.contract_table = QTableWidget()
        self.contract_table.setColumnCount(3)
        self.contract_table.setHorizontalHeaderLabels(["월", "계약 수", "계약 금액"])
        self.contract_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.contract_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #dee2e6;
                font-weight: bold;
            }
        """)
        
        # 샘플 데이터
        months = ["1월", "2월", "3월", "4월", "5월", "6월"]
        for i, month in enumerate(months):
            self.contract_table.insertRow(i)
            self.contract_table.setItem(i, 0, QTableWidgetItem(month))
            self.contract_table.setItem(i, 1, QTableWidgetItem("0"))
            self.contract_table.setItem(i, 2, QTableWidgetItem("0원"))
        
        chart_layout.addWidget(self.contract_table)
        return chart_frame
    
    def setup_recent_activities(self, layout):
        """최근 활동 영역 설정"""
        activities_frame = QFrame()
        activities_frame.setFrameStyle(QFrame.StyledPanel)
        activities_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        activities_layout = QVBoxLayout(activities_frame)
        
        # 제목
        title = QLabel("최근 활동")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        activities_layout.addWidget(title)
        
        # 활동 목록
        self.activities_table = QTableWidget()
        self.activities_table.setColumnCount(4)
        self.activities_table.setHorizontalHeaderLabels(["시간", "사용자", "활동", "상세"])
        self.activities_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.activities_table.setMaximumHeight(200)
        self.activities_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #dee2e6;
                font-weight: bold;
            }
        """)
        
        activities_layout.addWidget(self.activities_table)
        layout.addWidget(activities_frame)
    
    def setup_timer(self):
        """타이머 설정"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_dashboard)
        self.update_timer.start(60000)  # 1분마다 업데이트
    
    def load_data(self):
        """대시보드 데이터 로드"""
        if self.data_worker and self.data_worker.isRunning():
            return
        
        self.data_worker = DashboardDataWorker()
        self.data_worker.data_loaded.connect(self.on_data_loaded)
        self.data_worker.data_failed.connect(self.on_data_failed)
        self.data_worker.finished.connect(self.on_worker_finished)
        self.data_worker.start()
    
    def on_data_loaded(self, data: Dict[str, Any]):
        """데이터 로드 성공 처리"""
        self.dashboard_data = data
        self.update_dashboard()
    
    def on_data_failed(self, error_message: str):
        """데이터 로드 실패 처리"""
        QMessageBox.warning(self, "데이터 로드 실패", error_message)
    
    def on_worker_finished(self):
        """워커 스레드 완료 처리"""
        if self.data_worker:
            self.data_worker.deleteLater()
            self.data_worker = None
    
    def update_dashboard(self):
        """대시보드 업데이트"""
        try:
            # 통계 카드 업데이트
            self.update_statistics_cards()
            
            # 차트 업데이트
            self.update_charts()
            
            # 최근 활동 업데이트
            self.update_recent_activities()
            
        except Exception as e:
            logger.error(f"대시보드 업데이트 중 오류: {e}")
    
    def update_statistics_cards(self):
        """통계 카드 업데이트"""
        contract_summary = self.dashboard_data.get("contract_summary", {})
        financial_summary = self.dashboard_data.get("financial_summary", {})
        labor_summary = self.dashboard_data.get("labor_summary", {})
        
        # 계약 통계
        total_contracts = contract_summary.get("total_contracts", 0)
        active_contracts = contract_summary.get("active_contracts", 0)
        contract_trend = contract_summary.get("trend", "0%")
        
        self.update_stat_card(
            self.contract_card,
            total_contracts,
            f"이번 달 계약: {active_contracts}건",
            f"전월 대비 {contract_trend}"
        )
        
        # 재무 통계
        total_amount = financial_summary.get("total_amount", 0)
        monthly_amount = financial_summary.get("monthly_amount", 0)
        financial_trend = financial_summary.get("trend", "0%")
        
        self.update_stat_card(
            self.financial_card,
            f"{total_amount:,}",
            f"이번 달: {monthly_amount:,}원",
            f"전월 대비 {financial_trend}"
        )
        
        # 노무 통계
        total_workers = labor_summary.get("total_workers", 0)
        active_workers = labor_summary.get("active_workers", 0)
        utilization_rate = labor_summary.get("utilization_rate", 0)
        
        self.update_stat_card(
            self.labor_card,
            total_workers,
            f"현재 투입: {active_workers}명",
            f"가동률 {utilization_rate}%"
        )
        
        # 진행률 통계
        overall_progress = self.dashboard_data.get("overall_progress", 0)
        progress_trend = self.dashboard_data.get("progress_trend", "0%")
        
        self.update_stat_card(
            self.progress_card,
            overall_progress,
            "목표 대비",
            f"예정 대비 {progress_trend}"
        )
    
    def update_charts(self):
        """차트 업데이트"""
        # 진행률 차트 업데이트
        project_progress = self.dashboard_data.get("project_progress", {})
        for project_name, progress_bar in self.progress_bars.items():
            progress = project_progress.get(project_name, 0)
            progress_bar.setValue(progress)
        
        # 계약 현황 차트 업데이트
        monthly_contracts = self.dashboard_data.get("monthly_contracts", [])
        self.contract_table.setRowCount(len(monthly_contracts))
        
        for i, month_data in enumerate(monthly_contracts):
            self.contract_table.setItem(i, 0, QTableWidgetItem(month_data.get("month", "")))
            self.contract_table.setItem(i, 1, QTableWidgetItem(str(month_data.get("count", 0))))
            self.contract_table.setItem(i, 2, QTableWidgetItem(f"{month_data.get('amount', 0):,}원"))
    
    def update_recent_activities(self):
        """최근 활동 업데이트"""
        activities = self.dashboard_data.get("recent_activities", [])
        self.activities_table.setRowCount(len(activities))
        
        for i, activity in enumerate(activities):
            self.activities_table.setItem(i, 0, QTableWidgetItem(activity.get("time", "")))
            self.activities_table.setItem(i, 1, QTableWidgetItem(activity.get("user", "")))
            self.activities_table.setItem(i, 2, QTableWidgetItem(activity.get("action", "")))
            self.activities_table.setItem(i, 3, QTableWidgetItem(activity.get("details", ""))) 