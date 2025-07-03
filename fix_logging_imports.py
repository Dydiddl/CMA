#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI 파일들의 logging import 수정 스크립트
"""

import os
import re
from pathlib import Path

def fix_logging_imports():
    """모든 UI 파일에 logging import 추가"""
    
    # 데스크톱 UI 폴더의 모든 Python 파일
    ui_path = Path("desktop/ui")
    python_files = list(ui_path.glob("*.py"))
    
    for file_path in python_files:
        try:
            # 파일 읽기
            with open(file_path, 'r', encoding='utf-8', newline=\'\', encoding=\'utf-8\', newline=\'\', newline='', encoding='utf-8', newline='') as f:
                content = f.read()
            
            # 변경 전 내용 저장
            original_content = content
            
            # logging import가 없고 logger가 사용되는 경우
            if 'logger = logging.getLogger' in content and 'import logging' not in content:
                # import 문들 찾기
                import_lines = []
                lines = content.split('\n')
                
                for i, line in enumerate(lines):
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        import_lines.append(i)
                
                # logging import 추가
                if import_lines:
                    # 마지막 import 문 다음에 logging 추가
                    last_import_line = max(import_lines)
                    lines.insert(last_import_line + 1, 'import logging')
                    content = '\n'.join(lines)
                    
                    # 파일에 쓰기
                    with open(file_path, 'w', encoding='utf-8', newline=\'\', encoding=\'utf-8\', newline=\'\', newline='', encoding='utf-8', newline='') as f:
                        f.write(content)
                    
                    print(f"✅ {file_path.name}: logging import 추가됨")
                else:
                    print(f"⚠️ {file_path.name}: import 문을 찾을 수 없음")
            else:
                print(f"ℹ️ {file_path.name}: 이미 logging import가 있거나 logger가 사용되지 않음")
                
        except Exception as e:
            print(f"❌ {file_path.name}: 오류 발생 - {e}")

if __name__ == "__main__":
    fix_logging_imports()
    print("\n=== logging import 수정 완료 ===") 