from typing import List, Optional, Dict
from datetime import datetime, timedelta
import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import pandas as pd
from app.core.config import settings
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract

from app.models.cost import Cost, CostType, CostCategory
from app.models.budget import Budget
from app.schemas.cost import CostStatistics

class ReportGenerator:
    def __init__(self):
        self.template_dir = os.path.join(settings.BASE_DIR, "templates")
        self.output_dir = os.path.join(settings.BASE_DIR, "reports")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir)
        )
    
    def generate_project_report(
        self,
        project: Any,
        tasks: List[Any],
        report_type: str = "pdf"
    ) -> str:
        """
        프로젝트 보고서 생성
        """
        template = self.env.get_template("project_report.html")
        
        # 작업 통계 계산
        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t.status == "done")
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # HTML 생성
        html_content = template.render(
            project=project,
            tasks=tasks,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            progress=progress,
            generated_at=datetime.now()
        )
        
        # PDF 생성
        output_path = os.path.join(
            self.output_dir,
            f"project_report_{project.id}_{datetime.now().strftime('%Y%m%d')}.pdf"
        )
        HTML(string=html_content).write_pdf(output_path)
        
        return output_path
    
    def generate_tasks_report(
        self,
        tasks: List[Any],
        report_type: str = "pdf"
    ) -> str:
        """
        작업 보고서 생성
        """
        template = self.env.get_template("tasks_report.html")
        
        # 작업 상태별 통계
        status_counts = {}
        for task in tasks:
            status_counts[task.status] = status_counts.get(task.status, 0) + 1
        
        # HTML 생성
        html_content = template.render(
            tasks=tasks,
            status_counts=status_counts,
            generated_at=datetime.now()
        )
        
        # PDF 생성
        output_path = os.path.join(
            self.output_dir,
            f"tasks_report_{datetime.now().strftime('%Y%m%d')}.pdf"
        )
        HTML(string=html_content).write_pdf(output_path)
        
        return output_path
    
    def generate_summary_report(
        self,
        projects: List[Any],
        tasks: List[Any],
        period: str,
        report_type: str = "pdf"
    ) -> str:
        """
        요약 보고서 생성
        """
        template = self.env.get_template("summary_report.html")
        
        # 프로젝트 통계
        project_stats = {
            "total": len(projects),
            "active": sum(1 for p in projects if p.is_active),
            "completed": sum(1 for p in projects if p.status == "completed")
        }
        
        # 작업 통계
        task_stats = {
            "total": len(tasks),
            "completed": sum(1 for t in tasks if t.status == "done"),
            "overdue": sum(1 for t in tasks if t.due_date and t.due_date < datetime.now())
        }
        
        # HTML 생성
        html_content = template.render(
            projects=projects,
            tasks=tasks,
            project_stats=project_stats,
            task_stats=task_stats,
            period=period,
            generated_at=datetime.now()
        )
        
        # PDF 생성
        output_path = os.path.join(
            self.output_dir,
            f"summary_report_{period}_{datetime.now().strftime('%Y%m%d')}.pdf"
        )
        HTML(string=html_content).write_pdf(output_path)
        
        return output_path

