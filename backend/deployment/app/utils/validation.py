"""
데이터 검증 유틸리티 함수
"""
import re
from typing import Any, Dict, List, Optional

def validate_email(email: str) -> bool:
    """
    이메일 형식 검증
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> bool:
    """
    비밀번호 강도 검증
    - 최소 8자
    - 대문자, 소문자, 숫자, 특수문자 포함
    """
    if len(password) < 8:
        return False
    
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    
    return all([has_upper, has_lower, has_digit, has_special])

def validate_phone_number(phone: str) -> bool:
    """
    전화번호 형식 검증
    """
    pattern = r'^\+?1?\d{9,15}$'
    return bool(re.match(pattern, phone))

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> Optional[str]:
    """
    필수 필드 검증
    """
    for field in required_fields:
        if field not in data or data[field] is None:
            return f"Missing required field: {field}"
    return None

def sanitize_input(text: str) -> str:
    """
    입력 데이터 정제
    - HTML 태그 제거
    - 특수문자 이스케이프
    """
    # HTML 태그 제거
    text = re.sub(r'<[^>]+>', '', text)
    # 특수문자 이스케이프
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#x27;')
    return text 