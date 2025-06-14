import psutil
import time
from prometheus_client import Counter, Histogram, Gauge, Summary
from typing import Dict, Any
import logging
import logging.handlers
from datetime import datetime
import json
from pathlib import Path

# 시스템 메트릭
SYSTEM_MEMORY = Gauge(
    'system_memory_usage_bytes',
    'System memory usage in bytes'
)

SYSTEM_CPU = Gauge(
    'system_cpu_usage_percent',
    'System CPU usage percentage'
)

SYSTEM_DISK = Gauge(
    'system_disk_usage_bytes',
    'System disk usage in bytes'
)

# 애플리케이션 메트릭
APP_MEMORY = Gauge(
    'app_memory_usage_bytes',
    'Application memory usage in bytes'
)

APP_CPU = Gauge(
    'app_cpu_usage_percent',
    'Application CPU usage percentage'
)

# 데이터베이스 메트릭
DB_CONNECTION_POOL = Gauge(
    'db_connection_pool_size',
    'Database connection pool size',
    ['state']  # active, idle, total
)

DB_QUERY_DURATION = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds',
    ['query_type']
)

# 캐시 메트릭
CACHE_HITS = Counter(
    'cache_hits_total',
    'Total number of cache hits'
)

CACHE_MISSES = Counter(
    'cache_misses_total',
    'Total number of cache misses'
)

# 네트워크 메트릭
NETWORK_BYTES_SENT = Counter(
    'network_bytes_sent_total',
    'Total number of bytes sent'
)

NETWORK_BYTES_RECEIVED = Counter(
    'network_bytes_received_total',
    'Total number of bytes received'
)

class SystemMonitor:
    def __init__(self):
        self.process = psutil.Process()
        self.last_net_io = psutil.net_io_counters()
        self.last_time = time.time()

    def update_metrics(self):
        # 시스템 메트릭 업데이트
        SYSTEM_MEMORY.set(psutil.virtual_memory().used)
        SYSTEM_CPU.set(psutil.cpu_percent())
        SYSTEM_DISK.set(psutil.disk_usage('/').used)

        # 애플리케이션 메트릭 업데이트
        APP_MEMORY.set(self.process.memory_info().rss)
        APP_CPU.set(self.process.cpu_percent())

        # 네트워크 메트릭 업데이트
        current_net_io = psutil.net_io_counters()
        current_time = time.time()
        time_diff = current_time - self.last_time

        if time_diff > 0:
            bytes_sent_diff = current_net_io.bytes_sent - self.last_net_io.bytes_sent
            bytes_recv_diff = current_net_io.bytes_recv - self.last_net_io.bytes_recv

            if bytes_sent_diff >= 0:
                NETWORK_BYTES_SENT.inc(bytes_sent_diff)
            if bytes_recv_diff >= 0:
                NETWORK_BYTES_RECEIVED.inc(bytes_recv_diff)

        self.last_net_io = current_net_io
        self.last_time = current_time

class DatabaseMonitor:
    def __init__(self, engine):
        self.engine = engine

    def update_metrics(self):
        # 데이터베이스 연결 풀 상태 업데이트
        pool = self.engine.pool
        DB_CONNECTION_POOL.labels(state='active').set(pool.size() - pool.overflow())
        DB_CONNECTION_POOL.labels(state='idle').set(pool.overflow())
        DB_CONNECTION_POOL.labels(state='total').set(pool.size())

class CacheMonitor:
    def __init__(self):
        self.hits = 0
        self.misses = 0

    def record_hit(self):
        self.hits += 1
        CACHE_HITS.inc()

    def record_miss(self):
        self.misses += 1
        CACHE_MISSES.inc()

    def get_hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0

