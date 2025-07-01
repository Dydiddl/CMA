#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 데스크톱 애플리케이션 빌드 스크립트
Windows용 exe 파일 생성
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_windows_exe():
    """Windows용 exe 파일 빌드"""
    print("=== CMA Windows exe 빌드 시작 ===")
    
    # PyInstaller 설치 확인
    try:
        import PyInstaller
        print("[SUCCESS] PyInstaller가 설치되어 있습니다.")
    except ImportError:
        print("[INFO] PyInstaller를 설치합니다...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # 빌드 디렉토리 정리
    build_dir = Path("build")
    dist_dir = Path("dist")
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    # PyInstaller 명령 실행
    cmd = [
        "pyinstaller",
        "--onefile",                    # 단일 exe 파일
        "--windowed",                   # 콘솔 창 숨김
        "--name=CMA_Construction_Manager",  # 실행 파일명
        "--icon=assets/icon.ico",       # 아이콘 (있으면)
        "--add-data=assets;assets",     # 리소스 파일 포함
        "--add-data=config.json;.",     # 설정 파일 포함
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtGui", 
        "--hidden-import=PySide6.QtWidgets",
        "--hidden-import=sqlalchemy",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--hidden-import=pypdf",
        "main.py"
    ]
    
    print(f"[INFO] 빌드 명령 실행: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("[SUCCESS] exe 파일 빌드 완료!")
        print(f"[INFO] 생성된 파일: {dist_dir / 'CMA_Construction_Manager.exe'}")
        
        # 파일 크기 확인
        exe_path = dist_dir / "CMA_Construction_Manager.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"[INFO] 파일 크기: {size_mb:.1f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] 빌드 실패: {e}")
        print(f"[ERROR] 오류 출력: {e.stderr}")
        return False

def build_mac_app():
    """Mac용 app 파일 빌드"""
    print("=== CMA Mac app 빌드 시작 ===")
    
    # PyInstaller 설치 확인
    try:
        import PyInstaller
        print("[SUCCESS] PyInstaller가 설치되어 있습니다.")
    except ImportError:
        print("[INFO] PyInstaller를 설치합니다...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # 빌드 디렉토리 정리
    build_dir = Path("build")
    dist_dir = Path("dist")
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    # PyInstaller 명령 실행 (Mac용)
    cmd = [
        "pyinstaller",
        "--onefile",                    # 단일 app 파일
        "--windowed",                   # 콘솔 창 숨김
        "--name=CMA_Construction_Manager",  # 실행 파일명
        "--icon=assets/icon.icns",      # Mac 아이콘 (있으면)
        "--add-data=assets:assets",     # 리소스 파일 포함
        "--add-data=config.json:.",     # 설정 파일 포함
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtGui", 
        "--hidden-import=PySide6.QtWidgets",
        "--hidden-import=sqlalchemy",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--hidden-import=pypdf",
        "main.py"
    ]
    
    print(f"[INFO] 빌드 명령 실행: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("[SUCCESS] app 파일 빌드 완료!")
        print(f"[INFO] 생성된 파일: {dist_dir / 'CMA_Construction_Manager'}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] 빌드 실패: {e}")
        print(f"[ERROR] 오류 출력: {e.stderr}")
        return False

def main():
    """메인 함수"""
    platform = sys.platform
    
    if platform.startswith("win"):
        print("[INFO] Windows 환경에서 빌드합니다.")
        success = build_windows_exe()
    elif platform.startswith("darwin"):
        print("[INFO] Mac 환경에서 빌드합니다.")
        success = build_mac_app()
    else:
        print(f"[ERROR] 지원하지 않는 플랫폼: {platform}")
        print("[INFO] Windows 또는 Mac에서 빌드하세요.")
        return False
    
    if success:
        print("\n=== 빌드 완료 ===")
        print("[SUCCESS] 배포용 파일이 성공적으로 생성되었습니다!")
        print("[INFO] dist 폴더에서 생성된 파일을 확인하세요.")
        return True
    else:
        print("\n=== 빌드 실패 ===")
        print("[ERROR] 빌드 중 오류가 발생했습니다.")
        return False

if __name__ == "__main__":
    main() 