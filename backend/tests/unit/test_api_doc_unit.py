import pytest
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.api_doc import ApiDoc, ApiDocVersion, ApiDocComment
from app.schemas.api_doc import ApiDocCreate, ApiDocUpdate, ApiDocVersionCreate
from app.crud.api_doc import (
    create_api_doc,
    get_api_doc,
    get_api_docs,
    update_api_doc,
    delete_api_doc,
    create_api_doc_version,
    get_api_doc_versions,
    add_api_doc_tags,
    create_api_doc_comment,
    get_api_doc_comments,
    get_api_doc_statistics
)

def test_create_api_doc(db: Session) -> None:
    """API 문서 생성 유닛 테스트"""
    # 1. 테스트 데이터 준비
    doc_data = ApiDocCreate(
        title="유닛 테스트 API 문서",
        description="API 문서 유닛 테스트를 위한 문서",
        content="# 유닛 테스트\n\n## 개요\n이 문서는...",
        category="TEST",
        tags=["test", "unit"]
    )
    
    # 2. API 문서 생성
    doc = create_api_doc(db, doc_data)
    
    # 3. 생성된 문서 검증
    assert doc.title == doc_data.title
    assert doc.description == doc_data.description
    assert doc.content == doc_data.content
    assert doc.category == doc_data.category
    assert doc.tags == doc_data.tags
    assert doc.status == "DRAFT"
    assert doc.created_at is not None
    assert doc.updated_at is not None

def test_get_api_doc(db: Session) -> None:
    """API 문서 조회 유닛 테스트"""
    # 1. 테스트 데이터 생성
    doc_data = ApiDocCreate(
        title="조회 테스트 API 문서",
        description="API 문서 조회 테스트를 위한 문서",
        content="# 조회 테스트",
        category="TEST",
        tags=["test", "unit"]
    )
    doc = create_api_doc(db, doc_data)
    
    # 2. API 문서 조회
    retrieved_doc = get_api_doc(db, doc.id)
    
    # 3. 조회된 문서 검증
    assert retrieved_doc is not None
    assert retrieved_doc.id == doc.id
    assert retrieved_doc.title == doc.title
    assert retrieved_doc.description == doc.description

def test_get_api_docs(db: Session) -> None:
    """API 문서 목록 조회 유닛 테스트"""
    # 1. 테스트 데이터 생성
    for i in range(3):
        doc_data = ApiDocCreate(
            title=f"목록 테스트 API 문서 {i}",
            description=f"API 문서 목록 테스트를 위한 문서 {i}",
            content=f"# 목록 테스트 {i}",
            category="TEST",
            tags=["test", "unit"]
        )
        create_api_doc(db, doc_data)
    
    # 2. API 문서 목록 조회
    docs = get_api_docs(db, skip=0, limit=10)
    
    # 3. 조회된 목록 검증
    assert len(docs) >= 3
    assert all(isinstance(doc, ApiDoc) for doc in docs)

def test_update_api_doc(db: Session) -> None:
    """API 문서 수정 유닛 테스트"""
    # 1. 테스트 데이터 생성
    doc_data = ApiDocCreate(
        title="수정 테스트 API 문서",
        description="API 문서 수정 테스트를 위한 문서",
        content="# 수정 테스트",
        category="TEST",
        tags=["test", "unit"]
    )
    doc = create_api_doc(db, doc_data)
    
    # 2. API 문서 수정
    update_data = ApiDocUpdate(
        title="수정된 API 문서",
        description="수정된 설명",
        content="# 수정된 내용",
        category="TEST",
        tags=["test", "unit", "updated"]
    )
    updated_doc = update_api_doc(db, doc.id, update_data)
    
    # 3. 수정된 문서 검증
    assert updated_doc.title == update_data.title
    assert updated_doc.description == update_data.description
    assert updated_doc.content == update_data.content
    assert updated_doc.tags == update_data.tags
    assert updated_doc.updated_at > doc.created_at

def test_delete_api_doc(db: Session) -> None:
    """API 문서 삭제 유닛 테스트"""
    # 1. 테스트 데이터 생성
    doc_data = ApiDocCreate(
        title="삭제 테스트 API 문서",
        description="API 문서 삭제 테스트를 위한 문서",
        content="# 삭제 테스트",
        category="TEST",
        tags=["test", "unit"]
    )
    doc = create_api_doc(db, doc_data)
    
    # 2. API 문서 삭제
    delete_api_doc(db, doc.id)
    
    # 3. 삭제된 문서 조회 시도
    deleted_doc = get_api_doc(db, doc.id)
    assert deleted_doc is None

def test_create_api_doc_version(db: Session) -> None:
    """API 문서 버전 생성 유닛 테스트"""
    # 1. 테스트 데이터 생성
    doc_data = ApiDocCreate(
        title="버전 테스트 API 문서",
        description="API 문서 버전 테스트를 위한 문서",
        content="# 버전 테스트",
        category="TEST",
        tags=["test", "unit"]
    )
    doc = create_api_doc(db, doc_data)
    
    # 2. API 문서 버전 생성
    version_data = ApiDocVersionCreate(
        version="1.1.0",
        content="# 버전 1.1.0 내용",
        changes="내용 업데이트"
    )
    version = create_api_doc_version(db, doc.id, version_data)
    
    # 3. 생성된 버전 검증
    assert version.version == version_data.version
    assert version.content == version_data.content
    assert version.changes == version_data.changes
    assert version.api_doc_id == doc.id
    assert version.created_at is not None

