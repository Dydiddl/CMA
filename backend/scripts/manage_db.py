import argparse
import sys
from pathlib import Path
import time
from app.core.database import (
    backup_database,
    optimize_database,
    monitor_database_status,
    init_db
)
from app.core.local_postgres import (
    backup_database as pg_backup,
    restore_database as pg_restore,
    optimize_database as pg_optimize
)

def main():
    parser = argparse.ArgumentParser(description="데이터베이스 관리 스크립트")
    parser.add_argument("--type", choices=["sqlite", "postgresql"], default="sqlite",
                      help="데이터베이스 타입 (기본값: sqlite)")
    parser.add_argument("--action", choices=["backup", "restore", "optimize", "monitor", "init"],
                      required=True, help="수행할 작업")
    parser.add_argument("--backup-file", help="복원할 백업 파일 경로")
    
    args = parser.parse_args()
    
    try:
        if args.type == "sqlite":
            if args.action == "backup":
                backup_database()
            elif args.action == "optimize":
                optimize_database()
            elif args.action == "monitor":
                monitor_database_status()
            elif args.action == "init":
                init_db()
            else:
                print("SQLite에서는 복원 기능을 지원하지 않습니다.")
        
        elif args.type == "postgresql":
            if args.action == "backup":
                pg_backup()
            elif args.action == "restore":
                if not args.backup_file:
                    print("복원할 백업 파일을 지정해주세요.")
                    sys.exit(1)
                pg_restore(args.backup_file)
            elif args.action == "optimize":
                pg_optimize()
            elif args.action == "init":
                init_db()
            else:
                print("PostgreSQL에서는 모니터링 기능을 지원하지 않습니다.")
    
    except Exception as e:
        print(f"오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 