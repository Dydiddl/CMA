# 매출/지출 관리 API

## 기본 정보
- 엔드포인트: `/api/v1/transactions`
- 인증: JWT 토큰 필요
- 권한: 관리자, 일반 사용자

## API 목록

### 1. 거래 목록 조회
```http
GET /transactions
Authorization: Bearer {token}
```

#### 쿼리 파라미터
- `page`: 페이지 번호 (기본값: 1)
- `limit`: 페이지당 항목 수 (기본값: 20)
- `transaction_type`: 거래 유형 (income, expense)
- `contract_id`: 계약 ID
- `category`: 거래 카테고리
- `start_date`: 시작일
- `end_date`: 종료일
- `min_amount`: 최소 금액
- `max_amount`: 최대 금액
- `sort`: 정렬 기준 (transaction_date, amount)
- `order`: 정렬 방향 (asc, desc)

#### 응답
```json
{
    "status": "success",
    "data": {
        "items": [
            {
                "id": "transaction-uuid",
                "contract": {
                    "id": "contract-uuid",
                    "project_name": "아파트 신축공사"
                },
                "transaction_type": "income",
                "amount": 50000000,
                "transaction_date": "2024-03-20",
                "category": "계약금",
                "description": "1차 계약금 입금",
                "created_at": "2024-03-20T10:00:00Z"
            }
        ],
        "total": 100,
        "page": 1,
        "limit": 20,
        "summary": {
            "total_income": 1000000000,
            "total_expense": 500000000,
            "net_amount": 500000000
        }
    },
    "message": "거래 목록을 성공적으로 조회했습니다."
}
```

### 2. 거래 상세 조회
```http
GET /transactions/{transaction_id}
Authorization: Bearer {token}
```

#### 응답
```json
{
    "status": "success",
    "data": {
        "id": "transaction-uuid",
        "contract": {
            "id": "contract-uuid",
            "project_name": "아파트 신축공사",
            "vendor": {
                "id": "vendor-uuid",
                "company_name": "건설회사"
            }
        },
        "transaction_type": "income",
        "amount": 50000000,
        "transaction_date": "2024-03-20",
        "category": "계약금",
        "description": "1차 계약금 입금",
        "payment_method": "계좌이체",
        "bank_info": {
            "bank_name": "국민은행",
            "account_number": "123-456-789012"
        },
        "attachments": [
            "입금확인서.pdf"
        ],
        "created_at": "2024-03-20T10:00:00Z",
        "updated_at": "2024-03-20T15:30:00Z"
    },
    "message": "거래 정보를 성공적으로 조회했습니다."
}
```

### 3. 거래 등록
```http
POST /transactions
Authorization: Bearer {token}
Content-Type: application/json

{
    "contract_id": "contract-uuid",
    "transaction_type": "income",
    "amount": 50000000,
    "transaction_date": "2024-03-20",
    "category": "계약금",
    "description": "1차 계약금 입금",
    "payment_method": "계좌이체",
    "bank_info": {
        "bank_name": "국민은행",
        "account_number": "123-456-789012"
    },
    "attachments": [
        "입금확인서.pdf"
    ]
}
```

#### 응답
```json
{
    "status": "success",
    "data": {
        "id": "transaction-uuid",
        "contract": {
            "id": "contract-uuid",
            "project_name": "아파트 신축공사"
        },
        "transaction_type": "income",
        "amount": 50000000,
        "transaction_date": "2024-03-20",
        "category": "계약금",
        "description": "1차 계약금 입금",
        "payment_method": "계좌이체",
        "bank_info": {
            "bank_name": "국민은행",
            "account_number": "123-456-789012"
        },
        "attachments": [
            "입금확인서.pdf"
        ],
        "created_at": "2024-03-20T10:00:00Z"
    },
    "message": "거래가 성공적으로 등록되었습니다."
}
```

### 4. 거래 수정
```http
PUT /transactions/{transaction_id}
Authorization: Bearer {token}
Content-Type: application/json

{
    "amount": 55000000,
    "description": "1차 계약금 입금 수정",
    "attachments": [
        "입금확인서.pdf",
        "추가서류.pdf"
    ]
}
```

#### 응답
```json
{
    "status": "success",
    "data": {
        "id": "transaction-uuid",
        "contract": {
            "id": "contract-uuid",
            "project_name": "아파트 신축공사"
        },
        "transaction_type": "income",
        "amount": 55000000,
        "transaction_date": "2024-03-20",
        "category": "계약금",
        "description": "1차 계약금 입금 수정",
        "payment_method": "계좌이체",
        "bank_info": {
            "bank_name": "국민은행",
            "account_number": "123-456-789012"
        },
        "attachments": [
            "입금확인서.pdf",
            "추가서류.pdf"
        ],
        "updated_at": "2024-03-20T16:00:00Z"
    },
    "message": "거래 정보가 성공적으로 수정되었습니다."
}
```

## 에러 코드
- `TRANSACTION_NOT_FOUND`: 거래를 찾을 수 없음
- `CONTRACT_NOT_FOUND`: 계약을 찾을 수 없음
- `VALIDATION_ERROR`: 입력값 검증 실패
- `PERMISSION_DENIED`: 권한 없음
- `INVALID_TRANSACTION_TYPE`: 잘못된 거래 유형
- `INVALID_AMOUNT`: 잘못된 금액

## 요청 제한
- 목록 조회: 토큰당 1초에 30회
- 상세 조회: 토큰당 1초에 30회
- 등록/수정: 토큰당 1분에 10회 