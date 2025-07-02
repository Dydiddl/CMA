#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASCR 고급 로깅 시스템
구조화된 로깅 및 성능 모니터링
"""

import logging
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from contextlib import contextmanager
import threading
from dataclasses import dataclass, asdict
from enum import Enum

class LogLevel(Enum):
    """로그 레벨 열거형"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

@dataclass
class LogContext:
    """로그 컨텍스트 데이터 클래스"""
    operation: str
    file_path: Optional[str] = None
    page_number: Optional[int] = None
    memory_usage: Optional[float] = None
    processing_time: Optional[float] = None
    error_code: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class StructuredFormatter(logging.Formatter):
    """구조화된 로그 포매터"""
    
    def format(self, record):
        """로그 레코드 포매팅"""
        # 기본 로그 정보
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # 추가 컨텍스트 정보
        if hasattr(record, 'context'):
            log_entry.update(asdict(record.context))
        
        # 예외 정보
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry, ensure_ascii=False)

class PerformanceMonitor:
    """성능 모니터링 클래스"""
    
    def __init__(self):
        self.operation_times = {}
        self.memory_usage = {}
        self.error_counts = {}
        self._lock = threading.Lock()
    
    def record_operation(self, operation: str, duration: float, memory_usage: float = None):
        """작업 성능 기록"""
        with self._lock:
            if operation not in self.operation_times:
                self.operation_times[operation] = []
                self.memory_usage[operation] = []
            
            self.operation_times[operation].append(duration)
            if memory_usage:
                self.memory_usage[operation].append(memory_usage)
    
    def record_error(self, operation: str, error_type: str):
        """오류 기록"""
        with self._lock:
            if operation not in self.error_counts:
                self.error_counts[operation] = {}
            
            if error_type not in self.error_counts[operation]:
                self.error_counts[operation][error_type] = 0
            
            self.error_counts[operation][error_type] += 1
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """성능 요약 반환"""
        with self._lock:
            summary = {
                "operations": {},
                "errors": self.error_counts.copy()
            }
            
            for operation, times in self.operation_times.items():
                if times:
                    summary["operations"][operation] = {
                        "count": len(times),
                        "avg_time": sum(times) / len(times),
                        "min_time": min(times),
                        "max_time": max(times),
                        "total_time": sum(times)
                    }
                
                if operation in self.memory_usage and self.memory_usage[operation]:
                    memory_times = self.memory_usage[operation]
                    summary["operations"][operation]["memory"] = {
                        "avg_usage": sum(memory_times) / len(memory_times),
                        "max_usage": max(memory_times)
                    }
            
            return summary

