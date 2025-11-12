"""
OpenTelemetry configuration for Baiiab project.

Provides tracing and metrics setup with support for console and OTLP exporters.
Tracks user interactions, API calls, errors, and performance metrics.
"""

import os
import logging
import json
from datetime import datetime
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider, ReadableSpan
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SpanExporter,
    SpanExportResult,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
    ConsoleMetricExporter,
    MetricExporter,
    MetricExportResult,
)
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from typing import Sequence

logger = logging.getLogger(__name__)


def parse_resource_attributes(env_var: str) -> dict:
    """
    Parse OTEL_RESOURCE_ATTRIBUTES environment variable.
    
    Format: key1=value1,key2=value2
    Example: service.name=baiiab,service.version=1.0,deployment.environment=production
    
    Args:
        env_var: Value of OTEL_RESOURCE_ATTRIBUTES environment variable
        
    Returns:
        Dictionary of resource attributes
    """
    attributes = {}
    if not env_var:
        return attributes
    
    try:
        # Split by comma and parse key=value pairs
        for pair in env_var.split(','):
            pair = pair.strip()
            if '=' in pair:
                key, value = pair.split('=', 1)
                attributes[key.strip()] = value.strip()
    except Exception as e:
        logger.warning(f"Failed to parse OTEL_RESOURCE_ATTRIBUTES: {e}")
    
    return attributes


class FileSpanExporter(SpanExporter):
    """Export spans to a file."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        try:
            with open(self.file_path, 'a') as f:
                for span in spans:
                    span_dict = {
                        "timestamp": datetime.now().isoformat(),
                        "name": span.name,
                        "trace_id": format(span.context.trace_id, '032x'),
                        "span_id": format(span.context.span_id, '016x'),
                        "start_time": span.start_time,
                        "end_time": span.end_time,
                        "duration_ms": (span.end_time - span.start_time) / 1_000_000,
                        "attributes": dict(span.attributes) if span.attributes else {},
                        "status": span.status.status_code.name if span.status else "UNSET",
                    }
                    f.write(json.dumps(span_dict) + "\n")
            return SpanExportResult.SUCCESS
        except Exception as e:
            logger.error(f"Failed to export spans to file: {e}")
            return SpanExportResult.FAILURE
    
    def shutdown(self):
        pass


class FileMetricExporter(MetricExporter):
    """Export metrics to a file."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self._preferred_temporality = {}
        self._preferred_aggregation = {}
    
    def export(self, metrics_data, timeout_millis: float = 10_000, **kwargs) -> MetricExportResult:
        try:
            with open(self.file_path, 'a') as f:
                # Process metrics data
                for resource_metric in metrics_data.resource_metrics:
                    for scope_metric in resource_metric.scope_metrics:
                        for metric in scope_metric.metrics:
                            metric_dict = {
                                "timestamp": datetime.now().isoformat(),
                                "name": metric.name,
                                "description": metric.description,
                                "unit": metric.unit,
                                "data": str(metric.data)
                            }
                            f.write(json.dumps(metric_dict) + "\n")
            return MetricExportResult.SUCCESS
        except Exception as e:
            logger.error(f"Failed to export metrics to file: {e}")
            return MetricExportResult.FAILURE
    
    def shutdown(self, timeout_millis: float = 30_000, **kwargs):
        pass
    
    def force_flush(self, timeout_millis: float = 10_000) -> bool:
        return True


