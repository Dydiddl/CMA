#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 도움말 탭 컴포넌트
"""

import logging
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton, QTextEdit, QTabWidget,
    QScrollArea, QGroupBox, QListWidget, QListWidgetItem,
    QSplitter, QTreeWidget, QTreeWidgetItem, QMessageBox
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont, QColor, QPixmap, QDesktopServices
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class HelpTab(QWidget):
    """도움말 탭 클래스"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 제목
        title = QLabel("도움말")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # 도움말 탭 위젯
        self.help_tabs = QTabWidget()
        self.help_tabs.setStyleSheet("""
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
        
        # 시작하기 탭
        self.setup_getting_started_tab()
        
        # 사용자 가이드 탭
        self.setup_user_guide_tab()
        
        # FAQ 탭
        self.setup_faq_tab()
        
        # 문제 해결 탭
        self.setup_troubleshooting_tab()
        
        # 정보 탭
        self.setup_about_tab()
        
        layout.addWidget(self.help_tabs)
    
    def setup_getting_started_tab(self):
        """시작하기 탭"""
        getting_started_widget = QWidget()
        layout = QVBoxLayout(getting_started_widget)
        layout.setSpacing(20)
        
        # 환영 메시지
        welcome_group = QGroupBox("CMA에 오신 것을 환영합니다!")
        welcome_layout = QVBoxLayout(welcome_group)
        
        welcome_text = QLabel("""
        <h3>건설 관리 시스템 (CMA) 시작하기</h3>
        <p>CMA는 건설 프로젝트의 계약, 재무, 노무 관리를 통합적으로 지원하는 시스템입니다.</p>
        <p>이 가이드를 통해 CMA의 기본 기능을 빠르게 익혀보세요.</p>
        """)
        welcome_text.setWordWrap(True)
        welcome_layout.addWidget(welcome_text)
        
        layout.addWidget(welcome_group)
        
        # 빠른 시작 가이드
        quick_start_group = QGroupBox("빠른 시작 가이드")
        quick_start_layout = QVBoxLayout(quick_start_group)
        
        steps = [
            "1. <b>로그인</b>: 사용자 계정으로 로그인합니다.",
            "2. <b>대시보드 확인</b>: 전체 프로젝트 현황을 확인합니다.",
            "3. <b>계약 관리</b>: 새로운 계약을 등록하거나 기존 계약을 관리합니다.",
            "4. <b>재무 관리</b>: 예산과 비용을 추적하고 관리합니다.",
            "5. <b>노무 관리</b>: 인력과 작업 시간을 관리합니다.",
            "6. <b>프로젝트 관리</b>: 프로젝트별 진행 상황을 관리합니다."
        ]
        
        for step in steps:
            step_label = QLabel(step)
            step_label.setWordWrap(True)
            step_label.setStyleSheet("margin: 5px 0;")
            quick_start_layout.addWidget(step_label)
        
        layout.addWidget(quick_start_group)
        
        # 주요 기능 소개
        features_group = QGroupBox("주요 기능")
        features_layout = QVBoxLayout(features_group)
        
        features = [
            "📊 <b>실시간 대시보드</b>: 프로젝트 현황을 한눈에 확인",
            "📋 <b>계약 관리</b>: 계약서 작성, 수정, 추적",
            "💰 <b>재무 관리</b>: 예산 관리, 비용 분석, 보고서 생성",
            "👥 <b>노무 관리</b>: 인력 관리, 시간 추적, 임금 계산",
            "📈 <b>프로젝트 관리</b>: 진행률 추적, 일정 관리",
            "⚙️ <b>설정 관리</b>: 시스템 설정, 사용자 환경 구성"
        ]
        
        for feature in features:
            feature_label = QLabel(feature)
            feature_label.setWordWrap(True)
            feature_label.setStyleSheet("margin: 5px 0;")
            features_layout.addWidget(feature_label)
        
        layout.addWidget(features_group)
        layout.addStretch()
        
        self.help_tabs.addTab(getting_started_widget, "시작하기")
    
    def setup_user_guide_tab(self):
        """사용자 가이드 탭"""
        user_guide_widget = QWidget()
        layout = QHBoxLayout(user_guide_widget)
        
        # 왼쪽: 목차
        left_panel = QFrame()
        left_panel.setMaximumWidth(300)
        left_layout = QVBoxLayout(left_panel)
        
        left_layout.addWidget(QLabel("목차"))
        
        self.guide_tree = QTreeWidget()
        self.guide_tree.setHeaderLabel("사용자 가이드")
        self.guide_tree.setStyleSheet("""
            QTreeWidget {
                border: 1px solid #dee2e6;
                background-color: white;
            }
            QTreeWidget::item {
                padding: 5px;
            }
            QTreeWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
        """)
        
        # 가이드 목차 구성
        self.setup_guide_tree()
        left_layout.addWidget(self.guide_tree)
        
        # 오른쪽: 내용
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        
        self.guide_content = QTextEdit()
        self.guide_content.setReadOnly(True)
        self.guide_content.setStyleSheet("""
            QTextEdit {
                border: 1px solid #dee2e6;
                background-color: white;
                padding: 10px;
            }
        """)
        right_layout.addWidget(self.guide_content)
        
        # 기본 내용 표시
        self.show_guide_content("대시보드")
        
        layout.addWidget(left_panel)
        layout.addWidget(right_panel)
        
        # 트리 클릭 이벤트 연결
        self.guide_tree.itemClicked.connect(self.on_guide_item_clicked)
        
        self.help_tabs.addTab(user_guide_widget, "사용자 가이드")
    
    def setup_guide_tree(self):
        """가이드 트리 구성"""
        # 대시보드
        dashboard_item = QTreeWidgetItem(self.guide_tree, ["대시보드"])
        QTreeWidgetItem(dashboard_item, ["대시보드 개요"])
        QTreeWidgetItem(dashboard_item, ["통계 카드 이해하기"])
        QTreeWidgetItem(dashboard_item, ["차트 및 그래프"])
        
        # 계약 관리
        contract_item = QTreeWidgetItem(self.guide_tree, ["계약 관리"])
        QTreeWidgetItem(contract_item, ["새 계약 등록"])
        QTreeWidgetItem(contract_item, ["계약 수정 및 삭제"])
        QTreeWidgetItem(contract_item, ["계약 검색 및 필터링"])
        QTreeWidgetItem(contract_item, ["계약 내보내기"])
        
        # 재무 관리
        financial_item = QTreeWidgetItem(self.guide_tree, ["재무 관리"])
        QTreeWidgetItem(financial_item, ["예산 설정"])
        QTreeWidgetItem(financial_item, ["비용 입력"])
        QTreeWidgetItem(financial_item, ["재무 보고서"])
        QTreeWidgetItem(financial_item, ["비용 분석"])
        
        # 노무 관리
        labor_item = QTreeWidgetItem(self.guide_tree, ["노무 관리"])
        QTreeWidgetItem(labor_item, ["인력 등록"])
        QTreeWidgetItem(labor_item, ["작업 시간 기록"])
        QTreeWidgetItem(labor_item, ["임금 계산"])
        QTreeWidgetItem(labor_item, ["노무 보고서"])
        
        # 프로젝트 관리
        project_item = QTreeWidgetItem(self.guide_tree, ["프로젝트 관리"])
        QTreeWidgetItem(project_item, ["프로젝트 생성"])
        QTreeWidgetItem(project_item, ["진행률 관리"])
        QTreeWidgetItem(project_item, ["일정 관리"])
        
        # 설정
        settings_item = QTreeWidgetItem(self.guide_tree, ["설정"])
        QTreeWidgetItem(settings_item, ["일반 설정"])
        QTreeWidgetItem(settings_item, ["데이터베이스 설정"])
        QTreeWidgetItem(settings_item, ["API 설정"])
        QTreeWidgetItem(settings_item, ["백업 설정"])
        
        self.guide_tree.expandAll()
    
    def on_guide_item_clicked(self, item, column):
        """가이드 항목 클릭 처리"""
        guide_title = item.text(0)
        self.show_guide_content(guide_title)
    
    def show_guide_content(self, title: str):
        """가이드 내용 표시"""
        content_map = {
            "대시보드": """
            <h2>대시보드 사용법</h2>
            <p>대시보드는 CMA의 핵심 기능으로, 모든 프로젝트의 현황을 한눈에 볼 수 있습니다.</p>
            
            <h3>주요 구성 요소</h3>
            <ul>
                <li><b>통계 카드</b>: 계약 수, 총 금액, 인력 수, 진행률 등 주요 지표</li>
                <li><b>차트 및 그래프</b>: 월별 추이, 부문별 분포 등 시각적 데이터</li>
                <li><b>최근 활동</b>: 최근 등록된 계약, 수정된 데이터 등</li>
            </ul>
            
            <h3>사용 팁</h3>
            <ul>
                <li>새로고침 버튼을 클릭하여 최신 데이터를 확인하세요.</li>
                <li>각 통계 카드를 클릭하면 해당 관리 페이지로 이동합니다.</li>
                <li>차트의 범례를 클릭하여 특정 항목을 숨기거나 표시할 수 있습니다.</li>
            </ul>
            """,
            
            "계약 관리": """
            <h2>계약 관리 사용법</h2>
            <p>계약 관리에서는 프로젝트와 관련된 모든 계약을 체계적으로 관리할 수 있습니다.</p>
            
            <h3>새 계약 등록</h3>
            <ol>
                <li>"새 계약" 버튼을 클릭합니다.</li>
                <li>필수 정보를 입력합니다 (계약명, 계약번호, 발주처 등).</li>
                <li>계약 금액과 기간을 설정합니다.</li>
                <li>"저장" 버튼을 클릭하여 등록을 완료합니다.</li>
            </ol>
            
            <h3>계약 검색 및 필터링</h3>
            <ul>
                <li>검색창에 계약명, 계약번호, 발주처명을 입력하여 검색할 수 있습니다.</li>
                <li>상태 필터를 사용하여 진행중, 완료, 중단된 계약을 구분하여 볼 수 있습니다.</li>
            </ul>
            
            <h3>계약 수정 및 삭제</h3>
            <ul>
                <li>계약을 더블클릭하거나 "편집" 버튼을 클릭하여 수정할 수 있습니다.</li>
                <li>"삭제" 버튼을 클릭하여 계약을 삭제할 수 있습니다 (주의: 복구 불가).</li>
            </ul>
            """,
            
            "재무 관리": """
            <h2>재무 관리 사용법</h2>
            <p>재무 관리에서는 프로젝트의 예산과 비용을 체계적으로 관리할 수 있습니다.</p>
            
            <h3>예산 설정</h3>
            <ol>
                <li>프로젝트별로 예산을 설정합니다.</li>
                <li>부문별 세부 예산을 입력합니다.</li>
                <li>예산 대비 실제 지출을 추적합니다.</li>
            </ol>
            
            <h3>비용 입력</h3>
            <ul>
                <li>실제 발생한 비용을 카테고리별로 입력합니다.</li>
                <li>영수증이나 증빙서류를 첨부할 수 있습니다.</li>
                <li>비용 승인 절차를 거칠 수 있습니다.</li>
            </ul>
            
            <h3>재무 보고서</h3>
            <ul>
                <li>월별, 분기별, 연간 재무 보고서를 생성할 수 있습니다.</li>
                <li>예산 대비 실적을 분석할 수 있습니다.</li>
                <li>Excel 형태로 내보낼 수 있습니다.</li>
            </ul>
            """,
            
            "노무 관리": """
            <h2>노무 관리 사용법</h2>
            <p>노무 관리에서는 프로젝트에 투입되는 인력과 작업 시간을 관리할 수 있습니다.</p>
            
            <h3>인력 등록</h3>
            <ol>
                <li>작업자 정보를 등록합니다 (이름, 연락처, 특기 등).</li>
                <li>작업자별 임금 정보를 설정합니다.</li>
                <li>작업자 상태를 관리합니다 (활성/비활성).</li>
            </ol>
            
            <h3>작업 시간 기록</h3>
            <ul>
                <li>일별 작업 시간을 기록합니다.</li>
                <li>작업 내용과 위치를 기록합니다.</li>
                <li>초과근무 시간을 별도로 관리합니다.</li>
            </ul>
            
            <h3>임금 계산</h3>
            <ul>
                <li>기본급, 수당, 공제 등을 자동으로 계산합니다.</li>
                <li>월별 임금 명세서를 생성합니다.</li>
                <li>세금 계산 및 공제를 처리합니다.</li>
            </ul>
            """,
            
            "프로젝트 관리": """
            <h2>프로젝트 관리 사용법</h2>
            <p>프로젝트 관리에서는 전체 프로젝트의 진행 상황을 관리할 수 있습니다.</p>
            
            <h3>프로젝트 생성</h3>
            <ol>
                <li>새 프로젝트를 생성합니다.</li>
                <li>프로젝트 기본 정보를 입력합니다.</li>
                <li>프로젝트 팀원을 배정합니다.</li>
                <li>프로젝트 일정을 설정합니다.</li>
            </ol>
            
            <h3>진행률 관리</h3>
            <ul>
                <li>전체 프로젝트 진행률을 추적합니다.</li>
                <li>부문별 진행률을 세부적으로 관리합니다.</li>
                <li>지연 사유와 대응 방안을 기록합니다.</li>
            </ul>
            
            <h3>일정 관리</h3>
            <ul>
                <li>마일스톤과 데드라인을 설정합니다.</li>
                <li>작업 간 의존성을 관리합니다.</li>
                <li>일정 변경 시 영향도를 분석합니다.</li>
            </ul>
            """,
            
            "설정": """
            <h2>설정 사용법</h2>
            <p>설정에서는 CMA 시스템의 다양한 옵션을 구성할 수 있습니다.</p>
            
            <h3>일반 설정</h3>
            <ul>
                <li><b>언어</b>: 한국어, 영어, 일본어 중 선택</li>
                <li><b>테마</b>: 라이트, 다크, 시스템 테마 중 선택</li>
                <li><b>자동 저장</b>: 자동 저장 기능 사용 여부 및 간격 설정</li>
            </ul>
            
            <h3>데이터베이스 설정</h3>
            <ul>
                <li>데이터베이스 연결 정보를 설정합니다.</li>
                <li>연결 테스트를 수행할 수 있습니다.</li>
                <li>데이터베이스 백업 설정을 구성합니다.</li>
            </ul>
            
            <h3>API 설정</h3>
            <ul>
                <li>API 서버 URL과 버전을 설정합니다.</li>
                <li>인증 관련 옵션을 구성합니다.</li>
                <li>API 연결 테스트를 수행할 수 있습니다.</li>
            </ul>
            
            <h3>백업 설정</h3>
            <ul>
                <li>자동 백업 사용 여부와 주기를 설정합니다.</li>
                <li>백업 파일 저장 경로를 지정합니다.</li>
                <li>백업 보관 기간을 설정합니다.</li>
            </ul>
            """
        }
        
        content = content_map.get(title, f"<h2>{title}</h2><p>이 항목에 대한 상세한 가이드는 준비 중입니다.</p>")
        self.guide_content.setHtml(content)
    
    def setup_faq_tab(self):
        """FAQ 탭"""
        faq_widget = QWidget()
        layout = QVBoxLayout(faq_widget)
        layout.setSpacing(20)
        
        # FAQ 목록
        faqs = [
            {
                "question": "CMA는 어떤 시스템인가요?",
                "answer": "CMA(Construction Management System)는 건설 프로젝트의 계약, 재무, 노무 관리를 통합적으로 지원하는 시스템입니다. 건설업계의 특성을 고려하여 설계되었으며, 효율적인 프로젝트 관리를 도와줍니다."
            },
            {
                "question": "로그인이 되지 않습니다. 어떻게 해야 하나요?",
                "answer": "사용자명과 비밀번호를 정확히 입력했는지 확인해주세요. 계정이 잠겼거나 비밀번호가 만료된 경우 관리자에게 문의하세요. 네트워크 연결 상태도 확인해주세요."
            },
            {
                "question": "데이터를 백업하려면 어떻게 해야 하나요?",
                "answer": "설정 > 백업 탭에서 수동 백업 버튼을 클릭하거나, 자동 백업을 설정할 수 있습니다. 백업 파일은 지정한 경로에 저장되며, 필요시 복원할 수 있습니다."
            },
            {
                "question": "계약 데이터를 Excel로 내보낼 수 있나요?",
                "answer": "네, 계약 관리 탭에서 '내보내기' 버튼을 클릭하면 Excel 형태로 데이터를 내보낼 수 있습니다. 다양한 형식과 필터 옵션을 제공합니다."
            },
            {
                "question": "시스템이 느리게 작동합니다. 어떻게 개선할 수 있나요?",
                "answer": "데이터베이스 연결 상태를 확인하고, 불필요한 데이터를 정리해보세요. 시스템 설정에서 성능 최적화 옵션을 조정할 수도 있습니다."
            },
            {
                "question": "여러 사용자가 동시에 사용할 수 있나요?",
                "answer": "네, CMA는 다중 사용자 환경을 지원합니다. 각 사용자는 자신의 권한에 따라 데이터에 접근할 수 있으며, 동시 편집 시 충돌 방지 기능이 제공됩니다."
            },
            {
                "question": "모바일에서도 사용할 수 있나요?",
                "answer": "현재는 데스크톱 애플리케이션으로만 제공되며, 모바일 지원은 추후 개발 예정입니다. 웹 버전도 계획 중에 있습니다."
            },
            {
                "question": "기술 지원은 어떻게 받을 수 있나요?",
                "answer": "이메일이나 전화를 통해 기술 지원을 받을 수 있습니다. 자세한 연락처는 '정보' 탭에서 확인할 수 있습니다."
            }
        ]
        
        for i, faq in enumerate(faqs, 1):
            faq_group = QGroupBox(f"Q{i}. {faq['question']}")
            faq_layout = QVBoxLayout(faq_group)
            
            answer_label = QLabel(f"<b>A.</b> {faq['answer']}")
            answer_label.setWordWrap(True)
            answer_label.setStyleSheet("padding: 10px; background-color: #f8f9fa; border-radius: 4px;")
            faq_layout.addWidget(answer_label)
            
            layout.addWidget(faq_group)
        
        layout.addStretch()
        self.help_tabs.addTab(faq_widget, "FAQ")
    
    def setup_troubleshooting_tab(self):
        """문제 해결 탭"""
        troubleshooting_widget = QWidget()
        layout = QVBoxLayout(troubleshooting_widget)
        layout.setSpacing(20)
        
        # 일반적인 문제 해결
        common_issues_group = QGroupBox("일반적인 문제 해결")
        common_layout = QVBoxLayout(common_issues_group)
        
        issues = [
            {
                "problem": "로그인 실패",
                "solutions": [
                    "사용자명과 비밀번호를 다시 확인하세요.",
                    "대소문자를 정확히 입력했는지 확인하세요.",
                    "계정이 잠겼는지 확인하세요.",
                    "네트워크 연결을 확인하세요."
                ]
            },
            {
                "problem": "데이터가 저장되지 않음",
                "solutions": [
                    "필수 필드를 모두 입력했는지 확인하세요.",
                    "데이터베이스 연결 상태를 확인하세요.",
                    "권한이 있는지 확인하세요.",
                    "시스템을 재시작해보세요."
                ]
            },
            {
                "problem": "시스템이 느림",
                "solutions": [
                    "불필요한 데이터를 정리하세요.",
                    "시스템 리소스 사용량을 확인하세요.",
                    "데이터베이스 연결을 최적화하세요.",
                    "캐시를 정리해보세요."
                ]
            },
            {
                "problem": "인쇄가 되지 않음",
                "solutions": [
                    "프린터 연결 상태를 확인하세요.",
                    "프린터 드라이버를 업데이트하세요.",
                    "인쇄 설정을 확인하세요.",
                    "다른 프린터로 시도해보세요."
                ]
            }
        ]
        
        for issue in issues:
            issue_frame = QFrame()
            issue_frame.setFrameStyle(QFrame.StyledPanel)
            issue_layout = QVBoxLayout(issue_frame)
            
            problem_label = QLabel(f"<b>문제:</b> {issue['problem']}")
            problem_label.setStyleSheet("color: #e74c3c; font-size: 14px; margin-bottom: 5px;")
            issue_layout.addWidget(problem_label)
            
            solutions_label = QLabel("<b>해결 방법:</b>")
            solutions_label.setStyleSheet("margin-top: 10px;")
            issue_layout.addWidget(solutions_label)
            
            for solution in issue['solutions']:
                solution_label = QLabel(f"• {solution}")
                solution_label.setStyleSheet("margin-left: 20px;")
                issue_layout.addWidget(solution_label)
            
            common_layout.addWidget(issue_frame)
        
        layout.addWidget(common_issues_group)
        
        # 시스템 진단
        diagnosis_group = QGroupBox("시스템 진단")
        diagnosis_layout = QVBoxLayout(diagnosis_group)
        
        diagnosis_text = QLabel("""
        <p>시스템 진단을 통해 현재 상태를 확인할 수 있습니다.</p>
        <ul>
            <li>데이터베이스 연결 상태</li>
            <li>API 서버 연결 상태</li>
            <li>시스템 리소스 사용량</li>
            <li>설정 파일 상태</li>
        </ul>
        """)
        diagnosis_text.setWordWrap(True)
        diagnosis_layout.addWidget(diagnosis_text)
        
        diagnose_button = QPushButton("시스템 진단 실행")
        diagnose_button.setStyleSheet("""
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
        diagnose_button.clicked.connect(self.run_system_diagnosis)
        diagnosis_layout.addWidget(diagnose_button)
        
        layout.addWidget(diagnosis_group)
        layout.addStretch()
        
        self.help_tabs.addTab(troubleshooting_widget, "문제 해결")
    
    def setup_about_tab(self):
        """정보 탭"""
        about_widget = QWidget()
        layout = QVBoxLayout(about_widget)
        layout.setSpacing(20)
        
        # 애플리케이션 정보
        app_info_group = QGroupBox("애플리케이션 정보")
        app_layout = QVBoxLayout(app_info_group)
        
        app_info_text = QLabel("""
        <h3>CMA - Construction Management System</h3>
        <p><b>버전:</b> 2.0.0</p>
        <p><b>개발사:</b> CMA Development Team</p>
        <p><b>라이선스:</b> Proprietary</p>
        <p><b>빌드 날짜:</b> 2025년 1월</p>
        <p><b>Python 버전:</b> 3.12+</p>
        <p><b>PySide6 버전:</b> 6.6.1</p>
        """)
        app_info_text.setWordWrap(True)
        app_layout.addWidget(app_info_text)
        
        layout.addWidget(app_info_group)
        
        # 개발팀 정보
        team_group = QGroupBox("개발팀")
        team_layout = QVBoxLayout(team_group)
        
        team_text = QLabel("""
        <h4>개발팀 구성</h4>
        <ul>
            <li><b>프로젝트 매니저:</b> [이름]</li>
            <li><b>백엔드 개발:</b> [이름]</li>
            <li><b>프론트엔드 개발:</b> [이름]</li>
            <li><b>UI/UX 디자인:</b> [이름]</li>
            <li><b>테스트:</b> [이름]</li>
        </ul>
        """)
        team_text.setWordWrap(True)
        team_layout.addWidget(team_text)
        
        layout.addWidget(team_group)
        
        # 연락처 정보
        contact_group = QGroupBox("연락처")
        contact_layout = QVBoxLayout(contact_group)
        
        contact_text = QLabel("""
        <h4>기술 지원</h4>
        <p><b>이메일:</b> support@cma-system.com</p>
        <p><b>전화:</b> 02-1234-5678</p>
        <p><b>팩스:</b> 02-1234-5679</p>
        <p><b>주소:</b> 서울특별시 강남구 테헤란로 123</p>
        <p><b>웹사이트:</b> <a href="https://www.cma-system.com">www.cma-system.com</a></p>
        """)
        contact_text.setWordWrap(True)
        contact_text.setOpenExternalLinks(True)
        contact_layout.addWidget(contact_text)
        
        layout.addWidget(contact_group)
        
        # 라이선스 정보
        license_group = QGroupBox("라이선스 정보")
        license_layout = QVBoxLayout(license_group)
        
        license_text = QLabel("""
        <p>CMA는 독점 소프트웨어입니다. 무단 복제 및 배포를 금지합니다.</p>
        <p>사용권은 구매 시 제공되는 라이선스 계약에 따릅니다.</p>
        <p>기술 지원은 유지보수 계약에 포함됩니다.</p>
        """)
        license_text.setWordWrap(True)
        license_layout.addWidget(license_text)
        
        layout.addWidget(license_group)
        layout.addStretch()
        
        self.help_tabs.addTab(about_widget, "정보")
    
    def run_system_diagnosis(self):
        """시스템 진단 실행"""
        QMessageBox.information(self, "알림", "시스템 진단 기능은 추후 구현 예정입니다.") 