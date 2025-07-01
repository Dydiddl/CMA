#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
크로스 플랫폼 개발을 위한 플랫폼 유틸리티
"""

import os
import platform
from pathlib import Path
from typing import Any, Dict


def get_platform_info() -> Dict[str, str]:
    """플랫폼 정보 반환"""
    return {
        "os": platform.system(),
        "version": platform.version(),
        "python_version": platform.python_version(),
        "architecture": platform.architecture()[0],
        "machine": platform.machine(),
        "processor": platform.processor(),
    }


def get_platform_specific_path(base_path: str) -> Path:
    """플랫폼별 경로 반환"""
    if platform.system() == "Windows":
        return Path(os.getenv("CMA_HOME", "C:\\CMA")) / base_path
    elif platform.system() == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "CMA" / base_path
    else:  # Linux
        return Path.home() / ".cma" / base_path


def is_wsl() -> bool:
    """WSL 환경인지 확인"""
    return platform.system() == "Linux" and "microsoft" in platform.release().lower()


def is_windows() -> bool:
    """Windows 플랫폼인지 확인"""
    return platform.system() == "Windows"


def is_macos() -> bool:
    """macOS 플랫폼인지 확인"""
    return platform.system() == "Darwin"


def is_linux() -> bool:
    """Linux 플랫폼인지 확인"""
    return platform.system() == "Linux"


def get_temp_dir() -> Path:
    """플랫폼별 임시 디렉토리 반환"""
    if platform.system() == "Windows":
        return Path(os.environ.get("TEMP", "C:\\Temp"))
    else:
        return Path("/tmp")


def get_home_dir() -> Path:
    """플랫폼별 홈 디렉토리 반환"""
    if platform.system() == "Windows":
        return Path(os.environ.get("USERPROFILE", "C:\\Users\\Default"))
    else:
        return Path.home()


def get_executable_name(base_name: str) -> str:
    """플랫폼별 실행 파일 이름 반환"""
    if platform.system() == "Windows":
        return f"{base_name}.exe"
    else:
        return base_name


def get_python_command() -> str:
    """플랫폼별 Python 명령어 반환"""
    if platform.system() == "Windows":
        return "python"
    else:
        return "python3"


def get_path_separator() -> str:
    """플랫폼별 경로 구분자 반환"""
    return os.pathsep


def get_line_ending() -> str:
    """플랫폼별 라인 엔딩 반환"""
    if platform.system() == "Windows":
        return "\r\n"
    else:
        return "\n"


def create_cross_platform_path(*parts: str) -> Path:
    """크로스 플랫폼 경로 생성"""
    return Path(*parts)


def ensure_directory(path: Path) -> bool:
    """디렉토리 존재 확인 및 생성"""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False


def get_platform_specific_config() -> Dict[str, Any]:
    """플랫폼별 설정 반환"""
    config = {
        "max_file_size": 50 * 1024 * 1024,  # 기본 50MB
        "encoding": "utf-8",
        "line_ending": get_line_ending(),
        "temp_dir": str(get_temp_dir()),
        "home_dir": str(get_home_dir()),
    }

    # 플랫폼별 설정 조정
    if is_windows():
        config.update(
            {
                "max_file_size": 100 * 1024 * 1024,  # Windows: 100MB
                "default_encoding": "cp949",  # Windows 기본 인코딩
            }
        )
    elif is_macos():
        config.update(
            {
                "max_file_size": 50 * 1024 * 1024,  # macOS: 50MB
                "default_encoding": "utf-8",
            }
        )
    else:  # Linux
        config.update(
            {
                "max_file_size": 50 * 1024 * 1024,  # Linux: 50MB
                "default_encoding": "utf-8",
            }
        )

    return config


def validate_cross_platform_setup() -> Dict[str, bool]:
    """크로스 플랫폼 설정 검증"""
    validation = {
        "pathlib_available": True,
        "platform_module_available": True,
        "temp_dir_writable": False,
        "home_dir_accessible": False,
        "encoding_supported": False,
    }

    # 임시 디렉토리 쓰기 가능 확인
    try:
        temp_file = get_temp_dir() / "test_cross_platform.txt"
        temp_file.write_text("test", encoding="utf-8")
        temp_file.unlink()
        validation["temp_dir_writable"] = True
    except Exception:
        pass

    # 홈 디렉토리 접근 가능 확인
    try:
        home_dir = get_home_dir()
        if home_dir.exists():
            validation["home_dir_accessible"] = True
    except Exception:
        pass

    # 인코딩 지원 확인
    try:
        test_content = "한글 테스트"
        encoded = test_content.encode("utf-8")
        decoded = encoded.decode("utf-8")
        if decoded == test_content:
            validation["encoding_supported"] = True
    except Exception:
        pass

    return validation


def get_platform_specific_environment_vars() -> Dict[str, str]:
    """플랫폼별 환경 변수 반환"""
    env_vars = {}

    if is_windows():
        env_vars.update(
            {
                "CMA_HOME": os.getenv("CMA_HOME", "C:\\CMA"),
                "CMA_TEMP": os.getenv("CMA_TEMP", "C:\\Temp"),
                "CMA_DATA": os.getenv("CMA_DATA", "C:\\CMA\\data"),
            }
        )
    elif is_macos():
        env_vars.update(
            {
                "CMA_HOME": os.getenv(
                    "CMA_HOME",
                    str(Path.home() / "Library" / "Application Support" / "CMA"),
                ),
                "CMA_TEMP": os.getenv("CMA_TEMP", "/tmp"),
                "CMA_DATA": os.getenv(
                    "CMA_DATA",
                    str(
                        Path.home() / "Library" / "Application Support" / "CMA" / "data"
                    ),
                ),
            }
        )
    else:  # Linux
        env_vars.update(
            {
                "CMA_HOME": os.getenv("CMA_HOME", str(Path.home() / ".cma")),
                "CMA_TEMP": os.getenv("CMA_TEMP", "/tmp"),
                "CMA_DATA": os.getenv("CMA_DATA", str(Path.home() / ".cma" / "data")),
            }
        )

    return env_vars


def setup_platform_environment() -> bool:
    """플랫폼별 환경 설정"""
    try:
        # 환경 변수 설정
        env_vars = get_platform_specific_environment_vars()
        for key, value in env_vars.items():
            if key not in os.environ:
                os.environ[key] = value

        # 필요한 디렉토리 생성
        directories = [
            get_platform_specific_path("data"),
            get_platform_specific_path("logs"),
            get_platform_specific_path("temp"),
            get_platform_specific_path("uploads"),
        ]

        for directory in directories:
            ensure_directory(directory)

        return True
    except Exception:
        return False


# 플랫폼 정보 캐시
_PLATFORM_INFO = None
_PLATFORM_CONFIG = None


def get_cached_platform_info() -> Dict[str, str]:
    """캐시된 플랫폼 정보 반환"""
    global _PLATFORM_INFO
    if _PLATFORM_INFO is None:
        _PLATFORM_INFO = get_platform_info()
    return _PLATFORM_INFO


def get_cached_platform_config() -> Dict[str, Any]:
    """캐시된 플랫폼 설정 반환"""
    global _PLATFORM_CONFIG
    if _PLATFORM_CONFIG is None:
        _PLATFORM_CONFIG = get_platform_specific_config()
    return _PLATFORM_CONFIG
