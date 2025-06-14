import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.config import settings
from app.tests.utils.utils import get_superuser_token_headers
from app.tests.utils.notification import create_random_notification
from app.tests.utils.user import create_random_user

client = TestClient(app)

def test_create_notification(
    db: Session, superuser_token_headers: dict
) -> None:
    """알림 생성 테스트"""
    data = {
        "title": "테스트 알림",
        "message": "테스트 알림 메시지",
        "type": "SYSTEM",
        "user_id": create_random_user(db).id,
        "metadata": {
            "key": "value"
        }
    }
    response = client.post(
        f"{settings.API_V1_STR}/notifications/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["message"] == data["message"]
    assert content["type"] == data["type"]
    assert content["user_id"] == data["user_id"]
    assert content["metadata"] == data["metadata"]
    assert "id" in content

def test_read_notification(
    db: Session, superuser_token_headers: dict
) -> None:
    """알림 조회 테스트"""
    notification = create_random_notification(db)
    response = client.get(
        f"{settings.API_V1_STR}/notifications/{notification.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == notification.id
    assert content["title"] == notification.title
    assert content["message"] == notification.message

def test_read_notifications(
    db: Session, superuser_token_headers: dict
) -> None:
    """알림 목록 조회 테스트"""
    notification = create_random_notification(db)
    response = client.get(
        f"{settings.API_V1_STR}/notifications/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["items"]) > 0
    assert content["items"][0]["id"] == notification.id

def test_update_notification(
    db: Session, superuser_token_headers: dict
) -> None:
    """알림 수정 테스트"""
    notification = create_random_notification(db)
    data = {
        "is_read": True
    }
    response = client.put(
        f"{settings.API_V1_STR}/notifications/{notification.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["is_read"] == data["is_read"]

def test_delete_notification(
    db: Session, superuser_token_headers: dict
) -> None:
    """알림 삭제 테스트"""
    notification = create_random_notification(db)
    response = client.delete(
        f"{settings.API_V1_STR}/notifications/{notification.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "알림이 성공적으로 삭제되었습니다."

def test_batch_read_notifications(
    db: Session, superuser_token_headers: dict
) -> None:
    """알림 일괄 읽음 처리 테스트"""
    notification1 = create_random_notification(db)
    notification2 = create_random_notification(db)
    data = {
        "notification_ids": [notification1.id, notification2.id]
    }
    response = client.put(
        f"{settings.API_V1_STR}/notifications/batch/read",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["updated_count"] == 2

def test_batch_delete_notifications(
    db: Session, superuser_token_headers: dict
) -> None:
    """알림 일괄 삭제 테스트"""
    notification1 = create_random_notification(db)
    notification2 = create_random_notification(db)
    data = {
        "notification_ids": [notification1.id, notification2.id]
    }
    response = client.delete(
        f"{settings.API_V1_STR}/notifications/batch",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["deleted_count"] == 2

def test_create_notification_template(
    db: Session, superuser_token_headers: dict
) -> None:
    """알림 템플릿 생성 테스트"""
    data = {
        "name": "테스트 템플릿",
        "content": "{user_name}님이 {project_name} 프로젝트에 할당되었습니다.",
        "category": "PROJECT",
        "variables": ["user_name", "project_name"],
        "is_active": True
    }
    response = client.post(
        f"{settings.API_V1_STR}/notifications/templates",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["content"] == data["content"]
    assert content["category"] == data["category"]
    assert content["variables"] == data["variables"]
    assert content["is_active"] == data["is_active"]

def test_read_notification_templates(
    db: Session, superuser_token_headers: dict
) -> None:
    """알림 템플릿 목록 조회 테스트"""
    response = client.get(
        f"{settings.API_V1_STR}/notifications/templates",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "items" in content

def test_get_notification_statistics(
    db: Session, superuser_token_headers: dict
) -> None:
    """알림 통계 조회 테스트"""
    response = client.get(
        f"{settings.API_V1_STR}/notifications/statistics",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "total_notifications" in content
    assert "unread_count" in content
    assert "notifications_by_type" in content
    assert "recent_notifications" in content

def test_notification_permissions(
    db: Session, superuser_token_headers: dict
) -> None:
    """알림 권한 테스트"""
    # 일반 사용자 토큰 생성
    user = create_random_user(db)
    user_token_headers = {"Authorization": f"Bearer {user.id}"}
    
    # 일반 사용자가 알림 생성 시도
    response = client.post(
        f"{settings.API_V1_STR}/notifications/",
        headers=user_token_headers,
        json={},
    )
    assert response.status_code == 403
    
    # 일반 사용자가 알림 템플릿 생성 시도
    response = client.post(
        f"{settings.API_V1_STR}/notifications/templates",
        headers=user_token_headers,
        json={},
    )
    assert response.status_code == 403 