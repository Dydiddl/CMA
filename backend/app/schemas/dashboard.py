from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class ProjectProgress(BaseModel):
    project_id: int
    project_name: str
    progress: float

class ProjectDashboard(BaseModel):
    total_projects: int
    in_progress_count: int
    completed_count: int
    planned_count: int
    project_progress: List[ProjectProgress]

class MonthlyCost(BaseModel):
    year: int
    month: int
    amount: float

class FinancialDashboard(BaseModel):
    total_budget: float
    total_cost: float
    total_contract: float
    total_receivable: float
    monthly_costs: List[MonthlyCost]

class DashboardResponse(BaseModel):
    project_stats: ProjectDashboard
    financial_stats: FinancialDashboard 