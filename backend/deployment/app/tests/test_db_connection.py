from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base

def test_database_connection():
    try:
        print(f"DB URI: {settings.SQLALCHEMY_DATABASE_URI}")
        # 데이터베이스 엔진 생성
        engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
        
        # 연결 테스트
        with engine.connect() as connection:
            print("데이터베이스 연결 성공!")
            
            # 테이블 존재 여부 확인
            # inspector = inspect(engine)
            # tables = inspector.get_table_names()
            # print(f"현재 데이터베이스의 테이블 목록: {tables}")
            
            return True
            
    except Exception as e:
        print(f"데이터베이스 연결 실패: {str(e)}")
        return False

if __name__ == "__main__":
    test_database_connection() 