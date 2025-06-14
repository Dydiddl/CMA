# 계약 관리 API

## 기본 정보
- 엔드포인트: `/api/v1/contracts`
- 인증: JWT 토큰 필요
- 권한: 관리자, 일반 사용자

## API 목록

### 1. 계약 목록 조회
```http
GET /contracts
Authorization: Bearer {token}
```

#### 쿼리 파라미터
- `page`: 페이지 번호 (기본값: 1)
- `limit`: 페이지당 항목 수 (기본값: 20)
- `search`: 검색어 (프로젝트명)
- `status`: 계약 상태 (진행중, 완료, 취소)
- `vendor_id`: 거래처 ID
- `start_date`: 시작일
- `end_date`: 종료일
- `sort`: 정렬 기준 (created_at, contract_date, contract_amount)
- `order`: 정렬 방향 (asc, desc)

#### 응답
```json
{
    "status": "success",
    "data": {
        "items": [
            {
                "id": "contract-uuid",
                "project_name": "아파트 신축공사",
                "contract_amount": 1000000000,
                "contract_date": "2024-03-20",
                "vendor": {
                    "id": "vendor-uuid",
                    "company_name": "건설회사"
                },
                "status": "진행중",
                "created_at": "2024-03-20T10:00:00Z"
            }
        ],
        "total": 100,
        "page": 1,
        "limit": 20
    },
    "message": "계약 목록을 성공적으로 조회했습니다."
}
```

### 2. 계약 상세 조회
```http
GET /contracts/{contract_id}
Authorization: Bearer {token}
```

#### 응답
```json
{
    "status": "success",
    "data": {
        "id": "contract-uuid",
        "project_name": "아파트 신축공사",
        "contract_amount": 1000000000,
        "contract_date": "2024-03-20",
        "vendor": {
            "id": "vendor-uuid",
            "company_name": "건설회사",
            "representative": "김대표"
        },
        "status": "진행중",
        "documents": {
            "contract_file": "계약서.pdf",
            "attachments": [
                "부록1.pdf",
                "부록2.pdf"
            ]
        },
        "payments": [
            {
                "id": "payment-uuid",
                "amount": 300000000,
                "due_date": "2024-04-20",
                "status": "미지급"
            }
        ],
        "created_at": "2024-03-20T10:00:00Z",
        "updated_at": "2024-03-20T15:30:00Z"
    },
    "message": "계약 정보를 성공적으로 조회했습니다."
}
```

### 3. 계약 등록
```http
POST /contracts
Authorization: Bearer {token}
Content-Type: application/json

{
    "project_name": "아파트 신축공사",
    "contract_amount": 1000000000,
    "contract_date": "2024-03-20",
    "vendor_id": "vendor-uuid",
    "status": "진행중",
    "documents": {
        "contract_file": "계약서.pdf",
        "attachments": [
            "부록1.pdf",
            "부록2.pdf"
        ]
    }
}
```

#### 응답
```json
{
    "status": "success",
    "data": {
        "id": "contract-uuid",
        "project_name": "아파트 신축공사",
        "contract_amount": 1000000000,
        "contract_date": "2024-03-20",
        "vendor": {
            "id": "vendor-uuid",
            "company_name": "건설회사"
        },
        "status": "진행중",
        "documents": {
            "contract_file": "계약서.pdf",
            "attachments": [
                "부록1.pdf",
                "부록2.pdf"
            ]
        },
        "created_at": "2024-03-20T10:00:00Z"
    },
    "message": "계약이 성공적으로 등록되었습니다."
}
```

### 4. 계약 수정
```http
PUT /contracts/{contract_id}
Authorization: Bearer {token}
Content-Type: application/json

{
    "status": "완료",
    "documents": {
        "attachments": [
            "부록1.pdf",
            "부록2.pdf",
            "부록3.pdf"
        ]
    }
}
```

#### 응답
```json
{
    "status": "success",
    "data": {
        "id": "contract-uuid",
        "project_name": "아파트 신축공사",
        "contract_amount": 1000000000,
        "contract_date": "2024-03-20",
        "vendor": {
            "id": "vendor-uuid",
            "company_name": "건설회사"
        },
        "status": "완료",
        "documents": {
            "contract_file": "계약서.pdf",
            "attachments": [
                "부록1.pdf",
                "부록2.pdf",
                "부록3.pdf"
            ]
        },
        "updated_at": "2024-03-20T16:00:00Z"
    },
    "message": "계약 정보가 성공적으로 수정되었습니다."
}
```

## 에러 코드
- `CONTRACT_NOT_FOUND`: 계약을 찾을 수 없음
- `VENDOR_NOT_FOUND`: 거래처를 찾을 수 없음
- `VALIDATION_ERROR`: 입력값 검증 실패
- `PERMISSION_DENIED`: 권한 없음
- `INVALID_STATUS`: 잘못된 계약 상태

## 요청 제한
- 목록 조회: 토큰당 1초에 30회
- 상세 조회: 토큰당 1초에 30회
- 등록/수정: 토큰당 1분에 10회 