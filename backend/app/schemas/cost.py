from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.cost import CostType, PaymentStatus, CostCategory

# Cost Base Schema
class CostBase(BaseModel):
    project_id: int
    cost_type: CostType
    category: CostCategory
    amount: float = Field(..., gt=0)
    description: Optional[str] = None
    payment_date: Optional[datetime] = None
    payment_method: Optional[str] = None
    payment_reference: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[datetime] = None
    vendor_id: Optional[int] = None
    department_id: Optional[int] = None
    metadata: Optional[dict] = None

# Cost Create Schema
class CostCreate(CostBase):
    pass

# Cost Update Schema
class CostUpdate(BaseModel):
    cost_type: Optional[CostType] = None
    category: Optional[CostCategory] = None
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None
    payment_date: Optional[datetime] = None
    payment_status: Optional[PaymentStatus] = None
    payment_method: Optional[str] = None
    payment_reference: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[datetime] = None
    vendor_id: Optional[int] = None
    department_id: Optional[int] = None
    metadata: Optional[dict] = None

# Cost Schema
class Cost(CostBase):
    id: int
    payment_status: PaymentStatus
    created_by: int
    approved_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Cost Attachment Base Schema
class CostAttachmentBase(BaseModel):
    file_name: str
    file_path: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    description: Optional[str] = None

# Cost Attachment Create Schema
class CostAttachmentCreate(CostAttachmentBase):
    cost_id: int

# Cost Attachment Schema
class CostAttachment(CostAttachmentBase):
    id: int
    cost_id: int
    uploaded_by: int
    uploaded_at: datetime

    class Config:
        orm_mode = True

# Cost Approval Base Schema
class CostApprovalBase(BaseModel):
    cost_id: int
    status: PaymentStatus
    comment: Optional[str] = None
    metadata: Optional[dict] = None

# Cost Approval Create Schema
class CostApprovalCreate(CostApprovalBase):
    pass

# Cost Approval Schema
class CostApproval(CostApprovalBase):
    id: int
    approver_id: int
    approved_at: datetime

    class Config:
        orm_mode = True

# Cost Filter Schema
class CostFilter(BaseModel):
    project_id: Optional[int] = None
    cost_type: Optional[CostType] = None
    category: Optional[CostCategory] = None
    payment_status: Optional[PaymentStatus] = None
    vendor_id: Optional[int] = None
    department_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None

# Cost Statistics Schema
class CostStatistics(BaseModel):
    total_amount: float
    count: int
    by_type: dict[CostType, float]
    by_category: dict[CostCategory, float]
    by_status: dict[PaymentStatus, int]
    by_department: dict[int, float]
    by_vendor: dict[int, float]
    by_month: dict[str, float] 