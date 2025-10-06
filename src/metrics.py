"""
© Rajan Mishra — 2025
Agentic AI for Azure Supportability Test
"""
"""
Metrics Module - Prometheus Metrics for Azure RDP Agent
Designed by Rajan Mishra for production observability
"""
from prometheus_client import Counter, Histogram, Gauge, start_http_server, CollectorRegistry
import time
from typing import Optional
import structlog

logger = structlog.get_logger()

# Custom registry to avoid conflicts
REGISTRY = CollectorRegistry()

# Issue Detection Metrics
rdp_issues_detected = Counter(
    'rdp_issues_detected_total',
    'Total RDP connectivity issues detected',
    ['root_cause', 'vm_name', 'resource_group'],
    registry=REGISTRY
)

# Resolution Metrics
auto_resolutions_successful = Counter(
    'auto_resolutions_successful_total',
    'Total successful automatic resolutions',
    ['fix_type', 'vm_name'],
    registry=REGISTRY
)

auto_resolutions_failed = Counter(
    'auto_resolutions_failed_total',
    'Total failed automatic resolution attempts',
    ['fix_type', 'failure_reason'],
    registry=REGISTRY
)

escalated_to_human = Counter(
    'escalated_to_human_total',
    'Total cases escalated to human intervention',
    ['reason', 'vm_name'],
    registry=REGISTRY
)

# Performance Metrics
resolution_duration = Histogram(
    'resolution_duration_seconds',
    'Time taken to resolve RDP issues',
    ['root_cause'],
    buckets=[5, 10, 30, 60, 120, 300],
    registry=REGISTRY
)

diagnostic_duration = Histogram(
    'diagnostic_duration_seconds',
    'Time taken for diagnostic checks',
    buckets=[1, 3, 5, 10, 15, 30],
    registry=REGISTRY
)

remediation_duration = Histogram(
    'remediation_duration_seconds',
    'Time taken for remediation actions',
    ['action_type'],
    buckets=[5, 10, 20, 30, 60, 120],
    registry=REGISTRY
)

validation_duration = Histogram(
    'validation_duration_seconds',
    'Time taken for post-fix validation',
    buckets=[1, 2, 5, 10, 20],
    registry=REGISTRY
)

# AI/ML Metrics
openai_api_calls = Counter(
    'openai_api_calls_total',
    'Total OpenAI API calls made',
    ['model', 'purpose'],
    registry=REGISTRY
)

openai_tokens_used = Counter(
    'openai_tokens_used_total',
    'Total OpenAI tokens consumed',
    ['model'],
    registry=REGISTRY
)

openai_api_latency = Histogram(
    'openai_api_latency_seconds',
    'OpenAI API response time',
    ['model'],
    buckets=[0.5, 1, 2, 5, 10, 30],
    registry=REGISTRY
)

# System Health Metrics
active_incidents = Gauge(
    'active_incidents',
    'Number of currently active RDP incidents',
    registry=REGISTRY
)

vms_monitored = Gauge(
    'vms_monitored_total',
    'Total number of VMs being monitored',
    registry=REGISTRY
)

agent_uptime_seconds = Gauge(
    'agent_uptime_seconds',
    'Agent uptime in seconds',
    registry=REGISTRY
)


