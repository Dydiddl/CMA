#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 머신러닝 학습 시스템

2025년 정답 데이터만을 활용하여 목차 분류 모델을 학습시킵니다.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
from collections import defaultdict, Counter
import numpy as np
from dataclasses import dataclass

@dataclass
class TrainingData:
    """훈련 데이터 구조체"""
    text: str
    features: Dict[str, Any]
    label: str
    page: int
    confidence: float

class SimpleMLTrainer:
    """간단한 머신러닝 학습 시스템"""
    
    def __init__(self, ground_truth_path: str = "data/ground truth/toc_ground_truth_2025.md"):
        self.ground_truth_path = Path(ground_truth_path)
        self.training_data = []
        self.models = {}
        self.performance_metrics = {}
        
    def collect_ground_truth_data(self) -> Dict[str, Any]:
        """정답 데이터 수집"""
        print("📊 정답 데이터 수집 시작...")
        
        if not self.ground_truth_path.exists():
            print(f"❌ 정답 데이터 파일이 없습니다: {self.ground_truth_path}")
            return {"total_items": 0, "sections": {}}
        
        try:
            with open(self.ground_truth_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 들여쓰기 기반 계층 구조 파싱
            lines = content.split('\n')
            training_items = []
            current_section = None
            
            for line in lines:
                line = line.strip()
                
                # 빈 줄 건너뛰기
                if not line:
                    continue
                
                # 들여쓰기 레벨 계산
                indent_level = len(line) - len(line.lstrip())
                
                # 부문 레벨 (최소 들여쓰기)
                if indent_level <= 4 and "부문" in line:
                    current_section = line.strip()
                    print(f"  - 부문 발견: {current_section}")
                    continue
                
                # 목차 항목 (들여쓰기가 있는 경우)
                if indent_level > 4 and current_section and "," in line:
                    # 페이지 번호 추출
                    parts = line.split(',')
                    if len(parts) >= 2:
                        item_text = parts[0].strip()
                        try:
                            page_number = int(parts[1].strip())
                        except ValueError:
                            page_number = 0
                        
                        # 특성 추출
                        features = self._extract_features(item_text)
                        
                        # 훈련 데이터 생성
                        training_item = TrainingData(
                            text=item_text,
                            features=features,
                            label=current_section,
                            page=page_number,
                            confidence=1.0
                        )
                        training_items.append(training_item)
            
            self.training_data = training_items
            
            # 통계 계산
            section_counts = Counter([item.label for item in training_items])
            
            print(f"✅ 정답 데이터 수집 완료: {len(training_items)}개 항목")
            for section, count in section_counts.items():
                print(f"  - {section}: {count}개")
            
            return {
                "total_items": len(training_items),
                "sections": dict(section_counts)
            }
            
        except Exception as e:
            print(f"❌ 정답 데이터 수집 중 오류: {e}")
            import traceback
            traceback.print_exc()
            return {"total_items": 0, "sections": {}}
    
    def _extract_features(self, text: str) -> Dict[str, Any]:
        """목차 항목에서 특성 추출"""
        # 번호와 제목 분리
        parts = text.split(' ', 1)
        number = parts[0] if parts else ""
        title = parts[1] if len(parts) > 1 else ""
        
        # 기본 특성
        features = {
            "number_length": len(number),
            "title_length": len(title),
            "word_count": len(title.split()),
            "has_numbers": bool(re.search(r'\d', title)),
            "has_parentheses": bool(re.search(r'[\(\)]', title)),
            "has_korean": bool(re.search(r'[가-힣]', title)),
            "has_english": bool(re.search(r'[a-zA-Z]', title)),
            "level": len(number.split('-')) if number else 0,
            "chapter_number": int(number.split('-')[0]) if number and number.split('-')[0].isdigit() else 0
        }
        
        # 키워드 특성
        keywords = {
            "설치": "설치" in title,
            "해체": "해체" in title,
            "공사": "공사" in title,
            "시설": "시설" in title,
            "장비": "장비" in title,
            "재료": "재료" in title,
            "도로": "도로" in title,
            "건물": "건물" in title,
            "배관": "배관" in title,
            "전기": "전기" in title,
            "조경": "조경" in title,
            "방수": "방수" in title,
            "단열": "단열" in title,
            "도장": "도장" in title,
            "철근": "철근" in title,
            "콘크리트": "콘크리트" in title
        }
        features.update(keywords)
        
        return features
    
    def train_ml_models(self) -> Dict[str, Any]:
        """머신러닝 모델 훈련"""
        print("\n🎯 머신러닝 모델 훈련 시작...")
        
        if not self.training_data:
            print("❌ 훈련 데이터가 없습니다.")
            return {}
        
        # 특성 벡터와 라벨 준비
        X = []
        y = []
        
        for item in self.training_data:
            # 특성 벡터 생성
            feature_vector = list(item.features.values())
            X.append(feature_vector)
            y.append(item.label)
        
        print(f"  - 특성 벡터 크기: {len(X[0]) if X else 0}")
        print(f"  - 훈련 샘플 수: {len(X)}")
        print(f"  - 클래스 수: {len(set(y))}")
        
        # 데이터 분할
        try:
            from sklearn.model_selection import train_test_split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
        except ImportError:
            print("❌ scikit-learn이 설치되지 않았습니다.")
            print("설치 명령: pip install scikit-learn")
            return {}
        
        # 다양한 모델 훈련
        models = {}
        performance = {}
        
        # 1. 결정 트리
        print("🌳 결정 트리 모델 훈련...")
        try:
            from sklearn.tree import DecisionTreeClassifier
            dt_model = DecisionTreeClassifier(random_state=42, max_depth=10)
            dt_model.fit(X_train, y_train)
            models["decision_tree"] = dt_model
        except Exception as e:
            print(f"  ❌ 결정 트리 훈련 실패: {e}")
        
        # 2. 랜덤 포레스트
        print("🌲 랜덤 포레스트 모델 훈련...")
        try:
            from sklearn.ensemble import RandomForestClassifier
            rf_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
            rf_model.fit(X_train, y_train)
            models["random_forest"] = rf_model
        except Exception as e:
            print(f"  ❌ 랜덤 포레스트 훈련 실패: {e}")
        
        # 3. 로지스틱 회귀
        print("📊 로지스틱 회귀 모델 훈련...")
        try:
            from sklearn.linear_model import LogisticRegression
            lr_model = LogisticRegression(random_state=42, max_iter=1000)
            lr_model.fit(X_train, y_train)
            models["logistic_regression"] = lr_model
        except Exception as e:
            print(f"  ❌ 로지스틱 회귀 훈련 실패: {e}")
        
        # 모델 성능 평가
        from sklearn.metrics import accuracy_score, classification_report
        
        for model_name, model in models.items():
            try:
                y_pred = model.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                
                performance[model_name] = {
                    "accuracy": accuracy,
                    "classification_report": classification_report(y_test, y_pred, output_dict=True)
                }
                
                print(f"  - {model_name}: {accuracy:.3f} 정확도")
            except Exception as e:
                print(f"  ❌ {model_name} 성능 평가 실패: {e}")
        
        self.models = models
        self.performance_metrics = performance
        
        return {
            "models": list(models.keys()),
            "performance": performance,
            "best_model": max(performance.items(), key=lambda x: x[1]["accuracy"])[0] if performance else None
        }
    
    def demonstrate_prediction(self, test_texts: List[str]):
        """예측 시연"""
        if not self.models:
            print("❌ 훈련된 모델이 없습니다.")
            return
        
        best_model_name = max(self.performance_metrics.items(), key=lambda x: x[1]["accuracy"])[0]
        best_model = self.models[best_model_name]
        
        print(f"\n🔮 예측 시연 (최적 모델: {best_model_name})")
        print("=" * 60)
        
        for test_text in test_texts:
            # 특성 추출
            features = self._extract_features(test_text)
            feature_vector = list(features.values())
            
            # 예측
            try:
                prediction = best_model.predict([feature_vector])[0]
                probabilities = best_model.predict_proba([feature_vector])[0]
                
                print(f"\n📝 입력: '{test_text}'")
                print(f"🎯 예측: {prediction}")
                print(f"📊 확률 분포:")
                
                # 클래스별 확률 출력
                classes = best_model.classes_
                for i, (class_name, prob) in enumerate(zip(classes, probabilities)):
                    marker = "✅" if class_name == prediction else "  "
                    print(f"  {marker} {class_name}: {prob:.3f} ({prob*100:.1f}%)")
                
            except Exception as e:
                print(f"❌ 예측 실패: {e}")
    
    def generate_training_report(self) -> str:
        """훈련 결과 보고서 생성"""
        report = f"""# 🤖 머신러닝 모델 훈련 보고서

## 📊 훈련 데이터 현황
- **총 훈련 항목**: {len(self.training_data)}개
- **부문별 분포**: {dict(Counter(item.label for item in self.training_data))}

## 🎯 모델 성능 비교

"""
        
        if self.performance_metrics:
            for model_name, metrics in self.performance_metrics.items():
                accuracy = metrics["accuracy"]
                report += f"### {model_name.replace('_', ' ').title()}\n"
                report += f"- **정확도**: {accuracy:.3f} ({accuracy*100:.1f}%)\n"
                
                # 부문별 성능
                section_metrics = metrics["classification_report"]
                for section in ["공통부문", "토목부문", "건축부문", "기계설비부문", "유지관리부문"]:
                    if section in section_metrics:
                        precision = section_metrics[section]["precision"]
                        recall = section_metrics[section]["recall"]
                        f1 = section_metrics[section]["f1-score"]
                        report += f"- **{section}**: 정밀도 {precision:.3f}, 재현율 {recall:.3f}, F1 {f1:.3f}\n"
                report += "\n"
        
        best_model = max(self.performance_metrics.items(), key=lambda x: x[1]["accuracy"])[0] if self.performance_metrics else None
        if best_model:
            report += f"## 🏆 최적 모델\n- **모델**: {best_model}\n"
            report += f"- **정확도**: {self.performance_metrics[best_model]['accuracy']:.3f}\n"
        
        return report
    
    def save_models(self, output_dir: str = "output/ml_models"):
        """훈련된 모델 저장"""
        if not self.models:
            print("❌ 저장할 모델이 없습니다.")
            return
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"\n💾 모델 저장 중... ({output_path})")
        
        # 모델 저장
        import pickle
        
        for model_name, model in self.models.items():
            model_file = output_path / f"{model_name}_model.pkl"
            with open(model_file, 'wb') as f:
                pickle.dump(model, f)
            print(f"  - {model_name} 모델 저장: {model_file}")
        
        # 성능 메트릭 저장
        metrics_file = output_path / "performance_metrics.json"
        with open(metrics_file, 'w', encoding='utf-8') as f:
            json.dump(self.performance_metrics, f, ensure_ascii=False, indent=2)
        print(f"  - 성능 메트릭 저장: {metrics_file}")

