"""
날짜 관련 유틸리티 함수
"""
from datetime import datetime, timezone
from typing import Optional

def get_current_time() -> datetime:
    """
    현재 UTC 시간을 반환
    """
    return datetime.now(timezone.utc)

def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    datetime 객체를 문자열로 변환
    """
    return dt.strftime(format_str)

def parse_datetime(date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """
    문자열을 datetime 객체로 변환
    """
    try:
        return datetime.strptime(date_str, format_str)
    except ValueError:
        return None

def is_valid_date_range(start_date: datetime, end_date: datetime) -> bool:
    """
    날짜 범위가 유효한지 검사
    """
    return start_date < end_date 