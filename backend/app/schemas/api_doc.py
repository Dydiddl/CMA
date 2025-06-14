from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.api_doc import APIDocStatus, APIDocType

# Base schemas
class APIDocBase(BaseModel):
    title: str
    description: Optional[str] = None
    doc_type: APIDocType
    status: APIDocStatus = APIDocStatus.DRAFT
    version: Optional[str] = None
    endpoint: Optional[str] = None
    method: Optional[str] = None
    request_schema: Optional[Dict[str, Any]] = None
    response_schema: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None
    examples: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class APIDocVersionBase(BaseModel):
    version_number: str
    content: Dict[str, Any]
    changes: Optional[str] = None

class APIDocTagBase(BaseModel):
    name: str

class APIDocCommentBase(BaseModel):
    content: str
    is_resolved: bool = False

# Create schemas
class APIDocCreate(APIDocBase):
    pass

class APIDocVersionCreate(APIDocVersionBase):
    pass

class APIDocTagCreate(APIDocTagBase):
    pass

class APIDocCommentCreate(APIDocCommentBase):
    pass

# Update schemas
class APIDocUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[APIDocStatus] = None
    version: Optional[str] = None
    endpoint: Optional[str] = None
    method: Optional[str] = None
    request_schema: Optional[Dict[str, Any]] = None
    response_schema: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None
    examples: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class APIDocCommentUpdate(BaseModel):
    content: Optional[str] = None
    is_resolved: Optional[bool] = None

# Response schemas
class APIDocVersion(APIDocVersionBase):
    id: int
    api_doc_id: int
    created_by: int
    created_at: datetime

    class Config:
        orm_mode = True

class APIDocTag(APIDocTagBase):
    id: int
    api_doc_id: int
    created_by: int
    created_at: datetime

    class Config:
        orm_mode = True

class APIDocComment(APIDocCommentBase):
    id: int
    api_doc_id: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class APIDoc(APIDocBase):
    id: int
    created_by: int
    updated_by: int
    created_at: datetime
    updated_at: datetime
    versions: List[APIDocVersion] = []
    tags: List[APIDocTag] = []
    comments: List[APIDocComment] = []

    class Config:
        orm_mode = True

# Filter schemas
class APIDocFilter(BaseModel):
    title: Optional[str] = None
    doc_type: Optional[APIDocType] = None
    status: Optional[APIDocStatus] = None
    version: Optional[str] = None
    endpoint: Optional[str] = None
    method: Optional[str] = None
    created_by: Optional[int] = None
    created_at_from: Optional[datetime] = None
    created_at_to: Optional[datetime] = None

# Statistics schema
class APIDocStatistics(BaseModel):
    total_docs: int
    docs_by_type: Dict[str, int]
    docs_by_status: Dict[str, int]
    docs_by_version: Dict[str, int]
    recent_updates: List[APIDoc]
    popular_tags: Dict[str, int]
    active_users: Dict[int, int]

# API 문서 스키마
class ApiDocBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    content: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1, max_length=50)
    tags: List[str] = Field(default_factory=list)

class ApiDocCreate(ApiDocBase):
    pass

class ApiDocUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    content: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    status: Optional[str] = Field(None, min_length=1, max_length=20)
    tags: Optional[List[str]] = None

class ApiDoc(ApiDocBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    created_by: int
    updated_by: int
    tags: List[APIDocTag]

    class Config:
        orm_mode = True

# API 문서 버전 스키마
class ApiDocVersionBase(BaseModel):
    version: str = Field(..., min_length=1, max_length=20)
    content: str = Field(..., min_length=1)
    changes: Optional[str] = None

class ApiDocVersionCreate(ApiDocVersionBase):
    pass

class ApiDocVersion(ApiDocVersionBase):
    id: int
    api_doc_id: int
    created_at: datetime
    created_by: int

    class Config:
        orm_mode = True

# API 문서 댓글 스키마
class ApiDocCommentBase(BaseModel):
    content: str = Field(..., min_length=1)

class ApiDocCommentCreate(ApiDocCommentBase):
    parent_id: Optional[int] = None

class ApiDocCommentUpdate(BaseModel):
    content: str = Field(..., min_length=1)

class ApiDocComment(ApiDocCommentBase):
    id: int
    api_doc_id: int
    parent_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    created_by: int
    updated_by: int

    class Config:
        orm_mode = True

# API 문서 통계 스키마
class ApiDocStatistics(BaseModel):
    total_docs: int
    docs_by_category: Dict[str, int]
    docs_by_status: Dict[str, int]
    recent_updates: List[Dict[str, Any]]

    class Config:
        orm_mode = True

# 응답 스키마
class ApiDocResponse(BaseModel):
    items: List[ApiDoc]
    total: int

class ApiDocVersionResponse(BaseModel):
    items: List[ApiDocVersion]
    total: int

class ApiDocCommentResponse(BaseModel):
    items: List[ApiDocComment]
    total: int 