from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# 공유 속성
class FileBase(BaseModel):
    filename: str
    file_path: str
    file_size: int
    file_type: str

# 생성 시 필요한 속성
class FileCreate(FileBase):
    uploaded_by: int

# 업데이트 시 필요한 속성
class FileUpdate(BaseModel):
    filename: Optional[str] = None
    file_type: Optional[str] = None

# API 응답에 포함되는 속성
class FileInDB(FileBase):
    id: int
    uploaded_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class FileResponse(FileInDB):
    pass

class FileList(BaseModel):
    items: List[FileResponse]
    total: int
    skip: int
    limit: int 