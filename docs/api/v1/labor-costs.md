# 노무비 관리 API

## 기본 정보
- 엔드포인트: `/api/v1/labor-costs`
- 인증: JWT 토큰 필요
- 권한: 관리자, 일반 사용자

## API 목록

### 1. 노무비 목록 조회
```http
GET /labor-costs
Authorization: Bearer {token}
```

#### 쿼리 파라미터
- `page`: 페이지 번호 (기본값: 1)
- `limit`: 페이지당 항목 수 (기본값: 20)
- `contract_id`: 계약 ID
- `worker_name`: 작업자 이름
- `work_type`: 작업 유형
- `start_date`: 시작일
- `end_date`: 종료일
- `sort`: 정렬 기준 (work_date, daily_wage)
- `order`: 정렬 방향 (asc, desc)

#### 응답
```json
{
    "status": "success",
    "data": {
        "items": [
            {
                "id": "labor-cost-uuid",
                "contract": {
                    "id": "contract-uuid",
                    "project_name": "아파트 신축공사"
                },
                "worker_name": "김일용",
                "work_date": "2024-03-20",
                "daily_wage": 150000,
                "work_type": "철근공사",
                "created_at": "2024-03-20T10:00:00Z"
            }
        ],
        "total": 100,
        "page": 1,
        "limit": 20
    },
    "message": "노무비 목록을 성공적으로 조회했습니다."
}
```

### 2. 노무비 상세 조회
```http
GET /labor-costs/{labor_cost_id}
Authorization: Bearer {token}
```

#### 응답
```json
{
    "status": "success",
    "data": {
        "id": "labor-cost-uuid",
        "contract": {
            "id": "contract-uuid",
            "project_name": "아파트 신축공사",
            "vendor": {
                "id": "vendor-uuid",
                "company_name": "건설회사"
            }
        },
        "worker_name": "김일용",
        "work_date": "2024-03-20",
        "daily_wage": 150000,
        "work_type": "철근공사",
        "work_details": "1층 철근 배근 작업",
        "payment_status": "미지급",
        "created_at": "2024-03-20T10:00:00Z",
        "updated_at": "2024-03-20T15:30:00Z"
    },
    "message": "노무비 정보를 성공적으로 조회했습니다."
}
```

### 3. 노무비 등록
```http
POST /labor-costs
Authorization: Bearer {token}
Content-Type: application/json

{
    "contract_id": "contract-uuid",
    "worker_name": "김일용",
    "work_date": "2024-03-20",
    "daily_wage": 150000,
    "work_type": "철근공사",
    "work_details": "1층 철근 배근 작업"
}
```

#### 응답
```json
{
    "status": "success",
    "data": {
        "id": "labor-cost-uuid",
        "contract": {
            "id": "contract-uuid",
            "project_name": "아파트 신축공사"
        },
        "worker_name": "김일용",
        "work_date": "2024-03-20",
        "daily_wage": 150000,
        "work_type": "철근공사",
        "work_details": "1층 철근 배근 작업",
        "payment_status": "미지급",
        "created_at": "2024-03-20T10:00:00Z"
    },
    "message": "노무비가 성공적으로 등록되었습니다."
}
```

### 4. 노무비 수정
```http
PUT /labor-costs/{labor_cost_id}
Authorization: Bearer {token}
Content-Type: application/json

{
    "daily_wage": 160000,
    "work_details": "1층 철근 배근 작업 수정",
    "payment_status": "지급완료"
}
```

#### 응답
```json
{
    "status": "success",
    "data": {
        "id": "labor-cost-uuid",
        "contract": {
            "id": "contract-uuid",
            "project_name": "아파트 신축공사"
        },
        "worker_name": "김일용",
        "work_date": "2024-03-20",
        "daily_wage": 160000,
        "work_type": "철근공사",
        "work_details": "1층 철근 배근 작업 수정",
        "payment_status": "지급완료",
        "updated_at": "2024-03-20T16:00:00Z"
    },
    "message": "노무비 정보가 성공적으로 수정되었습니다."
}
```

## 에러 코드
- `LABOR_COST_NOT_FOUND`: 노무비를 찾을 수 없음
- `CONTRACT_NOT_FOUND`: 계약을 찾을 수 없음
- `VALIDATION_ERROR`: 입력값 검증 실패
- `PERMISSION_DENIED`: 권한 없음
- `INVALID_PAYMENT_STATUS`: 잘못된 지급 상태

## 요청 제한
- 목록 조회: 토큰당 1초에 30회
- 상세 조회: 토큰당 1초에 30회
- 등록/수정: 토큰당 1분에 10회 