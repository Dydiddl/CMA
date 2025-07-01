#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
글꼴 테스트 모듈
다양한 문자와 폰트 렌더링을 테스트하기 위한 코드
"""

def test_font_rendering():
    """폰트 렌더링 테스트"""
    print("=" * 60)
    print("글꼴 테스트 리포트")
    print("=" * 60)
    
    # 기본 문자 테스트
    print("\n[영문 대소문자]")
    print("Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm Nn Oo Pp Qq Rr Ss Tt Uu Vv Ww Xx Yy Zz")
    
    print("\n[숫자]")
    print("0 1 2 3 4 5 6 7 8 9")
    
    print("\n[한글 자음]")
    print("ㄱ ㄴ ㄷ ㄹ ㅁ ㅂ ㅅ ㅇ ㅈ ㅊ ㅋ ㅌ ㅍ ㅎ")
    
    print("\n[한글 모음]")
    print("ㅏ ㅑ ㅓ ㅕ ㅗ ㅛ ㅜ ㅠ ㅡ ㅣ")
    
    print("\n[한글 완성형]")
    print("가 나 다 라 마 바 사 아 자 차 카 타 파 하")
    
    print("\n[특수문자]")
    print("! @ # $ % ^ & * ( ) _ + - = { } [ ] | \\ : ; \" ' < > , . ? /")
    
    print("\n[프로그래밍 연산자]")
    print("== != <= >= += -= *= /= //= %= **= &= |= ^= <<= >>=")
    
    print("\n[화살표]")
    print("-> <- => <= <->")
    
    print("\n[수학기호]")
    print("± × ÷ √ ∞ ∫ ∑ ∏ ∂ ∆ ∇")
    
    print("\n[그리스문자]")
    print("α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω")
    
    print("\n[혼동하기 쉬운 문자]")
    print("숫자 0과 문자 O: 0 O 0O0 O0O")
    print("숫자 1과 문자 l: 1 l 1l1 l1l")
    print("숫자 5과 문자 S: 5 S 5S5 S5S")
    print("문자 I와 문자 l: I l IlI lIl")
    
    print("\n[리가처 테스트 - 프로그래밍 폰트에서 하나의 심볼로 표시됨]")
    print("화살표: -> <- => <= <->")
    print("비교연산자: == != <= >= ===")
    print("할당연산자: += -= *= /= //= %= **=")
    print("논리연산자: && || != ===")
    print("비트연산자: &= |= ^= <<= >>=")
    
    print("\n[코드 예시]")
    print("def calculate_total(labor_cost: float, material_cost: float) -> float:")
    print("const processData = (data) => { return data.map(item => item.id); }")
    print("SELECT * FROM contracts WHERE amount >= 1000000 AND status = 'active'")
    print(".contract-item:hover { background-color: #f0f0f0; }")
    print("<div class='contract-container' data-id='123'>")
    print(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$")
    print('{"contract_id": "CON-2024-001", "amount": 1000000}')
    
    print("\n[유니코드 테스트]")
    print("한국어: 안녕하세요 반갑습니다")
    print("일본어: こんにちは ありがとう")
    print("중국어: 你好 谢谢")
    print("이모지: 🚀 💻 🔧 ⚡ 🎯 📊 🔍 ✅ ❌ ⚠️ ℹ️")
    print("수학기호: ∑ ∏ ∫ ∂ ∇ ∆ ∞ ≠ ≤ ≥ ± × ÷ √")
    print("화학기호: H₂O CO₂ NaCl Fe₂O₃")
    print("통화기호: $ € ¥ £ ₩ ₹ ₽")
    
    print("\n" + "=" * 60)
    print("글꼴 테스트 완료")
    print("=" * 60)

if __name__ == "__main__":
    test_font_rendering() 