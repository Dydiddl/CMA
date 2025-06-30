#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 목차 추출 모듈 (TOC PDF Extractor)

이 모듈은 PDF에서 목차 부분을 추출하는 기능을 제공합니다.
"""

import re
from pathlib import Path
from typing import Optional, Tuple

# ASCR 커스텀 로깅 시스템 사용
from ..log import get_logger

# 로거 초기화
logger = get_logger("TOCPDFExtractor")

class TOCPDFExtractor:
    """PDF에서 목차 추출 클래스"""
    
    def __init__(self):
        self.toc_keywords = [
            '목차', '차례', 'INDEX', 'CONTENTS', 'Table of Contents',
            '目次', 'CONTENIDO', 'INHALTSVERZEICHNIS', 'SOMMAIRE',
            '부문', '장', 'Chapter', 'Section', 'Part',
            'TABLE OF CONTENTS', 'CONTENTS', 'INDEX'
        ]
        
        self.toc_patterns = [
            r'제\d+장', r'\d+장', r'\d+\.\s*[가-힣]',
            r'Chapter\s*\d+', r'Section\s*\d+', r'Part\s*\d+',
            r'\d+-\d+', r'\d+\.\d+',
            r'\d+\s*\.{2,}\s*\d+', r'\d+\s*-\s*\d+'
        ]
        
        # 숫자+목차 패턴 (새로운 규칙)
        self.number_toc_patterns = [
            r'\d+\s*목\s*차',      # "1 목 차", "2 목 차" 등
            r'목\s*차\s*\d+',      # "목 차 1", "목 차 2" 등
            r'\d+목\s*차',         # "1목 차", "2목 차" 등
            r'목\s*차\d+',         # "목 차1", "목 차2" 등
        ]
        
        # 목차 끝을 나타내는 패턴들
        self.toc_end_patterns = [
            r'제1장\s*[가-힣]+',  # 첫 번째 장 시작
            r'공통부문\s*제1장',   # 공통부문 첫 장
            r'토목부문\s*제1장',   # 토목부문 첫 장
            r'건축부문\s*제1장',   # 건축부문 첫 장
            r'기계설비부문\s*제1장', # 기계설비부문 첫 장
            r'유지관리부문\s*제1장', # 유지관리부문 첫 장
            r'본\s*문',           # 본문 시작
            r'제\s*1\s*장',       # 제1장 (공백 포함)
        ]
    
    def extract_toc_pdf(self, pdf_path: Path, output_path: Optional[Path] = None, 
                       max_pages: int = 100, force_end_page: int = None) -> Optional[Path]:
        """
        PDF에서 목차 부분을 추출하여 별도 PDF로 저장
        force_end_page: 강제로 목차 끝 페이지를 지정할 수 있음 (1-based)
        """
        try:
            from pypdf import PdfReader, PdfWriter
            logger.info(f"목차 PDF 추출 시작: {pdf_path}")
            reader = PdfReader(pdf_path)
            writer = PdfWriter()
            total_pages = len(reader.pages)
            
            # 목차 시작/끝 페이지 감지
            toc_start, toc_end = self._find_toc_page_range_multi(reader, max_pages, force_end_page=force_end_page)
            if toc_start is None or toc_end is None:
                logger.warning("목차 범위 감지 실패, 첫 페이지만 추출")
                toc_start, toc_end = 0, 0
            
            # 페이지 추출
            for page_num in range(toc_start, toc_end + 1):
                if page_num < total_pages:
                    page = reader.pages[page_num]
                    writer.add_page(page)
                    progress = ((page_num - toc_start + 1) / (toc_end - toc_start + 1)) * 100
                    print(f"\r목차 추출 진행률: {progress:.1f}%", end='')
            print()
            
            if output_path is None:
                output_path = pdf_path.parent / "index.pdf"
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            logger.info(f"목차 PDF 추출 완료: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"목차 PDF 추출 실패: {e}")
            return None

    def _find_toc_page_range_multi(self, reader, max_pages: int = 100, force_end_page: int = None) -> Tuple[Optional[int], Optional[int]]:
        """목차 시작~끝 페이지 범위 자동 감지 (숫자+목차 패턴 기반 개선 버전)"""
        toc_start, toc_end = None, None
        found = False
        no_pattern_count = 0
        N = 5  # 연속 미매칭 허용 페이지 수
        
        print(f"🔍 목차 범위 감지 시작 (최대 {max_pages}페이지 검색)")
        
        for page_num in range(min(max_pages, len(reader.pages))):
            try:
                page = reader.pages[page_num]
                text = page.extract_text()
                
                if page_num < 10:
                    preview = text[:100].replace('\n', ' ').strip()
                    print(f"   페이지 {page_num+1}: {preview}...")
                
                # 목차 시작점 찾기
                if not found:
                    # 1. 숫자+목차 패턴 우선 확인 (가장 정확한 규칙)
                    for pattern in self.number_toc_patterns:
                        if re.search(pattern, text):
                            toc_start = page_num
                            found = True
                            print(f"✅ 목차 시작점 발견: 페이지 {page_num+1} (숫자+목차 패턴: {pattern})")
                            break
                    
                    # 2. 기존 키워드 확인
                    if not found:
                        for keyword in self.toc_keywords:
                            if keyword.lower() in text.lower():
                                toc_start = page_num
                                found = True
                                print(f"✅ 목차 시작점 발견: 페이지 {page_num+1} (키워드: {keyword})")
                                break
                    
                    # 3. 기존 패턴 확인
                    if not found:
                        for pattern in self.toc_patterns:
                            if re.search(pattern, text):
                                toc_start = page_num
                                found = True
                                print(f"✅ 목차 시작점 발견: 페이지 {page_num+1} (패턴: {pattern})")
                                break
                
                # 목차 끝점 찾기 (시작점을 찾은 후)
                else:
                    # 1. 숫자+목차 패턴이 더 이상 없는지 확인
                    has_number_toc = any(re.search(pattern, text) for pattern in self.number_toc_patterns)
                    
                    # 2. 목차 끝 패턴 확인
                    has_end_pattern = any(re.search(pattern, text) for pattern in self.toc_end_patterns)
                    
                    # 3. 목차 패턴이 있는지 확인
                    has_toc_pattern = any(re.search(pattern, text) for pattern in self.toc_patterns)
                    
                    # 숫자+목차 패턴이 없고, 끝 패턴이 있으면 목차 끝
                    if not has_number_toc and has_end_pattern:
                        toc_end = page_num - 1  # 이전 페이지까지가 목차
                        print(f"✅ 목차 끝점 발견: 페이지 {toc_end+1} (숫자+목차 패턴 없음 + 끝 패턴 있음)")
                        break
                    
                    # 숫자+목차 패턴이 있으면 계속 목차로 간주
                    if has_number_toc:
                        no_pattern_count = 0
                        print(f"   📋 페이지 {page_num+1}: 숫자+목차 패턴 발견 - 목차 계속")
                    elif has_toc_pattern:
                        no_pattern_count = 0
                    else:
                        no_pattern_count += 1
                    
                    # 4. 연속 미매칭 시 끝점 (보조 방법)
                    if no_pattern_count >= N:
                        toc_end = page_num - no_pattern_count
                        print(f"✅ 목차 끝점 발견: 페이지 {toc_end+1} (연속 {N}페이지 미매칭)")
                        break
                    
                    # 5. 강제 끝점 옵션
                    if force_end_page and page_num >= force_end_page - 1:
                        toc_end = force_end_page - 1
                        print(f"✅ 강제 목차 끝점 지정: 페이지 {toc_end+1}")
                        break
                        
            except Exception as e:
                print(f"⚠️ 페이지 {page_num+1} 처리 중 오류: {e}")
                continue
        
        # 목차 끝점을 찾지 못한 경우 처리
        if found and toc_end is None:
            # 최소 50페이지는 목차로 간주 (실제 목차가 길 수 있음)
            min_toc_pages = 50
            if toc_start + min_toc_pages < len(reader.pages):
                toc_end = toc_start + min_toc_pages - 1
                print(f"⚠️ 목차 끝점을 찾지 못해 최소 {min_toc_pages}페이지로 설정: 페이지 {toc_start+1} ~ {toc_end+1}")
            else:
                toc_end = toc_start  # 최소 1페이지라도 추출
                print(f"⚠️ 목차 끝점을 찾지 못해 시작점과 동일하게 설정: 페이지 {toc_start+1}")
        
        if toc_start is not None:
            print(f"📋 목차 범위: 페이지 {toc_start+1} ~ {toc_end+1} (총 {toc_end - toc_start + 1}페이지)")
        else:
            print("❌ 목차 범위를 찾지 못했습니다.")
        
        return toc_start, toc_end 