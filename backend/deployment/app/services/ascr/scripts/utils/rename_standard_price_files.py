#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
표준품셈 PDF 파일명 일괄 변경 스크립트
한글 파일명을 영문 형식으로 변환
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple


class StandardPriceFileRenamer:
    """표준품셈 파일명 변경 클래스"""
    
    def __init__(self, directory_path: str):
        self.directory_path = Path(directory_path)
        self.rename_mapping = {}
        
    def analyze_current_files(self) -> List[Dict[str, str]]:
        """현재 파일들을 분석하여 변환 규칙 생성"""
        files_info = []
        
        if not self.directory_path.exists():
            print(f"오류: 디렉토리가 존재하지 않습니다: {self.directory_path}")
            return files_info
        
        for file_path in self.directory_path.glob("*.pdf"):
            file_info = {
                "original_name": file_path.name,
                "year": self._extract_year(file_path.name),
                "suffix": self._extract_suffix(file_path.name),
                "new_name": "",
                "file_path": file_path
            }
            files_info.append(file_info)
        
        return files_info
    
    def _extract_year(self, filename: str) -> str:
        """파일명에서 년도 추출"""
        year_match = re.search(r'(\d{4})년', filename)
        if year_match:
            return year_match.group(1)
        return ""
    
    def _extract_suffix(self, filename: str) -> str:
        """파일명에서 특별한 접미사 추출 (수정, 적용 등)"""
        if "(수정)" in filename:
            return "_revised"
        elif "적용" in filename:
            return "_applied"
        return ""
    
    def generate_new_names(self, files_info: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """새로운 파일명 생성"""
        for file_info in files_info:
            year = file_info["year"]
            suffix = file_info["suffix"]
            
            if year:
                new_name = f"{year}_construction_work_standard_price_list{suffix}.pdf"
                file_info["new_name"] = new_name
                
                # 변환 매핑 저장
                self.rename_mapping[file_info["original_name"]] = new_name
        
        return files_info
    
    def preview_changes(self, files_info: List[Dict[str, str]]) -> None:
        """변경 사항 미리보기"""
        print("📋 파일명 변경 미리보기")
        print("=" * 80)
        
        for file_info in files_info:
            if file_info["new_name"]:
                print(f"📄 {file_info['original_name']}")
                print(f"   → {file_info['new_name']}")
                print()
            else:
                print(f"⚠️  변환 실패: {file_info['original_name']}")
                print()
    
    def execute_rename(self, files_info: List[Dict[str, str]], dry_run: bool = True) -> bool:
        """파일명 변경 실행"""
        if dry_run:
            print("🔍 드라이 런 모드 - 실제 변경하지 않습니다")
        else:
            print("🚀 실제 파일명 변경을 시작합니다")
        
        print("=" * 80)
        
        success_count = 0
        error_count = 0
        
        for file_info in files_info:
            if not file_info["new_name"]:
                print(f"❌ 변환 실패: {file_info['original_name']}")
                error_count += 1
                continue
            
            original_path = file_info["file_path"]
            new_path = original_path.parent / file_info["new_name"]
            
            # 중복 파일명 확인
            if new_path.exists() and not dry_run:
                print(f"⚠️  중복 파일명: {file_info['new_name']}")
                error_count += 1
                continue
            
            try:
                if not dry_run:
                    original_path.rename(new_path)
                    print(f"✅ 변경 완료: {file_info['original_name']} → {file_info['new_name']}")
                else:
                    print(f"📝 변경 예정: {file_info['original_name']} → {file_info['new_name']}")
                success_count += 1
                
            except Exception as e:
                print(f"❌ 변경 실패: {file_info['original_name']} - {e}")
                error_count += 1
        
        print("=" * 80)
        print(f"📊 결과: 성공 {success_count}개, 실패 {error_count}개")
        
        return error_count == 0
    
    def create_backup_mapping_file(self) -> None:
        """변경 매핑을 파일로 저장"""
        mapping_file = self.directory_path / "rename_mapping.txt"
        
        with open(mapping_file, 'w', encoding='utf-8') as f:
            f.write("표준품셈 파일명 변경 매핑\n")
            f.write("=" * 50 + "\n\n")
            
            for original, new in self.rename_mapping.items():
                f.write(f"{original} → {new}\n")
        
        print(f"📄 매핑 파일 저장: {mapping_file}")


def main():
    """메인 실행 함수"""
    # 디렉토리 경로 설정
    directory_path = "input/By_year_Construction_work_standard_price_list"
    
    print("🏗️ 표준품셈 파일명 일괄 변경 도구")
    print("=" * 50)
    
    # 리네이머 초기화
    renamer = StandardPriceFileRenamer(directory_path)
    
    # 1단계: 현재 파일 분석
    print("1️⃣ 현재 파일 분석 중...")
    files_info = renamer.analyze_current_files()
    
    if not files_info:
        print("❌ 처리할 PDF 파일을 찾을 수 없습니다.")
        return
    
    print(f"📁 발견된 파일: {len(files_info)}개")
    
    # 2단계: 새로운 파일명 생성
    print("\n2️⃣ 새로운 파일명 생성 중...")
    files_info = renamer.generate_new_names(files_info)
    
    # 3단계: 변경 사항 미리보기
    print("\n3️⃣ 변경 사항 미리보기")
    renamer.preview_changes(files_info)
    
    # 4단계: 사용자 확인
    print("\n4️⃣ 실행 확인")
    print("실제로 파일명을 변경하시겠습니까? (y/N): ", end="")
    
    user_input = input().strip().lower()
    
    if user_input in ['y', 'yes', '예']:
        # 5단계: 실제 변경 실행
        print("\n5️⃣ 파일명 변경 실행")
        success = renamer.execute_rename(files_info, dry_run=False)
        
        if success:
            # 6단계: 매핑 파일 생성
            print("\n6️⃣ 매핑 파일 생성")
            renamer.create_backup_mapping_file()
            print("\n✅ 모든 작업이 완료되었습니다!")
        else:
            print("\n❌ 일부 파일 변경에 실패했습니다.")
    else:
        # 드라이 런으로 미리보기만
        print("\n🔍 드라이 런 모드로 실행")
        renamer.execute_rename(files_info, dry_run=True)
        print("\n💡 실제 변경을 원하시면 스크립트를 다시 실행하세요.")


if __name__ == "__main__":
    main() 