class MetricsServer:
    """
    Prometheus metrics server manager
    
    Handles:
    - Starting/stopping metrics HTTP server
    - Exporting metrics in Prometheus format
    - Integration with Azure Monitor
    """
    
    def __init__(self, port: int = 8000):
        self.port = port
        self.server_started = False
        self.start_time = time.time()
    
    def start(self) -> bool:
        """
        Start Prometheus metrics HTTP server
        
        Returns:
            bool: True if started successfully, False otherwise
        """
        if self.server_started:
            logger.warning("metrics.already_started", port=self.port)
            return True
        
        try:
            start_http_server(self.port, registry=REGISTRY)
            self.server_started = True
            logger.info("metrics.server_started", port=self.port)
            return True
        except OSError as e:
            # Port already in use
            if "10013" in str(e) or "10048" in str(e):
                logger.warning("metrics.port_in_use", port=self.port, error=str(e))
                return False
            raise
        except Exception as e:
            logger.error("metrics.start_failed", port=self.port, error=str(e))
            return False
    
    def update_uptime(self):
        """Update agent uptime metric"""
        uptime = time.time() - self.start_time
        agent_uptime_seconds.set(uptime)
    
    def record_issue_detected(
        self,
        root_cause: str,
        vm_name: str,
        resource_group: str
    ):
        """Record an RDP issue detection"""
        rdp_issues_detected.labels(
            root_cause=root_cause,
            vm_name=vm_name,
            resource_group=resource_group
        ).inc()
        logger.info(
            "metrics.issue_detected",
            root_cause=root_cause,
            vm_name=vm_name
        )
    
    def record_resolution_success(
        self,
        fix_type: str,
        vm_name: str,
        duration_seconds: float
    ):
        """Record successful resolution"""
        auto_resolutions_successful.labels(
            fix_type=fix_type,
            vm_name=vm_name
        ).inc()
        
        resolution_duration.labels(root_cause=fix_type).observe(duration_seconds)
        
        logger.info(
            "metrics.resolution_success",
            fix_type=fix_type,
            vm_name=vm_name,
            duration=duration_seconds
        )
    
    def record_resolution_failure(
        self,
        fix_type: str,
        failure_reason: str
    ):
        """Record failed resolution attempt"""
        auto_resolutions_failed.labels(
            fix_type=fix_type,
            failure_reason=failure_reason
        ).inc()
        
        logger.warning(
            "metrics.resolution_failed",
            fix_type=fix_type,
            reason=failure_reason
        )
    
    def record_escalation(
        self,
        reason: str,
        vm_name: str
    ):
        """Record escalation to human"""
        escalated_to_human.labels(
            reason=reason,
            vm_name=vm_name
        ).inc()
        
        active_incidents.inc()
        
        logger.warning(
            "metrics.escalated_to_human",
            reason=reason,
            vm_name=vm_name
        )
    
    def record_openai_call(
        self,
        model: str,
        purpose: str,
        tokens_used: int,
        latency_seconds: float
    ):
        """Record OpenAI API usage"""
        openai_api_calls.labels(model=model, purpose=purpose).inc()
        openai_tokens_used.labels(model=model).inc(tokens_used)
        openai_api_latency.labels(model=model).observe(latency_seconds)
        
        logger.debug(
            "metrics.openai_call",
            model=model,
            purpose=purpose,
            tokens=tokens_used,
            latency=latency_seconds
        )
    
    def record_diagnostic_time(self, duration_seconds: float):
        """Record diagnostic execution time"""
        diagnostic_duration.observe(duration_seconds)
    
    def record_remediation_time(
        self,
        action_type: str,
        duration_seconds: float
    ):
        """Record remediation execution time"""
        remediation_duration.labels(action_type=action_type).observe(duration_seconds)
    
    def record_validation_time(self, duration_seconds: float):
        """Record validation execution time"""
        validation_duration.observe(duration_seconds)
    
    def set_vms_monitored(self, count: int):
        """Update number of VMs being monitored"""
        vms_monitored.set(count)
    
    def get_metrics_url(self) -> str:
        """Get the metrics endpoint URL"""
        return f"http://localhost:{self.port}/metrics"


# Global metrics server instance
metrics_server: Optional[MetricsServer] = None


def get_metrics_server(port: int = 8000) -> MetricsServer:
    """
    Get or create global metrics server instance
    
    Args:
        port: Port to run metrics server on
        
    Returns:
        MetricsServer instance
    """
    global metrics_server
    if metrics_server is None:
        metrics_server = MetricsServer(port=port)
    return metrics_server


def start_metrics(port: int = 8000) -> MetricsServer:
    """
    Start metrics server and return instance
    
    Args:
        port: Port to run metrics server on
        
    Returns:
        MetricsServer instance
    """
    server = get_metrics_server(port)
    server.start()
    return server