class AlertManager:
    def __init__(self):
        self.alerts: Dict[str, Any] = {}
        self.alert_history: List[Dict[str, Any]] = []

    def check_thresholds(self, metrics: Dict[str, float]):
        alerts = []
        
        # 메모리 사용량 임계값 체크
        if metrics.get('memory_usage', 0) > 0.9:  # 90%
            alerts.append({
                'type': 'memory',
                'level': 'critical',
                'message': '메모리 사용량이 90%를 초과했습니다.'
            })

        # CPU 사용량 임계값 체크
        if metrics.get('cpu_usage', 0) > 0.8:  # 80%
            alerts.append({
                'type': 'cpu',
                'level': 'warning',
                'message': 'CPU 사용량이 80%를 초과했습니다.'
            })

        # 디스크 사용량 임계값 체크
        if metrics.get('disk_usage', 0) > 0.85:  # 85%
            alerts.append({
                'type': 'disk',
                'level': 'warning',
                'message': '디스크 사용량이 85%를 초과했습니다.'
            })

        return alerts

    def send_alert(self, alert: Dict[str, Any]):
        self.alerts[alert['type']] = alert
        self.alert_history.append({
            **alert,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # 로깅
        logging.warning(
            f"Alert: {alert['message']}",
            extra={
                'alert_type': alert['type'],
                'alert_level': alert['level']
            }
        )

class MonitoringManager:
    def __init__(self, engine):
        self.system_monitor = SystemMonitor()
        self.db_monitor = DatabaseMonitor(engine)
        self.cache_monitor = CacheMonitor()
        self.alert_manager = AlertManager()
        
        # 모니터링 로그 설정
        self.setup_monitoring_logger()

    def setup_monitoring_logger(self):
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        monitoring_logger = logging.getLogger('monitoring')
        monitoring_logger.setLevel(logging.INFO)
        
        # 파일 핸들러
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / 'monitoring.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        
        # JSON 포맷터
        class JSONFormatter(logging.Formatter):
            def format(self, record):
                log_record = {
                    'timestamp': datetime.utcnow().isoformat(),
                    'level': record.levelname,
                    'message': record.getMessage(),
                    'module': record.module,
                    'function': record.funcName,
                    'line': record.lineno
                }
                if hasattr(record, 'extra'):
                    log_record.update(record.extra)
                return json.dumps(log_record)
        
        file_handler.setFormatter(JSONFormatter())
        monitoring_logger.addHandler(file_handler)
        
        return monitoring_logger

    def update_all_metrics(self):
        self.system_monitor.update_metrics()
        self.db_monitor.update_metrics()
        
        # 현재 메트릭 수집
        current_metrics = {
            'memory_usage': SYSTEM_MEMORY._value.get() / psutil.virtual_memory().total,
            'cpu_usage': SYSTEM_CPU._value.get(),
            'disk_usage': SYSTEM_DISK._value.get() / psutil.disk_usage('/').total,
            'cache_hit_rate': self.cache_monitor.get_hit_rate()
        }
        
        # 임계값 체크 및 알림
        alerts = self.alert_manager.check_thresholds(current_metrics)
        for alert in alerts:
            self.alert_manager.send_alert(alert)

    def get_metrics_summary(self) -> Dict[str, Any]:
        return {
            'system': {
                'memory_usage': SYSTEM_MEMORY._value.get(),
                'cpu_usage': SYSTEM_CPU._value.get(),
                'disk_usage': SYSTEM_DISK._value.get()
            },
            'application': {
                'memory_usage': APP_MEMORY._value.get(),
                'cpu_usage': APP_CPU._value.get()
            },
            'database': {
                'active_connections': DB_CONNECTION_POOL.labels(state='active')._value.get(),
                'idle_connections': DB_CONNECTION_POOL.labels(state='idle')._value.get()
            },
            'cache': {
                'hits': CACHE_HITS._value.get(),
                'misses': CACHE_MISSES._value.get(),
                'hit_rate': self.cache_monitor.get_hit_rate()
            },
            'network': {
                'bytes_sent': NETWORK_BYTES_SENT._value.get(),
                'bytes_received': NETWORK_BYTES_RECEIVED._value.get()
            }
        } 