from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.budget import BudgetType, BudgetStatus, BudgetCategory

# 기본 스키마
class BudgetBase(BaseModel):
    project_id: int
    budget_type: BudgetType
    total_amount: float
    start_date: datetime
    end_date: datetime
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

# 생성 스키마
class BudgetCreate(BudgetBase):
    pass

# 업데이트 스키마
class BudgetUpdate(BaseModel):
    budget_type: Optional[BudgetType] = None
    total_amount: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

# 예산 항목 스키마
class BudgetItemBase(BaseModel):
    category: BudgetCategory
    subcategory: str
    description: str
    amount: float
    unit: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None

class BudgetItemCreate(BudgetItemBase):
    pass

class BudgetItemUpdate(BaseModel):
    category: Optional[BudgetCategory] = None
    subcategory: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    unit: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None

class BudgetItem(BudgetItemBase):
    id: int
    budget_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 첨부파일 스키마
class BudgetAttachmentBase(BaseModel):
    file_name: str
    file_path: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    description: Optional[str] = None

class BudgetAttachmentCreate(BudgetAttachmentBase):
    pass

class BudgetAttachment(BudgetAttachmentBase):
    id: int
    budget_id: int
    uploaded_by: int
    created_at: datetime

    class Config:
        orm_mode = True

# 승인 스키마
class BudgetApprovalBase(BaseModel):
    status: BudgetStatus
    comments: Optional[str] = None

class BudgetApprovalCreate(BudgetApprovalBase):
    pass

class BudgetApproval(BudgetApprovalBase):
    id: int
    budget_id: int
    approver_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 알림 스키마
class BudgetAlertBase(BaseModel):
    alert_type: str
    threshold: float
    current_value: float
    message: str
    is_active: bool = True

class BudgetAlertCreate(BudgetAlertBase):
    pass

class BudgetAlertUpdate(BaseModel):
    alert_type: Optional[str] = None
    threshold: Optional[float] = None
    current_value: Optional[float] = None
    message: Optional[str] = None
    is_active: Optional[bool] = None

class BudgetAlert(BudgetAlertBase):
    id: int
    budget_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 예산 응답 스키마
class Budget(BudgetBase):
    id: int
    budget_status: BudgetStatus
    version: int
    created_by: int
    approved_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    items: List[BudgetItem] = []
    attachments: List[BudgetAttachment] = []
    approvals: List[BudgetApproval] = []
    alerts: List[BudgetAlert] = []

    class Config:
        orm_mode = True

# 필터 스키마
class BudgetFilter(BaseModel):
    project_id: Optional[int] = None
    budget_type: Optional[BudgetType] = None
    budget_status: Optional[BudgetStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_by: Optional[int] = None
    skip: int = 0
    limit: int = 100

# 통계 스키마
class BudgetStatistics(BaseModel):
    total_budgets: int
    total_amount: float
    total_actual_cost: float
    total_variance: float
    budget_status_distribution: Dict[str, int]
    category_distribution: Dict[str, float]
    monthly_trend: Dict[str, float]
    variance_by_category: Dict[str, float]
    alert_count: int 