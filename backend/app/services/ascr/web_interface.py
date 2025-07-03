#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASCR 웹 인터페이스
브라우저 기반 PDF 처리 관리 인터페이스
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import aiofiles
from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import uvicorn

logger = logging.getLogger(__name__)

# 웹 인터페이스 라우터
router = APIRouter(prefix="/ascr", tags=["ASCR Web Interface"])

# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates/ascr")

class ASCRWebInterface:
    """ASCR 웹 인터페이스 클래스"""
    
    def __init__(self):
        self.template_dir = Path("templates/ascr")
        self.static_dir = Path("static/ascr")
        self.upload_dir = Path("uploads/ascr")
        
        # 디렉토리 생성
        self.template_dir.mkdir(parents=True, exist_ok=True)
        self.static_dir.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    def create_templates(self):
        """HTML 템플릿 생성"""
        # 메인 페이지 템플릿
        main_template = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASCR PDF 처리 시스템</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .upload-area {
            border: 2px dashed #ccc;
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            background-color: #f8f9fa;
            transition: all 0.3s ease;
        }
        .upload-area:hover {
            border-color: #007bff;
            background-color: #e3f2fd;
        }
        .upload-area.dragover {
            border-color: #28a745;
            background-color: #d4edda;
        }
        .progress-bar {
            height: 20px;
            border-radius: 10px;
        }
        .task-card {
            border-left: 4px solid #007bff;
            margin-bottom: 15px;
        }
        .task-card.completed {
            border-left-color: #28a745;
        }
        .task-card.error {
            border-left-color: #dc3545;
        }
        .task-card.processing {
            border-left-color: #ffc107;
        }
        .stats-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="fas fa-file-pdf me-2"></i>
                ASCR PDF 처리 시스템
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="#upload">업로드</a>
                <a class="nav-link" href="#tasks">작업 관리</a>
                <a class="nav-link" href="#stats">통계</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <!-- 통계 카드 -->
        <div class="row mb-4" id="stats">
            <div class="col-md-3">
                <div class="card stats-card">
                    <div class="card-body text-center">
                        <h3 id="total-tasks">0</h3>
                        <p class="mb-0">총 작업</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stats-card">
                    <div class="card-body text-center">
                        <h3 id="completed-tasks">0</h3>
                        <p class="mb-0">완료</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stats-card">
                    <div class="card-body text-center">
                        <h3 id="processing-tasks">0</h3>
                        <p class="mb-0">처리중</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stats-card">
                    <div class="card-body text-center">
                        <h3 id="success-rate">0%</h3>
                        <p class="mb-0">성공률</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- 파일 업로드 섹션 -->
        <div class="row mb-4" id="upload">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-upload me-2"></i>PDF 파일 업로드</h5>
                    </div>
                    <div class="card-body">
                        <form id="upload-form" enctype="multipart/form-data">
                            <div class="upload-area" id="upload-area">
                                <i class="fas fa-cloud-upload-alt fa-3x text-muted mb-3"></i>
                                <h5>PDF 파일을 드래그하거나 클릭하여 업로드</h5>
                                <p class="text-muted">지원 형식: PDF</p>
                                <input type="file" id="pdf-file" name="file" accept=".pdf" class="d-none" multiple>
                                <button type="button" class="btn btn-primary" onclick="document.getElementById('pdf-file').click()">
                                    파일 선택
                                </button>
                            </div>
                            
                            <div class="mt-3">
                                <label class="form-label">처리 타입</label>
                                <select class="form-select" name="processing_type">
                                    <option value="standard">표준 처리</option>
                                    <option value="optimized">최적화 처리</option>
                                    <option value="ml_enhanced">ML 강화 처리</option>
                                </select>
                            </div>
                            
                            <div class="mt-3">
                                <button type="submit" class="btn btn-success">
                                    <i class="fas fa-play me-2"></i>처리 시작
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        <!-- 작업 목록 섹션 -->
        <div class="row" id="tasks">
            <div class="col-12">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5><i class="fas fa-tasks me-2"></i>작업 목록</h5>
                        <button class="btn btn-sm btn-outline-primary" onclick="refreshTasks()">
                            <i class="fas fa-sync-alt me-1"></i>새로고침
                        </button>
                    </div>
                    <div class="card-body">
                        <div id="tasks-list">
                            <!-- 작업 목록이 여기에 동적으로 로드됩니다 -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 모달 -->
    <div class="modal fade" id="taskDetailModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">작업 상세 정보</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body" id="task-detail-content">
                    <!-- 작업 상세 정보가 여기에 로드됩니다 -->
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // 전역 변수
        let currentTasks = [];
        
        // 페이지 로드 시 초기화
        document.addEventListener('DOMContentLoaded', function() {
            loadStats();
            loadTasks();
            setupUploadArea();
            setupForm();
            
            // 5초마다 자동 새로고침
            setInterval(function() {
                loadStats();
                loadTasks();
            }, 5000);
        });
        
        // 업로드 영역 설정
        function setupUploadArea() {
            const uploadArea = document.getElementById('upload-area');
            const fileInput = document.getElementById('pdf-file');
            
            // 드래그 앤 드롭 이벤트
            uploadArea.addEventListener('dragover', function(e) {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });
            
            uploadArea.addEventListener('dragleave', function(e) {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
            });
            
            uploadArea.addEventListener('drop', function(e) {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                fileInput.files = e.dataTransfer.files;
            });
            
            // 파일 선택 이벤트
            fileInput.addEventListener('change', function() {
                if (this.files.length > 0) {
                    uploadArea.innerHTML = `
                        <i class="fas fa-check-circle fa-3x text-success mb-3"></i>
                        <h5>선택된 파일: ${this.files.length}개</h5>
                        <p class="text-muted">처리 시작 버튼을 클릭하세요</p>
                    `;
                }
            });
        }
        
        // 폼 설정
        function setupForm() {
            document.getElementById('upload-form').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const formData = new FormData(this);
                const submitBtn = this.querySelector('button[type="submit"]');
                
                try {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>업로드 중...';
                    
                    const response = await fetch('/api/v1/ascr/upload', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (response.ok) {
                        const result = await response.json();
                        alert('파일 업로드 성공!');
                        loadTasks();
                    } else {
                        throw new Error('업로드 실패');
                    }
                } catch (error) {
                    alert('업로드 중 오류가 발생했습니다: ' + error.message);
                } finally {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<i class="fas fa-play me-2"></i>처리 시작';
                }
            });
        }
        
        // 통계 로드
        async function loadStats() {
            try {
                const response = await fetch('/api/v1/ascr/stats');
                const stats = await response.json();
                
                document.getElementById('total-tasks').textContent = stats.total_tasks;
                document.getElementById('completed-tasks').textContent = stats.completed_tasks;
                document.getElementById('processing-tasks').textContent = stats.pending_tasks;
                document.getElementById('success-rate').textContent = stats.success_rate.toFixed(1) + '%';
            } catch (error) {
                console.error('통계 로드 실패:', error);
            }
        }
        
        // 작업 목록 로드
        async function loadTasks() {
            try {
                const response = await fetch('/api/v1/ascr/tasks');
                currentTasks = await response.json();
                
                const tasksList = document.getElementById('tasks-list');
                tasksList.innerHTML = '';
                
                if (currentTasks.length === 0) {
                    tasksList.innerHTML = '<p class="text-muted text-center">작업이 없습니다.</p>';
                    return;
                }
                
                currentTasks.forEach(task => {
                    const taskCard = createTaskCard(task);
                    tasksList.appendChild(taskCard);
                });
            } catch (error) {
                console.error('작업 목록 로드 실패:', error);
            }
        }
        
        // 작업 카드 생성
        function createTaskCard(task) {
            const card = document.createElement('div');
            card.className = `card task-card ${task.status}`;
            
            const statusIcon = {
                'pending': 'fas fa-clock text-warning',
                'processing': 'fas fa-cog fa-spin text-primary',
                'completed': 'fas fa-check-circle text-success',
                'error': 'fas fa-exclamation-triangle text-danger',
                'cancelled': 'fas fa-ban text-secondary'
            }[task.status] || 'fas fa-question text-muted';
            
            const statusText = {
                'pending': '대기중',
                'processing': '처리중',
                'completed': '완료',
                'error': '오류',
                'cancelled': '취소됨'
            }[task.status] || '알 수 없음';
            
            card.innerHTML = `
                <div class="card-body">
                    <div class="row align-items-center">
                        <div class="col-md-8">
                            <h6 class="card-title mb-1">
                                <i class="${statusIcon} me-2"></i>
                                ${task.task_id}
                            </h6>
                            <p class="card-text text-muted mb-1">
                                상태: ${statusText} | 
                                생성: ${new Date(task.created_at).toLocaleString()}
                            </p>
                            ${task.progress > 0 ? `
                                <div class="progress mb-2" style="height: 8px;">
                                    <div class="progress-bar" style="width: ${task.progress * 100}%"></div>
                                </div>
                            ` : ''}
                        </div>
                        <div class="col-md-4 text-end">
                            <button class="btn btn-sm btn-outline-primary me-2" onclick="viewTaskDetail('${task.task_id}')">
                                <i class="fas fa-eye me-1"></i>상세
                            </button>
                            ${task.status === 'pending' || task.status === 'processing' ? `
                                <button class="btn btn-sm btn-outline-danger" onclick="cancelTask('${task.task_id}')">
                                    <i class="fas fa-times me-1"></i>취소
                                </button>
                            ` : ''}
                        </div>
                    </div>
                </div>
            `;
            
            return card;
        }
        
        // 작업 상세 보기
        async function viewTaskDetail(taskId) {
            try {
                const response = await fetch(`/api/v1/ascr/status/${taskId}`);
                const task = await response.json();
                
                const modal = new bootstrap.Modal(document.getElementById('taskDetailModal'));
                const content = document.getElementById('task-detail-content');
                
                content.innerHTML = `
                    <div class="row">
                        <div class="col-md-6">
                            <h6>기본 정보</h6>
                            <table class="table table-sm">
                                <tr><td>작업 ID</td><td>${task.task_id}</td></tr>
                                <tr><td>상태</td><td>${task.status}</td></tr>
                                <tr><td>진행률</td><td>${(task.progress * 100).toFixed(1)}%</td></tr>
                                <tr><td>생성 시간</td><td>${new Date(task.created_at).toLocaleString()}</td></tr>
                                <tr><td>업데이트 시간</td><td>${new Date(task.updated_at).toLocaleString()}</td></tr>
                            </table>
                        </div>
                        <div class="col-md-6">
                            <h6>결과</h6>
                            <pre class="bg-light p-3 rounded">${JSON.stringify(task.result || {}, null, 2)}</pre>
                        </div>
                    </div>
                    ${task.error ? `
                        <div class="row mt-3">
                            <div class="col-12">
                                <h6 class="text-danger">오류 정보</h6>
                                <div class="alert alert-danger">${task.error}</div>
                            </div>
                        </div>
                    ` : ''}
                `;
                
                modal.show();
            } catch (error) {
                alert('작업 상세 정보 로드 실패: ' + error.message);
            }
        }
        
        // 작업 취소
        async function cancelTask(taskId) {
            if (!confirm('정말로 이 작업을 취소하시겠습니까?')) {
                return;
            }
            
            try {
                const response = await fetch(`/api/v1/ascr/tasks/${taskId}`, {
                    method: 'DELETE'
                });
                
                if (response.ok) {
                    alert('작업이 취소되었습니다.');
                    loadTasks();
                } else {
                    throw new Error('취소 실패');
                }
            } catch (error) {
                alert('작업 취소 실패: ' + error.message);
            }
        }
        
        // 작업 목록 새로고침
        function refreshTasks() {
            loadStats();
            loadTasks();
        }
    </script>
