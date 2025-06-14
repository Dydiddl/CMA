import pytest
import time
from unittest.mock import Mock, patch
import logging
from backend.monitoring import (
    SystemMonitor,
    DatabaseMonitor,
    CacheMonitor,
    AlertManager,
    MonitoringManager
)

@pytest.fixture
def mock_engine():
    engine = Mock()
    pool = Mock()
    pool.size.return_value = 10
    pool.overflow.return_value = 2
    engine.pool = pool
    return engine

@pytest.fixture
def system_monitor():
    return SystemMonitor()

@pytest.fixture
def db_monitor(mock_engine):
    return DatabaseMonitor(mock_engine)

@pytest.fixture
def cache_monitor():
    return CacheMonitor()

@pytest.fixture
def alert_manager():
    return AlertManager()

@pytest.fixture
def monitoring_manager(mock_engine):
    return MonitoringManager(mock_engine)

class TestSystemMonitor:
    def test_update_metrics(self, system_monitor):
        with patch('psutil.virtual_memory') as mock_memory, \
             patch('psutil.cpu_percent') as mock_cpu, \
             patch('psutil.disk_usage') as mock_disk, \
             patch('psutil.net_io_counters') as mock_net_io:
            
            # Mock 설정
            mock_memory.return_value.used = 1000
            mock_cpu.return_value = 50.0
            mock_disk.return_value.used = 2000
            mock_net_io.return_value.bytes_sent = 100
            mock_net_io.return_value.bytes_recv = 200
            
            # 메트릭 업데이트
            system_monitor.update_metrics()
            
            # 검증
            assert system_monitor.last_net_io.bytes_sent == 100
            assert system_monitor.last_net_io.bytes_recv == 200

class TestDatabaseMonitor:
    def test_update_metrics(self, db_monitor):
        db_monitor.update_metrics()
        
        # 검증
        assert db_monitor.engine.pool.size.called
        assert db_monitor.engine.pool.overflow.called

class TestCacheMonitor:
    def test_cache_operations(self, cache_monitor):
        # 캐시 히트/미스 기록
        cache_monitor.record_hit()
        cache_monitor.record_hit()
        cache_monitor.record_miss()
        
        # 검증
        assert cache_monitor.hits == 2
        assert cache_monitor.misses == 1
        assert cache_monitor.get_hit_rate() == 2/3

class TestAlertManager:
    def test_check_thresholds(self, alert_manager):
        # 임계값 초과 메트릭
        metrics = {
            'memory_usage': 0.95,  # 95%
            'cpu_usage': 0.85,     # 85%
            'disk_usage': 0.90     # 90%
        }
        
        alerts = alert_manager.check_thresholds(metrics)
        
        # 검증
        assert len(alerts) == 3
        assert any(alert['type'] == 'memory' for alert in alerts)
        assert any(alert['type'] == 'cpu' for alert in alerts)
        assert any(alert['type'] == 'disk' for alert in alerts)

    def test_send_alert(self, alert_manager):
        alert = {
            'type': 'memory',
            'level': 'critical',
            'message': '메모리 사용량이 90%를 초과했습니다.'
        }
        
        with patch('logging.warning') as mock_logging:
            alert_manager.send_alert(alert)
            
            # 검증
            assert alert['type'] in alert_manager.alerts
            assert len(alert_manager.alert_history) == 1
            assert mock_logging.called

class TestMonitoringManager:
    def test_update_all_metrics(self, monitoring_manager):
        with patch.object(monitoring_manager.system_monitor, 'update_metrics') as mock_system, \
             patch.object(monitoring_manager.db_monitor, 'update_metrics') as mock_db, \
             patch.object(monitoring_manager.alert_manager, 'check_thresholds') as mock_check, \
             patch.object(monitoring_manager.alert_manager, 'send_alert') as mock_send:
            
            monitoring_manager.update_all_metrics()
            
            # 검증
            assert mock_system.called
            assert mock_db.called
            assert mock_check.called

    def test_get_metrics_summary(self, monitoring_manager):
        summary = monitoring_manager.get_metrics_summary()
        
        # 검증
        assert 'system' in summary
        assert 'application' in summary
        assert 'database' in summary
        assert 'cache' in summary
        assert 'network' in summary

    def test_setup_monitoring_logger(self, monitoring_manager):
        # 로거 설정 검증
        logger = monitoring_manager.setup_monitoring_logger()
        assert logger is not None
        assert logger.level == logging.INFO
        assert len(logger.handlers) > 0 