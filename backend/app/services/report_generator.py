from typing import List, Optional
from datetime import datetime
import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import pandas as pd
from app.core.config import settings

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