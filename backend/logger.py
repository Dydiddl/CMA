import logging
import sys
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
from pathlib import Path
from .config import settings

# 로그 디렉토리 생성
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# 로그 파일명 설정 (날짜 포함)
current_date = datetime.now().strftime("%Y-%m-%d")
log_file = log_dir / f"app_{current_date}.log"

# 로그 포맷 설정
log_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)

def setup_logger(name: str) -> logging.Logger:
    """
    애플리케이션 로거를 설정합니다.
    
    Args:
        name (str): 로거 이름
        
    Returns:
        logging.Logger: 설정된 로거 인스턴스
    """
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)

    # 이미 핸들러가 있다면 추가하지 않음
    if logger.handlers:
        return logger

    # 콘솔 핸들러
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # 파일 핸들러 (최대 10MB, 최대 5개 파일 유지)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    return logger

# 기본 로거 설정
logger = setup_logger("app")

# 로그 레벨별 함수
def debug(message: str, *args, **kwargs):
    logger.debug(message, *args, **kwargs)

def info(message: str, *args, **kwargs):
    logger.info(message, *args, **kwargs)

def warning(message: str, *args, **kwargs):
    logger.warning(message, *args, **kwargs)

def error(message: str, *args, **kwargs):
    logger.error(message, *args, **kwargs)

def critical(message: str, *args, **kwargs):
    logger.critical(message, *args, **kwargs)

# 예외 로깅을 위한 데코레이터
def log_exceptions(logger=logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"함수 {func.__name__} 실행 중 예외 발생: {str(e)}")
                raise
        return wrapper
    return decorator

# 애플리케이션 로거
app_logger = setup_logger("app")
# 데이터베이스 로거
db_logger = setup_logger("database")
# API 로거
api_logger = setup_logger("api")
# 알림 로거
notification_logger = setup_logger("notification") 