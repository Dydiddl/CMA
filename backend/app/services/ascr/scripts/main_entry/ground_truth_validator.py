#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
정답 데이터 검증 모듈 - 개선된 부문 분류 로직

변환된 목차 구조를 정답 데이터와 비교하여 정확도를 측정하고 개선 방안을 제시합니다.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime

class GroundTruthValidator:
    """정답 데이터 검증 클래스 - 개선된 부문 분류"""
    
    def __init__(self, ground_truth_path: str):
        self.ground_truth_path = Path(ground_truth_path)
        self.ground_truth_data = self._load_ground_truth()
        
    def _load_ground_truth(self) -> Dict[str, Any]:
        """정답 데이터 로드"""
        try:
            with open(self.ground_truth_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 정답 데이터 파싱
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
    
    def validate_toc_structure(self, toc_structure: Dict[str, Any]) -> Dict[str, Any]:
        """목차 구조 검증 - 개선된 부문 분류"""
        try:
            # 추출된 목차에서 부문별 항목 재분류
            reclassified_structure = self._reclassify_sections(toc_structure)
            
            # 검증 수행
            validation_result = {
                "overall_accuracy": 0.0,
                "section_accuracy": {},
                "chapter_accuracy": {},
                "item_accuracy": {},
                "missing_sections": [],
                "missing_chapters": [],
                "missing_items": [],
                "incorrect_classifications": [],
                "reclassified_structure": reclassified_structure
            }
            
            # 부문별 정확도 계산
            for section_name in self.ground_truth_data.keys():
                section_accuracy = self._calculate_section_accuracy(
                    section_name, reclassified_structure.get(section_name, {})
                )
                validation_result["section_accuracy"][section_name] = section_accuracy
            
            # 전체 정확도 계산
            total_sections = len(self.ground_truth_data)
            if total_sections > 0:
                validation_result["overall_accuracy"] = sum(
                    validation_result["section_accuracy"].values()
                ) / total_sections
            
            # 누락된 항목 분석
            self._analyze_missing_items(validation_result, reclassified_structure)
            
            # 잘못된 분류 분석
            self._analyze_incorrect_classifications(validation_result, reclassified_structure)
            
            return validation_result
            
        except Exception as e:
            print(f"목차 구조 검증 실패: {e}")
            return {"error": str(e), "overall_accuracy": 0.0, "incorrect_classifications": []}
    
    def _reclassify_sections(self, toc_structure: Dict[str, Any]) -> Dict[str, Any]:
        """부문별 항목 재분류"""
        reclassified = {
            "공통부문": {"chapters": {}, "items": []},
            "토목부문": {"chapters": {}, "items": []},
            "건축부문": {"chapters": {}, "items": []},
            "기계설비부문": {"chapters": {}, "items": []},
            "유지관리부문": {"chapters": {}, "items": []}
        }
        
        entries = toc_structure.get("entries", [])
        
        for entry in entries:
            # 장 번호로 부문 분류
            section = self._classify_by_chapter_number(entry)
            if section:
                # 장 정보 추가
                if entry.get("level") == 1 and "제" in str(entry.get("number", "")):
                    chapter_key = f"{entry['number']} {entry['title']}"
                    reclassified[section]["chapters"][chapter_key] = {
                        "number": entry["number"],
                        "title": entry["title"],
                        "page": entry.get("page", 0),
                        "items": []
                    }
                
                # 항목 정보 추가
                if entry.get("level") >= 2:
                    item_data = {
                        "number": entry["number"],
                        "title": entry["title"],
                        "page": entry.get("page", 0),
                        "chapter": entry.get("chapter", ""),
                        "section": section
                    }
                    reclassified[section]["items"].append(item_data)
        
        return reclassified
    
    def _classify_by_chapter_number(self, entry: Dict[str, Any]) -> Optional[str]:
        """장 번호로 부문 분류"""
        chapter_num = None
        
        # 장 번호 추출
        if entry.get("level") == 1 and "제" in str(entry.get("number", "")):
            match = re.match(r'제(\d+)장', str(entry.get("number", "")))
            if match:
                chapter_num = int(match.group(1))
        elif entry.get("level") >= 2:
            # 상위 장 번호 확인
            parent = entry.get("parent", "")
            match = re.match(r'제(\d+)장', parent)
            if match:
                chapter_num = int(match.group(1))
        
        if chapter_num is None:
            return None
        
        # 부문 분류 규칙
        if chapter_num <= 8:
            return "공통부문"
        elif chapter_num <= 17:
            return "토목부문"
        elif chapter_num <= 28:
            return "건축부문"
        elif chapter_num <= 41:
            return "기계설비부문"
        else:
            return "유지관리부문"
    
    def _calculate_section_accuracy(self, section_name: str, extracted_section: Dict[str, Any]) -> float:
        """부문별 정확도 계산"""
        ground_truth_section = self.ground_truth_data.get(section_name, {})
        
        if not ground_truth_section:
            return 0.0
        
        # 장 정확도
        gt_chapters = set(ground_truth_section.get("chapters", {}).keys())
        extracted_chapters = set(extracted_section.get("chapters", {}).keys())
        
        chapter_accuracy = len(gt_chapters & extracted_chapters) / len(gt_chapters) if gt_chapters else 0.0
        
        # 항목 정확도
        gt_items = set(item["number"] for item in ground_truth_section.get("items", []))
        extracted_items = set(item["number"] for item in extracted_section.get("items", []))
        
        item_accuracy = len(gt_items & extracted_items) / len(gt_items) if gt_items else 0.0
        
        # 종합 정확도 (장 40%, 항목 60%)
        return chapter_accuracy * 0.4 + item_accuracy * 0.6
    
    def _analyze_missing_items(self, validation_result: Dict[str, Any], reclassified_structure: Dict[str, Any]):
        """누락된 항목 분석"""
        for section_name, ground_truth_section in self.ground_truth_data.items():
            extracted_section = reclassified_structure.get(section_name, {})
            
            # 누락된 장
            gt_chapters = set(ground_truth_section.get("chapters", {}).keys())
            extracted_chapters = set(extracted_section.get("chapters", {}).keys())
            missing_chapters = gt_chapters - extracted_chapters
            validation_result["missing_chapters"].extend(list(missing_chapters))
            
            # 누락된 항목
            gt_items = set(item["number"] for item in ground_truth_section.get("items", []))
            extracted_items = set(item["number"] for item in extracted_section.get("items", []))
            missing_items = gt_items - extracted_items
            
            for item_number in missing_items:
                # 해당 항목의 상세 정보 찾기
                for item in ground_truth_section.get("items", []):
                    if item["number"] == item_number:
                        validation_result["missing_items"].append({
                            "number": item["number"],
                            "title": item["title"],
                            "chapter": item["chapter"],
                            "section": item["section"]
                        })
                        break
    
    def _analyze_incorrect_classifications(self, validation_result: Dict[str, Any], reclassified_structure: Dict[str, Any]):
        """잘못된 분류 분석"""
        incorrect_items = []
        
        # 정답 데이터와 추출된 데이터 비교
        for section_name, ground_truth_section in self.ground_truth_data.items():
            extracted_section = reclassified_structure.get(section_name, {})
            
            # 정답 데이터의 항목들
            gt_items = ground_truth_section.get("items", [])
            extracted_items = extracted_section.get("items", [])
            
            # 추출된 항목 중 잘못된 부문에 분류된 것들 찾기
            for item in extracted_items:
                item_number = item.get("number", "")
                item_title = item.get("title", "")
                
                # 정답 데이터에서 해당 항목 찾기
                gt_item = None
                for gt in gt_items:
                    if gt.get("number") == item_number and gt.get("title") == item_title:
                        gt_item = gt
                        break
                
                # 정답 데이터에 없거나 다른 부문에 있는 경우
                if gt_item is None or gt_item.get("section") != section_name:
                    incorrect_items.append({
                        "item": f"{item_number} {item_title}",
                        "current_section": section_name,
                        "expected_section": gt_item.get("section") if gt_item else "알 수 없음",
                        "reason": "잘못된 부문 분류"
                    })
        
        validation_result["incorrect_classifications"] = incorrect_items
    
    def generate_validation_report(self, validation_result: Dict[str, Any], output_dir: str) -> str:
        """검증 리포트 생성"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = Path(output_dir) / f"validation_report_{timestamp}.md"
        
        report_content = f"""# 📊 목차 추출 정확도 검증 리포트
**검증 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**정답 데이터**: {self.ground_truth_path.name}

## 🎯 전체 정확도: {validation_result.get('overall_accuracy', 0.0):.1%}

## 📋 부문별 정확도
"""
        
        for section_name, accuracy in validation_result.get("section_accuracy", {}).items():
            report_content += f"- **{section_name}**: {accuracy:.1%}\n"
        
        report_content += "\n## ❌ 오류 분석\n"
        
        # 누락된 부문
        missing_sections = [section for section, accuracy in validation_result.get("section_accuracy", {}).items() 
                           if accuracy == 0.0]
        if missing_sections:
            report_content += f"### 누락된 부문 ({len(missing_sections)}개)\n"
            for section in missing_sections:
                report_content += f"- {section}\n"
            report_content += "\n"
        
        # 누락된 장
        missing_chapters = validation_result.get("missing_chapters", [])
        if missing_chapters:
            report_content += f"### 누락된 장 ({len(missing_chapters)}개)\n"
            for chapter in missing_chapters[:20]:  # 처음 20개만 표시
                report_content += f"- {chapter}\n"
            if len(missing_chapters) > 20:
                report_content += f"- ... 외 {len(missing_chapters) - 20}개\n"
            report_content += "\n"
        
        # 누락된 항목
        missing_items = validation_result.get("missing_items", [])
        if missing_items:
            report_content += f"### 누락된 항목 ({len(missing_items)}개)\n"
            for item in missing_items[:20]:  # 처음 20개만 표시
                report_content += f"- {item['number']} {item['title']} ({item['chapter']})\n"
            if len(missing_items) > 20:
                report_content += f"- ... 외 {len(missing_items) - 20}개\n"
            report_content += "\n"
        
        # 개선 방안
        report_content += "## 💡 개선 방안\n"
        if validation_result.get("overall_accuracy", 0.0) < 0.5:
            report_content += "- 목차 항목 누락 개선이 필요합니다.\n"
            report_content += "- - 들여쓰기 기반 계층 구조 인식 강화\n"
            report_content += "- - 다양한 목차 패턴 지원 확대\n"
        
        if missing_sections:
            report_content += "- 부문 누락 개선이 필요합니다.\n"
            report_content += f"- 누락된 부문: {', '.join(missing_sections)}\n"
        
        # 리포트 저장
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return str(report_path)
    
    def save_validation_result(self, validation_result: Dict[str, Any], output_dir: str) -> str:
        """검증 결과 JSON 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_path = Path(output_dir) / f"validation_result_{timestamp}.json"
        
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(validation_result, f, ensure_ascii=False, indent=2)
        
        return str(result_path)

def main():
    """테스트 실행"""
    validator = GroundTruthValidator("data/ground truth/toc_ground_truth_2025.md")
    
    # 테스트용 목차 구조
    test_structure = {
        "entries": [
            {
                "number": "제1장",
                "title": "적용기준",
                "page": 3,
                "level": 1,
                "section": "공통부문",
                "parent": "공통부문"
            }
        ]
    }
    
    result = validator.validate_toc_structure(test_structure)
    print(f"검증 결과: {result.get('overall_accuracy', 0.0):.1%}")

if __name__ == "__main__":
    main()