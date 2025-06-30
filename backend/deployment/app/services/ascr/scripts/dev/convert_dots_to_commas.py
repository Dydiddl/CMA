#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
점을 쉼표로 변환하는 스크립트

toc_ground_truth_2025.md 파일에서 ···· (점들)을 , (쉼표)로 변환합니다.
"""

import re
import sys
from pathlib import Path
from datetime import datetime

def convert_dots_to_commas(input_file: Path, output_file: Path = None) -> bool:
    """
    파일에서 점들을 쉼표로 변환
    
    Args:
        input_file: 입력 파일 경로
        output_file: 출력 파일 경로 (None이면 백업 후 원본 수정)
    
    Returns:
        성공 여부
    """
    try:
        # 파일 읽기
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 변환 전 통계
        dots_count = content.count('····')
        print(f"📊 변환 전 점 개수: {dots_count}")
        
        # 점을 쉼표로 변환
        # 여러 개의 점이 연속된 경우를 모두 쉼표로 변환
        converted_content = re.sub(r'·+', ',', content)
        
        # 변환 후 통계
        commas_count = converted_content.count(',')
        print(f"📊 변환 후 쉼표 개수: {commas_count}")
        
        # 출력 파일 결정
        if output_file is None:
            # 백업 파일 생성
            backup_file = input_file.parent / f"{input_file.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}{input_file.suffix}"
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"💾 백업 파일 생성: {backup_file}")
            
            # 원본 파일 수정
            output_file = input_file
        
        # 변환된 내용 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(converted_content)
        
        print(f"✅ 변환 완료: {output_file}")
        print(f"📈 변환된 항목 수: {dots_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ 변환 실패: {e}")
        return False

def validate_conversion(input_file: Path) -> bool:
    """
    변환 결과 검증
    
    Args:
        input_file: 검증할 파일 경로
    
    Returns:
        검증 성공 여부
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 점이 남아있는지 확인
        remaining_dots = content.count('····')
        if remaining_dots > 0:
            print(f"⚠️ 경고: {remaining_dots}개의 점이 남아있습니다.")
            return False
        
        # 쉼표 개수 확인
        commas_count = content.count(',')
        print(f"✅ 검증 완료: {commas_count}개의 쉼표가 있습니다.")
        
        # 샘플 출력
        lines = content.split('\n')
        sample_lines = [line for line in lines if ',' in line and '제' in line][:5]
        
        print("\n📋 변환 결과 샘플:")
        for line in sample_lines:
            print(f"  {line.strip()}")
        
        return True
        
    except Exception as e:
        print(f"❌ 검증 실패: {e}")
        return False

def main():
    """메인 함수"""
    # 입력 파일 경로
    input_file = Path("data/ground truth/toc_ground_truth_2025.md")
    
    if not input_file.exists():
        print(f"❌ 파일을 찾을 수 없습니다: {input_file}")
        return False
    
    print("🔄 점을 쉼표로 변환하는 작업을 시작합니다...")
    print(f"📄 입력 파일: {input_file}")
    
    # 변환 실행
    success = convert_dots_to_commas(input_file)
    
    if success:
        # 검증 실행
        print("\n🔍 변환 결과 검증 중...")
        validation_success = validate_conversion(input_file)
        
        if validation_success:
            print("\n🎉 모든 작업이 성공적으로 완료되었습니다!")
            print("💡 이제 스크립트에서 정규식 패턴 매칭이 훨씬 쉬워집니다.")
        else:
            print("\n⚠️ 변환은 완료되었지만 검증에 문제가 있습니다.")
    else:
        print("\n❌ 변환에 실패했습니다.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 