def main():
    """메인 함수"""
    print("🚀 간단한 머신러닝 학습 시스템 시작")
    print("=" * 60)
    
    # 학습 시스템 초기화
    trainer = SimpleMLTrainer()
    
    # 1. 정답 데이터 수집
    collection_results = trainer.collect_ground_truth_data()
    
    if collection_results["total_items"] == 0:
        print("❌ 수집된 데이터가 없습니다. 프로그램을 종료합니다.")
        return
    
    # 2. 머신러닝 모델 훈련
    training_results = trainer.train_ml_models()
    
    if not training_results:
        print("❌ 모델 훈련에 실패했습니다.")
        return
    
    # 3. 예측 시연
    test_cases = [
        "1-1-1 목적",
        "2-8-11 계단난간대 설치 및 해체",
        "1-1 도로포장공사",
        "1-1 철골공사",
        "1-1 배관공사"
    ]
    
    trainer.demonstrate_prediction(test_cases)
    
    # 4. 보고서 생성
    report = trainer.generate_training_report()
    
    # 5. 모델 저장
    trainer.save_models()
    
    # 6. 보고서 저장
    report_file = Path("output/ml_models/training_report.md")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 학습 완료! 보고서: {report_file}")
    print("\n" + "=" * 60)
    print("📋 최종 결과 요약")
    print("=" * 60)
    print(report)

if __name__ == "__main__":
    main() 

    