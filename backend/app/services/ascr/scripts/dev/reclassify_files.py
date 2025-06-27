#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
자동 재분류 스크립트

이 스크립트는 개선된 분류 시스템을 사용하여 파일들을 재분류합니다.
"""

import shutil
from pathlib import Path
import sys

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.common.utils import determine_section

def reclassify_files():
    """파일 재분류 실행"""
    base_dir = Path("output/split_pdfs")
    common_dir = base_dir / "공통부문"
    
    if not common_dir.exists():
        print("❌ 공통부문 디렉토리를 찾을 수 없습니다.")
        return
    
    # 대상 디렉토리 생성
    target_dirs = {
        "기계설비부문": base_dir / "기계설비부문",
        "건축부문": base_dir / "건축부문", 
        "토목부문": base_dir / "토목부문",
        "유지관리부문": base_dir / "유지관리부문",
        "미분류": base_dir / "미분류"
    }
    
    for dir_path in target_dirs.values():
        dir_path.mkdir(exist_ok=True)
    
    moved_files = 0
    total_files = 0
    
    for file_path in common_dir.glob("*.pdf"):
        total_files += 1
        title = file_path.stem
        new_section = determine_section(title)
        
        if new_section != "공통부문":
            target_dir = target_dirs.get(new_section)
            if target_dir:
                target_path = target_dir / file_path.name
                try:
                    shutil.move(str(file_path), str(target_path))
                    print(f"✅ {title} -> {new_section}")
                    moved_files += 1
                except Exception as e:
                    print(f"❌ {title} 이동 실패: {e}")
    
    print(f"\n📊 재분류 완료: {moved_files}/{total_files}개 파일 이동")

if __name__ == "__main__":
    reclassify_files()
