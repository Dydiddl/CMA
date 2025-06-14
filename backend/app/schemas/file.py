from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

# 공유 속성
class FileBase(BaseModel):
    description: Optional[str] = Field(None, description="파일 설명")

# 생성 시 필요한 속성
class FileCreate(FileBase):
    project_id: Optional[int] = Field(None, description="프로젝트 ID")
    task_id: Optional[int] = Field(None, description="작업 ID")

# 업데이트 시 필요한 속성
class FileUpdate(FileBase):
    pass

# API 응답에 포함되는 속성
class File(FileBase):
    id: int
    filename: str
    original_filename: str
    file_path: str
    file_type: str
    file_size: int
    project_id: Optional[int]
    task_id: Optional[int]
    uploader_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 