class CostReportGenerator:
    def __init__(self, db: Session):
        self.db = db

    def generate_monthly_report(self, project_id: int, year: int, month: int) -> Dict:
        """월별 비용 리포트 생성"""
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        # 비용 데이터 조회
        costs = self.db.query(Cost).filter(
            and_(
                Cost.project_id == project_id,
                Cost.payment_date >= start_date,
                Cost.payment_date < end_date
            )
        ).all()

        # 예산 데이터 조회
        budget = self.db.query(Budget).filter(
            and_(
                Budget.project_id == project_id,
                Budget.year == year,
                Budget.month == month
            )
        ).first()

        # 비용 통계 계산
        total_cost = sum(cost.amount for cost in costs)
        cost_by_type = self._calculate_cost_by_type(costs)
        cost_by_category = self._calculate_cost_by_category(costs)

        # 예산 대비 실적
        budget_vs_actual = self._compare_budget_actual(budget, costs)

        return {
            "period": f"{year}년 {month}월",
            "total_cost": total_cost,
            "cost_by_type": cost_by_type,
            "cost_by_category": cost_by_category,
            "budget_vs_actual": budget_vs_actual,
            "generated_at": datetime.utcnow()
        }

    def generate_quarterly_report(self, project_id: int, year: int, quarter: int) -> Dict:
        """분기별 비용 리포트 생성"""
        start_month = (quarter - 1) * 3 + 1
        end_month = quarter * 3 + 1
        start_date = datetime(year, start_month, 1)
        end_date = datetime(year, end_month, 1)

        # 비용 데이터 조회
        costs = self.db.query(Cost).filter(
            and_(
                Cost.project_id == project_id,
                Cost.payment_date >= start_date,
                Cost.payment_date < end_date
            )
        ).all()

        # 예산 데이터 조회
        budgets = self.db.query(Budget).filter(
            and_(
                Budget.project_id == project_id,
                Budget.year == year,
                Budget.month >= start_month,
                Budget.month < end_month
            )
        ).all()

        # 비용 통계 계산
        total_cost = sum(cost.amount for cost in costs)
        cost_by_type = self._calculate_cost_by_type(costs)
        cost_by_category = self._calculate_cost_by_category(costs)
        monthly_trend = self._calculate_monthly_trend(costs, start_month, end_month)

        # 예산 대비 실적
        budget_vs_actual = self._compare_budget_actual_quarterly(budgets, costs)

        return {
            "period": f"{year}년 {quarter}분기",
            "total_cost": total_cost,
            "cost_by_type": cost_by_type,
            "cost_by_category": cost_by_category,
            "monthly_trend": monthly_trend,
            "budget_vs_actual": budget_vs_actual,
            "generated_at": datetime.utcnow()
        }

    def generate_yearly_report(self, project_id: int, year: int) -> Dict:
        """연도별 비용 리포트 생성"""
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1)

        # 비용 데이터 조회
        costs = self.db.query(Cost).filter(
            and_(
                Cost.project_id == project_id,
                Cost.payment_date >= start_date,
                Cost.payment_date < end_date
            )
        ).all()

        # 예산 데이터 조회
        budgets = self.db.query(Budget).filter(
            and_(
                Budget.project_id == project_id,
                Budget.year == year
            )
        ).all()

        # 비용 통계 계산
        total_cost = sum(cost.amount for cost in costs)
        cost_by_type = self._calculate_cost_by_type(costs)
        cost_by_category = self._calculate_cost_by_category(costs)
        quarterly_trend = self._calculate_quarterly_trend(costs)
        monthly_trend = self._calculate_monthly_trend(costs, 1, 13)

        # 예산 대비 실적
        budget_vs_actual = self._compare_budget_actual_yearly(budgets, costs)

        return {
            "period": f"{year}년",
            "total_cost": total_cost,
            "cost_by_type": cost_by_type,
            "cost_by_category": cost_by_category,
            "quarterly_trend": quarterly_trend,
            "monthly_trend": monthly_trend,
            "budget_vs_actual": budget_vs_actual,
            "generated_at": datetime.utcnow()
        }

    def _calculate_cost_by_type(self, costs: List[Cost]) -> Dict:
        """비용 유형별 집계"""
        result = {cost_type.value: 0 for cost_type in CostType}
        for cost in costs:
            result[cost.cost_type.value] += cost.amount
        return result

    def _calculate_cost_by_category(self, costs: List[Cost]) -> Dict:
        """비용 카테고리별 집계"""
        result = {category.value: 0 for category in CostCategory}
        for cost in costs:
            result[cost.category.value] += cost.amount
        return result

    def _calculate_monthly_trend(self, costs: List[Cost], start_month: int, end_month: int) -> Dict:
        """월별 추이 계산"""
        result = {month: 0 for month in range(start_month, end_month)}
        for cost in costs:
            month = cost.payment_date.month
            if start_month <= month < end_month:
                result[month] += cost.amount
        return result

    def _calculate_quarterly_trend(self, costs: List[Cost]) -> Dict:
        """분기별 추이 계산"""
        result = {quarter: 0 for quarter in range(1, 5)}
        for cost in costs:
            month = cost.payment_date.month
            quarter = (month - 1) // 3 + 1
            result[quarter] += cost.amount
        return result

    def _compare_budget_actual(self, budget: Optional[Budget], costs: List[Cost]) -> Dict:
        """예산 대비 실적 비교"""
        if not budget:
            return {
                "budget": 0,
                "actual": sum(cost.amount for cost in costs),
                "variance": 0,
                "variance_percentage": 0
            }

        actual = sum(cost.amount for cost in costs)
        variance = actual - budget.total_amount
        variance_percentage = (variance / budget.total_amount * 100) if budget.total_amount > 0 else 0

        return {
            "budget": budget.total_amount,
            "actual": actual,
            "variance": variance,
            "variance_percentage": variance_percentage
        }

    def _compare_budget_actual_quarterly(self, budgets: List[Budget], costs: List[Cost]) -> Dict:
        """분기별 예산 대비 실적 비교"""
        total_budget = sum(budget.total_amount for budget in budgets)
        total_actual = sum(cost.amount for cost in costs)
        variance = total_actual - total_budget
        variance_percentage = (variance / total_budget * 100) if total_budget > 0 else 0

        return {
            "budget": total_budget,
            "actual": total_actual,
            "variance": variance,
            "variance_percentage": variance_percentage
        }

    def _compare_budget_actual_yearly(self, budgets: List[Budget], costs: List[Cost]) -> Dict:
        """연도별 예산 대비 실적 비교"""
        total_budget = sum(budget.total_amount for budget in budgets)
        total_actual = sum(cost.amount for cost in costs)
        variance = total_actual - total_budget
        variance_percentage = (variance / total_budget * 100) if total_budget > 0 else 0

        return {
            "budget": total_budget,
            "actual": total_actual,
            "variance": variance,
            "variance_percentage": variance_percentage
        } 