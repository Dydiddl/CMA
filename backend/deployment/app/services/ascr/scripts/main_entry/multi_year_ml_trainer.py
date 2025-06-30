#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
다년도 표준품셈 PDF 머신러닝 훈련 시스템
1990년도부터 2025년도까지의 PDF 데이터를 활용한 목차 분류 모델 훈련
"""

import os
import re
import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
import joblib
import argparse

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MultiYearMLTrainer:
    """다년도 머신러닝 훈련 시스템"""
    
    def __init__(self, input_dir: str = "input/By_year_Construction_work_standard_price_list", output_dir: str = "output"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 연도별 데이터 저장소
        self.year_data = {}
        self.combined_data = []
        
        # 머신러닝 모델
        self.vectorizer = None
        self.classifier = None
        self.pipeline = None
        
        # 성능 메트릭
        self.performance_metrics = {}
        
    def discover_pdf_files(self) -> Dict[int, List[Path]]:
        """연도별 PDF 파일 발견"""
        year_files = {}
        
        # PDF 파일 패턴 매칭 (연도 추출)
        pdf_pattern = re.compile(r'(\d{4})_construction_work_standard_price_list\.pdf')
        
        for pdf_file in self.input_dir.glob("*.pdf"):
            match = pdf_pattern.match(pdf_file.name)
            if match:
                year = int(match.group(1))
                if 1990 <= year <= 2025:
                    if year not in year_files:
                        year_files[year] = []
                    year_files[year].append(pdf_file)
                    logger.info(f"발견된 PDF: {year}년도 - {pdf_file.name}")
        
        # 연도별 정렬
        year_files = dict(sorted(year_files.items()))
        
        logger.info(f"총 {len(year_files)}개 연도의 PDF 파일 발견")
        for year, files in year_files.items():
            logger.info(f"  {year}년도: {len(files)}개 파일")
        
        return year_files
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """PDF에서 텍스트 추출"""
        try:
            from pypdf import PdfReader
            
            reader = PdfReader(pdf_path)
            text = ""
            
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            return text
            
        except Exception as e:
            logger.error(f"PDF 텍스트 추출 실패: {pdf_path} - {e}")
            return ""
    
    def extract_toc_from_text(self, text: str) -> List[Dict[str, Any]]:
        """텍스트에서 목차 추출"""
        toc_items = []
        
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # 장 패턴: "제n장"
            chapter_match = re.match(r'^제(\d+)장$', line)
            if chapter_match:
                chapter_num = chapter_match.group(1)
                
                # 다음 줄에서 제목과 페이지 추출
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    # 제목과 페이지 분리 (점선으로 구분)
                    parts = next_line.split('·')
                    if len(parts) >= 2:
                        title = parts[0].strip()
                        # 마지막 부분에서 페이지 번호 추출
                        page_part = parts[-1].strip()
                        page_match = re.search(r'(\d+)$', page_part)
                        if page_match:
                            page_num = int(page_match.group(1))
                            
                            toc_items.append({
                                'line_num': i + 1,
                                'number': f'제{chapter_num}장',
                                'title': title,
                                'page': page_num,
                                'type': 'chapter'
                            })
                continue
            
            # 절/조 패턴: "n-n" 또는 "n-n-n"
            section_match = re.match(r'^(\d+-\d+(?:-\d+)?)\s+(.+?)\s*·+', line)
            if section_match:
                number = section_match.group(1)
                title = section_match.group(2).strip()
                
                # 페이지 번호 추출 (점선 뒤의 숫자)
                page_match = re.search(r'·+\s*(\d+)$', line)
                if page_match:
                    page_num = int(page_match.group(1))
                    
                    toc_items.append({
                        'line_num': i + 1,
                        'number': number,
                        'title': title,
                        'page': page_num,
                        'type': 'section' if '-' in number and number.count('-') == 1 else 'subsection'
                    })
        
        return toc_items
    
    def classify_toc_item(self, item: Dict[str, Any]) -> str:
        """목차 항목 분류"""
        title = item['title'].lower()
        number = item['number']
        
        # 부문별 키워드 정의
        section_keywords = {
            '공통부문': ['공통', '일반', '적용', '기준', '가설', '안전', '통행'],
            '토목부문': ['토목', '도로', '교량', '터널', '댐', '제방', '하천', '지반'],
            '건축부문': ['건축', '건물', '철근', '콘크리트', '조적', '미장', '도장', '지붕'],
            '기계설비부문': ['기계', '설비', '배관', '전기', '통신', '소방', '공조', '냉난방'],
            '유지관리부문': ['유지', '관리', '보수', '점검', '정비', '청소', '방역']
        }
        
        # 키워드 기반 분류
        for section, keywords in section_keywords.items():
            for keyword in keywords:
                if keyword in title:
                    return section
        
        # 번호 패턴 기반 분류 (간단한 규칙)
        if number.startswith('1-'):
            return '공통부문'
        elif number.startswith('2-'):
            return '토목부문'
        elif number.startswith('3-'):
            return '건축부문'
        elif number.startswith('4-'):
            return '기계설비부문'
        elif number.startswith('5-'):
            return '유지관리부문'
        
        # 기본값
        return '공통부문'
    
    def process_year_data(self, year: int, pdf_files: List[Path]) -> List[Dict[str, Any]]:
        """연도별 데이터 처리"""
        year_items = []
        
        for pdf_file in pdf_files:
            logger.info(f"{year}년도 PDF 처리 중: {pdf_file.name}")
            
            # 텍스트 추출
            text = self.extract_text_from_pdf(pdf_file)
            if not text:
                continue
            
            # 목차 추출
            toc_items = self.extract_toc_from_text(text)
            
            # 분류 및 데이터 준비
            for item in toc_items:
                section = self.classify_toc_item(item)
                
                # 특성 추출
                features = {
                    'year': year,
                    'title': item['title'],
                    'number': item['number'],
                    'page': item['page'],
                    'type': item['type'],
                    'title_length': len(item['title']),
                    'has_numbers': bool(re.search(r'\d', item['title'])),
                    'has_korean': bool(re.search(r'[가-힣]', item['title'])),
                    'section': section
                }
                
                year_items.append(features)
        
        logger.info(f"{year}년도: {len(year_items)}개 항목 추출")
        return year_items
    
    def prepare_training_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """훈련 데이터 준비"""
        # 모든 연도 데이터 결합
        all_data = []
        for year, items in self.year_data.items():
            all_data.extend(items)
        
        # DataFrame 생성
        df = pd.DataFrame(all_data)
        
        # 특성과 레이블 분리
        X = df[['title', 'number', 'title_length', 'has_numbers', 'has_korean']]
        y = df['section']
        
        # 텍스트 특성 결합
        X['text_features'] = X['title'] + ' ' + X['number']
        
        logger.info(f"훈련 데이터 준비 완료: {len(df)}개 샘플")
        logger.info(f"클래스 분포:\n{y.value_counts()}")
        
        return X, y
    
    def train_model(self, X: pd.DataFrame, y: pd.Series) -> None:
        """머신러닝 모델 훈련"""
        logger.info("머신러닝 모델 훈련 시작")
        
        # 데이터 분할
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # 파이프라인 구성
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=1000,
                ngram_range=(1, 2),
                stop_words=None,
                lowercase=True
            )),
            ('classifier', RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                n_jobs=-1
            ))
        ])
        
        # 모델 훈련
        self.pipeline.fit(X_train['text_features'], y_train)
        
        # 성능 평가
        y_pred = self.pipeline.predict(X_test['text_features'])
        
        # 메트릭 저장
        self.performance_metrics = {
            'accuracy': (y_pred == y_test).mean(),
            'classification_report': classification_report(y_test, y_pred, output_dict=True),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        
        # 교차 검증
        cv_scores = cross_val_score(
            self.pipeline, X['text_features'], y, 
            cv=5, scoring='accuracy'
        )
        self.performance_metrics['cv_mean'] = cv_scores.mean()
        self.performance_metrics['cv_std'] = cv_scores.std()
        
        logger.info(f"모델 훈련 완료 - 정확도: {self.performance_metrics['accuracy']:.3f}")
        logger.info(f"교차 검증 점수: {self.performance_metrics['cv_mean']:.3f} ± {self.performance_metrics['cv_std']:.3f}")
    
    def save_model(self) -> None:
        """모델 저장"""
        model_path = self.output_dir / "multi_year_toc_classifier.joblib"
        joblib.dump(self.pipeline, model_path)
        logger.info(f"모델 저장 완료: {model_path}")
        
        # 성능 메트릭 저장
        metrics_path = self.output_dir / "performance_metrics.json"
        with open(metrics_path, 'w', encoding='utf-8') as f:
            json.dump(self.performance_metrics, f, ensure_ascii=False, indent=2)
        logger.info(f"성능 메트릭 저장 완료: {metrics_path}")
    
    def generate_training_report(self) -> str:
        """훈련 보고서 생성"""
        report = f"""# 다년도 머신러닝 훈련 보고서

