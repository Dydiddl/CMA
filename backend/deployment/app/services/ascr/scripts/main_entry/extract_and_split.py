#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 목차 추출 및 분할 통합 스크립트

이 스크립트는 기존 index.pdf 파일에서 목차를 추출하고, 목차 구조를 분석하여 PDF를 분할하는 통합 기능을 제공합니다.
리팩토링된 유틸리티 모듈들을 사용하여 중복을 제거하고 단순화된 구조로 동작합니다.
PDF 생성 없이 기존 파일을 직접 사용합니다.
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.extract.toc_extractor import TOCExtractor, extract_toc_from_pdf
from src.utils.extract.pdf_text_extractor import PDFTextExtractor
from src.utils.split.pdf_split_utils import PDFSplitUtils
from src.validate.validate import validate_pdf_structure
from src.utils.report import generate_processing_report

# 계층 구조 검증 및 수정 모듈 import
from scripts.main_entry.hierarchy_validator import HierarchyValidator

# 정답 데이터 검증 모듈 import
from scripts.main_entry.ground_truth_validator import GroundTruthValidator

def save_toc_markdown(toc_structure, md_path):
    """TOCStructure를 계층적 마크다운 파일로 저장"""
    entries = toc_structure.entries
    entry_dict = {e.number: e for e in entries}
    # parent가 None인 루트 노드들부터 시작
    roots = [e for e in entries if not e.parent]

    def render_entry(entry, depth=0):
        indent = '  ' * depth
        page_info = f" (p.{entry.page})" if entry.page else ""
        number_info = f"{entry.number} " if entry.number else ""
        section_info = f"[{entry.section}] " if entry.section else ""
        line = f"{indent}- {section_info}{number_info}{entry.title}{page_info}\n"
        # 자식 노드 재귀
        for child_num in entry.children:
            child = entry_dict.get(child_num)
            if child:
                line += render_entry(child, depth+1)
        return line

    md = "# 📋 표준품셈 목차 구조 (계층적 트리)\n\n"
    for root in roots:
        md += render_entry(root)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md)

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description="PDF 목차 추출 및 분할 통합 스크립트",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python extract_and_split.py input.pdf --extract-only
  python extract_and_split.py input.pdf --split-mode chapter
  python extract_and_split.py input.pdf --split-mode section --output-dir output
        """
    )
    
    parser.add_argument("pdf_file", type=str, help="처리할 PDF 파일 경로")
    parser.add_argument("--extract-only", action="store_true", help="목차 추출만 수행")
    parser.add_argument("--split-mode", choices=["chapter", "section"], default="chapter", 
                       help="분할 모드 (기본값: chapter)")
    parser.add_argument("--output-dir", type=str, default="output", help="출력 디렉토리")
    parser.add_argument("--method", choices=["auto", "pattern", "structure", "manual"], 
                       default="auto", help="목차 추출 방법")
    parser.add_argument("--max-pages", type=int, default=100, help="목차 검색 최대 페이지 수")
    parser.add_argument("--auto-fix", choices=["true", "false"], default="true", 
                       help="자동으로 계층 구조 검증 및 수정 (기본값: true)")
    parser.add_argument("--validate-ground-truth", action="store_true", help="정답 데이터와 비교 검증")
    parser.add_argument("--ground-truth-file", type=str, 
                       default="data/ground truth/toc_ground_truth_2025.md",
                       help="정답 데이터 파일 경로")
    
    args = parser.parse_args()
    
    # 파일 경로 검증
    pdf_path = Path(args.pdf_file)
    if not pdf_path.exists():
        print(f"❌ PDF 파일이 존재하지 않습니다: {pdf_path}")
        sys.exit(1)
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=== PDF 목차 추출 및 분할 시작 ===")
    print(f"📄 입력 파일: {pdf_path}")
    print(f"📂 출력 디렉토리: {output_dir}")
    print(f"🔧 분할 모드: {args.split_mode}")
    print(f"📋 추출 방법: {args.method}")
    print(f"🔧 자동 수정: {'활성화' if args.auto_fix == 'true' else '비활성화'}")
    print(f"💡 기존 index.pdf 파일을 사용합니다 (PDF 생성 없음)")
    print()
    
    try:
        # 1단계: 목차 추출
        print("1️⃣ 목차 추출 중...")
        
        # 목차 추출 방법 설정
        extraction_method = "improved"  # 개선된 추출 방법 사용
        
        # 기존 index.pdf 파일을 직접 사용
        if pdf_path.name == "index.pdf":
            # index.pdf에서 직접 텍스트 추출
            from pypdf import PdfReader
            reader = PdfReader(pdf_path)
            content = ""
            for page in reader.pages:
                content += page.extract_text() + "\n"
            
            # 목차 구조 분석
            extractor = TOCExtractor()
            toc_structure = extractor.extract_toc_structure(content, extraction_method)
        else:
            # 일반 PDF 파일인 경우 기존 로직 사용
            toc_structure = extract_toc_from_pdf(pdf_path, extraction_method)
        
        if not toc_structure or not toc_structure.entries:
            print("❌ 목차 추출에 실패했습니다.")
            sys.exit(1)
        
        print(f"✅ 목차 추출 완료: {len(toc_structure.entries)}개 항목 발견")
        
        # 2단계: 목차 구조 검증
        print("\n2️⃣ 목차 구조 검증 중...")
        if not validate_pdf_structure(toc_structure):
            print("⚠️ 목차 구조 검증에 실패했지만 계속 진행합니다.")
        else:
            print("✅ 목차 구조 검증 완료")
        
        # 3단계: 계층 구조 자동 수정 (새로 추가)
        if args.auto_fix == "true":
            print("\n3️⃣ 계층 구조 자동 수정 중...")
            
            # TOCStructure를 딕셔너리로 변환
            toc_dict = {
                "entries": [
                    {
                        "number": entry.number,
                        "title": entry.title,
                        "level": entry.level,
                        "page": entry.page,
                        "section": entry.section,
                        "chapter": entry.chapter,
                        "parent": entry.parent,
                        "children": entry.children,
                        "subsection": entry.subsection
                    }
                    for entry in toc_structure.entries
                ],
                "sections": toc_structure.sections,
                "metadata": toc_structure.metadata
            }
            
            # 계층 구조 검증 및 수정
            validator = HierarchyValidator()
            fixed_structure = validator.validate_and_fix_hierarchy(toc_dict)
            
            # 수정된 구조를 다시 TOCStructure로 변환
            from src.common.types import TOCEntry, TOCStructure
            
            fixed_entries = []
            for entry_dict in fixed_structure["entries"]:
                entry = TOCEntry(
                    number=entry_dict["number"],
                    title=entry_dict["title"],
                    level=entry_dict["level"],
                    page=entry_dict["page"],
                    section=entry_dict["section"],
                    chapter=entry_dict["chapter"],
                    parent=entry_dict["parent"],
                    children=entry_dict["children"],
                    subsection=entry_dict["subsection"]
                )
                fixed_entries.append(entry)
            
            toc_structure = TOCStructure(
                entries=fixed_entries,
                sections=fixed_structure["sections"],
                metadata=fixed_structure["metadata"]
            )
            
            print("✅ 계층 구조 자동 수정 완료")
            
            # 수정 사항 요약 출력
            original_count = len(toc_dict["entries"])
            fixed_count = len(fixed_structure["entries"])
            print(f"📊 수정 전: {original_count}개 항목")
            print(f"📊 수정 후: {fixed_count}개 항목")
            
            # 부문별 통계 출력
            print("\n📋 부문별 통계:")
            for section_name, stats in fixed_structure["sections"].items():
                print(f"  {section_name}: {stats['count']}개 항목, {len(stats['chapters'])}개 장")
        
        # 4단계: 목차 JSON 저장
        print(f"\n{'4️⃣' if args.auto_fix != 'true' else '4️⃣'} 목차 구조 저장 중...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 수정 여부에 따라 파일명 구분
        if args.auto_fix == "true":
            toc_json_path = output_dir / f"toc_structure_fixed_{timestamp}.json"
            toc_md_path = output_dir / f"toc_structure_fixed_{timestamp}.md"
        else:
            toc_json_path = output_dir / f"toc_structure_{timestamp}.json"
            toc_md_path = output_dir / f"toc_structure_{timestamp}.md"
        
        extractor = TOCExtractor()
        if extractor.save_toc_structure(toc_structure, toc_json_path, 'json'):
            print(f"✅ 목차 구조 저장 완료: {toc_json_path}")
            # 마크다운도 저장
            save_toc_markdown(toc_structure, toc_md_path)
            print(f"✅ 목차 마크다운 저장 완료: {toc_md_path}")
        else:
            print("❌ 목차 구조 저장에 실패했습니다.")
            sys.exit(1)
        
        # 5단계: 매핑 설정 생성 및 저장
        print(f"\n{'5️⃣' if args.auto_fix != 'true' else '5️⃣'} 매핑 설정 생성 중...")
        mapping_config = extractor.generate_mapping_config(toc_structure)
        
        # 수정 여부에 따라 파일명 구분
        if args.auto_fix == "true":
            mapping_path = output_dir / f"mapping_config_fixed_{timestamp}.json"
        else:
            mapping_path = output_dir / f"mapping_config_{timestamp}.json"
        
        import json
        with open(mapping_path, 'w', encoding='utf-8') as f:
            json.dump(mapping_config, f, ensure_ascii=False, indent=2)
        print(f"✅ 매핑 설정 저장 완료: {mapping_path}")
        
        # 6단계: 정답 데이터와 비교 검증 (옵션)
        if args.validate_ground_truth:
            ground_truth_file = Path(args.ground_truth_file)
            if ground_truth_file.exists():
                print(f"\n📊 정답 데이터와 비교 검증 중...")
                print(f"📋 정답 데이터: {ground_truth_file}")
                
                # TOCStructure 객체를 딕셔너리로 변환
                if hasattr(toc_structure, 'to_dict'):
                    toc_dict = toc_structure.to_dict()
                elif hasattr(toc_structure, '__dict__'):
                    toc_dict = toc_structure.__dict__
                else:
                    # 기본 딕셔너리 구조로 변환
                    toc_dict = {
                        "items": getattr(toc_structure, 'items', []),
                        "sections": getattr(toc_structure, 'sections', {}),
                        "total_items": getattr(toc_structure, 'total_items', 0)
                    }
                
                # 정답 데이터 검증 실행
                validator = GroundTruthValidator(ground_truth_file)
                validation_result = validator.validate_toc_structure(toc_dict)
                
                # 검증 결과 출력
                accuracy_percent = validation_result["overall_accuracy"] * 100
                print(f"🎯 전체 정확도: {accuracy_percent:.1f}%")
                
                # 부문별 정확도 출력
                for section, accuracy in validation_result["section_accuracy"].items():
                    section_accuracy = accuracy * 100
                    print(f"📋 {section}: {section_accuracy:.1f}%")
                
                # 오류 분석 출력
                if validation_result["missing_sections"]:
                    print(f"❌ 누락된 부문: {', '.join(validation_result['missing_sections'])}")
                
                if validation_result["missing_chapters"]:
                    print(f"❌ 누락된 장: {len(validation_result['missing_chapters'])}개")
                
                if validation_result["missing_items"]:
                    print(f"❌ 누락된 항목: {len(validation_result['missing_items'])}개")
                
                if validation_result["incorrect_classifications"]:
                    print(f"❌ 잘못된 분류: {len(validation_result['incorrect_classifications'])}개")
                
                if validation_result["incorrect_pages"]:
                    print(f"❌ 잘못된 페이지: {len(validation_result['incorrect_pages'])}개")
                
                # 개선 방안 출력
                if validation_result["improvement_suggestions"]:
                    print(f"\n💡 개선 방안:")
                    for suggestion in validation_result["improvement_suggestions"]:
                        print(f"  - {suggestion}")
                
                # 검증 리포트 생성
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                report = validator.generate_validation_report(validation_result)
                report_file = output_dir / f"validation_report_{timestamp}.md"
                
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write(report)
                
                # JSON 결과 저장
                json_file = output_dir / f"validation_result_{timestamp}.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(validation_result, f, ensure_ascii=False, indent=2)
                
                print(f"📄 검증 리포트: {report_file}")
                print(f"📋 JSON 결과: {json_file}")
                
            else:
                print(f"⚠️ 정답 데이터 파일을 찾을 수 없습니다: {ground_truth_file}")
        
        # 7단계: 처리 보고서 생성
        print(f"\n{'7️⃣' if args.auto_fix != 'true' else '7️⃣'} 처리 보고서 생성 중...")
        report_path = output_dir / f"processing_report_{timestamp}.txt"
        
        report_data = {
            "input_file": str(pdf_path),
            "output_dir": str(output_dir),
            "split_mode": args.split_mode,
            "extraction_method": extraction_method,
            "auto_fix_applied": args.auto_fix == "true",
            "toc_entries_count": len(toc_structure.entries),
            "toc_json_path": str(toc_json_path),
            "mapping_path": str(mapping_path),
            "processing_time": datetime.now().isoformat()
        }
        
        generate_processing_report(report_data, report_path)
        print(f"✅ 처리 보고서 생성 완료: {report_path}")
        
        # 8단계: PDF 분할
        print(f"\n{'8️⃣' if args.auto_fix != 'true' else '8️⃣'} PDF 분할 중... (모드: {args.split_mode})")
        splitter = PDFSplitUtils(toc_json_path, pdf_path, output_dir)
        
        if splitter.split(args.split_mode):
            print("✅ PDF 분할 완료")
        else:
            print("❌ PDF 분할에 실패했습니다.")
            sys.exit(1)
        
        # 9단계: 최종 요약
        print(f"\n🎉 모든 작업이 성공적으로 완료되었습니다!")
        print(f"📂 결과물 위치: {output_dir}")
        if args.auto_fix == "true":
            print("🔧 계층 구조가 자동으로 수정되어 정확도가 향상되었습니다.")
        
        # 정답 데이터 검증 결과가 있으면 정확도 표시
        if args.validate_ground_truth and 'validation_result' in locals():
            print(f"🎯 최종 정확도: {validation_result['overall_accuracy']*100:.1f}%")
        
    except KeyboardInterrupt:
        print("\n⚠️ 사용자에 의해 작업이 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 작업 중 오류가 발생했습니다: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 