def setup_telemetry(
    service_name="baiiab",
    service_version="1.0.0",
    use_console_exporter=True,
    use_otlp_exporter=False,
    otlp_endpoint=None,
    otlp_headers=None,
    use_file_exporter=False,
    file_path=None,
    otlp_traces_only=False
):
    """
    Initialize OpenTelemetry tracing and metrics.
    
    Args:
        service_name: Name of the service
        service_version: Version of the service
        use_console_exporter: Whether to export to console (useful for development)
        use_otlp_exporter: Whether to export to OTLP endpoint (e.g., Jaeger, Prometheus)
        otlp_endpoint: OTLP endpoint URL (e.g., "localhost:4317" or "host:443")
        otlp_headers: Dictionary of headers for authentication (e.g., {"Authorization": "ApiKey xxx"})
        use_file_exporter: Whether to export to file (useful for simulator)
        file_path: File path for file exporter
        otlp_traces_only: Only send traces to OTLP, not metrics (for Jaeger)
    
    Returns:
        tuple: (tracer, meter) for creating spans and recording metrics
    """
    
    # Create resource with service information
    # Start with defaults
    attributes = {
        SERVICE_NAME: service_name,
        SERVICE_VERSION: service_version,
        "deployment.environment": os.getenv("ENVIRONMENT", "development"),
    }
    
    # Merge with OTEL_RESOURCE_ATTRIBUTES from environment if present
    env_attributes = parse_resource_attributes(os.getenv("OTEL_RESOURCE_ATTRIBUTES", ""))
    if env_attributes:
        logger.info(f"Merging resource attributes from OTEL_RESOURCE_ATTRIBUTES: {env_attributes}")
        attributes.update(env_attributes)
    
    resource = Resource(attributes=attributes)
    
    # ============= TRACING SETUP =============
    tracer_provider = TracerProvider(resource=resource)
    
    # Add exporters
    if use_console_exporter:
        console_span_exporter = ConsoleSpanExporter()
        tracer_provider.add_span_processor(BatchSpanProcessor(console_span_exporter))
        logger.info("Console span exporter enabled")
    
    if use_file_exporter and file_path:
        file_span_exporter = FileSpanExporter(file_path)
        tracer_provider.add_span_processor(BatchSpanProcessor(file_span_exporter))
        logger.info(f"File span exporter enabled: {file_path}")
    
    if use_otlp_exporter and otlp_endpoint:
        # Parse headers if provided as string
        headers_dict = None
        if otlp_headers:
            if isinstance(otlp_headers, str):
                # Parse "key1=value1,key2=value2" format
                headers_dict = {}
                for pair in otlp_headers.split(','):
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        headers_dict[key.strip()] = value.strip()
            else:
                headers_dict = otlp_headers
        
        # HTTP exporter expects full URL with scheme
        # If no scheme provided, auto-detect based on port
        if not otlp_endpoint.startswith(('http://', 'https://')):
            if ':443' in otlp_endpoint or headers_dict:
                endpoint_url = f"https://{otlp_endpoint}"
            else:
                endpoint_url = f"http://{otlp_endpoint}"
        else:
            endpoint_url = otlp_endpoint
        
        # Add /v1/traces path if not present
        if not endpoint_url.endswith(('/v1/traces', '/v1/metrics')):
            trace_endpoint = f"{endpoint_url}/v1/traces"
        else:
            trace_endpoint = endpoint_url
        
        # Create OTLP span exporter (HTTP)
        exporter_kwargs = {"endpoint": trace_endpoint}
        if headers_dict:
            exporter_kwargs["headers"] = headers_dict
        
        otlp_span_exporter = OTLPSpanExporter(**exporter_kwargs)
        tracer_provider.add_span_processor(BatchSpanProcessor(otlp_span_exporter))
        
        headers_info = f" with auth" if headers_dict else ""
        logger.info(f"OTLP span exporter enabled: {trace_endpoint} (HTTP{headers_info})")
    
    trace.set_tracer_provider(tracer_provider)
    
    # ============= METRICS SETUP =============
    metric_readers = []
    
    if use_console_exporter:
        console_metric_reader = PeriodicExportingMetricReader(
            ConsoleMetricExporter(), export_interval_millis=60000
        )
        metric_readers.append(console_metric_reader)
        logger.info("Console metric exporter enabled")
    
    if use_file_exporter and file_path:
        file_metric_reader = PeriodicExportingMetricReader(
            FileMetricExporter(file_path), export_interval_millis=60000
        )
        metric_readers.append(file_metric_reader)
        logger.info(f"File metric exporter enabled: {file_path}")
    
    # Only export metrics to OTLP if not traces_only (Jaeger doesn't support metrics)
    if use_otlp_exporter and otlp_endpoint and not otlp_traces_only:
        # Parse headers if provided
        headers_dict = None
        if otlp_headers:
            if isinstance(otlp_headers, str):
                headers_dict = {}
                for pair in otlp_headers.split(','):
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        headers_dict[key.strip()] = value.strip()
            else:
                headers_dict = otlp_headers
        
        # HTTP exporter expects full URL with scheme
        if not otlp_endpoint.startswith(('http://', 'https://')):
            if ':443' in otlp_endpoint or headers_dict:
                endpoint_url = f"https://{otlp_endpoint}"
            else:
                endpoint_url = f"http://{otlp_endpoint}"
        else:
            endpoint_url = otlp_endpoint
        
        # Add /v1/metrics path if not present
        if not endpoint_url.endswith(('/v1/traces', '/v1/metrics')):
            metrics_endpoint = f"{endpoint_url}/v1/metrics"
        else:
            metrics_endpoint = endpoint_url
        
        # Create OTLP metric exporter (HTTP)
        exporter_kwargs = {"endpoint": metrics_endpoint}
        if headers_dict:
            exporter_kwargs["headers"] = headers_dict
        
        otlp_metric_reader = PeriodicExportingMetricReader(
            OTLPMetricExporter(**exporter_kwargs),
            export_interval_millis=60000
        )
        metric_readers.append(otlp_metric_reader)
        
        headers_info = f" with auth" if headers_dict else ""
        logger.info(f"OTLP metric exporter enabled: {metrics_endpoint} (HTTP{headers_info})")
    elif use_otlp_exporter and otlp_traces_only:
        logger.info("OTLP metrics disabled (traces only mode for Jaeger)")
    
    meter_provider = MeterProvider(resource=resource, metric_readers=metric_readers)
    metrics.set_meter_provider(meter_provider)
    
    # ============= LOGGING INSTRUMENTATION =============
    LoggingInstrumentor().instrument(set_logging_format=True)
    
    # Get tracer and meter instances
    tracer = trace.get_tracer(__name__)
    meter = metrics.get_meter(__name__)
    
    logger.info(f"OpenTelemetry initialized for {service_name} v{service_version}")
    
    return tracer, meter


