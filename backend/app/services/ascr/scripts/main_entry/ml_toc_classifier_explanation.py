#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
머신러닝 기반 목차 분류 시스템 작동 원리 설명

정답 데이터를 활용하여 머신러닝 모델이 어떻게 목차를 분류하는지 단계별로 설명합니다.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import Counter
import numpy as np

class MLTOCClassifierExplanation:
    """머신러닝 목차 분류 시스템 작동 원리 설명 클래스"""
    
    def __init__(self, ground_truth_path: str):
        self.ground_truth_path = Path(ground_truth_path)
        self.training_data = []
        self.feature_vectors = []
        self.labels = []
        
    def explain_ml_workflow(self):
        """머신러닝 워크플로우 단계별 설명"""
        
        print("🤖 머신러닝 기반 목차 분류 시스템 작동 원리")
        print("=" * 60)
        
        # 1단계: 데이터 수집 및 전처리
        print("\n📊 1단계: 데이터 수집 및 전처리")
        print("-" * 40)
        self._explain_data_collection()
        
        # 2단계: 특성 추출
        print("\n🔍 2단계: 특성 추출 (Feature Extraction)")
        print("-" * 40)
        self._explain_feature_extraction()
        
        # 3단계: 모델 훈련
        print("\n🎯 3단계: 모델 훈련 (Model Training)")
        print("-" * 40)
        self._explain_model_training()
        
        # 4단계: 예측 및 분류
        print("\n🔮 4단계: 예측 및 분류 (Prediction)")
        print("-" * 40)
        self._explain_prediction()
        
        # 5단계: 성능 평가
        print("\n📈 5단계: 성능 평가 (Evaluation)")
        print("-" * 40)
        self._explain_evaluation()
    
    def _explain_data_collection(self):
        """데이터 수집 단계 설명"""
        print("""
목차 항목들을 수집하여 훈련 데이터를 만듭니다.

예시 데이터:
- "1-1-1 목적" → 공통부문
- "2-8-11 계단난간대 설치 및 해체" → 공통부문  
- "1-1 도로포장공사" → 토목부문
- "1-1 철골공사" → 건축부문
- "1-1 배관공사" → 기계설비부문
- "1-1 공통" → 유지관리부문

각 항목은 다음과 같은 정보를 포함합니다:
- 항목 번호 (예: "1-1-1", "2-8-11")
- 항목 제목 (예: "목적", "계단난간대 설치 및 해체")
- 페이지 번호
- 소속 부문 (정답 라벨)
        """)
    
    def _explain_feature_extraction(self):
        """특성 추출 단계 설명"""
        print("""
각 목차 항목에서 머신러닝이 학습할 수 있는 특성들을 추출합니다.

추출되는 특성들:

1. 텍스트 특성:
   - 항목 번호 길이 (예: "1-1-1" = 5글자)
   - 항목 제목 길이 (예: "목적" = 2글자)
   - 단어 개수 (예: "계단난간대 설치 및 해체" = 4개 단어)
   - 숫자 포함 여부 (제목에 숫자가 있는지)
   - 괄호 포함 여부 (제목에 괄호가 있는지)
   - 한국어 포함 여부
   - 영어 포함 여부

2. 구조적 특성:
   - 계층 레벨 (예: "1-1-1" = 3레벨)
   - 상위 장 번호 (예: "제1장", "제2장")
   - 페이지 번호

3. 패턴 특성:
   - 특정 키워드 포함 여부 (예: "설치", "해체", "공사")
   - 특수문자 사용 패턴
   - 번호 형식 패턴

예시 특성 벡터:
"2-8-11 계단난간대 설치 및 해체" → [5, 12, 4, True, False, True, False, 3, 2, 52, True, True, False]
        """)
    
    def _explain_model_training(self):
        """모델 훈련 단계 설명"""
        print("""
수집된 데이터로 머신러닝 모델을 훈련시킵니다.

훈련 과정:

1. 데이터 분할:
   - 훈련 데이터 (80%): 모델이 학습할 데이터
   - 검증 데이터 (20%): 모델 성능을 평가할 데이터

2. 모델 선택:
   - 결정 트리 (Decision Tree): 규칙 기반 분류
   - 랜덤 포레스트 (Random Forest): 여러 결정 트리 조합
   - 서포트 벡터 머신 (SVM): 경계선 기반 분류
   - 신경망 (Neural Network): 복잡한 패턴 학습

3. 학습 과정:
   - 모델이 특성과 정답 라벨 간의 관계를 학습
   - 예: "제2장"으로 시작하는 항목은 "공통부문"에 속할 확률이 높음
   - "설치" 키워드가 있으면 "기계설비부문"일 가능성 증가

예시 학습 규칙:
- IF (장번호 <= 8) THEN 부문 = "공통부문"
- IF (제목에 "설치" 포함) AND (장번호 > 8) THEN 부문 = "기계설비부문"
- IF (제목에 "공사" 포함) AND (장번호 <= 17) THEN 부문 = "토목부문"
        """)
    
    def _explain_prediction(self):
        """예측 단계 설명"""
        print("""
훈련된 모델로 새로운 목차 항목을 분류합니다.

예측 과정:

1. 새로운 항목 입력:
   입력: "3-2-1 굴착(인력/토사)"

2. 특성 추출:
   - 번호 길이: 7
   - 제목 길이: 8
   - 단어 개수: 2
   - 숫자 포함: True
   - 괄호 포함: True
   - 계층 레벨: 3
   - 장 번호: 3
   - 특성 벡터: [7, 8, 2, True, True, True, False, 3, 3, 0, False, False, True]

3. 모델 예측:
   - 공통부문: 0.05 (5%)
   - 토목부문: 0.85 (85%) ← 가장 높은 확률
   - 건축부문: 0.05 (5%)
   - 기계설비부문: 0.03 (3%)
   - 유지관리부문: 0.02 (2%)

4. 결과 출력:
   예측 결과: "토목부문" (85% 확신도)

예측 근거:
- 장 번호 3은 토목부문 범위 (9-17)
- "굴착" 키워드는 토목공사 관련
- 괄호 안의 "인력/토사"는 토목공사 특성
        """)
    
    def _explain_evaluation(self):
        """성능 평가 단계 설명"""
        print("""
모델의 성능을 다양한 지표로 평가합니다.

평가 지표:

1. 정확도 (Accuracy):
   - 전체 예측 중 올바른 예측 비율
   - 예: 100개 중 85개 정확 → 85% 정확도

2. 정밀도 (Precision):
   - 특정 부문으로 예측한 것 중 실제로 맞은 비율
   - 예: 토목부문으로 예측한 20개 중 18개 정확 → 90% 정밀도

3. 재현율 (Recall):
   - 실제 특정 부문인 것 중 올바르게 예측한 비율
   - 예: 실제 토목부문 25개 중 18개 정확 예측 → 72% 재현율

4. F1 점수:
   - 정밀도와 재현율의 조화평균
   - 예: (90% × 72%) / (90% + 72%) = 80% F1 점수

5. 혼동 행렬 (Confusion Matrix):
   예측\실제    공통  토목  건축  기계  유지
   공통부문      15    2    1    0    0
   토목부문       1   18    1    1    0
   건축부문       0    1   12    1    0
   기계설비부문   0    0    1   14    1
   유지관리부문   0    0    0    1    8

성능 개선 방법:
- 더 많은 훈련 데이터 수집
- 특성 엔지니어링 개선
- 모델 하이퍼파라미터 튜닝
- 앙상블 방법 사용
        """)
    
    def create_training_example(self):
        """훈련 데이터 예시 생성"""
        example_data = [
            {
                "text": "1-1-1 목적",
                "features": {
                    "number_length": 5,
                    "title_length": 2,
                    "word_count": 1,
                    "has_numbers": False,
                    "has_parentheses": False,
                    "level": 3,
                    "chapter_number": 1
                },
                "label": "공통부문"
            },
            {
                "text": "2-8-11 계단난간대 설치 및 해체",
                "features": {
                    "number_length": 7,
                    "title_length": 12,
                    "word_count": 4,
                    "has_numbers": False,
                    "has_parentheses": False,
                    "level": 3,
                    "chapter_number": 2
                },
                "label": "공통부문"
            },
            {
                "text": "1-1 도로포장공사",
                "features": {
                    "number_length": 4,
                    "title_length": 6,
                    "word_count": 1,
                    "has_numbers": False,
                    "has_parentheses": False,
                    "level": 2,
                    "chapter_number": 1
                },
                "label": "토목부문"
            }
        ]
        
        return example_data
    
    def demonstrate_prediction(self, input_text: str):
        """예측 과정 시연"""
        print(f"\n🔮 예측 시연: '{input_text}'")
        print("-" * 50)
        
        # 특성 추출 시연
        features = self._extract_features_demo(input_text)
        print("📊 추출된 특성:")
        for key, value in features.items():
            print(f"  - {key}: {value}")
        
        # 예측 결과 시연
        prediction = self._predict_demo(features)
        print(f"\n🎯 예측 결과: {prediction['label']} (확신도: {prediction['confidence']:.1%})")
        print(f"📝 예측 근거: {prediction['reasoning']}")
    
    def _extract_features_demo(self, text: str) -> Dict[str, Any]:
        """특성 추출 시연"""
        # 간단한 특성 추출 로직
        parts = text.split(' ', 1)
        number = parts[0] if parts else ""
        title = parts[1] if len(parts) > 1 else ""
        
        features = {
            "number_length": len(number),
            "title_length": len(title),
            "word_count": len(title.split()),
            "has_numbers": bool(re.search(r'\d', title)),
            "has_parentheses": bool(re.search(r'[\(\)]', title)),
            "level": len(number.split('-')),
            "chapter_number": int(number.split('-')[0]) if number else 0
        }
        
        return features
    
    def _predict_demo(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """예측 시연"""
        chapter_num = features["chapter_number"]
        
        # 간단한 규칙 기반 예측
        if chapter_num <= 8:
            label = "공통부문"
            confidence = 0.95
            reasoning = f"장 번호 {chapter_num}은 공통부문 범위(1-8)에 속합니다."
        elif chapter_num <= 17:
            label = "토목부문"
            confidence = 0.90
            reasoning = f"장 번호 {chapter_num}은 토목부문 범위(9-17)에 속합니다."
        elif chapter_num <= 28:
            label = "건축부문"
            confidence = 0.90
            reasoning = f"장 번호 {chapter_num}은 건축부문 범위(18-28)에 속합니다."
        elif chapter_num <= 41:
            label = "기계설비부문"
            confidence = 0.90
            reasoning = f"장 번호 {chapter_num}은 기계설비부문 범위(29-41)에 속합니다."
        else:
            label = "유지관리부문"
            confidence = 0.90
            reasoning = f"장 번호 {chapter_num}은 유지관리부문 범위(42+)에 속합니다."
        
        return {
            "label": label,
            "confidence": confidence,
            "reasoning": reasoning
        }

def main():
    """메인 함수"""
    explainer = MLTOCClassifierExplanation("data/ground truth/toc_ground_truth_2025.md")
    
    # 전체 워크플로우 설명
    explainer.explain_ml_workflow()
    
    # 예측 시연
    print("\n" + "=" * 60)
    print("🎯 실제 예측 시연")
    print("=" * 60)
    
    test_cases = [
        "1-1-1 목적",
        "2-8-11 계단난간대 설치 및 해체",
        "1-1 도로포장공사",
        "1-1 철골공사",
        "1-1 배관공사"
    ]
    
    for test_case in test_cases:
        explainer.demonstrate_prediction(test_case)
        print()

if __name__ == "__main__":
    main() 