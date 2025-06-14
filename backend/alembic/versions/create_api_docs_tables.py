"""create api docs tables

Revision ID: create_api_docs_tables
Revises: 
Create Date: 2024-03-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'create_api_docs_tables'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # API 문서 테이블 생성
    op.create_table(
        'api_docs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='DRAFT'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('updated_by', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_api_docs_id'), 'api_docs', ['id'], unique=False)

    # 태그 테이블 생성
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_tags_id'), 'tags', ['id'], unique=False)

    # API 문서와 태그의 다대다 관계 테이블 생성
    op.create_table(
        'api_doc_tag',
        sa.Column('api_doc_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['api_doc_id'], ['api_docs.id'], ),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
        sa.PrimaryKeyConstraint('api_doc_id', 'tag_id')
    )

    # API 문서 버전 테이블 생성
    op.create_table(
        'api_doc_versions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('api_doc_id', sa.Integer(), nullable=False),
        sa.Column('version', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('changes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['api_doc_id'], ['api_docs.id'], ),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_api_doc_versions_id'), 'api_doc_versions', ['id'], unique=False)

    # API 문서 댓글 테이블 생성
    op.create_table(
        'api_doc_comments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('api_doc_id', sa.Integer(), nullable=False),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('updated_by', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['api_doc_id'], ['api_docs.id'], ),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['parent_id'], ['api_doc_comments.id'], ),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_api_doc_comments_id'), 'api_doc_comments', ['id'], unique=False)

def downgrade():
    # 테이블 삭제 (역순)
    op.drop_index(op.f('ix_api_doc_comments_id'), table_name='api_doc_comments')
    op.drop_table('api_doc_comments')

    op.drop_index(op.f('ix_api_doc_versions_id'), table_name='api_doc_versions')
    op.drop_table('api_doc_versions')

    op.drop_table('api_doc_tag')

    op.drop_index(op.f('ix_tags_id'), table_name='tags')
    op.drop_table('tags')

    op.drop_index(op.f('ix_api_docs_id'), table_name='api_docs')
    op.drop_table('api_docs') 