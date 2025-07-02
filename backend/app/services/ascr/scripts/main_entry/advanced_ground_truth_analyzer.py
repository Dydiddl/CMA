#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
고급 정답 데이터 분석 도구

2025년 표준품셈 목차 정답 데이터를 활용한 다양한 분석 기능을 제공합니다.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
from collections import defaultdict, Counter

class AdvancedGroundTruthAnalyzer:
    """고급 정답 데이터 분석 클래스"""
    
    def __init__(self, ground_truth_path: str):
        self.ground_truth_path = Path(ground_truth_path)
        self.ground_truth_data = self._load_ground_truth()
        self.analysis_results = {}
        
    def _load_ground_truth(self) -> Dict[str, Any]:
        """정답 데이터 로드"""
        try:
            with open(self.ground_truth_path, 'r', encoding='utf-8', newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
                content = f.read()
            return self._parse_ground_truth_content(content)
        except Exception as e:
            print(f"정답 데이터 로드 실패: {e}")
            return {}
    
    def _parse_ground_truth_content(self, content: str) -> Dict[str, Any]:
        """정답 데이터 내용 파싱"""
        sections = {
            "공통부문": {"chapters": {}, "items": []},
            "토목부문": {"chapters": {}, "items": []},
            "건축부문": {"chapters": {}, "items": []},
            "기계설비부문": {"chapters": {}, "items": []},
            "유지관리부문": {"chapters": {}, "items": []}
        }
        
        current_section = None
        current_chapter = None
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # 부문 확인
            if line in sections.keys():
                current_section = line
                continue
            
            # 장 확인 (들여쓰기 8칸)
            if line.startswith('        ') and '제' in line and '장' in line:
                chapter_match = re.match(r'^\s*제(\d+)장\s+(.+?)\s*,\s*(\d+)$', line)
                if chapter_match and current_section:
                    chapter_num = chapter_match.group(1)
                    chapter_title = chapter_match.group(2).strip()
                    page = int(chapter_match.group(3))
                    chapter_key = f"제{chapter_num}장 {chapter_title}"
                    
                    sections[current_section]["chapters"][chapter_key] = {
                        "number": f"제{chapter_num}장",
                        "title": chapter_title,
                        "page": page,
                        "items": []
                    }
                    current_chapter = chapter_key
                continue
            
            # 항목 확인 (들여쓰기 12칸 이상)
            if line.startswith('            ') and current_chapter and current_section:
                item_match = re.match(r'^\s*(\d+-\d+(?:-\d+)?)\s+(.+?)\s*,\s*(\d+)$', line)
                if item_match:
                    item_number = item_match.group(1)
                    item_title = item_match.group(2).strip()
                    page = int(item_match.group(3))
                    
                    item_data = {
                        "number": item_number,
                        "title": item_title,
                        "page": page,
                        "chapter": current_chapter,
                        "section": current_section
                    }
                    
                    sections[current_section]["items"].append(item_data)
                    if current_chapter in sections[current_section]["chapters"]:
                        sections[current_section]["chapters"][current_chapter]["items"].append(item_data)
        
        return sections
    
    def analyze_structure_statistics(self) -> Dict[str, Any]:
        """구조 통계 분석"""
        stats = {
            "total_sections": len(self.ground_truth_data),
            "total_chapters": 0,
            "total_items": 0,
            "section_details": {},
            "page_distribution": {},
            "chapter_distribution": {},
            "item_distribution": {}
        }
        
        for section_name, section_data in self.ground_truth_data.items():
            chapters = section_data.get("chapters", {})
            items = section_data.get("items", [])
            
            stats["total_chapters"] += len(chapters)
            stats["total_items"] += len(items)
            
            # 부문별 상세 정보
            stats["section_details"][section_name] = {
                "chapters": len(chapters),
                "items": len(items),
                "page_range": self._get_page_range(items),
                "avg_items_per_chapter": len(items) / len(chapters) if chapters else 0
            }
            
            # 페이지 분포
            for item in items:
                page = item.get("page", 0)
                if page not in stats["page_distribution"]:
                    stats["page_distribution"][page] = []
                stats["page_distribution"][page].append(item)
            
            # 장별 항목 분포
            for chapter_name, chapter_data in chapters.items():
                chapter_items = chapter_data.get("items", [])
                stats["chapter_distribution"][chapter_name] = len(chapter_items)
        
        return stats
    
    def _get_page_range(self, items: List[Dict]) -> Tuple[int, int]:
        """페이지 범위 계산"""
        if not items:
            return (0, 0)
        
        pages = [item.get("page", 0) for item in items]
        return (min(pages), max(pages))
    
    def generate_training_dataset(self, output_dir: str) -> str:
        """머신러닝 훈련 데이터셋 생성"""
        training_data = []
        
        for section_name, section_data in self.ground_truth_data.items():
            for item in section_data.get("items", []):
                training_sample = {
                    "text": f"{item['number']} {item['title']}",
                    "number": item["number"],
                    "title": item["title"],
                    "page": item["page"],
                    "chapter": item["chapter"],
                    "section": section_name,
                    "level": self._get_item_level(item["number"]),
                    "features": self._extract_features(item)
                }
                training_data.append(training_sample)
        
        # 훈련 데이터 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dataset_path = Path(output_dir) / f"training_dataset_{timestamp}.json"
        
        with open(dataset_path, 'w', encoding='utf-8', newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
            json.dump(training_data, f, ensure_ascii=False, indent=2)
        
        return str(dataset_path)
    
    def _get_item_level(self, item_number: str) -> int:
        """항목 레벨 계산"""
        return len(item_number.split('-'))
    
    def _extract_features(self, item: Dict) -> Dict[str, Any]:
        """항목 특성 추출"""
        number = item["number"]
        title = item["title"]
        
        features = {
            "number_length": len(number),
            "title_length": len(title),
            "has_numbers": bool(re.search(r'\d', title)),
            "has_parentheses": bool(re.search(r'[\(\)]', title)),
            "has_korean": bool(re.search(r'[가-힣]', title)),
            "has_english": bool(re.search(r'[a-zA-Z]', title)),
            "word_count": len(title.split()),
            "level": self._get_item_level(number)
        }
        
        return features
    
    def create_validation_test_cases(self, output_dir: str) -> str:
        """검증 테스트 케이스 생성"""
        test_cases = []
        
        for section_name, section_data in self.ground_truth_data.items():
            # 부문별 테스트 케이스
            section_test = {
                "test_type": "section_validation",
                "section": section_name,
                "expected_chapters": list(section_data.get("chapters", {}).keys()),
                "expected_items": [item["number"] for item in section_data.get("items", [])]
            }
            test_cases.append(section_test)
            
            # 장별 테스트 케이스
            for chapter_name, chapter_data in section_data.get("chapters", {}).items():
                chapter_test = {
                    "test_type": "chapter_validation",
                    "chapter": chapter_name,
                    "section": section_name,
                    "expected_items": [item["number"] for item in chapter_data.get("items", [])],
                    "expected_page": chapter_data.get("page", 0)
                }
                test_cases.append(chapter_test)
        
        # 테스트 케이스 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_cases_path = Path(output_dir) / f"validation_test_cases_{timestamp}.json"
        
        with open(test_cases_path, 'w', encoding='utf-8', newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
            json.dump(test_cases, f, ensure_ascii=False, indent=2)
        
        return str(test_cases_path)
    
    def analyze_patterns(self) -> Dict[str, Any]:
        """패턴 분석"""
        patterns = {
            "number_patterns": Counter(),
            "title_patterns": Counter(),
            "page_patterns": Counter(),
            "common_words": Counter(),
            "special_characters": Counter()
        }
        
        for section_data in self.ground_truth_data.values():
            for item in section_data.get("items", []):
                number = item["number"]
                title = item["title"]
                page = item["page"]
                
                # 번호 패턴
                patterns["number_patterns"][number] += 1
                
                # 제목 패턴
                patterns["title_patterns"][title] += 1
                
                # 페이지 패턴
                patterns["page_patterns"][page] += 1
                
                # 단어 분석
                words = title.split()
                for word in words:
                    if len(word) > 1:  # 1글자 단어 제외
                        patterns["common_words"][word] += 1
                
                # 특수문자 분석
                special_chars = re.findall(r'[^\w\s가-힣]', title)
                for char in special_chars:
                    patterns["special_characters"][char] += 1
        
        return patterns
    
    def generate_comprehensive_report(self, output_dir: str) -> str:
        """종합 분석 리포트 생성"""
        # 모든 분석 실행
        stats = self.analyze_structure_statistics()
        patterns = self.analyze_patterns()
        
        # 리포트 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = Path(output_dir) / f"comprehensive_analysis_report_{timestamp}.md"
        
        report_content = f"""# 📊 2025년 표준품셈 목차 종합 분석 리포트
**분석 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**정답 데이터**: {self.ground_truth_path.name}

## 📈 구조 통계

### 전체 현황
- **총 부문 수**: {stats['total_sections']}개
- **총 장 수**: {stats['total_chapters']}개
- **총 항목 수**: {stats['total_items']}개

### 부문별 상세 통계
"""
        
        for section_name, details in stats["section_details"].items():
            report_content += f"""
#### {section_name}
- **장 수**: {details['chapters']}개
- **항목 수**: {details['items']}개
- **페이지 범위**: {details['page_range'][0]}~{details['page_range'][1]}
- **장당 평균 항목 수**: {details['avg_items_per_chapter']:.1f}개
"""
        
        # 패턴 분석 결과
        report_content += "\n## 🔍 패턴 분석\n"
        
        # 가장 많이 사용된 단어
        top_words = patterns["common_words"].most_common(20)
        report_content += "\n### 가장 많이 사용된 단어 (상위 20개)\n"
        for word, count in top_words:
            report_content += f"- **{word}**: {count}회\n"
        
        # 특수문자 분석
        top_chars = patterns["special_characters"].most_common(10)
        report_content += "\n### 특수문자 사용 빈도 (상위 10개)\n"
        for char, count in top_chars:
            report_content += f"- **{char}**: {count}회\n"
        
        # 활용 방안
        report_content += """
## 💡 활용 방안

### 1. 목차 추출 정확도 검증
- 추출된 목차와 정답 데이터 비교
- 부문별, 장별, 항목별 정확도 측정
- 누락된 항목 자동 감지

### 2. 머신러닝 모델 훈련
- 목차 항목 분류 모델 개발
- 패턴 기반 자동 분류 시스템 구축
- 새로운 문서의 목차 자동 추출

### 3. 품질 관리 시스템
- 목차 추출 결과 자동 검증
- 오류 패턴 분석 및 개선
- 지속적인 정확도 향상

### 4. 문서 구조 분석
- 표준품셈 문서의 구조적 특성 파악
- 부문별 특징 분석
- 페이지 분포 및 패턴 분석

### 5. 테스트 케이스 생성
- 자동화된 검증 테스트 케이스
- 다양한 시나리오 테스트
- 회귀 테스트 자동화
"""
        
        # 리포트 저장
        with open(report_path, 'w', encoding='utf-8', newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
            f.write(report_content)
        
        return str(report_path)

def main():
    """메인 함수"""
    analyzer = AdvancedGroundTruthAnalyzer("data/ground truth/toc_ground_truth_2025.md")
    
    # 출력 디렉토리 생성
    output_dir = Path("output/ground_truth_analysis")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("🔍 고급 정답 데이터 분석을 시작합니다...")
    
    # 1. 구조 통계 분석
    print("📊 구조 통계 분석 중...")
    stats = analyzer.analyze_structure_statistics()
    print(f"총 항목 수: {stats['total_items']}개")
    
    # 2. 훈련 데이터셋 생성
    print("🤖 훈련 데이터셋 생성 중...")
    dataset_path = analyzer.generate_training_dataset(str(output_dir))
    print(f"✅ 훈련 데이터셋 생성 완료: {dataset_path}")
    
    # 3. 테스트 케이스 생성
    print("🧪 테스트 케이스 생성 중...")
    test_cases_path = analyzer.create_validation_test_cases(str(output_dir))
    print(f"✅ 테스트 케이스 생성 완료: {test_cases_path}")
    
    # 4. 종합 리포트 생성
    print("📋 종합 리포트 생성 중...")
    report_path = analyzer.generate_comprehensive_report(str(output_dir))
    print(f"✅ 종합 리포트 생성 완료: {report_path}")
    
    print("\n🎉 모든 분석이 완료되었습니다!")

if __name__ == "__main__":
    main() 