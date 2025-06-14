from app.schemas.common_types import *
from pydantic import BaseModel, UUID4
from typing import Optional, Dict, List
from datetime import datetime

# Department Base Schema
class DepartmentBase(BaseModel):
    name: str
    code: str
    parent_id: Optional[UUID4] = None
    level: int = 1
    description: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    parent_id: Optional[UUID4] = None
    level: Optional[int] = None
    description: Optional[str] = None

class Department(DepartmentBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Department History Schema
class DepartmentHistoryBase(BaseModel):
    action_type: str
    previous_data: Optional[Dict] = None
    new_data: Optional[Dict] = None
    changed_by: UUID4

class DepartmentHistoryCreate(DepartmentHistoryBase):
    department_id: UUID4

class DepartmentHistory(DepartmentHistoryBase):
    id: UUID4
    department_id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True

# Department Tree Schema
class DepartmentTree(Department):
    children: List['DepartmentTree'] = []

    class Config:
        from_attributes = True 