def get_tracer(name=None):
    """Get a tracer instance."""
    return trace.get_tracer(name or __name__)


def get_meter(name=None):
    """Get a meter instance."""
    return metrics.get_meter(name or __name__)


# Convenience function to setup from environment variables
def setup_from_env():
    """
    Setup telemetry using environment variables.
    
    Environment variables:
        OTEL_SERVICE_NAME: Service name (default: "baiiab")
        OTEL_SERVICE_VERSION: Service version (default: "1.0.0")
        OTEL_CONSOLE_EXPORTER: Enable console exporter (default: "true")
        OTEL_FILE_EXPORTER: Enable file exporter (default: "false")
        OTEL_FILE_PATH: Path for file exporter (default: "logs/telemetry.jsonl")
        OTEL_EXPORTER_OTLP_ENDPOINT: OTLP endpoint URL
        OTEL_EXPORTER_OTLP_HEADERS: Headers for authentication (format: key1=value1,key2=value2)
        OTEL_EXPORTER_OTLP_TRACES_ONLY: Only send traces, not metrics (default: "true")
        OTEL_RESOURCE_ATTRIBUTES: Resource attributes (format: key1=value1,key2=value2)
        OTEL_ENABLED: Enable/disable telemetry (default: "true")
    """
    enabled = os.getenv("OTEL_ENABLED", "true").lower() == "true"
    
    if not enabled:
        logger.info("OpenTelemetry disabled via OTEL_ENABLED")
        return None, None
    
    service_name = os.getenv("OTEL_SERVICE_NAME", "baiiab")
    service_version = os.getenv("OTEL_SERVICE_VERSION", "1.0.0")
    use_console = os.getenv("OTEL_CONSOLE_EXPORTER", "true").lower() == "true"
    use_file = os.getenv("OTEL_FILE_EXPORTER", "false").lower() == "true"
    file_path = os.getenv("OTEL_FILE_PATH", "logs/telemetry.jsonl")
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    otlp_headers = os.getenv("OTEL_EXPORTER_OTLP_HEADERS")
    
    # Check if we should only send traces (Jaeger mode)
    # Jaeger doesn't support OTLP metrics service
    otlp_traces_only = os.getenv("OTEL_EXPORTER_OTLP_TRACES_ONLY", "true").lower() == "true"
    
    return setup_telemetry(
        service_name=service_name,
        service_version=service_version,
        use_console_exporter=use_console,
        use_file_exporter=use_file,
        file_path=file_path,
        use_otlp_exporter=bool(otlp_endpoint),
        otlp_endpoint=otlp_endpoint,
        otlp_headers=otlp_headers,
        otlp_traces_only=otlp_traces_only
    )
