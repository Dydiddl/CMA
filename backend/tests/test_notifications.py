from typing import Dict
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import random_lower_string
from app.tests.utils.notification import create_random_notification
from app.tests.utils.user import create_random_user

def test_create_notification(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    알림 생성 API 테스트
    """
    data = {
        "title": random_lower_string(),
        "message": random_lower_string(),
        "type": "INFO",
        "priority": "NORMAL",
        "user_id": create_random_user(db).id
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
    assert content["priority"] == data["priority"]
    assert "id" in content

def test_read_notification(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    알림 조회 API 테스트
    """
    notification = create_random_notification(db)
    response = client.get(
        f"{settings.API_V1_STR}/notifications/{notification.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == notification.title
    assert content["id"] == notification.id

def test_read_notifications(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    알림 목록 조회 API 테스트
    """
    create_random_notification(db)
    create_random_notification(db)
    response = client.get(
        f"{settings.API_V1_STR}/notifications/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) >= 2

def test_update_notification(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    알림 수정 API 테스트
    """
    notification = create_random_notification(db)
    data = {
        "title": random_lower_string(),
        "message": random_lower_string(),
        "is_read": True
    }
    response = client.put(
        f"{settings.API_V1_STR}/notifications/{notification.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["message"] == data["message"]
    assert content["is_read"] == data["is_read"]
    assert content["id"] == notification.id

def test_delete_notification(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    알림 삭제 API 테스트
    """
    notification = create_random_notification(db)
    response = client.delete(
        f"{settings.API_V1_STR}/notifications/{notification.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["status"] == "success"

def test_create_notification_template(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    알림 템플릿 생성 API 테스트
    """
    data = {
        "name": random_lower_string(),
        "description": random_lower_string(),
        "template_type": "EMAIL",
        "content": random_lower_string(),
        "variables": ["user_name", "project_name"],
        "category": "SYSTEM"
    }
    response = client.post(
        f"{settings.API_V1_STR}/notifications/templates",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["template_type"] == data["template_type"]
    assert content["category"] == data["category"]
    assert "id" in content

def test_get_notification_stats(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    알림 통계 API 테스트
    """
    response = client.get(
        f"{settings.API_V1_STR}/notifications/statistics",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "total_notifications" in content
    assert "unread_notifications" in content
    assert "notifications_by_type" in content

def test_notification_permissions(
    client: TestClient, normal_user_token_headers: Dict[str, str], db: Session
) -> None:
    """
    알림 API 권한 테스트
    """
    notification = create_random_notification(db)
    
    # 조회 권한 테스트
    response = client.get(
        f"{settings.API_V1_STR}/notifications/{notification.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 403
    
    # 수정 권한 테스트
    data = {"title": random_lower_string()}
    response = client.put(
        f"{settings.API_V1_STR}/notifications/{notification.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 403
    
    # 삭제 권한 테스트
    response = client.delete(
        f"{settings.API_V1_STR}/notifications/{notification.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 403 