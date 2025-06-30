#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
향상된 PDF 구조 분석기
PDF 구조 분석 알고리즘의 정확성을 크게 개선한 클래스

주요 개선사항:
1. 페이지 번호 기반 부문 분류
2. 개선된 키워드 가중치 시스템
3. 부문별 장 번호 관리
4. 컨텍스트 기반 신뢰도 계산
5. 부문 전환점 정확한 파악
6. 중복 제거 및 검증 로직

개발자: ASCR Team
버전: 3.0
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from pypdf import PdfReader

# 로깅 설정
logger = logging.getLogger(__name__)

@dataclass
class ChapterInfo:
    """장 정보 데이터 클래스"""
    number: str
    title: str
    page: int
    section: str
    confidence: float
    context: str
    position: int

@dataclass
class SectionInfo:
    """부문 정보 데이터 클래스"""
    name: str
    start_page: int
    end_page: int
    chapters: List[ChapterInfo]
    confidence: float
    keywords_found: List[str]

class EnhancedPDFStructureAnalyzer:
    """향상된 PDF 구조 분석기"""
    
    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self.reader = None
        self.page_contents = {}
        
        # 페이지 번호 기반 부문 분류 범위 (실제 PDF 구조에 맞춤)
        self.section_page_ranges = {
            "공통부문": (1, 12),
            "토목부문": (13, 25),
            "건축부문": (26, 35),
            "기계설비부문": (36, 42),
            "유지관리부문": (43, 47)
        }
        
        # 개선된 부문 키워드 정의 (우선순위 및 가중치 포함)
        self.section_keywords = {
            "공통부문": {
                "primary": {
                    "공통부문": 15,
                    "공 통 부 문": 15,
                    "적용기준": 12,
                    "가설공사": 10
                },
                "secondary": {
                    "토공사": 8,
                    "조경공사": 8,
                    "기초공사": 8,
                    "건설기계": 6
                },
                "exclude": ["토목부문", "건축부문", "기계설비부문", "유지관리부문"]
            },
            "토목부문": {
                "primary": {
                    "토목부문": 15,
                    "토 목 부 문": 15,
                    "도로포장공사": 12,
                    "하천공사": 10
                },
                "secondary": {
                    "터널공사": 8,
                    "궤도공사": 8,
                    "강구조공사": 8,
                    "관부설": 6
                },
                "exclude": ["건축부문", "기계설비부문", "유지관리부문"]
            },
            "건축부문": {
                "primary": {
                    "건축부문": 15,
                    "건 축 부 문": 15,
                    "철근콘크리트공사": 12,
                    "돌공사": 10
                },
                "secondary": {
                    "목공사": 8,
                    "도장공사": 8,
                    "지붕공사": 8,
                    "마감공사": 6
                },
                "exclude": ["토목부문", "기계설비부문", "유지관리부문"]
            },
            "기계설비부문": {
                "primary": {
                    "기계설비부문": 15,
                    "기 계 설 비 부 문": 15,
                    "급수설비공사": 12,
                    "급탕설비공사": 10
                },
                "secondary": {
                    "배수설비공사": 8,
                    "공기조화설비공사": 8,
                    "전기설비공사": 8,
                    "소방설비공사": 6
                },
                "exclude": ["토목부문", "건축부문", "유지관리부문"]
            },
            "유지관리부문": {
                "primary": {
                    "유지관리부문": 15,
                    "유 지 관 리 부 문": 15,
                    "유지관리": 12,
                    "보수공사": 10
                },
                "secondary": {
                    "점검": 8,
                    "관리": 8,
                    "보수": 8,
                    "정비": 6
                },
                "exclude": ["토목부문", "건축부문", "기계설비부문"]
            }
        }
        
        # 개선된 장 패턴 정의
        self.chapter_patterns = [
            # 표준 장 패턴: "제1장 적용기준 ········ 31"
            r'제(\d+)장\s+([가-힣A-Za-z0-9\-\s]+?)\s*[·\s]*(\d+)',
            # 간단한 장 패턴: "제1장 적용기준"
            r'제(\d+)장\s+([가-힣A-Za-z0-9\-\s]+?)(?:\s*$|\s*[·\s])',
            # 영문 패턴: "Chapter 1 Title"
            r'Chapter\s*(\d+)\s+([가-힣A-Za-z0-9\-\s]+?)(?:\s*$|\s*[·\s])'
        ]
        
        # 부문별 장 번호 관리
        self.section_chapter_mapping = {
            "공통부문": "공통",
            "토목부문": "토목",
            "건축부문": "건축", 
            "기계설비부문": "기계설비",
            "유지관리부문": "유지관리"
        }
    
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
    
    def classify_section_by_page_number(self, page_num: int) -> str:
        """페이지 번호 기반 부문 분류"""
        for section_name, (start, end) in self.section_page_ranges.items():
            if start <= page_num <= end:
                return section_name
        return "미분류"
    
    def analyze_page_sections_enhanced(self, page_num: int, content: str) -> Dict[str, Any]:
        """향상된 페이지 내 부문 분석"""
        section_scores = {}
        
        # 페이지 번호 기반 기본 분류
        page_based_section = self.classify_section_by_page_number(page_num)
        if page_based_section != "미분류":
            section_scores[page_based_section] = {
                "score": 20,  # 페이지 번호 기반 분류는 높은 가중치
                "matches": [{"keyword": f"페이지{page_num}기반", "weight": 20}],
                "confidence": 0.8
            }
        
        # 키워드 기반 분석
        for section_name, keywords in self.section_keywords.items():
            if section_name in section_scores:
                continue  # 이미 페이지 번호로 분류된 경우
            
            score = 0
            matches = []
            
            # 1차 키워드 검색
            for keyword, weight in keywords["primary"].items():
                if keyword in content:
                    positions = self._find_keyword_positions(content, keyword)
                    for pos in positions:
                        context = self._extract_context(content, pos, len(keyword), 50)
                        if not self._has_exclude_keywords(context, keywords["exclude"]):
                            score += weight
                            matches.append({
                                "keyword": keyword,
                                "position": pos,
                                "context": context,
                                "weight": weight
                            })
            
            # 2차 키워드 검색
            for keyword, weight in keywords["secondary"].items():
                if keyword in content:
                    positions = self._find_keyword_positions(content, keyword)
                    for pos in positions:
                        context = self._extract_context(content, pos, len(keyword), 30)
                        if not self._has_exclude_keywords(context, keywords["exclude"]):
                            score += weight
                            matches.append({
                                "keyword": keyword,
                                "position": pos,
                                "context": context,
                                "weight": weight
                            })
            
            if score > 0:
                section_scores[section_name] = {
                    "score": score,
                    "matches": matches,
                    "confidence": min(score / 30.0, 1.0)  # 최대 30점을 1.0으로 정규화
                }
        
        # 가장 높은 점수의 부문 선택
        if section_scores:
            best_section = max(section_scores.items(), key=lambda x: x[1]["score"])
            return {
                "primary_section": best_section[0],
                "all_sections": section_scores,
                "confidence": best_section[1]["confidence"],
                "page_based_section": page_based_section
            }
        
        return {
            "primary_section": "미분류",
            "all_sections": {},
            "confidence": 0.0,
            "page_based_section": page_based_section
        }
    
    def analyze_page_chapters_enhanced(self, page_num: int, content: str, section: str) -> List[ChapterInfo]:
        """향상된 페이지 내 장 분석"""
        chapters_found = []
        seen_chapters = set()  # 중복 제거용
        
        for pattern in self.chapter_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                chapter_num = match.group(1)
                chapter_title = match.group(2).strip()
                page_number = int(match.group(3)) if len(match.groups()) > 2 else 0
                
                # 중복 제거
                chapter_key = f"{chapter_num}_{chapter_title}"
                if chapter_key in seen_chapters:
                    continue
                seen_chapters.add(chapter_key)
                
                # 컨텍스트 추출
                start_pos = match.start()
                context = self._extract_context(content, start_pos, len(match.group(0)), 100)
                
                # 부문별 장 번호 관리
                managed_chapter_num = self._manage_chapter_number_by_section(section, chapter_num)
                
                # 신뢰도 계산
                confidence = self._calculate_chapter_confidence_enhanced(
                    chapter_num, chapter_title, context, section, page_number
                )
                
                chapter_info = ChapterInfo(
                    number=managed_chapter_num,
                    title=chapter_title,
                    page=page_number,
                    section=section,
                    confidence=confidence,
                    context=context,
                    position=start_pos
                )
                
                chapters_found.append(chapter_info)
        
        # 위치 순으로 정렬
        chapters_found.sort(key=lambda x: x.position)
        
        return chapters_found
    
    def _find_keyword_positions(self, content: str, keyword: str) -> List[int]:
        """키워드 위치 찾기"""
        positions = []
        start = 0
        while True:
            pos = content.find(keyword, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        return positions
    
    def _extract_context(self, content: str, position: int, keyword_length: int, context_size: int) -> str:
        """키워드 주변 컨텍스트 추출"""
        context_start = max(0, position - context_size)
        context_end = min(len(content), position + keyword_length + context_size)
        return content[context_start:context_end]
    
    def _has_exclude_keywords(self, context: str, exclude_keywords: List[str]) -> bool:
        """제외 키워드 포함 여부 확인"""
        return any(exclude in context for exclude in exclude_keywords)
    
    def _manage_chapter_number_by_section(self, section: str, chapter_num: str) -> str:
        """부문별 장 번호 관리"""
        if section in self.section_chapter_mapping:
            prefix = self.section_chapter_mapping[section]
            return f"{prefix}_{chapter_num}"
        return chapter_num
    
    def _calculate_chapter_confidence_enhanced(self, chapter_num: str, title: str, 
                                             context: str, section: str, page_number: int) -> float:
        """향상된 장 신뢰도 계산"""
        confidence = 0.5  # 기본 신뢰도
        
        # 장 번호 유효성 검증
        if chapter_num.isdigit() and 1 <= int(chapter_num) <= 100:
            confidence += 0.2
        
        # 제목 유효성 검증
        if len(title.strip()) > 0 and len(title.strip()) < 100:
            confidence += 0.2
        
        # 컨텍스트에서 장 관련 단어 확인
        chapter_indicators = ["장", "Chapter", "Section", "Part"]
        for indicator in chapter_indicators:
            if indicator in context:
                confidence += 0.1
                break
        
        # 페이지 번호 유효성 검증
        if page_number > 0 and page_number <= 1000:
            confidence += 0.1
        
        # 부문과 장의 일관성 검증
        if section != "미분류":
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def analyze_all_pages_enhanced(self, start_page: int = 1, end_page: int = None) -> Dict[str, Any]:
        """향상된 전체 페이지 분석"""
        if not self.load_pdf():
            return {}
        
        page_contents = self.extract_page_contents(start_page, end_page)
        
        analysis_results = {
            "pdf_info": {
                "filename": self.pdf_path.name,
                "total_pages": len(self.reader.pages),
                "analyzed_pages": len(page_contents),
                "analysis_time": datetime.now().isoformat(),
                "analyzer_version": "3.0"
            },
            "page_analysis": {},
            "section_analysis": {},
            "summary": {
                "sections_found": {},
                "chapters_found": [],
                "section_transitions": [],
                "issues": [],
                "confidence_stats": {
                    "high_confidence": 0,
                    "medium_confidence": 0,
                    "low_confidence": 0
                }
            }
        }
        
        # 각 페이지 분석
        for page_num, content in page_contents.items():
            logger.info(f"페이지 {page_num} 향상된 분석 중...")
            
            # 부문 분석
            section_analysis = self.analyze_page_sections_enhanced(page_num, content)
            primary_section = section_analysis["primary_section"]
            
            # 장 분석
            chapters = self.analyze_page_chapters_enhanced(page_num, content, primary_section)
            
            page_analysis = {
                "page_number": page_num,
                "content_length": len(content),
                "primary_section": primary_section,
                "section_confidence": section_analysis["confidence"],
                "page_based_section": section_analysis["page_based_section"],
                "all_sections": section_analysis["all_sections"],
                "chapters": chapters,
                "issues": []
            }
            
            # 문제점 검출
            if primary_section == "미분류":
                page_analysis["issues"].append("부문을 분류할 수 없음")
            
            if len(chapters) == 0:
                page_analysis["issues"].append("장 정보를 찾을 수 없음")
            
            if len(chapters) > 3:
                page_analysis["issues"].append(f"여러 장 발견: {len(chapters)}개")
            
            # 신뢰도 분석
            if section_analysis["confidence"] < 0.5:
                page_analysis["issues"].append(f"부문 신뢰도 낮음: {section_analysis['confidence']:.2f}")
            
            low_confidence_chapters = [c for c in chapters if c.confidence < 0.7]
            if low_confidence_chapters:
                page_analysis["issues"].append(f"신뢰도 낮은 장: {len(low_confidence_chapters)}개")
            
            analysis_results["page_analysis"][page_num] = page_analysis
            
            # 요약 정보 업데이트
            if primary_section not in analysis_results["summary"]["sections_found"]:
                analysis_results["summary"]["sections_found"][primary_section] = []
            analysis_results["summary"]["sections_found"][primary_section].append(page_num)
            
            for chapter in chapters:
                analysis_results["summary"]["chapters_found"].append({
                    "page": page_num,
                    "chapter": f"{chapter.number} {chapter.title}",
                    "section": chapter.section,
                    "confidence": chapter.confidence,
                    "page_number": chapter.page
                })
        
        # 부문 전환점 분석
        self._analyze_section_transitions_enhanced(analysis_results)
        
        # 전체 요약 분석
        self._analyze_summary_enhanced(analysis_results)
        
        return analysis_results
    
    def _analyze_section_transitions_enhanced(self, analysis_results: Dict[str, Any]):
        """향상된 부문 전환점 분석"""
        page_analysis = analysis_results["page_analysis"]
        transitions = []
        
        sorted_pages = sorted(page_analysis.keys())
        for i in range(1, len(sorted_pages)):
            prev_page = sorted_pages[i-1]
            curr_page = sorted_pages[i]
            
            prev_section = page_analysis[prev_page]["primary_section"]
            curr_section = page_analysis[curr_page]["primary_section"]
            
            if prev_section != curr_section and prev_section != "미분류" and curr_section != "미분류":
                transitions.append({
                    "from_page": prev_page,
                    "to_page": curr_page,
                    "from_section": prev_section,
                    "to_section": curr_section,
                    "transition_point": f"{prev_page}-{curr_page}"
                })
        
        analysis_results["summary"]["section_transitions"] = transitions
    
    def _analyze_summary_enhanced(self, analysis_results: Dict[str, Any]):
        """향상된 전체 요약 분석"""
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
        
        # 신뢰도 통계
        high_conf = len([c for c in chapters if c["confidence"] >= 0.8])
        medium_conf = len([c for c in chapters if 0.6 <= c["confidence"] < 0.8])
        low_conf = len([c for c in chapters if c["confidence"] < 0.6])
        
        summary["confidence_stats"] = {
            "high_confidence": high_conf,
            "medium_confidence": medium_conf,
            "low_confidence": low_conf
        }
    
    def generate_enhanced_report(self, analysis_results: Dict[str, Any]) -> str:
        """향상된 분석 보고서 생성"""
        report = []
        report.append("# 📄 향상된 PDF 구조 분석 보고서")
        report.append("")
        
        # PDF 정보
        pdf_info = analysis_results["pdf_info"]
        report.append(f"## 📋 분석 개요")
        report.append(f"- **파일명**: {pdf_info['filename']}")
        report.append(f"- **총 페이지**: {pdf_info['total_pages']}페이지")
        report.append(f"- **분석 페이지**: {pdf_info['analyzed_pages']}페이지")
        report.append(f"- **분석 시간**: {pdf_info['analysis_time']}")
        report.append(f"- **분석기 버전**: {pdf_info['analyzer_version']}")
        report.append("")
        
        # 부문별 분석
        summary = analysis_results["summary"]
        report.append("## 🏗️ 부문별 분석")
        for section, pages in summary["sections_found"].items():
            report.append(f"### {section}")
            report.append(f"- **발견 페이지**: {len(pages)}페이지")
            report.append(f"- **페이지 범위**: {min(pages)}-{max(pages)}")
            report.append("")
        
        # 장 분석
        report.append("## 📚 장 분석")
        chapters = summary["chapters_found"]
        if chapters:
            report.append(f"- **총 장 수**: {len(chapters)}개")
            report.append("")
            
            # 부문별 장 분류
            section_chapters = {}
            for chapter in chapters:
                section = chapter["section"]
                if section not in section_chapters:
                    section_chapters[section] = []
                section_chapters[section].append(chapter)
            
            for section, section_chapters_list in section_chapters.items():
                report.append(f"### {section}")
                for chapter in section_chapters_list:
                    confidence_emoji = "🟢" if chapter["confidence"] >= 0.8 else "🟡" if chapter["confidence"] >= 0.6 else "🔴"
                    report.append(f"- {confidence_emoji} {chapter['chapter']} (p.{chapter['page_number']}) - 신뢰도: {chapter['confidence']:.2f}")
                report.append("")
        
        # 부문 전환점
        transitions = summary["section_transitions"]
        if transitions:
            report.append("## 🔄 부문 전환점")
            for transition in transitions:
                report.append(f"- **{transition['from_section']}** → **{transition['to_section']}** (p.{transition['transition_point']})")
            report.append("")
        
        # 신뢰도 통계
        confidence_stats = summary["confidence_stats"]
        report.append("## 📊 신뢰도 통계")
        report.append(f"- **높은 신뢰도** (≥0.8): {confidence_stats['high_confidence']}개")
        report.append(f"- **중간 신뢰도** (0.6-0.8): {confidence_stats['medium_confidence']}개")
        report.append(f"- **낮은 신뢰도** (<0.6): {confidence_stats['low_confidence']}개")
        report.append("")
        
        # 문제점
        issues = summary["issues"]
        if issues:
            report.append("## ⚠️ 발견된 문제점")
            for issue in issues:
                report.append(f"- {issue}")
            report.append("")
        
        # 개선 권장사항
        report.append("## 💡 개선 권장사항")
        if confidence_stats['low_confidence'] > 0:
            report.append("- 신뢰도가 낮은 장들의 분류를 수동으로 검토하세요")
        if len(transitions) == 0:
            report.append("- 부문 전환이 발견되지 않았습니다. 부문 분류 로직을 검토하세요")
        if len(issues) > 0:
            report.append("- 발견된 문제점들을 해결하여 분석 정확도를 향상시키세요")
        
        return "\n".join(report)
    
    def save_enhanced_analysis_results(self, analysis_results: Dict[str, Any], output_dir: Path) -> Path:
        """향상된 분석 결과 저장"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # JSON 파일로 저장
        import json
        json_file = output_dir / f"enhanced_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # dataclass를 dict로 변환
        def convert_dataclass(obj):
            if hasattr(obj, '__dict__'):
                return obj.__dict__
            return obj
        
        # ChapterInfo 객체들을 dict로 변환
        for page_num, page_analysis in analysis_results["page_analysis"].items():
            if "chapters" in page_analysis:
                page_analysis["chapters"] = [convert_dataclass(chapter) for chapter in page_analysis["chapters"]]
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, ensure_ascii=False, indent=2, default=convert_dataclass)
        
        # 보고서 파일로 저장
        report_content = self.generate_enhanced_report(analysis_results)
        report_file = output_dir / f"enhanced_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        logger.info(f"향상된 분석 결과 저장 완료:")
        logger.info(f"- JSON: {json_file}")
        logger.info(f"- 보고서: {report_file}")
        
        return json_file 