#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
예외 처리 테스트
"""

import pytest
from src.utils.config.exceptions import (
    ASCRException, PDFProcessingError, ConfigurationError,
    FileOperationError, ValidationError, handle_exception, safe_execute
)

class TestASCRExceptions:
    """ASCR 예외 클래스 테스트"""
    
    def test_basic_exception(self):
        """기본 예외 테스트"""
        exc = ASCRException("테스트 메시지")
        assert str(exc) == "테스트 메시지"
        assert exc.message == "테스트 메시지"
        assert exc.error_code is None
        assert exc.details == {}
    
    def test_exception_with_error_code(self):
        """에러 코드가 있는 예외 테스트"""
        exc = ASCRException("테스트 메시지", "TEST_ERROR")
        assert str(exc) == "[TEST_ERROR] 테스트 메시지"
        assert exc.error_code == "TEST_ERROR"
    
    def test_exception_with_details(self):
        """상세 정보가 있는 예외 테스트"""
        details = {"file": "test.pdf", "line": 10}
        exc = ASCRException("테스트 메시지", "TEST_ERROR", details)
        assert exc.details == details
    
    def test_pdf_processing_error(self):
        """PDF 처리 오류 테스트"""
        exc = PDFProcessingError("PDF 처리 실패", "test.pdf", 5)
        assert exc.error_code == "PDF_PROCESSING_ERROR"
        assert exc.details["pdf_path"] == "test.pdf"
        assert exc.details["page_number"] == 5
    
    def test_configuration_error(self):
        """설정 오류 테스트"""
        exc = ConfigurationError("설정 파일 오류", "config.json", "api_key")
        assert exc.error_code == "CONFIGURATION_ERROR"
        assert exc.details["config_file"] == "config.json"
        assert exc.details["config_key"] == "api_key"
    
    def test_file_operation_error(self):
        """파일 작업 오류 테스트"""
        exc = FileOperationError("파일 읽기 실패", "test.txt", "read")
        assert exc.error_code == "FILE_OPERATION_ERROR"
        assert exc.details["file_path"] == "test.txt"
        assert exc.details["operation"] == "read"
    
    def test_validation_error(self):
        """검증 오류 테스트"""
        exc = ValidationError("잘못된 값", "age", 150)
        assert exc.error_code == "VALIDATION_ERROR"
        assert exc.details["field"] == "age"
        assert exc.details["value"] == 150

class TestExceptionDecorators:
    """예외 처리 데코레이터 테스트"""
    
    def test_handle_exception_success(self):
        """성공적인 함수 실행 테스트"""
        @handle_exception
        def test_func():
            return "success"
        
        result = test_func()
        assert result == "success"
    
    def test_handle_exception_failure(self):
        """실패한 함수 실행 테스트"""
        @handle_exception
        def test_func():
            raise ValueError("테스트 오류")
        
        with pytest.raises(ASCRException) as exc_info:
            test_func()
        
        assert exc_info.value.error_code == "UNEXPECTED_ERROR"
        assert "테스트 오류" in str(exc_info.value)
    
    def test_safe_execute_success(self):
        """안전한 실행 성공 테스트"""
        def test_func():
            return "success"
        
        result, error = safe_execute(test_func)
        assert result == "success"
        assert error is None
    
    def test_safe_execute_failure(self):
        """안전한 실행 실패 테스트"""
        def test_func():
            raise ValueError("테스트 오류")
        
        result, error = safe_execute(test_func)
        assert result is None
        assert isinstance(error, ValueError)
        assert str(error) == "테스트 오류" 