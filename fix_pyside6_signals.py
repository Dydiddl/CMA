#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 시그널 수정 스크립트
pyqtSignal을 Signal로 변경
"""

import os
import re
from pathlib import Path

def fix_pyside6_signals():
    """모든 파일에서 pyqtSignal을 Signal로 변경"""
    
    # 데스크톱 폴더의 모든 Python 파일
    desktop_path = Path("desktop")
    python_files = list(desktop_path.rglob("*.py"))
    
    for file_path in python_files:
        try:
            # 파일 읽기
            with open(file_path, 'r', encoding='utf-8', newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
                content = f.read()
            
            # 변경 전 내용 저장
            original_content = content
            
            # pyqtSignal을 Signal로 변경
            content = re.sub(r'\bpyqtSignal\b', 'Signal', content)
            
            # 변경사항이 있으면 파일에 쓰기
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8', newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
                    f.write(content)
                print(f"수정됨: {file_path}")
            
        except Exception as e:
            print(f"오류 발생: {file_path} - {e}")

if __name__ == "__main__":
    fix_pyside6_signals()
    print("PySide6 시그널 수정 완료!") 