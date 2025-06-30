#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
성능 모니터링 API 엔드포인트
시스템 성능 지표, 알림, 통계 등을 제공
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any, List
import logging

from ....middleware.performance import performance_monitor
from ....core.auth import get_current_user
from ....models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/metrics")
async def get_performance_metrics(current_user: User = Depends(get_current_user)):
    """현재 성능 지표 조회"""
    try:
        metrics = performance_monitor.get_metrics()
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "성능 지표를 성공적으로 조회했습니다.",
                "data": metrics
            }
        )
    except Exception as e:
        logger.error(f"성능 지표 조회 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"성능 지표 조회 실패: {str(e)}")

@router.get("/alerts")
async def get_performance_alerts(current_user: User = Depends(get_current_user)):
    """성능 알림 목록 조회"""
    try:
        alerts = performance_monitor.get_alerts()
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "성능 알림을 성공적으로 조회했습니다.",
                "data": alerts
            }
        )
    except Exception as e:
        logger.error(f"성능 알림 조회 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"성능 알림 조회 실패: {str(e)}")

@router.get("/health")
async def get_system_health(current_user: User = Depends(get_current_user)):
    """시스템 건강 상태 조회"""
    try:
        metrics = performance_monitor.get_metrics()
        
        # 건강 상태 판단
        health_status = "healthy"
        warnings = []
        
        if metrics.get('cpu_usage', 0) > 80:
            health_status = "warning"
            warnings.append("CPU 사용률이 높습니다")
        
        if metrics.get('memory_usage', 0) > 85:
            health_status = "warning"
            warnings.append("메모리 사용률이 높습니다")
        
        if metrics.get('disk_usage', 0) > 90:
            health_status = "critical"
            warnings.append("디스크 사용률이 매우 높습니다")
        
        health_data = {
            "status": health_status,
            "metrics": metrics,
            "warnings": warnings,
            "timestamp": metrics.get('timestamp', 0)
        }
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "시스템 건강 상태를 성공적으로 조회했습니다.",
                "data": health_data
            }
        )
    except Exception as e:
        logger.error(f"시스템 건강 상태 조회 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"시스템 건강 상태 조회 실패: {str(e)}")

@router.post("/thresholds")
async def update_performance_thresholds(
    thresholds: Dict[str, float],
    current_user: User = Depends(get_current_user)
):
    """성능 임계값 업데이트"""
    try:
        # 임계값 업데이트
        for key, value in thresholds.items():
            if key in performance_monitor.performance_thresholds:
                performance_monitor.performance_thresholds[key] = value
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "성능 임계값이 성공적으로 업데이트되었습니다.",
                "data": performance_monitor.performance_thresholds
            }
        )
    except Exception as e:
        logger.error(f"성능 임계값 업데이트 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"성능 임계값 업데이트 실패: {str(e)}")

@router.delete("/alerts")
async def clear_performance_alerts(current_user: User = Depends(get_current_user)):
    """성능 알림 초기화"""
    try:
        performance_monitor.alerts.clear()
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "성능 알림이 성공적으로 초기화되었습니다."
            }
        )
    except Exception as e:
        logger.error(f"성능 알림 초기화 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"성능 알림 초기화 실패: {str(e)}")

@router.get("/stats")
async def get_performance_stats(current_user: User = Depends(get_current_user)):
    """성능 통계 조회"""
    try:
        # 성능 통계 계산
        metrics = performance_monitor.get_metrics()
        alerts = performance_monitor.get_alerts()
        
        stats = {
            "current_metrics": metrics,
            "alert_count": len(alerts),
            "recent_alerts": alerts[-10:] if alerts else [],  # 최근 10개 알림
            "system_status": "normal"
        }
        
        # 시스템 상태 판단
        if metrics.get('cpu_usage', 0) > 90 or metrics.get('memory_usage', 0) > 95:
            stats["system_status"] = "critical"
        elif metrics.get('cpu_usage', 0) > 80 or metrics.get('memory_usage', 0) > 85:
            stats["system_status"] = "warning"
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "성능 통계를 성공적으로 조회했습니다.",
                "data": stats
            }
        )
    except Exception as e:
        logger.error(f"성능 통계 조회 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"성능 통계 조회 실패: {str(e)}") 