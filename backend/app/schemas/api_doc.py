from typing import Optional, List, Dict, Any
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