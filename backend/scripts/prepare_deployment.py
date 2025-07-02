#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 배포 준비 스크립트
"""

import os
import sys
import json
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DeploymentPreparer:
    """배포 준비 클래스"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.deployment_dir = self.project_root / "deployment"
        self.backup_dir = self.project_root / "backup"
        self.preparation_results = {}
    
    def create_deployment_structure(self) -> Dict[str, Any]:
        """배포 구조 생성"""
        logger.info("배포 구조 생성 시작")
        
        try:
            # 배포 디렉토리 생성
            self.deployment_dir.mkdir(exist_ok=True)
            
            # 하위 디렉토리 생성
            subdirs = [
                "app",
                "config",
                "logs",
                "data",
                "temp",
                "scripts",
                "tests"
            ]
            
            for subdir in subdirs:
                (self.deployment_dir / subdir).mkdir(exist_ok=True)
            
            # 백업 디렉토리 생성
            self.backup_dir.mkdir(exist_ok=True)
            
            return {
                "status": "SUCCESS",
                "message": "배포 구조 생성 완료",
                "deployment_dir": str(self.deployment_dir),
                "backup_dir": str(self.backup_dir)
            }
            
        except Exception as e:
            return {
                "status": "FAILED",
                "message": "배포 구조 생성 실패",
                "error": str(e)
            }
    
    def copy_application_files(self) -> Dict[str, Any]:
        """애플리케이션 파일 복사"""
        logger.info("애플리케이션 파일 복사 시작")
        
        try:
            # 복사할 디렉토리 및 파일 목록
            copy_items = [
                ("app", "app"),
                ("config", "config"),
                ("scripts", "scripts"),
                ("tests", "tests"),
                ("requirements.txt", "requirements.txt"),
                ("main.py", "main.py"),
                ("alembic.ini", "alembic.ini")
            ]
            
            copied_files = []
            skipped_files = []
            
            for source, dest in copy_items:
                source_path = self.project_root / source
                dest_path = self.deployment_dir / dest
                
                if source_path.exists():
                    if source_path.is_dir():
                        shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
                    else:
                        shutil.copy2(source_path, dest_path)
                    copied_files.append(f"{source} -> {dest}")
                else:
                    skipped_files.append(source)
            
            return {
                "status": "SUCCESS",
                "message": "애플리케이션 파일 복사 완료",
                "copied_files": copied_files,
                "skipped_files": skipped_files
            }
            
        except Exception as e:
            return {
                "status": "FAILED",
                "message": "애플리케이션 파일 복사 실패",
                "error": str(e)
            }
    
    def create_deployment_config(self) -> Dict[str, Any]:
        """배포 설정 파일 생성"""
        logger.info("배포 설정 파일 생성 시작")
        
        try:
            # 환경 설정 파일
            env_config = {
                "DATABASE_URL": "postgresql://postgres:password@localhost:5432/cma_db",
                "REDIS_URL": "redis://localhost:6379",
                "LOG_LEVEL": "INFO",
                "DEBUG": "False",
                "SECRET_KEY": "your-secret-key-here",
                "ALLOWED_HOSTS": "localhost,127.0.0.1",
                "CORS_ORIGINS": "http://localhost:3000,http://127.0.0.1:3000"
            }
            
            env_file = self.deployment_dir / ".env"
            with open(env_file, "w", encoding="utf-8", newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
                for key, value in env_config.items():
                    f.write(f"{key}={value}\n")
            
            # 배포 스크립트
            deployment_script = self.deployment_dir / "deploy.sh"
            with open(deployment_script, "w", encoding="utf-8", newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
                f.write("""#!/bin/bash
# CMA 배포 스크립트

echo "CMA 배포 시작..."

# 가상환경 활성화
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 마이그레이션
alembic upgrade head

# 애플리케이션 시작
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

echo "CMA 배포 완료"
""")
            
            # 실행 권한 부여
            os.chmod(deployment_script, 0o755)
            
            return {
                "status": "SUCCESS",
                "message": "배포 설정 파일 생성 완료",
                "created_files": [
                    ".env",
                    "deploy.sh"
                ]
            }
            
        except Exception as e:
            return {
                "status": "FAILED",
                "message": "배포 설정 파일 생성 실패",
                "error": str(e)
            }
    
    def create_backup(self) -> Dict[str, Any]:
        """현재 상태 백업"""
        logger.info("현재 상태 백업 시작")
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"cma_backup_{timestamp}"
            backup_path = self.backup_dir / backup_name
            
            # 백업 생성
            shutil.make_archive(str(backup_path), 'zip', self.project_root)
            
            return {
                "status": "SUCCESS",
                "message": "백업 생성 완료",
                "backup_file": f"{backup_name}.zip",
                "backup_size": (backup_path.with_suffix('.zip')).stat().st_size
            }
            
        except Exception as e:
            return {
                "status": "FAILED",
                "message": "백업 생성 실패",
                "error": str(e)
            }
    
    def validate_deployment(self) -> Dict[str, Any]:
        """배포 유효성 검사"""
        logger.info("배포 유효성 검사 시작")
        
        try:
            validation_results = {
                "required_files": [],
                "missing_files": [],
                "file_permissions": [],
                "config_validation": []
            }
            
            # 필수 파일 확인
            required_files = [
                "main.py",
                "requirements.txt",
                "app/",
                "config/",
                ".env",
                "deploy.sh"
            ]
            
            for file_path in required_files:
                full_path = self.deployment_dir / file_path
                if full_path.exists():
                    validation_results["required_files"].append(file_path)
                else:
                    validation_results["missing_files"].append(file_path)
            
            # 파일 권한 확인
            deploy_script = self.deployment_dir / "deploy.sh"
            if deploy_script.exists():
                stat = deploy_script.stat()
                if stat.st_mode & 0o111:  # 실행 권한 확인
                    validation_results["file_permissions"].append("deploy.sh: 실행 권한 있음")
                else:
                    validation_results["file_permissions"].append("deploy.sh: 실행 권한 없음")
            
            # 설정 파일 유효성 확인
            env_file = self.deployment_dir / ".env"
            if env_file.exists():
                with open(env_file, "r", encoding="utf-8", newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
                    env_content = f.read()
                    if "DATABASE_URL" in env_content and "REDIS_URL" in env_content:
                        validation_results["config_validation"].append(".env: 필수 설정 포함")
                    else:
                        validation_results["config_validation"].append(".env: 필수 설정 누락")
            
            # 전체 유효성 판단
            is_valid = (
                len(validation_results["missing_files"]) == 0 and
                len(validation_results["required_files"]) > 0
            )
            
            return {
                "status": "SUCCESS" if is_valid else "FAILED",
                "message": "배포 유효성 검사 완료",
                "is_valid": is_valid,
                "validation_results": validation_results
            }
            
        except Exception as e:
            return {
                "status": "FAILED",
                "message": "배포 유효성 검사 실패",
                "error": str(e)
            }
    
    def generate_deployment_report(self) -> Dict[str, Any]:
        """배포 보고서 생성"""
        logger.info("배포 보고서 생성 시작")
        
        try:
            report = {
                "deployment_info": {
                    "timestamp": datetime.now().isoformat(),
                    "deployment_dir": str(self.deployment_dir),
                    "backup_dir": str(self.backup_dir)
                },
                "preparation_results": self.preparation_results,
                "deployment_instructions": [
                    "1. 배포 디렉토리로 이동: cd deployment",
                    "2. 환경 설정 확인: cat .env",
                    "3. 배포 스크립트 실행: ./deploy.sh",
                    "4. 애플리케이션 접속: http://localhost:8000",
                    "5. 로그 확인: tail -f logs/app.log"
                ]
            }
            
            # 보고서 파일 저장
            report_file = self.deployment_dir / "deployment_report.json"
            with open(report_file, "w", encoding="utf-8", newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
                json.dump(report, f, ensure_ascii=False, indent=2, default=str)
            
            return {
                "status": "SUCCESS",
                "message": "배포 보고서 생성 완료",
                "report_file": str(report_file)
            }
            
        except Exception as e:
            return {
                "status": "FAILED",
                "message": "배포 보고서 생성 실패",
                "error": str(e)
            }
    
    def prepare_deployment(self) -> Dict[str, Any]:
        """전체 배포 준비 실행"""
        logger.info("=== CMA 배포 준비 시작 ===")
        
        try:
            # 1. 배포 구조 생성
            logger.info("1. 배포 구조 생성")
            self.preparation_results["structure_creation"] = self.create_deployment_structure()
            
            # 2. 애플리케이션 파일 복사
            logger.info("2. 애플리케이션 파일 복사")
            self.preparation_results["file_copy"] = self.copy_application_files()
            
            # 3. 배포 설정 파일 생성
            logger.info("3. 배포 설정 파일 생성")
            self.preparation_results["config_creation"] = self.create_deployment_config()
            
            # 4. 백업 생성
            logger.info("4. 백업 생성")
            self.preparation_results["backup"] = self.create_backup()
            
            # 5. 배포 유효성 검사
            logger.info("5. 배포 유효성 검사")
            self.preparation_results["validation"] = self.validate_deployment()
            
            # 6. 배포 보고서 생성
            logger.info("6. 배포 보고서 생성")
            self.preparation_results["report"] = self.generate_deployment_report()
            
            logger.info("=== CMA 배포 준비 완료 ===")
            return self.preparation_results
            
        except Exception as e:
            logger.error(f"배포 준비 실패: {e}")
            return {"error": str(e)}


def main():
    """메인 실행 함수"""
    logger.info("CMA 배포 준비 스크립트 시작")
    
    try:
        # 배포 준비 실행
        preparer = DeploymentPreparer()
        results = preparer.prepare_deployment()
        
        # 결과 출력
        print("\n" + "="*60)
        print("CMA 배포 준비 결과")
        print("="*60)
        
        for step_name, step_result in results.items():
            if isinstance(step_result, dict):
                status = step_result.get("status", "UNKNOWN")
                message = step_result.get("message", "No message")
                print(f"{step_name}: {status} - {message}")
                
                if step_name == "validation" and step_result.get("is_valid"):
                    print("  [SUCCESS] 배포 준비가 성공적으로 완료되었습니다!")
                elif step_name == "validation" and not step_result.get("is_valid"):
                    print("  [WARNING] 배포 준비에 문제가 있습니다. 검토가 필요합니다.")
        
        print("="*60)
        
        # 배포 디렉토리 정보
        deployment_dir = Path(__file__).parent.parent / "deployment"
        if deployment_dir.exists():
            print(f"\n배포 디렉토리: {deployment_dir}")
            print("배포를 시작하려면 위 디렉토리로 이동하여 ./deploy.sh를 실행하세요.")
        
        return results
        
    except Exception as e:
        logger.error(f"배포 준비 스크립트 실행 실패: {e}")
        raise


if __name__ == "__main__":
    main() 