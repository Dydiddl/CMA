#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
개선된 PDF 구조 검증 스크립트

테스트 결과를 바탕으로 다음 문제점들을 해결합니다:
1. 페이지 내 여러 부문이 발견되는 문제
2. 장 번호가 연속되지 않는 문제
3. 부문 분류의 정확성 향상
4. 페이지별 부문과 장의 정확한 매핑

실제 PDF 파일을 사용하여 정확한 검증을 수행합니다.
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.log import get_logger
from pypdf import PdfReader

# 로거 초기화
logger = get_logger("ImprovedPDFValidator")

class ImprovedPDFStructureValidator:
    """개선된 PDF 구조 검증 클래스"""
    
    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self.reader = None
        self.page_contents = {}
        self.page_analysis = {}
        
        # 개선된 부문 키워드 정의 (우선순위 순)
        self.section_keywords = {
            "공통부문": {
                "primary": ["공통부문", "공 통 부 문"],
                "secondary": ["적용기준", "가설공사", "토공사", "조경공사", "기초공사"],
                "exclude": ["토목", "건축", "기계설비", "유지관리"]
            },
            "토목부문": {
                "primary": ["토목부문", "토 목 부 문"],
                "secondary": ["도로포장공사", "하천공사", "터널공사", "궤도공사", "강구조공사"],
                "exclude": ["건축", "기계설비", "유지관리"]
            },
            "건축부문": {
                "primary": ["건축부문", "건 축 부 문"],
                "secondary": ["철근콘크리트공사", "돌공사", "목공사", "도장공사", "지붕공사"],
                "exclude": ["토목", "기계설비", "유지관리"]
            },
            "기계설비부문": {
                "primary": ["기계설비부문", "기 계 설 비 부 문"],
                "secondary": ["급수설비공사", "급탕설비공사", "배수설비공사", "공기조화설비공사"],
                "exclude": ["토목", "건축", "유지관리"]
            },
            "유지관리부문": {
                "primary": ["유지관리부문", "유 지 관 리 부 문"],
                "secondary": ["유지관리", "보수공사", "점검", "관리"],
                "exclude": ["토목", "건축", "기계설비"]
            }
        }
        
        # 개선된 장 패턴 정의
        self.chapter_patterns = [
            r'제(\d+)장\s*([가-힣A-Za-z0-9\-\s]+?)(?:\s*········|\s*$|\s*\d+)',
            r'(\d+)장\s*([가-힣A-Za-z0-9\-\s]+?)(?:\s*········|\s*$|\s*\d+)',
            r'Chapter\s*(\d+)\s*([가-힣A-Za-z0-9\-\s]+?)(?:\s*········|\s*$|\s*\d+)'
        ]
    
    def load_pdf(self) -> bool:
        """PDF 파일 로드"""
        try:
            self.reader = PdfReader(self.pdf_path)
            logger.info(f"PDF 로드 완료: {len(self.reader.pages)}페이지")
            return True
        except Exception as e:
            logger.error(f"PDF 로드 실패: {e}")
            return False
    
    def extract_page_contents(self, start_page: int = 1, end_page: int = None) -> Dict[int, str]:
        """페이지별 텍스트 추출"""
        if not self.reader:
            logger.error("PDF가 로드되지 않았습니다.")
            return {}
        
        if end_page is None:
            end_page = len(self.reader.pages)
        
        page_contents = {}
        
        for page_num in range(start_page - 1, min(end_page, len(self.reader.pages))):
            try:
                page = self.reader.pages[page_num]
                text = page.extract_text()
                page_contents[page_num + 1] = text
                logger.info(f"페이지 {page_num + 1} 텍스트 추출 완료 ({len(text)}자)")
            except Exception as e:
                logger.error(f"페이지 {page_num + 1} 텍스트 추출 실패: {e}")
        
        self.page_contents = page_contents
        return page_contents
    
    def analyze_page_sections_improved(self, page_num: int, content: str) -> Dict[str, Any]:
        """개선된 페이지 내 부문 분석"""
        section_scores = {}
        
        for section_name, keywords in self.section_keywords.items():
            score = 0
            matches = []
            
            # 1차 키워드 검색 (높은 가중치)
            for keyword in keywords["primary"]:
                if keyword in content:
                    positions = []
                    start = 0
                    while True:
                        pos = content.find(keyword, start)
                        if pos == -1:
                            break
                        positions.append(pos)
                        start = pos + 1
                    
                    for pos in positions:
                        context_start = max(0, pos - 50)
                        context_end = min(len(content), pos + len(keyword) + 50)
                        context = content[context_start:context_end]
                        
                        # 제외 키워드 확인
                        has_exclude = any(exclude in context for exclude in keywords["exclude"])
                        if not has_exclude:
                            score += 10  # 1차 키워드 가중치
                            matches.append({
                                "keyword": keyword,
                                "position": pos,
                                "context": context,
                                "weight": 10
                            })
            
            # 2차 키워드 검색 (중간 가중치)
            for keyword in keywords["secondary"]:
                if keyword in content:
                    positions = []
                    start = 0
                    while True:
                        pos = content.find(keyword, start)
                        if pos == -1:
                            break
                        positions.append(pos)
                        start = pos + 1
                    
                    for pos in positions:
                        context_start = max(0, pos - 30)
                        context_end = min(len(content), pos + len(keyword) + 30)
                        context = content[context_start:context_end]
                        
                        # 제외 키워드 확인
                        has_exclude = any(exclude in context for exclude in keywords["exclude"])
                        if not has_exclude:
                            score += 5  # 2차 키워드 가중치
                            matches.append({
                                "keyword": keyword,
                                "position": pos,
                                "context": context,
                                "weight": 5
                            })
            
            if score > 0:
                section_scores[section_name] = {
                    "score": score,
                    "matches": matches,
                    "confidence": min(score / 20.0, 1.0)  # 최대 20점을 1.0으로 정규화
                }
        
        # 가장 높은 점수의 부문 선택
        if section_scores:
            best_section = max(section_scores.items(), key=lambda x: x[1]["score"])
            return {
                "primary_section": best_section[0],
                "all_sections": section_scores,
                "confidence": best_section[1]["confidence"]
            }
        
        return {
            "primary_section": "미분류",
            "all_sections": {},
            "confidence": 0.0
        }
    
    def analyze_page_chapters_improved(self, page_num: int, content: str) -> List[Dict[str, Any]]:
        """개선된 페이지 내 장 분석"""
        chapters_found = []
        seen_chapters = set()  # 중복 제거용
        
        for pattern in self.chapter_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                chapter_num = match.group(1)
                chapter_title = match.group(2).strip()
                
                # 중복 제거
                chapter_key = f"{chapter_num}_{chapter_title}"
                if chapter_key in seen_chapters:
                    continue
                seen_chapters.add(chapter_key)
                
                # 컨텍스트 추출
                start_pos = match.start()
                context_start = max(0, start_pos - 100)
                context_end = min(len(content), start_pos + 200)
                context = content[context_start:context_end]
                
                # 페이지 번호 추출 시도
                page_number = self._extract_page_number(context)
                
                chapters_found.append({
                    "chapter_number": chapter_num,
                    "chapter_title": chapter_title,
                    "full_text": f"제{chapter_num}장 {chapter_title}",
                    "position": start_pos,
                    "context": context,
                    "page_number": page_number,
                    "confidence": self._calculate_chapter_confidence_improved(chapter_num, chapter_title, context)
                })
        
        # 위치 순으로 정렬
        chapters_found.sort(key=lambda x: x["position"])
        
        return chapters_found
    
    def _extract_page_number(self, context: str) -> int:
        """컨텍스트에서 페이지 번호 추출"""
        # 페이지 번호 패턴들
        page_patterns = [
            r'(\d{1,4})\s*페이지',
            r'페이지\s*(\d{1,4})',
            r'(\d{1,4})\s*$',
            r'(\d{1,4})\s*········'
        ]
        
        for pattern in page_patterns:
            match = re.search(pattern, context)
            if match:
                page_num = int(match.group(1))
                if 1 <= page_num <= 9999:  # 현실적인 페이지 범위
                    return page_num
        
        return 0
    
    def _calculate_chapter_confidence_improved(self, chapter_num: str, title: str, context: str) -> float:
        """개선된 장 신뢰도 계산"""
        confidence = 0.5  # 기본 신뢰도
        
        # 장 번호가 유효한지 확인
        if chapter_num.isdigit() and 1 <= int(chapter_num) <= 100:
            confidence += 0.2
        
        # 제목이 의미있는지 확인
        if len(title.strip()) > 0 and not title.strip().isdigit():
            confidence += 0.2
        
        # 컨텍스트에서 장 관련 단어 확인
        chapter_indicators = ["장", "Chapter", "Section", "Part"]
        for indicator in chapter_indicators:
            if indicator in context:
                confidence += 0.1
        
        # 페이지 번호가 있는지 확인
        if self._extract_page_number(context) > 0:
            confidence += 0.1
        
        # 특수문자나 점선이 있는지 확인 (목차 형식)
        if "····" in context or "·" * 10 in context:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def analyze_all_pages_improved(self, start_page: int = 1, end_page: int = None) -> Dict[str, Any]:
        """개선된 모든 페이지 분석"""
        if not self.load_pdf():
            return {}
        
        page_contents = self.extract_page_contents(start_page, end_page)
        analysis_results = {
            "pdf_info": {
                "filename": self.pdf_path.name,
                "total_pages": len(self.reader.pages),
                "analyzed_pages": len(page_contents),
                "analysis_time": datetime.now().isoformat()
            },
            "page_analysis": {},
            "summary": {
                "sections_found": {},
                "chapters_found": [],
                "section_transitions": [],
                "issues": []
            }
        }
        
        # 각 페이지 분석
        for page_num, content in page_contents.items():
            logger.info(f"페이지 {page_num} 개선된 분석 중...")
            
            # 개선된 부문 분석
            section_analysis = self.analyze_page_sections_improved(page_num, content)
            
            # 개선된 장 분석
            chapters = self.analyze_page_chapters_improved(page_num, content)
            
            page_analysis = {
                "page_number": page_num,
                "content_length": len(content),
                "primary_section": section_analysis["primary_section"],
                "section_confidence": section_analysis["confidence"],
                "all_sections": section_analysis["all_sections"],
                "chapters": chapters,
                "issues": []
            }
            
            # 문제점 검출
            if section_analysis["primary_section"] == "미분류":
                page_analysis["issues"].append("부문을 분류할 수 없음")
            
            if len(chapters) == 0:
                page_analysis["issues"].append("장 정보를 찾을 수 없음")
            
            if len(chapters) > 2:
                page_analysis["issues"].append(f"여러 장 발견: {len(chapters)}개")
            
            # 신뢰도가 낮은 항목들
            if section_analysis["confidence"] < 0.5:
                page_analysis["issues"].append(f"부문 신뢰도 낮음: {section_analysis['confidence']:.2f}")
            
            low_confidence_chapters = [c for c in chapters if c["confidence"] < 0.7]
            if low_confidence_chapters:
                page_analysis["issues"].append(f"신뢰도 낮은 장: {len(low_confidence_chapters)}개")
            
            analysis_results["page_analysis"][page_num] = page_analysis
            
            # 요약 정보 업데이트
            primary_section = section_analysis["primary_section"]
            if primary_section not in analysis_results["summary"]["sections_found"]:
                analysis_results["summary"]["sections_found"][primary_section] = []
            analysis_results["summary"]["sections_found"][primary_section].append(page_num)
            
            for chapter_info in chapters:
                analysis_results["summary"]["chapters_found"].append({
                    "page": page_num,
                    "chapter": chapter_info["full_text"],
                    "confidence": chapter_info["confidence"],
                    "page_number": chapter_info["page_number"]
                })
        
        # 부문 전환점 분석
        self._analyze_section_transitions(analysis_results)
        
        # 전체 요약 분석
        self._analyze_summary_improved(analysis_results)
        
        return analysis_results
    
    def _analyze_section_transitions(self, analysis_results: Dict[str, Any]):
        """부문 전환점 분석"""
        page_analysis = analysis_results["page_analysis"]
        transitions = []
        
        pages = sorted(page_analysis.keys(), key=int)
        for i in range(len(pages) - 1):
            current_page = int(pages[i])
            next_page = int(pages[i + 1])
            current_section = page_analysis[pages[i]]["primary_section"]
            next_section = page_analysis[pages[i + 1]]["primary_section"]
            
            if current_section != next_section:
                transitions.append({
                    "from_page": current_page,
                    "to_page": next_page,
                    "from_section": current_section,
                    "to_section": next_section,
                    "transition_point": f"p.{current_page}-{next_page}"
                })
        
        analysis_results["summary"]["section_transitions"] = transitions
    
    def _analyze_summary_improved(self, analysis_results: Dict[str, Any]):
        """개선된 전체 요약 분석"""
        summary = analysis_results["summary"]
        
        # 부문 분포 분석
        section_distribution = summary["sections_found"]
        if len(section_distribution) == 0:
            summary["issues"].append("전체 문서에서 부문을 찾을 수 없음")
        elif len(section_distribution) == 1:
            summary["issues"].append("단일 부문만 발견됨 - 부문 분류 검토 필요")
        
        # 장 분포 분석
        chapters = summary["chapters_found"]
        if len(chapters) == 0:
            summary["issues"].append("전체 문서에서 장을 찾을 수 없음")
        else:
            # 장 번호 순서 확인
            chapter_numbers = []
            for chapter in chapters:
                match = re.search(r'제(\d+)장', chapter["chapter"])
                if match:
                    chapter_numbers.append(int(match.group(1)))
            
            if chapter_numbers:
                chapter_numbers.sort()
                expected_sequence = list(range(min(chapter_numbers), max(chapter_numbers) + 1))
                missing_chapters = set(expected_sequence) - set(chapter_numbers)
                if missing_chapters:
                    summary["issues"].append(f"누락된 장 번호: {sorted(missing_chapters)}")
        
        # 부문 전환 분석
        transitions = summary["section_transitions"]
        if len(transitions) == 0:
            summary["issues"].append("부문 전환이 발견되지 않음")
        
        # 신뢰도 분석
        low_confidence_chapters = [c for c in chapters if c["confidence"] < 0.7]
        if low_confidence_chapters:
            summary["issues"].append(f"신뢰도가 낮은 장 발견: {len(low_confidence_chapters)}개")
    
    def generate_improved_report(self, analysis_results: Dict[str, Any]) -> str:
        """개선된 상세 분석 보고서 생성"""
        report = []
        report.append("# 📄 개선된 PDF 구조 검증 보고서")
        report.append("")
        
        # PDF 정보
        pdf_info = analysis_results["pdf_info"]
        report.append(f"## 📋 PDF 정보")
        report.append(f"- **파일명**: {pdf_info['filename']}")
        report.append(f"- **총 페이지**: {pdf_info['total_pages']}")
        report.append(f"- **분석 페이지**: {pdf_info['analyzed_pages']}")
        report.append(f"- **분석 시간**: {pdf_info['analysis_time']}")
        report.append("")
        
        # 요약 정보
        summary = analysis_results["summary"]
        report.append("## 📊 개선된 분석 요약")
        
        # 부문별 분포
        report.append("### 🏗️ 부문별 분포 (개선됨)")
        for section, pages in summary["sections_found"].items():
            report.append(f"- **{section}**: {len(pages)}페이지 ({', '.join(map(str, pages))})")
        report.append("")
        
        # 부문 전환점
        if summary["section_transitions"]:
            report.append("### 🔄 부문 전환점")
            for transition in summary["section_transitions"]:
                report.append(f"- **{transition['from_section']}** → **{transition['to_section']}** ({transition['transition_point']})")
            report.append("")
        
        # 장별 분포
        report.append("### 📚 장별 분포 (개선됨)")
        chapters = summary["chapters_found"]
        for chapter in chapters:
            confidence_icon = "✅" if chapter["confidence"] >= 0.7 else "⚠️"
            page_info = f"p.{chapter['page']}"
            if chapter["page_number"] > 0:
                page_info += f" (내용: p.{chapter['page_number']})"
            report.append(f"- {confidence_icon} **{chapter['chapter']}** ({page_info}, 신뢰도: {chapter['confidence']:.2f})")
        report.append("")
        
        # 문제점
        if summary["issues"]:
            report.append("### ⚠️ 발견된 문제점")
            for issue in summary["issues"]:
                report.append(f"- {issue}")
            report.append("")
        
        # 페이지별 상세 분석
        report.append("## 📄 페이지별 상세 분석 (개선됨)")
        for page_num, page_analysis in analysis_results["page_analysis"].items():
            report.append(f"### 📄 페이지 {page_num}")
            report.append(f"- **내용 길이**: {page_analysis['content_length']}자")
            report.append(f"- **주요 부문**: {page_analysis['primary_section']} (신뢰도: {page_analysis['section_confidence']:.2f})")
            
            # 모든 부문 정보
            if page_analysis["all_sections"]:
                report.append("- **모든 부문 점수**:")
                for section, data in page_analysis["all_sections"].items():
                    report.append(f"  - {section}: {data['score']}점 (신뢰도: {data['confidence']:.2f})")
            
            # 장 정보
            if page_analysis["chapters"]:
                report.append("- **발견된 장**:")
                for chapter in page_analysis["chapters"]:
                    confidence_icon = "✅" if chapter["confidence"] >= 0.7 else "⚠️"
                    page_info = f"p.{chapter['page_number']}" if chapter["page_number"] > 0 else "페이지 번호 없음"
                    report.append(f"  - {confidence_icon} {chapter['full_text']} ({page_info}, 신뢰도: {chapter['confidence']:.2f})")
            else:
                report.append("- **발견된 장**: 없음")
            
            # 문제점
            if page_analysis["issues"]:
                report.append("- **문제점**:")
                for issue in page_analysis["issues"]:
                    report.append(f"  - ⚠️ {issue}")
            
            report.append("")
        
        return "\n".join(report)
    
    def save_improved_analysis_results(self, analysis_results: Dict[str, Any], output_dir: Path) -> Path:
        """개선된 분석 결과 저장"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # JSON 파일 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = output_dir / f"improved_pdf_structure_analysis_{timestamp}.json"
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, ensure_ascii=False, indent=2)
        
        # 보고서 파일 저장
        report_path = output_dir / f"improved_pdf_structure_report_{timestamp}.md"
        report_content = self.generate_improved_report(analysis_results)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return json_path

def main():
    """메인 함수"""
    print("=== 개선된 PDF 구조 검증 테스트 시작 ===")
    
    # 입력 파일 확인
    pdf_path = Path("input/index.pdf")
    if not pdf_path.exists():
        print(f"❌ PDF 파일을 찾을 수 없습니다: {pdf_path}")
        print("💡 input/index.pdf 파일을 추가한 후 다시 실행하세요.")
        return
    
    # 출력 디렉토리 설정
    output_dir = Path("output/improved_validation_test")
    
    # 개선된 검증기 초기화
    validator = ImprovedPDFStructureValidator(pdf_path)
    
    try:
        # 전체 페이지 분석 (처음 20페이지만 테스트)
        print("🔍 개선된 PDF 구조 분석 중...")
        analysis_results = validator.analyze_all_pages_improved(start_page=1, end_page=20)
        
        if not analysis_results:
            print("❌ 분석에 실패했습니다.")
            return
        
        # 결과 저장
        print("💾 개선된 분석 결과 저장 중...")
        json_path = validator.save_improved_analysis_results(analysis_results, output_dir)
        
        # 요약 출력
        summary = analysis_results["summary"]
        print("\n=== 📊 개선된 분석 결과 요약 ===")
        print(f"📄 분석된 페이지: {analysis_results['pdf_info']['analyzed_pages']}페이지")
        print(f"🏗️ 발견된 부문: {len(summary['sections_found'])}개")
        print(f"📚 발견된 장: {len(summary['chapters_found'])}개")
        print(f"🔄 부문 전환점: {len(summary['section_transitions'])}개")
        
        if summary["issues"]:
            print(f"⚠️ 발견된 문제점: {len(summary['issues'])}개")
            for issue in summary["issues"][:3]:  # 처음 3개만 출력
                print(f"  - {issue}")
        
        print(f"\n✅ 개선된 분석 완료!")
        print(f"📁 결과 파일: {json_path}")
        print(f"📄 상세 보고서: {output_dir}/improved_pdf_structure_report_*.md")
        
    except Exception as e:
        print(f"❌ 분석 중 오류 발생: {e}")
        logger.error(f"분석 중 오류 발생: {e}")

if __name__ == "__main__":
    main() 