# 거래처 관리 API

## 기본 정보
- 엔드포인트: `/api/v1/vendors`
- 인증: JWT 토큰 필요
- 권한: 관리자, 일반 사용자

## API 목록

### 1. 거래처 목록 조회
```http
GET /vendors
Authorization: Bearer {token}
```

#### 쿼리 파라미터
- `page`: 페이지 번호 (기본값: 1)
- `limit`: 페이지당 항목 수 (기본값: 20)
- `search`: 검색어 (회사명, 대표자명)
- `sort`: 정렬 기준 (created_at, company_name)
- `order`: 정렬 방향 (asc, desc)

#### 응답
```json
{
    "status": "success",
    "data": {
        "items": [
            {
                "id": "vendor-uuid",
                "company_name": "건설회사",
                "business_number": "123-45-67890",
                "representative": "김대표",
                "address": "서울시 강남구",
                "contact": "02-1234-5678",
                "bank_info": {
                    "bank_name": "국민은행",
                    "account_number": "123-456-789012"
                },
                "created_at": "2024-03-20T10:00:00Z"
            }
        ],
        "total": 100,
        "page": 1,
        "limit": 20
    },
    "message": "거래처 목록을 성공적으로 조회했습니다."
}
```

### 2. 거래처 상세 조회
```http
GET /vendors/{vendor_id}
Authorization: Bearer {token}
```

#### 응답
```json
{
    "status": "success",
    "data": {
        "id": "vendor-uuid",
        "company_name": "건설회사",
        "business_number": "123-45-67890",
        "representative": "김대표",
        "address": "서울시 강남구",
        "contact": "02-1234-5678",
        "bank_info": {
            "bank_name": "국민은행",
            "account_number": "123-456-789012"
        },
        "contracts": [
            {
                "id": "contract-uuid",
                "project_name": "아파트 신축공사",
                "contract_amount": 1000000000,
                "contract_date": "2024-03-20"
            }
        ],
        "created_at": "2024-03-20T10:00:00Z",
        "updated_at": "2024-03-20T15:30:00Z"
    },
    "message": "거래처 정보를 성공적으로 조회했습니다."
}
```

### 3. 거래처 등록
```http
POST /vendors
Authorization: Bearer {token}
Content-Type: application/json

{
    "company_name": "건설회사",
    "business_number": "123-45-67890",
    "representative": "김대표",
    "address": "서울시 강남구",
    "contact": "02-1234-5678",
    "bank_info": {
        "bank_name": "국민은행",
        "account_number": "123-456-789012"
    }
}
```

#### 응답
```json
{
    "status": "success",
    "data": {
        "id": "vendor-uuid",
        "company_name": "건설회사",
        "business_number": "123-45-67890",
        "representative": "김대표",
        "address": "서울시 강남구",
        "contact": "02-1234-5678",
        "bank_info": {
            "bank_name": "국민은행",
            "account_number": "123-456-789012"
        },
        "created_at": "2024-03-20T10:00:00Z"
    },
    "message": "거래처가 성공적으로 등록되었습니다."
}
```

### 4. 거래처 수정
```http
PUT /vendors/{vendor_id}
Authorization: Bearer {token}
Content-Type: application/json

{
    "company_name": "건설회사 수정",
    "contact": "02-9876-5432"
}
```

#### 응답
```json
{
    "status": "success",
    "data": {
        "id": "vendor-uuid",
        "company_name": "건설회사 수정",
        "business_number": "123-45-67890",
        "representative": "김대표",
        "address": "서울시 강남구",
        "contact": "02-9876-5432",
        "bank_info": {
            "bank_name": "국민은행",
            "account_number": "123-456-789012"
        },
        "updated_at": "2024-03-20T16:00:00Z"
    },
    "message": "거래처 정보가 성공적으로 수정되었습니다."
}
```

## 에러 코드
- `VENDOR_NOT_FOUND`: 거래처를 찾을 수 없음
- `VENDOR_ALREADY_EXISTS`: 이미 존재하는 거래처
- `VALIDATION_ERROR`: 입력값 검증 실패
- `PERMISSION_DENIED`: 권한 없음

## 요청 제한
- 목록 조회: 토큰당 1초에 30회
- 상세 조회: 토큰당 1초에 30회
- 등록/수정: 토큰당 1분에 10회 