class AdvancedLogger:
    """고급 로거 클래스"""
    
    def __init__(self, name: str, log_dir: Path = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # 성능 모니터
        self.performance_monitor = PerformanceMonitor()
        
        # 로그 디렉토리 설정
        if log_dir is None:
            log_dir = Path("logs")
        
        log_dir.mkdir(exist_ok=True)
        
        # 파일 핸들러 설정
        self._setup_file_handlers(log_dir)
        
        # 콘솔 핸들러 설정
        self._setup_console_handler()
    
    def _setup_file_handlers(self, log_dir: Path):
        """파일 핸들러 설정"""
        # 일반 로그 파일
        general_handler = logging.FileHandler(
            log_dir / "ascr_general.log",
            encoding='utf-8'
        )
        general_handler.setLevel(logging.INFO)
        general_handler.setFormatter(StructuredFormatter())
        
        # 오류 로그 파일
        error_handler = logging.FileHandler(
            log_dir / "ascr_errors.log",
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(StructuredFormatter())
        
        # 성능 로그 파일
        performance_handler = logging.FileHandler(
            log_dir / "ascr_performance.log",
            encoding='utf-8'
        )
        performance_handler.setLevel(logging.INFO)
        performance_handler.setFormatter(StructuredFormatter())
        
        # 핸들러 추가
        self.logger.addHandler(general_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(performance_handler)
    
    def _setup_console_handler(self):
        """콘솔 핸들러 설정"""
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 콘솔용 간단한 포매터
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(console_handler)
    
    def log_with_context(self, level: LogLevel, message: str, context: LogContext):
        """컨텍스트와 함께 로그 기록"""
        record = self.logger.makeRecord(
            self.logger.name, level.value, "", 0, message, (), None
        )
        record.context = context
        self.logger.handle(record)
    
    @contextmanager
    def operation_context(self, operation: str, file_path: str = None, user_id: str = None):
        """작업 컨텍스트 매니저"""
        start_time = time.time()
        session_id = f"session_{int(start_time)}"
        
        context = LogContext(
            operation=operation,
            file_path=file_path,
            user_id=user_id,
            session_id=session_id
        )
        
        try:
            self.log_with_context(LogLevel.INFO, f"작업 시작: {operation}", context)
            yield context
        except Exception as e:
            context.error_code = type(e).__name__
            self.log_with_context(LogLevel.ERROR, f"작업 실패: {operation} - {e}", context)
            self.performance_monitor.record_error(operation, type(e).__name__)
            raise
        finally:
            duration = time.time() - start_time
            context.processing_time = duration
            self.log_with_context(LogLevel.INFO, f"작업 완료: {operation} (소요시간: {duration:.2f}초)", context)
            self.performance_monitor.record_operation(operation, duration)
    
    def log_pdf_processing(self, pdf_path: str, page_count: int, processing_time: float):
        """PDF 처리 로그"""
        context = LogContext(
            operation="pdf_processing",
            file_path=pdf_path,
            processing_time=processing_time
        )
        
        self.log_with_context(
            LogLevel.INFO,
            f"PDF 처리 완료: {pdf_path} (페이지: {page_count}, 소요시간: {processing_time:.2f}초)",
            context
        )
    
    def log_memory_usage(self, operation: str, memory_mb: float):
        """메모리 사용량 로그"""
        context = LogContext(
            operation=operation,
            memory_usage=memory_mb
        )
        
        self.log_with_context(
            LogLevel.INFO,
            f"메모리 사용량: {operation} - {memory_mb:.1f}MB",
            context
        )
    
    def log_error_with_context(self, error: Exception, operation: str, context_data: Dict[str, Any] = None):
        """컨텍스트와 함께 오류 로그"""
        context = LogContext(
            operation=operation,
            error_code=type(error).__name__
        )
        
        if context_data:
            for key, value in context_data.items():
                setattr(context, key, value)
        
        self.log_with_context(
            LogLevel.ERROR,
            f"오류 발생: {operation} - {str(error)}",
            context
        )
        
        self.performance_monitor.record_error(operation, type(error).__name__)
    
    def get_performance_report(self) -> Dict[str, Any]:
        """성능 보고서 생성"""
        summary = self.performance_monitor.get_performance_summary()
        
        # 성능 통계 계산
        total_operations = sum(op["count"] for op in summary["operations"].values())
        total_errors = sum(sum(errors.values()) for errors in summary["errors"].values())
        
        report = {
            "summary": {
                "total_operations": total_operations,
                "total_errors": total_errors,
                "success_rate": (total_operations - total_errors) / total_operations * 100 if total_operations > 0 else 0
            },
            "operations": summary["operations"],
            "errors": summary["errors"],
            "generated_at": datetime.now().isoformat()
        }
        
        return report
    
    def save_performance_report(self, output_path: Path):
        """성능 보고서 저장"""
        report = self.get_performance_report()
        
        with open(output_path, 'w', encoding='utf-8', newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        self.log_with_context(
            LogLevel.INFO,
            f"성능 보고서 저장: {output_path}",
            LogContext(operation="performance_report_save")
        )

# 사용 예시
def main():
    """고급 로거 사용 예시"""
    logger = AdvancedLogger("ASCR_Processor")
    
    # 작업 컨텍스트 사용
    with logger.operation_context("PDF_분할", "test.pdf", "user123") as context:
        # PDF 처리 시뮬레이션
        time.sleep(1)
        context.page_number = 10
        
        # 메모리 사용량 로그
        logger.log_memory_usage("PDF_분할", 256.5)
        
        # 오류 발생 시뮬레이션
        # raise Exception("테스트 오류")
    
    # 성능 보고서 생성
    report = logger.get_performance_report()
    print("성능 보고서:", json.dumps(report, ensure_ascii=False, indent=2))
    
    # 보고서 저장
    logger.save_performance_report(Path("performance_report.json"))

if __name__ == "__main__":
    main() 