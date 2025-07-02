#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
open() 함수에 newline='' 파라미터를 추가하는 자동 스크립트
"""

import re
import sys
from pathlib import Path
from typing import List


def add_newline_parameter(file_path: str) -> bool:
    """open() 함수에 newline='' 추가"""
    try:
        # 파일 읽기
        with open(file_path, "r", encoding="utf-8", newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
            content = f.read()

        original_content = content

        # open() 함수 패턴들
        patterns = [
            # 인코딩이 있는 경우
            (r"open\(([^)]*encoding=[^)]*)\)", r"open(\1, newline=\'\')"),
            # 인코딩이 없는 경우 (읽기 모드)
            (
                r'open\(([^)]*mode=[^)]*["\']r[^)]*)\)',
                r"open(\1, encoding=\'utf-8\', newline=\'\', newline=\'\')",
            ),
            (
                r'open\(([^)]*["\']r[^)]*)\)',
                r"open(\1, encoding=\'utf-8\', newline=\'\', newline=\'\')",
            ),
            # 인코딩이 없는 경우 (쓰기 모드)
            (
                r'open\(([^)]*mode=[^)]*["\']w[^)]*)\)',
                r"open(\1, encoding=\'utf-8\', newline=\'\', newline=\'\')",
            ),
            (
                r'open\(([^)]*["\']w[^)]*)\)',
                r"open(\1, encoding=\'utf-8\', newline=\'\', newline=\'\')",
            ),
            # 인코딩이 없는 경우 (추가 모드)
            (
                r'open\(([^)]*mode=[^)]*["\']a[^)]*)\)',
                r"open(\1, encoding=\'utf-8\', newline=\'\', newline=\'\')",
            ),
            (
                r'open\(([^)]*["\']a[^)]*)\)',
                r"open(\1, encoding=\'utf-8\', newline=\'\', newline=\'\')",
            ),
        ]

        # 패턴 적용
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)

        # 변경사항이 있으면 파일에 쓰기
        if content != original_content:
            with open(file_path, "w", encoding="utf-8", newline="", newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
                f.write(content)
            print(f"✅ newline 추가 완료: {file_path}")
            return True
        else:
            print(f"ℹ️ 변경사항 없음: {file_path}")
            return False

    except Exception as e:
        print(f"❌ 변환 실패: {file_path} - {e}")
        return False


def find_encoding_files(directory: str = ".") -> List[str]:
    """인코딩을 사용하는 파일들을 찾기"""
    encoding_files = []

    for py_file in Path(directory).rglob("*.py"):
        try:
            with open(py_file, "r", encoding="utf-8", newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
                content = f.read()
                if "open(" in content and "encoding=" in content:
                    encoding_files.append(str(py_file, newline=\'\'))
        except Exception as e:
            print(f"⚠️ 파일 읽기 실패: {py_file} - {e}")

    return encoding_files


def find_open_files(directory: str = ".") -> List[str]:
    """open() 함수를 사용하는 파일들을 찾기"""
    open_files = []

    for py_file in Path(directory).rglob("*.py"):
        try:
            with open(py_file, "r", encoding="utf-8", newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
                content = f.read()
                if "open(" in content:
                    open_files.append(str(py_file))
        except Exception as e:
            print(f"⚠️ 파일 읽기 실패: {py_file} - {e}")

    return open_files


def main():
    """메인 함수"""
    if len(sys.argv) > 1:
        # 특정 파일 변환
        file_path = sys.argv[1]
        if Path(file_path).exists():
            add_newline_parameter(file_path)
        else:
            print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
    else:
        # 전체 프로젝트에서 open() 사용 파일 찾기
        print("🔍 open() 함수 사용 파일 검색 중...")

        # 인코딩 사용 파일들 먼저 처리
        encoding_files = find_encoding_files()
        print(f"📁 인코딩 사용 파일: {len(encoding_files)}개")

        # open() 사용 파일들 찾기
        open_files = find_open_files()
        print(f"📁 open() 사용 파일: {len(open_files)}개")

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

        for file_path in encoding_files:
            if any(pattern in file_path for pattern in priority_patterns):
                priority_files.append(file_path)
            else:
                other_files.append(file_path)

        # 우선순위 파일들 처리
        if priority_files:
            print(f"\n🔴 우선순위 파일 처리 중... ({len(priority_files)}개)")
            for file_path in priority_files[:10]:  # 처음 10개만 처리
                add_newline_parameter(file_path)

        # 나머지 파일들 처리
        if other_files:
            print(f"\n🟡 나머지 파일 처리 중... ({len(other_files)}개)")
            for file_path in other_files[:20]:  # 처음 20개만 처리
                add_newline_parameter(file_path)

        print("\n📊 처리 완료:")
        print(f"- 인코딩 사용 파일: {len(encoding_files)}개")
        print(f"- open() 사용 파일: {len(open_files)}개")
        print(f"- 우선순위 파일: {len(priority_files)}개")
        print(f"- 나머지 파일: {len(other_files)}개")


if __name__ == "__main__":
    main()