## 📊 훈련 개요
- **훈련 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **처리된 연도**: {len(self.year_data)}개 연도
- **총 샘플 수**: {sum(len(items) for items in self.year_data.values())}개

## 📈 연도별 데이터 분포
"""
        
        for year in sorted(self.year_data.keys()):
            count = len(self.year_data[year])
            report += f"- **{year}년도**: {count}개 항목\n"
        
        report += f"""
## 🎯 모델 성능
- **정확도**: {self.performance_metrics.get('accuracy', 0):.3f}
- **교차 검증 평균**: {self.performance_metrics.get('cv_mean', 0):.3f}
- **교차 검증 표준편차**: {self.performance_metrics.get('cv_std', 0):.3f}

## 📋 분류 보고서
"""
        
        if 'classification_report' in self.performance_metrics:
            report += "### 부문별 성능\n"
            for section, metrics in self.performance_metrics['classification_report'].items():
                if isinstance(metrics, dict):
                    report += f"- **{section}**:\n"
                    report += f"  - 정밀도: {metrics.get('precision', 0):.3f}\n"
                    report += f"  - 재현율: {metrics.get('recall', 0):.3f}\n"
                    report += f"  - F1-점수: {metrics.get('f1-score', 0):.3f}\n"
        
        report += f"""
## 💡 권장사항
1. **데이터 품질 향상**: 더 많은 연도 데이터 수집
2. **특성 엔지니어링**: 추가 특성 개발
3. **모델 튜닝**: 하이퍼파라미터 최적화
4. **정기 재훈련**: 새로운 연도 데이터로 모델 업데이트

