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
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from typing import Sequence

logger = logging.getLogger(__name__)


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
        otlp_endpoint: OTLP endpoint URL (e.g., "http://localhost:4317")
        use_file_exporter: Whether to export to file (useful for simulator)
        file_path: File path for file exporter
        otlp_traces_only: Only send traces to OTLP, not metrics (for Jaeger)
    
    Returns:
        tuple: (tracer, meter) for creating spans and recording metrics
    """
    
    # Create resource with service information
    resource = Resource(attributes={
        SERVICE_NAME: service_name,
        SERVICE_VERSION: service_version,
        "deployment.environment": os.getenv("ENVIRONMENT", "development"),
    })
    
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
        otlp_span_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
        tracer_provider.add_span_processor(BatchSpanProcessor(otlp_span_exporter))
        logger.info(f"OTLP span exporter enabled: {otlp_endpoint}")
    
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
        otlp_metric_reader = PeriodicExportingMetricReader(
            OTLPMetricExporter(endpoint=otlp_endpoint, insecure=True),
            export_interval_millis=60000
        )
        metric_readers.append(otlp_metric_reader)
        logger.info(f"OTLP metric exporter enabled: {otlp_endpoint}")
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
        OTEL_EXPORTER_OTLP_ENDPOINT: OTLP endpoint URL
        OTEL_ENABLED: Enable/disable telemetry (default: "true")
    """
    enabled = os.getenv("OTEL_ENABLED", "true").lower() == "true"
    
    if not enabled:
        logger.info("OpenTelemetry disabled via OTEL_ENABLED")
        return None, None
    
    service_name = os.getenv("OTEL_SERVICE_NAME", "baiiab")
    service_version = os.getenv("OTEL_SERVICE_VERSION", "1.0.0")
    use_console = os.getenv("OTEL_CONSOLE_EXPORTER", "true").lower() == "true"
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    
    # Check if we should only send traces (Jaeger mode)
    # Jaeger doesn't support OTLP metrics service
    otlp_traces_only = os.getenv("OTEL_TRACES_ONLY", "true").lower() == "true"
    
    return setup_telemetry(
        service_name=service_name,
        service_version=service_version,
        use_console_exporter=use_console,
        use_otlp_exporter=bool(otlp_endpoint),
        otlp_endpoint=otlp_endpoint,
        otlp_traces_only=otlp_traces_only
    )
