from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.document import DocumentType, DocumentStatus

# 기본 스키마
class DocumentBase(BaseModel):
    project_id: int
    document_type: DocumentType
    title: str
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

# 생성 스키마
class DocumentCreate(DocumentBase):
    pass

# 업데이트 스키마
class DocumentUpdate(BaseModel):
    document_type: Optional[DocumentType] = None
    title: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

# 버전 스키마
class DocumentVersionBase(BaseModel):
    version_number: int
    file_path: str
    file_name: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    changes: Optional[str] = None

class DocumentVersionCreate(DocumentVersionBase):
    pass

class DocumentVersion(DocumentVersionBase):
    id: int
    document_id: int
    created_by: int
    created_at: datetime

    class Config:
        orm_mode = True

# 태그 스키마
class DocumentTagBase(BaseModel):
    name: str

class DocumentTagCreate(DocumentTagBase):
    pass

class DocumentTag(DocumentTagBase):
    id: int
    document_id: int
    created_by: int
    created_at: datetime

    class Config:
        orm_mode = True

# 댓글 스키마
class DocumentCommentBase(BaseModel):
    content: str
    is_resolved: bool = False

class DocumentCommentCreate(DocumentCommentBase):
    pass

class DocumentCommentUpdate(BaseModel):
    content: Optional[str] = None
    is_resolved: Optional[bool] = None

class DocumentComment(DocumentCommentBase):
    id: int
    document_id: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 공유 스키마
class DocumentShareBase(BaseModel):
    user_id: int
    permission: str
    expires_at: Optional[datetime] = None

class DocumentShareCreate(DocumentShareBase):
    pass

class DocumentShareUpdate(BaseModel):
    permission: Optional[str] = None
    expires_at: Optional[datetime] = None

class DocumentShare(DocumentShareBase):
    id: int
    document_id: int
    created_by: int
    created_at: datetime

    class Config:
        orm_mode = True

# 문서 응답 스키마
class Document(DocumentBase):
    id: int
    file_path: str
    file_name: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    version: int
    status: DocumentStatus
    created_by: int
    approved_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    versions: List[DocumentVersion] = []
    tags: List[DocumentTag] = []
    comments: List[DocumentComment] = []

    class Config:
        orm_mode = True

# 필터 스키마
class DocumentFilter(BaseModel):
    project_id: Optional[int] = None
    document_type: Optional[DocumentType] = None
    status: Optional[DocumentStatus] = None
    created_by: Optional[int] = None
    tag: Optional[str] = None
    search: Optional[str] = None
    skip: int = 0
    limit: int = 100

# 통계 스키마
class DocumentStatistics(BaseModel):
    total_documents: int
    documents_by_type: Dict[str, int]
    documents_by_status: Dict[str, int]
    total_size: int
    recent_uploads: List[Document]
    popular_tags: Dict[str, int]
    active_users: Dict[str, int]

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