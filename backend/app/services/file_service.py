import os
import shutil
from datetime import datetime
from typing import Optional, Tuple
from fastapi import UploadFile
import aiofiles
from pathlib import Path

class FileService:
    def __init__(self, base_upload_dir: str = "uploads"):
        self.base_upload_dir = base_upload_dir
        self._ensure_upload_dirs()

    def _ensure_upload_dirs(self):
        """필요한 업로드 디렉토리들을 생성합니다."""
        # 기본 업로드 디렉토리
        os.makedirs(self.base_upload_dir, exist_ok=True)
        
        # 문서 유형별 디렉토리
        document_types = [
            # 계약 관련
            "contracts/construction",     # 공사계약서
            "contracts/material",         # 자재계약서
            "contracts/equipment",        # 장비계약서
            "contracts/subcontract",      # 하도급계약서
            "contracts/others",           # 기타계약서
            
            # 도면 관련
            "drawings/architectural",     # 건축도면
            "drawings/structural",        # 구조도면
            "drawings/mechanical",        # 기계설비도면
            "drawings/electrical",        # 전기설비도면
            "drawings/plumbing",          # 위생설비도면
            "drawings/fire",              # 소방설비도면
            "drawings/landscape",         # 조경도면
            "drawings/interior",          # 인테리어도면
            "drawings/asbuilt",           # 준공도면
            "drawings/others",            # 기타도면
            
            # 시방서 관련
            "specs/general",              # 일반시방서
            "specs/architectural",        # 건축시방서
            "specs/structural",           # 구조시방서
            "specs/mechanical",           # 기계설비시방서
            "specs/electrical",           # 전기설비시방서
            "specs/plumbing",             # 위생설비시방서
            "specs/fire",                 # 소방설비시방서
            "specs/landscape",            # 조경시방서
            "specs/interior",             # 인테리어시방서
            "specs/others",               # 기타시방서
            
            # 허가 관련
            "permits/building",           # 건축허가
            "permits/construction",       # 공사허가
            "permits/environmental",      # 환경허가
            "permits/safety",             # 안전허가
            "permits/others",             # 기타허가
            
            # 보고서 관련
            "reports/progress",           # 공정보고서
            "reports/safety",             # 안전보고서
            "reports/quality",            # 품질보고서
            "reports/inspection",         # 검사보고서
            "reports/meeting",            # 회의보고서
            "reports/incident",           # 사고보고서
            "reports/completion",         # 준공보고서
            "reports/others",             # 기타보고서
            
            # 검사 관련
            "inspections/safety",         # 안전검사
            "inspections/quality",        # 품질검사
            "inspections/equipment",      # 장비검사
            "inspections/material",       # 자재검사
            "inspections/completion",     # 준공검사
            "inspections/others",         # 기타검사
            
            # 안전 관련
            "safety/plans",               # 안전계획서
            "safety/training",            # 안전교육
            "safety/inspection",          # 안전점검
            "safety/incident",            # 사고기록
            "safety/others",              # 기타안전문서
            
            # 품질 관련
            "quality/plans",              # 품질계획서
            "quality/control",            # 품질관리
            "quality/test",               # 시험성적서
            "quality/certification",      # 인증서
            "quality/others",             # 기타품질문서
            
            # 재무 관련
            "financial/contracts",        # 계약금액
            "financial/estimates",        # 견적서
            "financial/invoices",         # 청구서
            "financial/payments",         # 지급서
            "financial/taxes",            # 세금관련
            "financial/others",           # 기타재무문서
            
            # 기타 문서
            "others/official/contract_submission",    # 계약제출서류
            "others/official/construction_start",     # 착공신고
            "others/official/completion",            # 준공신고
            "others/official/change_management",     # 변경관리
            "others/official/approval",              # 승인서류
            "others/official/report",                # 제출보고서
            "others/official/notification",          # 통지서류
            "others/official/others",                # 기타공문서
            
            # 공지사항
            "others/notices/general",                # 일반공지
            "others/notices/safety",                 # 안전공지
            "others/notices/quality",                # 품질공지
            "others/notices/meeting",                # 회의공지
            "others/notices/others",                 # 기타공지
            
            # 매뉴얼
            "others/manuals/operation",              # 운영매뉴얼
            "others/manuals/maintenance",            # 유지보수매뉴얼
            "others/manuals/safety",                 # 안전매뉴얼
            "others/manuals/quality",                # 품질매뉴얼
            "others/manuals/others",                 # 기타매뉴얼
            
            # 양식
            "others/forms/contract",                 # 계약양식
            "others/forms/report",                   # 보고서양식
            "others/forms/inspection",               # 검사양식
            "others/forms/approval",                 # 승인양식
            "others/forms/others",                   # 기타양식
            
            # 기타문서
            "others/miscellaneous"                   # 기타문서
        ]
        
        for doc_type in document_types:
            os.makedirs(os.path.join(self.base_upload_dir, doc_type), exist_ok=True)

    async def save_file(
        self,
        file: UploadFile,
        document_type: str,
        document_id: int,
        version: Optional[str] = None
    ) -> Tuple[str, str, int]:
        """
        파일을 저장하고 파일 정보를 반환합니다.
        
        Args:
            file: 업로드된 파일
            document_type: 문서 유형
            document_id: 문서 ID
            version: 문서 버전 (선택사항)
            
        Returns:
            Tuple[str, str, int]: (파일 URL, 파일명, 파일 크기)
        """
        # 파일 확장자 확인
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        # 허용된 파일 형식 검증
        allowed_extensions = {
            # 문서
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            # 도면
            '.dwg', '.dxf', '.rvt', '.ifc',
            # 이미지
            '.jpg', '.jpeg', '.png', '.gif', '.bmp',
            # 기타
            '.txt', '.csv', '.zip', '.rar'
        }
        
        if file_ext not in allowed_extensions:
            raise ValueError(f"지원하지 않는 파일 형식입니다: {file_ext}")
        
        # 저장 경로 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if version:
            filename = f"{document_id}_v{version}_{timestamp}{file_ext}"
        else:
            filename = f"{document_id}_{timestamp}{file_ext}"
            
        save_path = os.path.join(self.base_upload_dir, document_type, filename)
        
        # 파일 저장
        async with aiofiles.open(save_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        # 파일 URL 생성 (실제 구현에서는 CDN이나 스토리지 서비스 URL로 대체)
        file_url = f"/uploads/{document_type}/{filename}"
        
        return file_url, filename, len(content)

    def delete_file(self, file_url: str) -> bool:
        """
        파일을 삭제합니다.
        
        Args:
            file_url: 삭제할 파일의 URL
            
        Returns:
            bool: 삭제 성공 여부
        """
        try:
            # URL에서 실제 파일 경로 추출
            file_path = os.path.join(self.base_upload_dir, file_url.lstrip('/uploads/'))
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False

    def get_file_info(self, file_url: str) -> Optional[dict]:
        """
        파일 정보를 조회합니다.
        
        Args:
            file_url: 파일 URL
            
        Returns:
            Optional[dict]: 파일 정보 (크기, 생성일, 수정일 등)
        """
        try:
            file_path = os.path.join(self.base_upload_dir, file_url.lstrip('/uploads/'))
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                return {
                    "size": stat.st_size,
                    "created_at": datetime.fromtimestamp(stat.st_ctime),
                    "modified_at": datetime.fromtimestamp(stat.st_mtime),
                    "file_type": os.path.splitext(file_path)[1]
                }
            return None
        except Exception:
            return None

    def move_file(self, old_url: str, new_document_type: str) -> Optional[str]:
        """
        파일을 다른 문서 유형 디렉토리로 이동합니다.
        
        Args:
            old_url: 현재 파일 URL
            new_document_type: 새로운 문서 유형
            
        Returns:
            Optional[str]: 새로운 파일 URL
        """
        try:
            old_path = os.path.join(self.base_upload_dir, old_url.lstrip('/uploads/'))
            if os.path.exists(old_path):
                filename = os.path.basename(old_path)
                new_path = os.path.join(self.base_upload_dir, new_document_type, filename)
                shutil.move(old_path, new_path)
                return f"/uploads/{new_document_type}/{filename}"
            return None
        except Exception:
            return None 