## 🔮 향후 계획
- 2026년도 데이터 출시 시 자동 학습
- 실시간 분류 시스템 구축
- 웹 인터페이스 개발
"""
        
        return report
    
    def run_complete_training(self) -> Dict[str, Any]:
        """완전한 훈련 프로세스 실행"""
        logger.info("다년도 머신러닝 훈련 시작")
        
        try:
            # 1단계: PDF 파일 발견
            year_files = self.discover_pdf_files()
            if not year_files:
                logger.error("처리할 PDF 파일이 없습니다")
                return {"success": False, "error": "PDF 파일 없음"}
            
            # 2단계: 연도별 데이터 처리
            for year, pdf_files in year_files.items():
                logger.info(f"{year}년도 데이터 처리 시작")
                year_items = self.process_year_data(year, pdf_files)
                self.year_data[year] = year_items
            
            # 3단계: 훈련 데이터 준비
            X, y = self.prepare_training_data()
            if len(X) == 0:
                logger.error("훈련 데이터가 없습니다")
                return {"success": False, "error": "훈련 데이터 없음"}
            
            # 4단계: 모델 훈련
            self.train_model(X, y)
            
            # 5단계: 모델 저장
            self.save_model()
            
            # 6단계: 보고서 생성
            report = self.generate_training_report()
            report_path = self.output_dir / "training_report.md"
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            
            logger.info("다년도 머신러닝 훈련 완료")
            
            return {
                "success": True,
                "total_samples": len(X),
                "years_processed": len(self.year_data),
                "accuracy": self.performance_metrics.get('accuracy', 0),
                "report_path": str(report_path)
            }
            
        except Exception as e:
            logger.error(f"훈련 중 오류 발생: {e}")
            return {"success": False, "error": str(e)}

def main():
    """메인 실행 함수"""
    print("🚀 다년도 머신러닝 훈련 시스템 시작")
    
    parser = argparse.ArgumentParser(description="다년도 표준품셈 머신러닝 훈련")
    parser.add_argument("--input_dir", type=str, default="input/By_year_Construction_work_standard_price_list", help="입력 PDF 폴더 경로")
    parser.add_argument("--output_dir", type=str, default="output", help="출력 폴더 경로")
    args = parser.parse_args()
    
    # 훈련 시스템 초기화
    trainer = MultiYearMLTrainer(input_dir=args.input_dir, output_dir=args.output_dir)
    
    # 완전한 훈련 실행
    result = trainer.run_complete_training()
    
    if result["success"]:
        print(f"✅ 훈련 완료!")
        print(f"   - 처리된 연도: {result['years_processed']}개")
        print(f"   - 총 샘플 수: {result['total_samples']}개")
        print(f"   - 정확도: {result['accuracy']:.3f}")
        print(f"   - 보고서: {result['report_path']}")
    else:
        print(f"❌ 훈련 실패: {result['error']}")

if __name__ == "__main__":
    main() 