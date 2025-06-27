#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
반자동화된 정답 데이터 생성기

기존 2025년 정답 데이터를 기반으로 2023, 2024년 PDF에서 
목차를 자동 추출하고, 수동 검증을 통해 정답 데이터를 효율적으로 생성합니다.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
from collections import defaultdict, Counter
import difflib
import argparse

class SemiAutomatedGroundTruthGenerator:
    """반자동화된 정답 데이터 생성기"""
    
    def __init__(self, input_dir: str = "input", ground_truth_dir: str = "data/ground truth"):
        self.input_dir = Path(input_dir)
        self.ground_truth_dir = Path(ground_truth_dir)
        self.reference_data = {}  # 2025년 정답 데이터
        self.extracted_data = {}  # 추출된 데이터
        self.validation_results = {}
        
    def load_reference_ground_truth(self) -> Dict[str, Any]:
        """2025년 정답 데이터를 참조 데이터로 로드"""
        print("📚 참조 정답 데이터 로드 중...")
        
        gt_2025_file = self.ground_truth_dir / "toc_ground_truth_2025.md"
        if not gt_2025_file.exists():
            print(f"❌ 참조 데이터가 없습니다: {gt_2025_file}")
            return {}
        
        try:
            with open(gt_2025_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 2025년 정답 데이터 파싱
            reference_items = self._parse_ground_truth_content(content)
            
            # 부문별로 정리
            section_items = defaultdict(list)
            for item in reference_items:
                section_items[item['section']].append(item)
            
            self.reference_data = {
                'items': reference_items,
                'section_items': dict(section_items),
                'patterns': self._extract_patterns(reference_items)
            }
            
            print(f"✅ 참조 데이터 로드 완료: {len(reference_items)}개 항목")
            for section, items in section_items.items():
                print(f"  - {section}: {len(items)}개")
            
            return self.reference_data
            
        except Exception as e:
            print(f"❌ 참조 데이터 로드 실패: {e}")
            return {}
    
    def _parse_ground_truth_content(self, content: str) -> List[Dict[str, Any]]:
        """정답 데이터 내용 파싱"""
        items = []
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 부문 확인
            if "부문" in line and len(line) < 20:
                current_section = line
                continue
            
            # 목차 항목 확인 (들여쓰기 기반)
            if "," in line and current_section:
                parts = line.split(',')
                if len(parts) >= 2:
                    item_text = parts[0].strip()
                    try:
                        page_number = int(parts[1].strip())
                    except ValueError:
                        page_number = 0
                    
                    items.append({
                        'text': item_text,
                        'section': current_section,
                        'page': page_number
                    })
        
        return items
    
    def _extract_patterns(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """참조 데이터에서 패턴 추출"""
        patterns = {
            'section_keywords': defaultdict(list),
            'number_patterns': [],
            'common_titles': []
        }
        
        for item in items:
            text = item['text']
            section = item['section']
            
            # 번호 패턴 추출
            number_match = re.match(r'(\d+(-\d+)*)', text)
            if number_match:
                patterns['number_patterns'].append(number_match.group(1))
            
            # 제목 추출
            title_match = re.search(r'\d+(-\d+)*\s+(.+)', text)
            if title_match:
                title = title_match.group(2)
                patterns['common_titles'].append(title)
                
                # 부문별 키워드
                patterns['section_keywords'][section].append(title)
        
        return patterns
    
    def extract_toc_from_pdf_simple(self, pdf_filename: str, year: int) -> Dict[str, Any]:
        """PDF에서 간단한 목차 추출 (기본 규칙 기반)"""
        pdf_path = self.input_dir / pdf_filename
        if not pdf_path.exists():
            print(f"❌ PDF 파일이 없습니다: {pdf_path}")
            return {}
        
        print(f"\n🔍 {year}년 PDF 목차 추출 중: {pdf_filename}")
        
        try:
            # Python 라이브러리를 사용한 텍스트 추출
            pdf_text = self._extract_text_from_pdf(pdf_path)
            
            if not pdf_text:
                print(f"❌ PDF 텍스트 추출 실패")
                return {}
            
            # 기본 규칙 기반 목차 추출
            extracted_items = self._extract_toc_by_rules(pdf_text, year)
            
            print(f"  - 추출된 항목: {len(extracted_items)}개")
            return extracted_items
            
        except Exception as e:
            print(f"❌ PDF 처리 중 오류: {e}")
            return {}
    
    def _extract_text_from_pdf(self, pdf_path: Path) -> str:
        """PDF에서 텍스트 추출 (여러 방법 시도)"""
        # 방법 1: pypdf 사용
        try:
            from pypdf import PdfReader
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            if text.strip():
                return text
        except ImportError:
            print("  - pypdf 라이브러리가 없습니다.")
        except Exception as e:
            print(f"  - pypdf 추출 실패: {e}")
        
        # 방법 2: PyPDF2 사용
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                if text.strip():
                    return text
        except ImportError:
            print("  - PyPDF2 라이브러리가 없습니다.")
        except Exception as e:
            print(f"  - PyPDF2 추출 실패: {e}")
        
        # 방법 3: pdfplumber 사용
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
                if text.strip():
                    return text
        except ImportError:
            print("  - pdfplumber 라이브러리가 없습니다.")
        except Exception as e:
            print(f"  - pdfplumber 추출 실패: {e}")
        
        # 방법 4: subprocess로 pdftotext 시도
        try:
            import subprocess
            result = subprocess.run(['pdftotext', str(pdf_path), '-'], 
                                  capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout
        except Exception as e:
            print(f"  - pdftotext 명령어 실패: {e}")
        
        print("❌ 모든 PDF 텍스트 추출 방법이 실패했습니다.")
        return ""
    
    def _extract_toc_by_rules(self, text: str, year: int) -> List[Dict[str, Any]]:
        """기본 규칙 기반 목차 추출"""
        items = []
        lines = text.split('\n')
        
        # 부문별 장 번호 범위
        section_ranges = {
            "공통부문": (1, 8),
            "토목부문": (9, 17),
            "건축부문": (18, 28),
            "기계설비부문": (29, 41),
            "유지관리부문": (42, 100)
        }
        
        for line in lines:
            line = line.strip()
            
            # 목차 패턴 매칭
            patterns = [
                r'(\d+-\d+(-\d+)?)\s+(.+)',  # 1-1-1 목적
                r'제(\d+)장\s+(.+)',  # 제1장 적용기준
                r'(\d+)\s+(.+)',  # 1 목적
            ]
            
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    if pattern == r'제(\d+)장\s+(.+)':
                        chapter_num = int(match.group(1))
                        title = match.group(2)
                        number = f"제{chapter_num}장"
                    else:
                        number = match.group(1)
                        title = match.group(-1)  # 마지막 그룹
                    
                    # 부문 분류
                    section = self._classify_section_by_number(number, section_ranges)
                    
                    items.append({
                        'text': f"{number} {title}",
                        'section': section,
                        'page': 0,  # 페이지는 나중에 수동 보정
                        'year': year,
                        'confidence': 0.7  # 기본 확신도
                    })
                    break
        
        return items
    
    def _classify_section_by_number(self, number: str, section_ranges: Dict[str, Tuple[int, int]]) -> str:
        """번호 기반 부문 분류"""
        # 장 번호 추출
        chapter_match = re.search(r'(\d+)', number)
        if chapter_match:
            chapter_num = int(chapter_match.group(1))
            
            for section, (start, end) in section_ranges.items():
                if start <= chapter_num <= end:
                    return section
        
        return "공통부문"  # 기본값
    
    def generate_semi_automated_ground_truth(self, target_year: int) -> Dict[str, Any]:
        """반자동화된 정답 데이터 생성"""
        print(f"\n🤖 {target_year}년 반자동화 정답 데이터 생성 시작...")
        
        # 1. 참조 데이터 로드
        if not self.reference_data:
            self.load_reference_ground_truth()
        
        # 2. PDF에서 목차 추출
        pdf_filename = f"{target_year}_construction_work_standard_price_list.pdf"
        extracted_items = self.extract_toc_from_pdf_simple(pdf_filename, target_year)
        
        if not extracted_items:
            print(f"❌ {target_year}년 데이터 추출 실패")
            return {}
        
        # 3. 참조 데이터와 매칭하여 정확도 향상
        enhanced_items = self._enhance_with_reference(extracted_items)
        
        # 4. 검증 리포트 생성
        validation_report = self._generate_validation_report(enhanced_items, target_year)
        
        # 5. 결과 저장
        output_file = self.ground_truth_dir / f"toc_ground_truth_{target_year}_semi_auto.md"
        self._save_ground_truth(enhanced_items, output_file, target_year)
        
        return {
            'items': enhanced_items,
            'validation_report': validation_report,
            'output_file': output_file
        }
    
    def _enhance_with_reference(self, extracted_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """참조 데이터를 활용하여 추출 결과 향상"""
        enhanced_items = []
        
        for item in extracted_items:
            enhanced_item = item.copy()
            
            # 참조 데이터에서 유사한 항목 찾기
            similar_items = self._find_similar_items(item['text'])
            
            if similar_items:
                # 가장 유사한 항목의 정보로 보완
                best_match = similar_items[0]
                enhanced_item['reference_match'] = best_match['text']
                enhanced_item['confidence'] = min(0.95, enhanced_item['confidence'] + 0.2)
                
                # 부문이 다르면 경고
                if best_match['section'] != item['section']:
                    enhanced_item['section_warning'] = True
                    enhanced_item['suggested_section'] = best_match['section']
            
            enhanced_items.append(enhanced_item)
        
        return enhanced_items
    
    def _find_similar_items(self, text: str) -> List[Dict[str, Any]]:
        """참조 데이터에서 유사한 항목 찾기"""
        similar_items = []
        
        for ref_item in self.reference_data['items']:
            similarity = difflib.SequenceMatcher(None, text.lower(), ref_item['text'].lower()).ratio()
            
            if similarity > 0.6:  # 60% 이상 유사
                similar_items.append({
                    'text': ref_item['text'],
                    'section': ref_item['section'],
                    'similarity': similarity
                })
        
        # 유사도 순으로 정렬
        similar_items.sort(key=lambda x: x['similarity'], reverse=True)
        return similar_items[:3]  # 상위 3개만 반환
    
    def _generate_validation_report(self, items: List[Dict[str, Any]], year: int) -> str:
        """검증 리포트 생성"""
        report = f"""# {year}년 반자동화 정답 데이터 검증 리포트

## 📊 추출 결과 요약
- **총 추출 항목**: {len(items)}개
- **부문별 분포**: {dict(Counter(item['section'] for item in items))}

## ⚠️ 검증이 필요한 항목들

"""
        
        # 경고가 있는 항목들
        warning_items = [item for item in items if item.get('section_warning', False)]
        
        if warning_items:
            report += f"### 부문 분류 경고 ({len(warning_items)}개)\n"
            for item in warning_items:
                report += f"- **{item['text']}**\n"
                report += f"  - 현재 분류: {item['section']}\n"
                report += f"  - 제안 분류: {item['suggested_section']}\n"
                report += f"  - 참조 항목: {item['reference_match']}\n\n"
        else:
            report += "### ✅ 부문 분류 경고 없음\n\n"
        
        # 확신도가 낮은 항목들
        low_confidence_items = [item for item in items if item['confidence'] < 0.8]
        
        if low_confidence_items:
            report += f"### 낮은 확신도 항목 ({len(low_confidence_items)}개)\n"
            for item in low_confidence_items:
                report += f"- **{item['text']}** (확신도: {item['confidence']:.2f})\n"
                if 'reference_match' in item:
                    report += f"  - 참조 항목: {item['reference_match']}\n"
                report += "\n"
        
        report += f"""
## 💡 수동 검증 권장사항
1. 부문 분류 경고가 있는 항목들을 우선적으로 검토하세요
2. 낮은 확신도 항목들의 분류를 확인하세요
3. 페이지 번호를 수동으로 입력하세요
4. 누락된 항목이 있는지 확인하세요

## 📝 다음 단계
1. 이 리포트를 참고하여 수동 검증 수행
2. 검증 완료 후 `toc_ground_truth_{year}.md` 파일로 저장
3. 머신러닝 학습에 활용
"""
        
        return report
    
    def _save_ground_truth(self, items: List[Dict[str, Any]], output_file: Path, year: int):
        """정답 데이터 저장"""
        content = f"# {year}년 표준품셈 목차 정답 데이터\n\n"
        
        # 부문별로 정리
        section_items = defaultdict(list)
        for item in items:
            section_items[item['section']].append(item)
        
        for section in ["공통부문", "토목부문", "건축부문", "기계설비부문", "유지관리부문"]:
            if section in section_items:
                content += f"## {section}\n\n"
                
                for item in section_items[section]:
                    # 경고 표시
                    warning_mark = " ⚠️" if item.get('section_warning', False) else ""
                    confidence_mark = f" (확신도: {item['confidence']:.2f})" if item['confidence'] < 0.9 else ""
                    
                    content += f"- {item['text']} , {item['page']}{warning_mark}{confidence_mark}\n"
                    
                    if 'reference_match' in item:
                        content += f"  - 참조: {item['reference_match']}\n"
                
                content += "\n"
        
        # 파일 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 반자동화 정답 데이터 저장: {output_file}")
    
    def generate_all_years_ground_truth(self):
        """모든 연도의 반자동화 정답 데이터 생성"""
        print("🚀 모든 연도 반자동화 정답 데이터 생성 시작")
        print("=" * 60)
        
        results = {}
        
        # 2023, 2024년 데이터 생성
        for year in [2023, 2024]:
            result = self.generate_semi_automated_ground_truth(year)
            if result:
                results[year] = result
                
                # 검증 리포트 저장
                report_file = self.ground_truth_dir / f"validation_report_{year}.md"
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write(result['validation_report'])
                print(f"  - 검증 리포트 저장: {report_file}")
        
        # 종합 리포트 생성
        self._generate_comprehensive_report(results)
        
        return results
    
    def _generate_comprehensive_report(self, results: Dict[int, Dict[str, Any]]):
        """종합 리포트 생성"""
        report = """# 반자동화 정답 데이터 생성 종합 리포트

## 📊 생성 결과 요약

"""
        
        for year, result in results.items():
            items = result['items']
            report += f"### {year}년\n"
            report += f"- **총 항목**: {len(items)}개\n"
            report += f"- **부문별 분포**: {dict(Counter(item['section'] for item in items))}\n"
            report += f"- **평균 확신도**: {sum(item['confidence'] for item in items) / len(items):.3f}\n"
            report += f"- **경고 항목**: {len([item for item in items if item.get('section_warning', False)])}개\n\n"
        
        report += """
## 🎯 다음 단계 권장사항

1. **수동 검증 수행**
   - 각 연도별 검증 리포트를 참고하여 수동 검증
   - 부문 분류 경고 항목 우선 검토
   - 페이지 번호 수동 입력

2. **머신러닝 학습 준비**
   - 검증 완료된 정답 데이터로 머신러닝 모델 학습
   - 다년도 데이터 통합 학습으로 일반화 능력 향상

3. **목차 추출 프로그램 개선**
   - 학습된 모델로 목차 추출 정확도 향상
   - 새로운 연도 PDF 자동 처리 가능

## 📁 생성된 파일들

- `toc_ground_truth_2023_semi_auto.md`: 2023년 반자동화 정답 데이터
- `toc_ground_truth_2024_semi_auto.md`: 2024년 반자동화 정답 데이터
- `validation_report_2023.md`: 2023년 검증 리포트
- `validation_report_2024.md`: 2024년 검증 리포트
"""
        
        # 종합 리포트 저장
        report_file = self.ground_truth_dir / "comprehensive_generation_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 종합 리포트 저장: {report_file}")

def main():
    parser = argparse.ArgumentParser(description="반자동 ground truth 생성기")
    parser.add_argument("--input_dir", type=str, default="input/By_year_Construction_work_standard_price_list", help="입력 PDF 폴더 경로")
    parser.add_argument("--ground_truth_dir", type=str, default="data/ground truth", help="ground truth 폴더 경로")
    args = parser.parse_args()
    generator = SemiAutomatedGroundTruthGenerator(input_dir=args.input_dir, ground_truth_dir=args.ground_truth_dir)
    
    # 모든 연도 정답 데이터 생성
    results = generator.generate_all_years_ground_truth()
    
    if results:
        print("\n✅ 반자동화 정답 데이터 생성 완료!")
        print("\n📋 다음 단계:")
        print("1. 생성된 검증 리포트를 확인하세요")
        print("2. 수동 검증을 수행하세요")
        print("3. 검증 완료 후 머신러닝 학습을 진행하세요")
    else:
        print("\n❌ 정답 데이터 생성에 실패했습니다.")

if __name__ == "__main__":
    main() 