def test_get_api_doc_versions(db: Session) -> None:
    """API 문서 버전 목록 조회 유닛 테스트"""
    # 1. 테스트 데이터 생성
    doc_data = ApiDocCreate(
        title="버전 목록 테스트 API 문서",
        description="API 문서 버전 목록 테스트를 위한 문서",
        content="# 버전 목록 테스트",
        category="TEST",
        tags=["test", "unit"]
    )
    doc = create_api_doc(db, doc_data)
    
    # 2. 여러 버전 생성
    versions = []
    for i in range(3):
        version_data = ApiDocVersionCreate(
            version=f"1.{i}.0",
            content=f"# 버전 1.{i}.0 내용",
            changes=f"버전 1.{i}.0 변경사항"
        )
        version = create_api_doc_version(db, doc.id, version_data)
        versions.append(version)
    
    # 3. 버전 목록 조회
    retrieved_versions = get_api_doc_versions(db, doc.id)
    
    # 4. 조회된 버전 목록 검증
    assert len(retrieved_versions) == 3
    assert all(isinstance(version, ApiDocVersion) for version in retrieved_versions)
    assert all(version.api_doc_id == doc.id for version in retrieved_versions)

def test_add_api_doc_tags(db: Session) -> None:
    """API 문서 태그 추가 유닛 테스트"""
    # 1. 테스트 데이터 생성
    doc_data = ApiDocCreate(
        title="태그 테스트 API 문서",
        description="API 문서 태그 테스트를 위한 문서",
        content="# 태그 테스트",
        category="TEST",
        tags=["test", "unit"]
    )
    doc = create_api_doc(db, doc_data)
    
    # 2. 태그 추가
    new_tags = ["new-tag", "another-tag"]
    updated_doc = add_api_doc_tags(db, doc.id, new_tags)
    
    # 3. 추가된 태그 검증
    assert all(tag in updated_doc.tags for tag in new_tags)
    assert len(updated_doc.tags) == len(doc.tags) + len(new_tags)

def test_create_api_doc_comment(db: Session) -> None:
    """API 문서 댓글 생성 유닛 테스트"""
    # 1. 테스트 데이터 생성
    doc_data = ApiDocCreate(
        title="댓글 테스트 API 문서",
        description="API 문서 댓글 테스트를 위한 문서",
        content="# 댓글 테스트",
        category="TEST",
        tags=["test", "unit"]
    )
    doc = create_api_doc(db, doc_data)
    
    # 2. 댓글 생성
    comment_content = "테스트 댓글입니다."
    comment = create_api_doc_comment(db, doc.id, comment_content)
    
    # 3. 생성된 댓글 검증
    assert comment.content == comment_content
    assert comment.api_doc_id == doc.id
    assert comment.parent_id is None
    assert comment.created_at is not None

def test_get_api_doc_comments(db: Session) -> None:
    """API 문서 댓글 목록 조회 유닛 테스트"""
    # 1. 테스트 데이터 생성
    doc_data = ApiDocCreate(
        title="댓글 목록 테스트 API 문서",
        description="API 문서 댓글 목록 테스트를 위한 문서",
        content="# 댓글 목록 테스트",
        category="TEST",
        tags=["test", "unit"]
    )
    doc = create_api_doc(db, doc_data)
    
    # 2. 여러 댓글 생성
    comments = []
    for i in range(3):
        comment = create_api_doc_comment(db, doc.id, f"테스트 댓글 {i}")
        comments.append(comment)
    
    # 3. 댓글 목록 조회
    retrieved_comments = get_api_doc_comments(db, doc.id)
    
    # 4. 조회된 댓글 목록 검증
    assert len(retrieved_comments) == 3
    assert all(isinstance(comment, ApiDocComment) for comment in retrieved_comments)
    assert all(comment.api_doc_id == doc.id for comment in retrieved_comments)

def test_get_api_doc_statistics(db: Session) -> None:
    """API 문서 통계 조회 유닛 테스트"""
    # 1. 테스트 데이터 생성
    categories = ["TEST", "USER", "PROJECT"]
    for category in categories:
        doc_data = ApiDocCreate(
            title=f"{category} API 문서",
            description=f"{category} API 문서 테스트",
            content=f"# {category} API 문서",
            category=category,
            tags=["test", "unit"]
        )
        doc = create_api_doc(db, doc_data)
        # 각 문서에 댓글 추가
        create_api_doc_comment(db, doc.id, "테스트 댓글")
    
    # 2. 통계 정보 조회
    stats = get_api_doc_statistics(db)
    
    # 3. 통계 정보 검증
    assert stats["total_docs"] >= 3
    assert "docs_by_category" in stats
    assert "docs_by_status" in stats
    assert "recent_updates" in stats
    assert len(stats["docs_by_category"]) >= 3
    assert len(stats["recent_updates"]) > 0 