</body>
</html>
        """
        
        # 템플릿 파일 저장
        with open(self.template_dir / "index.html", "w", encoding="utf-8", , encoding=\'utf-8\', , newline='', encoding='utf-8', newline='') as f:
            f.write(main_template)
        
        logger.info("HTML 템플릿 생성 완료")

# 웹 인터페이스 인스턴스
web_interface = ASCRWebInterface()

@router.get("/", response_class=HTMLResponse)
async def ascr_web_interface(request: Request):
    """ASCR 웹 인터페이스 메인 페이지"""
    try:
        # 템플릿이 없으면 생성
        if not (web_interface.template_dir / "index.html").exists():
            web_interface.create_templates()
        
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        logger.error(f"웹 인터페이스 로드 실패: {e}")
        raise HTTPException(status_code=500, detail="웹 인터페이스 로드 실패")

@router.get("/health")
async def web_interface_health():
    """웹 인터페이스 헬스체크"""
    return {
        "status": "healthy",
        "interface": "ASCR Web Interface",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }

# 정적 파일 서빙 (CSS, JS 등)
@router.get("/static/{file_path:path}")
async def serve_static_files(file_path: str):
    """정적 파일 서빙"""
    static_file = web_interface.static_dir / file_path
    
    if not static_file.exists():
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")
    
    return StreamingResponse(
        open(static_file, "rb", encoding=\'utf-8\', , newline='', encoding='utf-8', newline=''),
        media_type="application/octet-stream"
    )

def start_web_interface(host: str = "0.0.0.0", port: int = 8080):
    """웹 인터페이스 서버 시작"""
    try:
        # 템플릿 생성
        web_interface.create_templates()
        
        # 서버 시작
        uvicorn.run(
            "app.services.ascr.web_interface:router",
            host=host,
            port=port,
            reload=True
        )
    except Exception as e:
        logger.error(f"웹 인터페이스 서버 시작 실패: {e}")

if __name__ == "__main__":
    start_web_interface() 