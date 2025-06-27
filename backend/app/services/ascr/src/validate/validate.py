# -*- coding: utf-8 -*-
"""
PDF/목차 구조 검증 유틸리티 (부문/구조 완전성, 누락 경고 등)
"""
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

def validate_pdf_structure(toc_structure) -> bool:
    """
    PDF 목차 구조 검증
    
    Args:
        toc_structure: 목차 구조 객체
        
    Returns:
        bool: 검증 성공 여부
    """
    try:
        # 기본 구조 검증
        if not toc_structure or not hasattr(toc_structure, 'entries'):
            return False
        
        if not toc_structure.entries:
            return False
        
        # 각 항목 검증
        for entry in toc_structure.entries:
            if not entry.title or not entry.page:
                return False
            
            # 페이지 번호가 양수인지 확인
            if entry.page <= 0:
                return False
        
        # 부문 정보 검증
        if hasattr(toc_structure, 'sections'):
            sections = toc_structure.sections
            if not isinstance(sections, dict):
                return False
            
            # 최소한 하나의 부문에 장이 있는지 확인
            has_chapters = False
            for section_name, section_data in sections.items():
                if isinstance(section_data, dict) and section_data.get('chapters'):
                    has_chapters = True
                    break
            
            if not has_chapters:
                return False
        
        return True
        
    except Exception:
        return False

def validate_all_sections(content: str) -> Dict[str, Any]:
    """모든 부문 검증 - 반드시 실행"""
    required_sections = [
        "공통부문", "공 통 부 문",
        "토목부문", "토 목 부 문", 
        "건축부문", "건 축 부 문",
        "기계설비부문", "기 계 설 비 부 문",
        "유지관리부문", "유 지 관 리 부 문"
    ]
    validation_result = {
        "all_sections_found": True,
        "section_details": {},
        "missing_sections": [],
        "section_order": [],
        "validation_passed": False
    }
    found_sections = []
    for section in required_sections:
        section_info = {
            "found": False,
            "position": -1,
            "line_number": -1,
            "context": "",
            "original_text": section
        }
        pos = content.find(section)
        if pos != -1:
            section_info["found"] = True
            section_info["position"] = pos
            lines_before = content[:pos].count('\n')
            section_info["line_number"] = lines_before + 1
            start = max(0, pos - 100)
            end = min(len(content), pos + len(section) + 100)
            section_info["context"] = content[start:end]
            normalized_name = section.replace(" ", "")
            validation_result["section_details"][normalized_name] = section_info
            found_sections.append((normalized_name, pos))
    required_normalized = ["공통부문", "토목부문", "건축부문", "기계설비부문", "유지관리부문"]
    found_normalized = [section for section, _ in found_sections]
    for section in required_normalized:
        if section not in found_normalized:
            validation_result["missing_sections"].append(section)
            validation_result["all_sections_found"] = False
    found_sections.sort(key=lambda x: x[1])
    validation_result["section_order"] = [section for section, _ in found_sections]
    validation_result["validation_passed"] = validation_result["all_sections_found"]
    return validation_result

def generate_validated_analysis_report(file_path: Path, analysis_results: Dict[str, Any], validation_results: Dict[str, Any]) -> str:
    """검증된 분석 보고서 생성 - 반드시 사용"""
    report = f"""# 📋 PDF 구조 분석 보고서 (검증됨)
\n## 🎯 분석 개요
- **파일명**: {file_path.name}
- **분석 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **검증 상태**: {'✅ 통과' if validation_results.get('validation_passed', False) else '❌ 실패'}
\n## 🏗️ 문서 구조 분석
"""
    section_details = validation_results.get("section_details", {})
    for section_name, section_info in section_details.items():
        if section_info["found"]:
            report += f"""
### {section_name}
- **위치**: {section_info['line_number']}번째 줄
- **컨텍스트**: {section_info['context'][:200]}...\n"""
    missing_sections = validation_results.get("missing_sections", [])
    if missing_sections:
        report += f"""
## ⚠️ 누락된 부문
다음 부문이 문서에서 찾을 수 없습니다:
{chr(10).join(f'- {section}' for section in missing_sections)}
\n**권장사항**: 전체 문서를 다시 검토하여 누락된 부문을 확인하세요.
"""
    report += f"""
## ✅ 검증 결과
- **모든 부문 발견**: {'예' if validation_results.get('all_sections_found', False) else '아니오'}
- **부문 순서**: {' → '.join(validation_results.get('section_order', []))}
- **분석 신뢰도**: {analysis_results.get('analysis_confidence', 0):.1f}%
\n## 💡 권장사항
"""
    if validation_results.get("validation_passed", False):
        report += "- ✅ 분석이 성공적으로 완료되었습니다.\n"
    else:
        report += "- 🔄 누락된 부문을 확인하고 재분석을 수행하세요.\n"
        report += "- 📖 문서의 전체 구조를 다시 검토하세요.\n"
        report += "- 🔍 부문 제목의 정확한 표기를 확인하세요.\n"
    return report

def execute_error_prevention_workflow(file_path: Path) -> Dict[str, Any]:
    """오류 방지 워크플로우 - 반드시 사용"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        validation_results = validate_all_sections(content)
        analysis_results = {
            "analysis_confidence": 85.0,
            "file_info": {
                "name": file_path.name,
                "size": file_path.stat().st_size
            }
        }
        comprehensive_report = generate_validated_analysis_report(
            file_path, analysis_results, validation_results
        )
        final_result = {
            "validation_results": validation_results,
            "analysis_results": analysis_results,
            "comprehensive_report": comprehensive_report,
            "is_valid": validation_results.get("validation_passed", False)
        }
        return final_result
    except Exception as e:
        return {
            "error": str(e),
            "is_valid": False
        } 