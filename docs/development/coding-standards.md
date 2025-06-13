# 코딩 표준

## 1. 일반적인 원칙

### 1.1 코드 스타일
- 일관된 들여쓰기 사용 (백엔드: 4칸, 프론트엔드: 2칸)
- 의미 있는 변수명과 함수명 사용
- 주석은 필요한 경우에만 작성
- 한 줄의 길이는 100자 이내로 유지

### 1.2 파일 구조
- 관련 파일들은 같은 디렉토리에 위치
- 파일명은 소문자와 하이픈 사용 (예: `user-service.ts`)
- 컴포넌트 파일은 PascalCase 사용 (예: `UserProfile.tsx`)

## 2. 백엔드 (Python)

### 2.1 코드 스타일
- PEP 8 준수
- Black 포맷터 사용
- Flake8 린터 사용

### 2.2 네이밍 컨벤션
```python
# 변수명: snake_case
user_name = "홍길동"

# 함수명: snake_case
def get_user_profile():
    pass

# 클래스명: PascalCase
class UserService:
    pass

# 상수: UPPER_SNAKE_CASE
MAX_RETRY_COUNT = 3
```

### 2.3 주석
```python
def calculate_total_amount(items: List[Item]) -> float:
    """
    주어진 아이템 리스트의 총 금액을 계산합니다.

    Args:
        items (List[Item]): 계산할 아이템 리스트

    Returns:
        float: 계산된 총 금액

    Raises:
        ValueError: 아이템 리스트가 비어있는 경우
    """
    if not items:
        raise ValueError("아이템 리스트가 비어있습니다.")
    return sum(item.price for item in items)
```

## 3. 프론트엔드 (TypeScript/React)

### 3.1 코드 스타일
- ESLint 규칙 준수
- Prettier 포맷터 사용
- TypeScript strict 모드 사용

### 3.2 네이밍 컨벤션
```typescript
// 변수명: camelCase
const userName = "홍길동";

// 함수명: camelCase
function getUserProfile() {
    // ...
}

// 컴포넌트명: PascalCase
const UserProfile: React.FC = () => {
    // ...
};

// 인터페이스명: PascalCase
interface UserData {
    id: string;
    name: string;
}

// 타입명: PascalCase
type UserRole = "admin" | "user";
```

### 3.3 컴포넌트 구조
```typescript
// 컴포넌트 파일 구조
import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { UserService } from '@/services';
import { UserCard } from '@/components';
import type { User } from '@/types';

interface UserListProps {
    role?: string;
}

export const UserList: React.FC<UserListProps> = ({ role }) => {
    const { data, isLoading } = useQuery(['users', role], () => 
        UserService.getUsers(role)
    );

    if (isLoading) return <div>로딩 중...</div>;

    return (
        <div className="user-list">
            {data?.map(user => (
                <UserCard key={user.id} user={user} />
            ))}
        </div>
    );
};
```

## 4. Git 커밋 메시지

### 4.1 커밋 메시지 형식
```
<type>: <subject>

<body>

<footer>
```

### 4.2 타입 종류
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포맷팅
- `refactor`: 코드 리팩토링
- `test`: 테스트 코드
- `chore`: 빌드 프로세스 수정

### 4.3 예시
```
feat: 사용자 인증 기능 추가

- JWT 기반 인증 구현
- 로그인/로그아웃 기능 추가
- 토큰 갱신 기능 구현

Resolves: #123
```

## 5. 테스트 코드

### 5.1 백엔드 테스트
```python
def test_calculate_total_amount():
    # Given
    items = [
        Item(price=1000),
        Item(price=2000),
        Item(price=3000)
    ]

    # When
    total = calculate_total_amount(items)

    # Then
    assert total == 6000
```

### 5.2 프론트엔드 테스트
```typescript
describe('UserList', () => {
    it('should render user cards', () => {
        // Given
        const users = [
            { id: '1', name: '홍길동' },
            { id: '2', name: '김철수' }
        ];

        // When
        render(<UserList users={users} />);

        // Then
        expect(screen.getByText('홍길동')).toBeInTheDocument();
        expect(screen.getByText('김철수')).toBeInTheDocument();
    });
});
```

## 6. 보안 가이드라인

### 6.1 백엔드
- 민감 정보는 환경 변수로 관리
- SQL Injection 방지
- XSS 방지
- CSRF 토큰 사용

### 6.2 프론트엔드
- API 키는 환경 변수로 관리
- 입력값 검증
- XSS 방지
- CORS 설정

## 7. 성능 최적화

### 7.1 백엔드
- 데이터베이스 인덱스 사용
- 캐싱 전략 수립
- N+1 문제 해결

### 7.2 프론트엔드
- 컴포넌트 메모이제이션
- 이미지 최적화
- 코드 스플리팅
- 레이지 로딩 