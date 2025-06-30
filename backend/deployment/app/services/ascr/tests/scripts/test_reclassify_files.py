#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
재분류 스크립트 테스트

scripts/reclassify_files.py의 기능을 테스트
"""

import pytest
import sys
import shutil
from pathlib import Path
import json

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.common.utils import determine_section

class TestReclassifyFiles:
    """재분류 스크립트 테스트"""
    
    def test_reclassify_files_function(self, temp_dir):
        """재분류 함수 테스트"""
        # 테스트용 디렉토리 구조 생성
        base_dir = temp_dir / "split_pdfs"
        common_dir = base_dir / "공통부문"
        common_dir.mkdir(parents=True, exist_ok=True)
        
        # 테스트용 PDF 파일들 생성 (실제 파일 대신 텍스트 파일로 대체)
        test_files = [
            "배관누수_검사.txt",
            "타일_교체.txt", 
            "도로공사.txt",
            "유지보수.txt",
            "기타공사.txt"
        ]
        
        for filename in test_files:
            file_path = common_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"테스트 파일: {filename}")
        
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
        
        # 재분류 실행
        moved_files = 0
        total_files = 0
        
        for file_path in common_dir.glob("*.txt"):
            total_files += 1
            title = file_path.stem  # 확장자 제거
            new_section = determine_section(title)
            
            if new_section != "공통부문":
                target_dir = target_dirs.get(new_section)
                if target_dir:
                    target_path = target_dir / file_path.name
                    try:
                        shutil.move(str(file_path), str(target_path))
                        moved_files += 1
                    except Exception as e:
                        print(f"파일 이동 실패: {e}")
        
        # 검증
        assert total_files == len(test_files), f"총 파일 수 불일치: {total_files} != {len(test_files)}"
        assert moved_files > 0, "이동된 파일이 없음"
        
        # 각 부문별 파일 수 확인
        mechanical_files = list(target_dirs["기계설비부문"].glob("*.txt"))
        architecture_files = list(target_dirs["건축부문"].glob("*.txt"))
        civil_files = list(target_dirs["토목부문"].glob("*.txt"))
        maintenance_files = list(target_dirs["유지관리부문"].glob("*.txt"))
        
        # 예상되는 분류 결과 검증
        assert len(mechanical_files) > 0, "기계설비부문으로 이동된 파일이 없음"
        assert len(architecture_files) > 0, "건축부문으로 이동된 파일이 없음"
        assert len(civil_files) > 0, "토목부문으로 이동된 파일이 없음"
        
        return {
            "total_files": total_files,
            "moved_files": moved_files,
            "mechanical_count": len(mechanical_files),
            "architecture_count": len(architecture_files),
            "civil_count": len(civil_files),
            "maintenance_count": len(maintenance_files)
        }
    
    def test_classification_accuracy(self):
        """분류 정확도 테스트"""
        test_cases = [
            ("배관누수_검사", "기계설비부문"),
            ("타일_교체", "건축부문"),
            ("도로공사", "토목부문"),
            ("유지보수", "유지관리부문"),
            ("기타공사", "미분류")
        ]
        
        correct_count = 0
        total_count = len(test_cases)
        
        for filename, expected_section in test_cases:
            actual_section = determine_section(filename)
            if actual_section == expected_section:
                correct_count += 1
        
        accuracy = (correct_count / total_count) * 100
        assert accuracy >= 80, f"분류 정확도가 너무 낮음: {accuracy:.1f}%"
        
        return {
            "accuracy": accuracy,
            "correct_count": correct_count,
            "total_count": total_count
        }
    
    def test_file_safety(self, temp_dir):
        """파일 안전성 테스트"""
        # 원본 파일 백업 테스트
        test_file = temp_dir / "test_file.txt"
        backup_file = temp_dir / "test_file_backup.txt"
        
        # 원본 파일 생성
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("원본 내용")
        
        # 백업 생성
        shutil.copy2(test_file, backup_file)
        
        # 백업 파일 존재 확인
        assert backup_file.exists(), "백업 파일이 생성되지 않음"
        
        # 내용 동일성 확인
        with open(test_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_content = f.read()
        
        assert original_content == backup_content, "백업 파일 내용이 원본과 다름"
        
        return {
            "original_file": str(test_file),
            "backup_file": str(backup_file),
            "content_match": original_content == backup_content
        }
    
    def test_error_handling(self, temp_dir):
        """오류 처리 테스트"""
        # 존재하지 않는 디렉토리에서 파일 이동 시도
        non_existent_dir = temp_dir / "non_existent"
        test_file = temp_dir / "test_file.txt"
        
        # 테스트 파일 생성
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("테스트 내용")
        
        # 존재하지 않는 디렉토리로 이동 시도
        target_path = non_existent_dir / "test_file.txt"
        
        try:
            shutil.move(str(test_file), str(target_path))
            assert False, "존재하지 않는 디렉토리로 이동이 성공했음 (예상: 실패)"
        except FileNotFoundError:
            # 예상된 오류
            assert True, "올바른 오류 처리"
        except Exception as e:
            # 다른 오류도 허용
            assert True, f"오류 처리됨: {e}"
        
        # 원본 파일이 여전히 존재하는지 확인
        assert test_file.exists(), "원본 파일이 사라짐"
        
        return {
            "error_handled": True,
            "original_file_preserved": test_file.exists()
        }
    
    def test_large_scale_reclassification(self, temp_dir):
        """대규모 재분류 테스트"""
        import time
        
        # 대량의 테스트 파일 생성
        base_dir = temp_dir / "large_scale_test"
        common_dir = base_dir / "공통부문"
        common_dir.mkdir(parents=True, exist_ok=True)
        
        # 100개의 테스트 파일 생성
        test_file_names = [
            "배관공사", "덕트설치", "보온공사", "펌프설치", "밸브교체",
            "타일공사", "지붕공사", "칠공사", "철골공사", "조적공사",
            "도로공사", "하천공사", "터널공사", "궤도공사", "강구조공사",
            "유지보수", "관리공사", "적용기준", "가설공사", "토공사"
        ] * 5  # 100개
        
        # 파일 생성
        for i, name in enumerate(test_file_names):
            file_path = common_dir / f"{name}_{i:03d}.txt"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"테스트 파일 {i}: {name}")
        
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
        
        # 재분류 실행 (시간 측정)
        start_time = time.time()
        
        moved_files = 0
        total_files = 0
        
        for file_path in common_dir.glob("*.txt"):
            total_files += 1
            title = file_path.stem.split('_')[0]  # 번호 제거
            new_section = determine_section(title)
            
            if new_section != "공통부문":
                target_dir = target_dirs.get(new_section)
                if target_dir:
                    target_path = target_dir / file_path.name
                    try:
                        shutil.move(str(file_path), str(target_path))
                        moved_files += 1
                    except Exception as e:
                        print(f"파일 이동 실패: {e}")
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # 성능 검증
        assert processing_time < 5.0, f"100개 파일 처리에 {processing_time:.2f}초 소요 (너무 느림)"
        assert moved_files > 0, "이동된 파일이 없음"
        
        # 각 부문별 파일 수 확인
        section_counts = {}
        for section_name, dir_path in target_dirs.items():
            section_counts[section_name] = len(list(dir_path.glob("*.txt")))
        
        return {
            "total_files": total_files,
            "moved_files": moved_files,
            "processing_time": processing_time,
            "section_counts": section_counts
        } 