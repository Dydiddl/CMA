#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
os.path를 pathlib.Path로 변환하는 자동 스크립트
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


def convert_os_path_to_pathlib(file_path: str) -> bool:
    """os.path를 pathlib.Path로 변환"""
    try:
        # 파일 읽기
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # 변환 패턴들
        patterns: List[Tuple[str, str]] = [
            # 기본 경로 결합
            (r"os\.path\.join\(([^)]+)\)", r"Path(\1)"),
            # 디렉토리 생성
            (
                r"os\.makedirs\(([^,]+), exist_ok=True\)",
                r"Path(\1).mkdir(parents=True, exist_ok=True)",
            ),
            (
                r"os\.makedirs\(([^)]+)\)",
                r"Path(\1).mkdir(parents=True, exist_ok=True)",
            ),
            # 파일 존재 확인
            (r"os\.path\.exists\(([^)]+)\)", r"Path(\1).exists()"),
            # 파일 정보
            (r"os\.path\.getsize\(([^)]+)\)", r"Path(\1).stat().st_size"),
            (r"os\.path\.basename\(([^)]+)\)", r"Path(\1).name"),
            (r"os\.path\.dirname\(([^)]+)\)", r"Path(\1).parent"),
            # 절대 경로
            (r"os\.path\.abspath\(([^)]+)\)", r"Path(\1).resolve()"),
            (r"os\.path\.realpath\(([^)]+)\)", r"Path(\1).resolve()"),
            # 경로 분할
            (r"os\.path\.splitext\(([^)]+)\)", r"Path(\1).suffix"),
            (r"os\.path\.split\(([^)]+)\)", r"Path(\1).parts"),
            # 경로 확인
            (r"os\.path\.isfile\(([^)]+)\)", r"Path(\1).is_file()"),
            (r"os\.path\.isdir\(([^)]+)\)", r"Path(\1).is_dir()"),
        ]

        # 패턴 적용
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)

        # pathlib import 추가
        if (
            "from pathlib import Path" not in content
            and "import pathlib" not in content
        ):
            if "import os" in content:
                content = content.replace(
                    "import os", "import os\nfrom pathlib import Path"
                )
            else:
                content = "from pathlib import Path\n" + content

        # 변경사항이 있으면 파일에 쓰기
        if content != original_content:
            with open(file_path, "w", encoding="utf-8", newline="") as f:
                f.write(content)
            print(f"✅ 변환 완료: {file_path}")
            return True
        else:
            print(f"ℹ️ 변경사항 없음: {file_path}")
            return False

    except Exception as e:
        print(f"❌ 변환 실패: {file_path} - {e}")
        return False


def find_os_path_files(directory: str = ".") -> List[str]:
    """os.path를 사용하는 파일들을 찾기"""
    os_path_files = []

    for py_file in Path(directory).rglob("*.py"):
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()
                if "os.path." in content:
                    os_path_files.append(str(py_file))
        except Exception as e:
            print(f"⚠️ 파일 읽기 실패: {py_file} - {e}")

    return os_path_files


def main():
    """메인 함수"""
    if len(sys.argv) > 1:
        # 특정 파일 변환
        file_path = sys.argv[1]
        if Path(file_path).exists():
            convert_os_path_to_pathlib(file_path)
        else:
            print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
    else:
        # 전체 프로젝트에서 os.path 사용 파일 찾기
        print("🔍 os.path 사용 파일 검색 중...")
        os_path_files = find_os_path_files()

        if not os_path_files:
            print("✅ os.path를 사용하는 파일이 없습니다.")
            return

        print(f"📁 발견된 파일: {len(os_path_files)}개")

        # 우선순위 파일들 먼저 처리
        priority_patterns = [
            "backend/app/services/ascr",
            "backend/app/core",
            "backend/app/utils",
            "desktop",
            "backend/app/models",
            "backend/app/schemas",
        ]

        priority_files = []
        other_files = []

        for file_path in os_path_files:
            if any(pattern in file_path for pattern in priority_patterns):
                priority_files.append(file_path)
            else:
                other_files.append(file_path)

        # 우선순위 파일들 처리
        if priority_files:
            print(f"\n🔴 우선순위 파일 처리 중... ({len(priority_files)}개)")
            for file_path in priority_files[:10]:  # 처음 10개만 처리
                convert_os_path_to_pathlib(file_path)

        # 나머지 파일들 처리
        if other_files:
            print(f"\n🟡 나머지 파일 처리 중... ({len(other_files)}개)")
            for file_path in other_files[:20]:  # 처음 20개만 처리
                convert_os_path_to_pathlib(file_path)

        print("\n📊 처리 완료:")
        print(f"- 우선순위 파일: {len(priority_files)}개")
        print(f"- 나머지 파일: {len(other_files)}개")
        print(f"- 총 파일: {len(os_path_files)}개")


if __name__ == "__main__":
    main()
