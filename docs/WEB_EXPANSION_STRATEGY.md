# 웹 API 확장 전략

## 🎯 확장 전략 개요

### 목표
PySide6 데스크톱 애플리케이션에서 검증된 비즈니스 로직을 웹 API로 확장하여 하이브리드 아키텍처 완성

### 확장 단계
1. **API 서버 구축**: FastAPI 기반 REST API 개발
2. **공통 로직 통합**: 데스크톱과 웹에서 공유하는 비즈니스 로직
3. **웹 프론트엔드 개발**: React + TypeScript 기반 웹 UI
4. **동기화 시스템**: 데스크톱-웹 간 데이터 동기화

## 🏗️ 아키텍처 설계

### 공통 비즈니스 로직 구조
```
CMA Core Business Logic
├── models/              # SQLAlchemy 모델 (공통)
├── services/            # 비즈니스 로직 (공통)
├── schemas/             # Pydantic 스키마 (공통)
├── utils/               # 유틸리티 함수 (공통)
└── config/              # 설정 관리 (공통)

PySide6 Desktop App
├── ui/                  # PySide6 UI 컴포넌트
├── controllers/         # UI 컨트롤러
└── main.py             # 데스크톱 앱 진입점

Web API (FastAPI)
├── api/                 # API 엔드포인트
├── middleware/          # 미들웨어
└── main.py             # 웹 API 진입점

Web Frontend (React)
├── components/          # React 컴포넌트
├── services/            # API 서비스
└── pages/               # 페이지 컴포넌트
```

## 📋 개발 로드맵

### Phase 2.1: API 서버 구축 (1개월)

#### 2.1.1 FastAPI 기반 API 개발
```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title="CMA API",
    description="Construction Management API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(api_router, prefix="/api/v1")
```

#### 2.1.2 공통 비즈니스 로직 통합
```python
# core/services/contract_service.py (공통)
class ContractService:
    """계약 관리 서비스 - 데스크톱과 웹에서 공유"""
    
    def __init__(self, db_session):
        self.db = db_session
    
    def create_contract(self, contract_data: dict) -> Contract:
        """계약 생성"""
        contract = Contract(**contract_data)
        self.db.add(contract)
        self.db.commit()
        return contract
    
    def get_contracts(self, filters: dict = None) -> List[Contract]:
        """계약 목록 조회"""
        query = self.db.query(Contract)
        if filters:
            # 필터 적용
            pass
        return query.all()

# backend/app/api/v1/endpoints/contracts.py
@router.post("/contracts", response_model=ContractResponse)
async def create_contract(
    contract: ContractCreate,
    service: ContractService = Depends(get_contract_service)
):
    """계약 생성 API"""
    return service.create_contract(contract.dict())

# desktop/controllers/contract_controller.py
class ContractController:
    def __init__(self, service: ContractService):
        self.service = service
    
    def create_contract(self, contract_data: dict):
        """데스크톱에서 계약 생성"""
        return self.service.create_contract(contract_data)
```

### Phase 2.2: 웹 프론트엔드 개발 (1-2개월)

#### 2.2.1 React + TypeScript 기반 UI
```typescript
// frontend/src/components/contract/ContractForm.tsx
import React, { useState } from 'react';
import { TextField, Button, Box, Typography } from '@mui/material';
import { ContractService } from '../../services/contractService';

interface ContractFormProps {
  onSubmit: (contract: ContractCreate) => void;
}

export const ContractForm: React.FC<ContractFormProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    name: '',
    contractNumber: '',
    amount: 0,
    startDate: '',
    endDate: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
      <Typography variant="h6" gutterBottom>
        새 계약 등록
      </Typography>
      
      <TextField
        fullWidth
        label="계약명"
        value={formData.name}
        onChange={(e) => setFormData({...formData, name: e.target.value})}
        required
        margin="normal"
      />
      
      <TextField
        fullWidth
        label="계약번호"
        value={formData.contractNumber}
        onChange={(e) => setFormData({...formData, contractNumber: e.target.value})}
        required
        margin="normal"
      />
      
      <TextField
        fullWidth
        label="계약금액"
        type="number"
        value={formData.amount}
        onChange={(e) => setFormData({...formData, amount: Number(e.target.value)})}
        required
        margin="normal"
      />
      
      <Button type="submit" variant="contained" sx={{ mt: 2 }}>
        계약 등록
      </Button>
    </Box>
  );
};
```

