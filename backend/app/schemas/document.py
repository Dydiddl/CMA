from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel

from app.models.document import DocumentType, DocumentStatus

# Document 스키마
class DocumentBase(BaseModel):
    document_number: str
    title: str
    document_type: DocumentType
    description: Optional[str] = None
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    version: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class DocumentCreate(DocumentBase):
    construction_id: Optional[int] = None
    contract_id: Optional[int] = None
    department_id: Optional[int] = None

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    version: Optional[str] = None
    status: Optional[DocumentStatus] = None
    metadata: Optional[Dict[str, Any]] = None
    department_id: Optional[int] = None

class Document(DocumentBase):
    id: int
    status: DocumentStatus
    construction_id: Optional[int] = None
    contract_id: Optional[int] = None
    created_by: int
    updated_by: int
    department_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# DocumentVersion 스키마
class DocumentVersionBase(BaseModel):
    version_number: str
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    changes: Optional[str] = None

class DocumentVersionCreate(DocumentVersionBase):
    document_id: int

class DocumentVersion(DocumentVersionBase):
    id: int
    document_id: int
    created_by: int
    created_at: datetime

    class Config:
        orm_mode = True

# DocumentApproval 스키마
class DocumentApprovalBase(BaseModel):
    status: DocumentStatus
    comments: Optional[str] = None

class DocumentApprovalCreate(DocumentApprovalBase):
    document_id: int
    approver_id: int

class DocumentApprovalUpdate(BaseModel):
    status: Optional[DocumentStatus] = None
    comments: Optional[str] = None

class DocumentApproval(DocumentApprovalBase):
    id: int
    document_id: int
    approver_id: int
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 필터 스키마
class DocumentFilter(BaseModel):
    document_number: Optional[str] = None
    title: Optional[str] = None
    document_type: Optional[DocumentType] = None
    status: Optional[DocumentStatus] = None
    construction_id: Optional[int] = None
    contract_id: Optional[int] = None
    department_id: Optional[int] = None
    created_by: Optional[int] = None
    created_at_from: Optional[datetime] = None
    created_at_to: Optional[datetime] = None

class DocumentVersionFilter(BaseModel):
    document_id: Optional[int] = None
    version_number: Optional[str] = None
    created_by: Optional[int] = None
    created_at_from: Optional[datetime] = None
    created_at_to: Optional[datetime] = None

class DocumentApprovalFilter(BaseModel):
    document_id: Optional[int] = None
    approver_id: Optional[int] = None
    status: Optional[DocumentStatus] = None
    created_at_from: Optional[datetime] = None
    created_at_to: Optional[datetime] = None 