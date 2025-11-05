"""OpenTelemetry configuration package."""
from .otel_config import setup_telemetry, get_tracer, get_meter, setup_from_env

__all__ = ['setup_telemetry', 'get_tracer', 'get_meter', 'setup_from_env']
