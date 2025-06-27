#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 구조 검증 테스트 스크립트

이 스크립트는 실제 PDF 파일을 사용하여 다음을 검증합니다:
1. 각 페이지별로 어떤 부문에 해당하는지 검증
2. 각 페이지별로 어떤 장에 해당하는지 검증
3. 페이지 내에서 부문과 장이 어떻게 분류되는지 상세 분석

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
logger = get_logger("PDFStructureValidator")

class PDFStructureValidator:
    """PDF 구조 검증 클래스"""
    
    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self.reader = None
        self.page_contents = {}
        self.page_analysis = {}
        
        # 부문 키워드 정의
        self.section_keywords = {
            "공통부문": ["공통부문", "공 통 부 문", "공통", "적용기준"],
            "토목부문": ["토목부문", "토 목 부 문", "토목", "토공사", "조경공사"],
            "건축부문": ["건축부문", "건 축 부 문", "건축", "철근콘크리트공사", "돌공사"],
            "기계설비부문": ["기계설비부문", "기 계 설 비 부 문", "기계설비", "기계", "설비"],
            "유지관리부문": ["유지관리부문", "유 지 관 리 부 문", "유지관리", "유지", "관리"]
        }
        
        # 장 패턴 정의
        self.chapter_patterns = [
            r'제(\d+)장\s*([가-힣A-Za-z0-9\-\s]+)',
            r'(\d+)장\s*([가-힣A-Za-z0-9\-\s]+)',
            r'Chapter\s*(\d+)\s*([가-힣A-Za-z0-9\-\s]+)'
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
    
    def analyze_page_sections(self, page_num: int, content: str) -> List[Dict[str, Any]]:
        """페이지 내 부문 분석"""
        sections_found = []
        
        for section_name, keywords in self.section_keywords.items():
            for keyword in keywords:
                if keyword in content:
                    # 키워드 위치 찾기
                    positions = []
                    start = 0
                    while True:
                        pos = content.find(keyword, start)
                        if pos == -1:
                            break
                        positions.append(pos)
                        start = pos + 1
                    
                    for pos in positions:
                        # 컨텍스트 추출 (앞뒤 100자)
                        context_start = max(0, pos - 100)
                        context_end = min(len(content), pos + len(keyword) + 100)
                        context = content[context_start:context_end]
                        
                        sections_found.append({
                            "section": section_name,
                            "keyword": keyword,
                            "position": pos,
                            "context": context,
                            "confidence": self._calculate_section_confidence(keyword, context)
                        })
        
        return sections_found
    
    def analyze_page_chapters(self, page_num: int, content: str) -> List[Dict[str, Any]]:
        """페이지 내 장 분석"""
        chapters_found = []
        
        for pattern in self.chapter_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                chapter_num = match.group(1)
                chapter_title = match.group(2).strip()
                
                # 컨텍스트 추출
                start_pos = match.start()
                context_start = max(0, start_pos - 100)
                context_end = min(len(content), start_pos + 200)
                context = content[context_start:context_end]
                
                chapters_found.append({
                    "chapter_number": chapter_num,
                    "chapter_title": chapter_title,
                    "full_text": f"제{chapter_num}장 {chapter_title}",
                    "position": start_pos,
                    "context": context,
                    "confidence": self._calculate_chapter_confidence(chapter_num, chapter_title, context)
                })
        
        return chapters_found
    
    def _calculate_section_confidence(self, keyword: str, context: str) -> float:
        """부문 신뢰도 계산"""
        confidence = 0.5  # 기본 신뢰도
        
        # 키워드 길이에 따른 가중치
        if len(keyword) >= 4:
            confidence += 0.2
        
        # 컨텍스트에서 부문 관련 단어 확인
        section_indicators = ["부문", "분류", "구분", "구성"]
        for indicator in section_indicators:
            if indicator in context:
                confidence += 0.1
        
        # 숫자나 특수문자가 포함되지 않은 경우 가중치
        if not re.search(r'\d', keyword) and not re.search(r'[^\w\s]', keyword):
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _calculate_chapter_confidence(self, chapter_num: str, title: str, context: str) -> float:
        """장 신뢰도 계산"""
        confidence = 0.5  # 기본 신뢰도
        
        # 장 번호가 유효한지 확인
        if chapter_num.isdigit() and 1 <= int(chapter_num) <= 100:
            confidence += 0.2
        
        # 제목이 의미있는지 확인
        if len(title.strip()) > 0:
            confidence += 0.2
        
        # 컨텍스트에서 장 관련 단어 확인
        chapter_indicators = ["장", "Chapter", "Section", "Part"]
        for indicator in chapter_indicators:
            if indicator in context:
                confidence += 0.1
        
        return min(confidence, 1.0)
    
    def analyze_all_pages(self, start_page: int = 1, end_page: int = None) -> Dict[str, Any]:
        """모든 페이지 분석"""
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
                "issues": []
            }
        }
        
        # 각 페이지 분석
        for page_num, content in page_contents.items():
            logger.info(f"페이지 {page_num} 분석 중...")
            
            page_analysis = {
                "page_number": page_num,
                "content_length": len(content),
                "sections": self.analyze_page_sections(page_num, content),
                "chapters": self.analyze_page_chapters(page_num, content),
                "issues": []
            }
            
            # 문제점 검출
            if len(page_analysis["sections"]) == 0:
                page_analysis["issues"].append("부문 정보를 찾을 수 없음")
            
            if len(page_analysis["chapters"]) == 0:
                page_analysis["issues"].append("장 정보를 찾을 수 없음")
            
            if len(page_analysis["sections"]) > 1:
                page_analysis["issues"].append(f"여러 부문 발견: {len(page_analysis['sections'])}개")
            
            if len(page_analysis["chapters"]) > 3:
                page_analysis["issues"].append(f"너무 많은 장 발견: {len(page_analysis['chapters'])}개")
            
            analysis_results["page_analysis"][page_num] = page_analysis
            
            # 요약 정보 업데이트
            for section_info in page_analysis["sections"]:
                section_name = section_info["section"]
                if section_name not in analysis_results["summary"]["sections_found"]:
                    analysis_results["summary"]["sections_found"][section_name] = []
                analysis_results["summary"]["sections_found"][section_name].append(page_num)
            
            for chapter_info in page_analysis["chapters"]:
                analysis_results["summary"]["chapters_found"].append({
                    "page": page_num,
                    "chapter": chapter_info["full_text"],
                    "confidence": chapter_info["confidence"]
                })
        
        # 전체 요약 분석
        self._analyze_summary(analysis_results)
        
        return analysis_results
    
    def _analyze_summary(self, analysis_results: Dict[str, Any]):
        """전체 요약 분석"""
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
                if chapter_numbers != list(range(min(chapter_numbers), max(chapter_numbers) + 1)):
                    summary["issues"].append("장 번호가 연속되지 않음")
        
        # 신뢰도 분석
        low_confidence_chapters = [c for c in chapters if c["confidence"] < 0.7]
        if low_confidence_chapters:
            summary["issues"].append(f"신뢰도가 낮은 장 발견: {len(low_confidence_chapters)}개")
    
    def generate_detailed_report(self, analysis_results: Dict[str, Any]) -> str:
        """상세 분석 보고서 생성"""
        report = []
        report.append("# 📄 PDF 구조 검증 상세 보고서")
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
        report.append("## 📊 분석 요약")
        
        # 부문별 분포
        report.append("### 🏗️ 부문별 분포")
        for section, pages in summary["sections_found"].items():
            report.append(f"- **{section}**: {len(pages)}페이지 ({', '.join(map(str, pages))})")
        report.append("")
        
        # 장별 분포
        report.append("### 📚 장별 분포")
        chapters = summary["chapters_found"]
        for chapter in chapters:
            confidence_icon = "✅" if chapter["confidence"] >= 0.7 else "⚠️"
            report.append(f"- {confidence_icon} **{chapter['chapter']}** (p.{chapter['page']}, 신뢰도: {chapter['confidence']:.2f})")
        report.append("")
        
        # 문제점
        if summary["issues"]:
            report.append("### ⚠️ 발견된 문제점")
            for issue in summary["issues"]:
                report.append(f"- {issue}")
            report.append("")
        
        # 페이지별 상세 분석
        report.append("## 📄 페이지별 상세 분석")
        for page_num, page_analysis in analysis_results["page_analysis"].items():
            report.append(f"### 📄 페이지 {page_num}")
            report.append(f"- **내용 길이**: {page_analysis['content_length']}자")
            
            # 부문 정보
            if page_analysis["sections"]:
                report.append("- **발견된 부문**:")
                for section in page_analysis["sections"]:
                    confidence_icon = "✅" if section["confidence"] >= 0.7 else "⚠️"
                    report.append(f"  - {confidence_icon} {section['section']} (키워드: {section['keyword']}, 신뢰도: {section['confidence']:.2f})")
            else:
                report.append("- **발견된 부문**: 없음")
            
            # 장 정보
            if page_analysis["chapters"]:
                report.append("- **발견된 장**:")
                for chapter in page_analysis["chapters"]:
                    confidence_icon = "✅" if chapter["confidence"] >= 0.7 else "⚠️"
                    report.append(f"  - {confidence_icon} {chapter['full_text']} (신뢰도: {chapter['confidence']:.2f})")
            else:
                report.append("- **발견된 장**: 없음")
            
            # 문제점
            if page_analysis["issues"]:
                report.append("- **문제점**:")
                for issue in page_analysis["issues"]:
                    report.append(f"  - ⚠️ {issue}")
            
            report.append("")
        
        return "\n".join(report)
    
    def save_analysis_results(self, analysis_results: Dict[str, Any], output_dir: Path) -> Path:
        """분석 결과 저장"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # JSON 파일 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = output_dir / f"pdf_structure_analysis_{timestamp}.json"
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, ensure_ascii=False, indent=2)
        
        # 보고서 파일 저장
        report_path = output_dir / f"pdf_structure_report_{timestamp}.md"
        report_content = self.generate_detailed_report(analysis_results)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return json_path

def main():
    """메인 함수"""
    print("=== PDF 구조 검증 테스트 시작 ===")
    
    # 입력 파일 확인
    pdf_path = Path("input/index.pdf")
    if not pdf_path.exists():
        print(f"❌ PDF 파일을 찾을 수 없습니다: {pdf_path}")
        print("💡 input/index.pdf 파일을 추가한 후 다시 실행하세요.")
        return
    
    # 출력 디렉토리 설정
    output_dir = Path("output/validation_test")
    
    # 검증기 초기화
    validator = PDFStructureValidator(pdf_path)
    
    try:
        # 전체 페이지 분석 (처음 20페이지만 테스트)
        print("🔍 PDF 구조 분석 중...")
        analysis_results = validator.analyze_all_pages(start_page=1, end_page=20)
        
        if not analysis_results:
            print("❌ 분석에 실패했습니다.")
            return
        
        # 결과 저장
        print("💾 분석 결과 저장 중...")
        json_path = validator.save_analysis_results(analysis_results, output_dir)
        
        # 요약 출력
        summary = analysis_results["summary"]
        print("\n=== 📊 분석 결과 요약 ===")
        print(f"📄 분석된 페이지: {analysis_results['pdf_info']['analyzed_pages']}페이지")
        print(f"🏗️ 발견된 부문: {len(summary['sections_found'])}개")
        print(f"📚 발견된 장: {len(summary['chapters_found'])}개")
        
        if summary["issues"]:
            print(f"⚠️ 발견된 문제점: {len(summary['issues'])}개")
            for issue in summary["issues"][:3]:  # 처음 3개만 출력
                print(f"  - {issue}")
        
        print(f"\n✅ 분석 완료!")
        print(f"📁 결과 파일: {json_path}")
        print(f"📄 상세 보고서: {output_dir}/pdf_structure_report_*.md")
        
    except Exception as e:
        print(f"❌ 분석 중 오류 발생: {e}")
        logger.error(f"분석 중 오류 발생: {e}")

if __name__ == "__main__":
    main() 