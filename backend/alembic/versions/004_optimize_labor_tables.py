"""optimize labor tables

Revision ID: 004
Revises: 003
Create Date: 2025-01-23 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    """노무 관리 테이블 최적화"""
    
    # 1. Labor 테이블 인덱스 추가
    op.create_index('ix_labor_worker_name', 'labor', ['worker_name'])
    op.create_index('ix_labor_job_type', 'labor', ['job_type'])
    op.create_index('ix_labor_status', 'labor', ['status'])
    op.create_index('ix_labor_hire_date', 'labor', ['hire_date'])
    op.create_index('ix_labor_contact', 'labor', ['contact'])
    
    # 2. 복합 인덱스 추가 (자주 함께 검색되는 컬럼들)
    op.create_index('ix_labor_job_status', 'labor', ['job_type', 'status'])
    op.create_index('ix_labor_name_contact', 'labor', ['worker_name', 'contact'])
    
    # 3. LaborRecord 테이블 인덱스 추가
    op.create_index('ix_labor_record_worker_id', 'labor_records', ['worker_id'])
    op.create_index('ix_labor_record_date', 'labor_records', ['work_date'])
    op.create_index('ix_labor_record_project_id', 'labor_records', ['project_id'])
    
    # 4. 복합 인덱스 추가
    op.create_index('ix_labor_record_worker_date', 'labor_records', ['worker_id', 'work_date'])
    op.create_index('ix_labor_record_project_date', 'labor_records', ['project_id', 'work_date'])
    
    # 5. 외래키 제약조건 추가 (성능 향상)
    op.create_foreign_key(
        'fk_labor_records_worker_id',
        'labor_records', 'labor',
        ['worker_id'], ['id'],
        ondelete='CASCADE'
    )
    
    op.create_foreign_key(
        'fk_labor_records_project_id',
        'labor_records', 'projects',
        ['project_id'], ['id'],
        ondelete='SET NULL'
    )
    
    # 6. 제약조건 추가
    # 시급은 0보다 커야 함
    op.create_check_constraint(
        'ck_labor_hourly_wage_positive',
        'labor',
        'hourly_wage > 0'
    )
    
    # 근무시간은 0-24시간 범위
    op.create_check_constraint(
        'ck_labor_work_hours_range',
        'labor',
        'work_hours >= 0 AND work_hours <= 24'
    )
    
    # 전화번호 형식 검증
    op.create_check_constraint(
        'ck_labor_contact_format',
        'labor',
        "contact ~ '^01[0-9]-[0-9]{3,4}-[0-9]{4}$'"
    )
    
    # 7. 뷰 생성 (자주 사용되는 복잡한 쿼리)
    op.execute("""
        CREATE VIEW labor_summary_view AS
        SELECT 
            l.id,
            l.worker_name,
            l.job_type,
            l.status,
            l.hourly_wage,
            l.work_hours,
            l.hire_date,
            COUNT(lr.id) as total_records,
            SUM(lr.hours_worked) as total_hours,
            SUM(lr.hours_worked * l.hourly_wage) as total_cost,
            AVG(lr.hours_worked) as avg_hours_per_day
        FROM labor l
        LEFT JOIN labor_records lr ON l.id = lr.worker_id
        GROUP BY l.id, l.worker_name, l.job_type, l.status, l.hourly_wage, l.work_hours, l.hire_date
    """)
    
    # 8. 통계 테이블 생성 (성능 최적화)
    op.create_table(
        'labor_statistics',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('total_workers', sa.Integer(), nullable=False, default=0),
        sa.Column('active_workers', sa.Integer(), nullable=False, default=0),
        sa.Column('total_labor_cost', sa.Float(), nullable=False, default=0.0),
        sa.Column('monthly_labor_cost', sa.Float(), nullable=False, default=0.0),
        sa.Column('average_wage', sa.Float(), nullable=False, default=0.0),
        sa.Column('total_hours', sa.Float(), nullable=False, default=0.0),
        sa.Column('weekly_hours', sa.Float(), nullable=False, default=0.0),
        sa.Column('utilization_rate', sa.Float(), nullable=False, default=0.0),
        sa.Column('last_updated', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    )
    
    # 통계 테이블 인덱스
    op.create_index('ix_labor_statistics_last_updated', 'labor_statistics', ['last_updated'])


def downgrade():
    """롤백"""
    
    # 뷰 삭제
    op.execute("DROP VIEW IF EXISTS labor_summary_view")
    
    # 통계 테이블 삭제
    op.drop_table('labor_statistics')
    
    # 제약조건 삭제
    op.drop_constraint('ck_labor_hourly_wage_positive', 'labor', type_='check')
    op.drop_constraint('ck_labor_work_hours_range', 'labor', type_='check')
    op.drop_constraint('ck_labor_contact_format', 'labor', type_='check')
    
    # 외래키 제약조건 삭제
    op.drop_constraint('fk_labor_records_worker_id', 'labor_records', type_='foreignkey')
    op.drop_constraint('fk_labor_records_project_id', 'labor_records', type_='foreignkey')
    
    # 인덱스 삭제
    op.drop_index('ix_labor_worker_name', table_name='labor')
    op.drop_index('ix_labor_job_type', table_name='labor')
    op.drop_index('ix_labor_status', table_name='labor')
    op.drop_index('ix_labor_hire_date', table_name='labor')
    op.drop_index('ix_labor_contact', table_name='labor')
    op.drop_index('ix_labor_job_status', table_name='labor')
    op.drop_index('ix_labor_name_contact', table_name='labor')
    
    op.drop_index('ix_labor_record_worker_id', table_name='labor_records')
    op.drop_index('ix_labor_record_date', table_name='labor_records')
    op.drop_index('ix_labor_record_project_id', table_name='labor_records')
    op.drop_index('ix_labor_record_worker_date', table_name='labor_records')
    op.drop_index('ix_labor_record_project_date', table_name='labor_records') 