#### 2.2.2 API 서비스 레이어
```typescript
// frontend/src/services/contractService.ts
import { Contract, ContractCreate, ContractUpdate } from '../types/contract';

export class ContractService {
  private static readonly BASE_URL = '/api/v1/contracts';

  static async getContracts(): Promise<Contract[]> {
    const response = await fetch(this.BASE_URL);
    if (!response.ok) {
      throw new Error('계약 목록 조회 실패');
    }
    return response.json();
  }

  static async createContract(contract: ContractCreate): Promise<Contract> {
    const response = await fetch(this.BASE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(contract),
    });
    if (!response.ok) {
      throw new Error('계약 생성 실패');
    }
    return response.json();
  }

  static async updateContract(id: string, contract: ContractUpdate): Promise<Contract> {
    const response = await fetch(`${this.BASE_URL}/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(contract),
    });
    if (!response.ok) {
      throw new Error('계약 수정 실패');
    }
    return response.json();
  }

  static async deleteContract(id: string): Promise<void> {
    const response = await fetch(`${this.BASE_URL}/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('계약 삭제 실패');
    }
  }
}
```

### Phase 2.3: 동기화 시스템 (1개월)

#### 2.3.1 데이터 동기화 전략
```python
# core/sync/sync_manager.py
class SyncManager:
    """데스크톱-웹 간 데이터 동기화 관리자"""
    
    def __init__(self, local_db, web_api_client):
        self.local_db = local_db
        self.web_api = web_api_client
        self.sync_queue = []
    
    def sync_to_web(self):
        """로컬 변경사항을 웹으로 동기화"""
        pending_changes = self.local_db.get_pending_changes()
        
        for change in pending_changes:
            try:
                if change.type == 'CREATE':
                    self.web_api.create(change.resource, change.data)
                elif change.type == 'UPDATE':
                    self.web_api.update(change.resource, change.id, change.data)
                elif change.type == 'DELETE':
                    self.web_api.delete(change.resource, change.id)
                
                # 동기화 완료 표시
                self.local_db.mark_synced(change.id)
                
            except Exception as e:
                # 동기화 실패 시 재시도 큐에 추가
                self.sync_queue.append(change)
    
    def sync_from_web(self):
        """웹에서 로컬로 동기화"""
        try:
            # 웹에서 최신 데이터 가져오기
            web_data = self.web_api.get_all()
            
            # 로컬 데이터와 비교하여 업데이트
            for item in web_data:
                local_item = self.local_db.get_by_id(item.id)
                if not local_item or local_item.updated_at < item.updated_at:
                    self.local_db.update_or_create(item)
                    
        except Exception as e:
            # 오프라인 모드로 전환
            self.enable_offline_mode()
    
    def enable_offline_mode(self):
        """오프라인 모드 활성화"""
        # 로컬 데이터베이스만 사용
        pass
```

#### 2.3.2 실시간 동기화
```python
# core/sync/realtime_sync.py
import asyncio
from datetime import datetime

class RealtimeSync:
    """실시간 동기화 시스템"""
    
    def __init__(self, sync_manager):
        self.sync_manager = sync_manager
        self.is_running = False
    
    async def start_sync(self):
        """실시간 동기화 시작"""
        self.is_running = True
        
        while self.is_running:
            try:
                # 주기적 동기화 (30초마다)
                await self.sync_manager.sync_to_web()
                await self.sync_manager.sync_from_web()
                
                await asyncio.sleep(30)
                
            except Exception as e:
                # 오류 발생 시 재시도 간격 증가
                await asyncio.sleep(60)
    
    def stop_sync(self):
        """실시간 동기화 중지"""
        self.is_running = False
```

## 🛠️ 기술 스택

### 백엔드 API
```python
# requirements_web.txt
fastapi==0.115.12
uvicorn==0.34.3
sqlalchemy==2.0.41
pydantic==2.11.7
alembic==1.16.1
redis==5.2.1
psycopg2-binary==2.9.10
python-multipart==0.0.20
python-jose==3.5.0
passlib==1.7.4
```

### 프론트엔드
```json
// package.json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.8.3",
    "@mui/material": "^5.17.1",
    "@mui/icons-material": "^5.17.1",
    "@emotion/react": "^11.11.0",
    "@emotion/styled": "^11.11.0",
    "react-router-dom": "^6.30.1",
    "axios": "^1.6.0",
    "zustand": "^4.5.7"
  }
}
```

## 📊 개발 우선순위

### High Priority (즉시 개발)
1. **API 서버 구축**
   - FastAPI 기반 REST API
   - 인증/권한 시스템
   - 데이터베이스 연동

2. **공통 비즈니스 로직 통합**
   - 서비스 레이어 분리
   - 모델 공유
   - 유틸리티 함수 통합

3. **기본 웹 UI**
   - 계약 관리 페이지
   - 재무 관리 페이지
   - 노무 관리 페이지

### Medium Priority (2차 개발)
1. **고급 웹 기능**
   - 실시간 업데이트
   - 데이터 시각화
   - 보고서 생성

2. **동기화 시스템**
   - 실시간 동기화
   - 오프라인 지원
   - 충돌 해결

### Low Priority (3차 개발)
1. **고급 기능**
   - 모바일 대응
   - PWA 지원
   - 고급 분석 기능

## 🧪 테스트 전략

### 1. API 테스트
```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_contract():
    """계약 생성 API 테스트"""
    contract_data = {
        "name": "테스트 계약",
        "contract_number": "CON-2024-001",
        "amount": 1000000
    }
    
    response = client.post("/api/v1/contracts", json=contract_data)
    assert response.status_code == 201
    assert response.json()["name"] == "테스트 계약"
```

### 2. 통합 테스트
```python
# tests/test_integration.py
def test_desktop_web_sync():
    """데스크톱-웹 동기화 테스트"""
    # 데스크톱에서 계약 생성
    desktop_contract = desktop_service.create_contract(contract_data)
    
    # 웹으로 동기화
    sync_manager.sync_to_web()
    
    # 웹에서 계약 확인
    web_contracts = web_api.get_contracts()
    assert any(c.id == desktop_contract.id for c in web_contracts)
```

## 🚀 배포 전략

### 1. API 서버 배포
```dockerfile
# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. 웹 프론트엔드 배포
```dockerfile
# frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
EXPOSE 80
```

## 📈 성공 지표

### 1. 개발 효율성
- [ ] API 개발 속도: 기존 대비 1.5배 빠름
- [ ] 코드 재사용률: 80% 이상
- [ ] 버그 발견률: 초기 단계에서 90% 이상 발견

### 2. 사용자 경험
- [ ] 웹 UI 로딩 시간: 2초 이내
- [ ] API 응답 시간: 500ms 이내
- [ ] 동기화 지연 시간: 30초 이내

### 3. 기술적 성과
- [ ] 테스트 커버리지: 85% 이상
- [ ] API 문서 완성도: 100%
- [ ] 보안 취약점: 0개

## 🎯 결론

PySide6 데스크톱 애플리케이션에서 웹 API로 확장하는 전략은 다음과 같은 이점을 제공합니다:

1. **점진적 확장**: 검증된 로직을 기반으로 안전한 확장
2. **코드 재사용**: 공통 비즈니스 로직의 효율적 활용
3. **사용자 접근성**: 웹을 통한 어디서나 접근 가능
4. **확장성**: 클라우드 기반 확장 가능
5. **유지보수성**: 통합된 코드베이스로 유지보수 효율성 향상

이 전략을 통해 CMA 시스템은 데스크톱의 강력함과 웹의 접근성을 모두 갖춘 완전한 하이브리드 솔루션으로 발전할 수 있습니다. 