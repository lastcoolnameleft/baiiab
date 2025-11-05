#!/usr/bin/env python3
"""
Test script to verify OpenTelemetry setup.
Run this to ensure telemetry is working correctly.
"""

import os
import sys

# Add parent directory to path so we can import from otel module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("OpenTelemetry Configuration Test")
print("=" * 70)

# Check if telemetry is enabled
enabled = os.getenv("OTEL_ENABLED", "true").lower() == "true"
print(f"\n✓ OTEL_ENABLED: {enabled}")

if not enabled:
    print("\n⚠️  Telemetry is DISABLED in .env")
    print("   Set OTEL_ENABLED=true to enable")
    sys.exit(0)

# Check OpenTelemetry packages
print("\nChecking OpenTelemetry packages...")
try:
    import opentelemetry
    print("✓ opentelemetry-api installed")
except ImportError:
    print("✗ opentelemetry-api NOT installed")
    print("  Run: pip install -r requirements.txt")
    sys.exit(1)

try:
    from opentelemetry.sdk.trace import TracerProvider
    print("✓ opentelemetry-sdk installed")
except ImportError:
    print("✗ opentelemetry-sdk NOT installed")
    sys.exit(1)

try:
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    print("✓ opentelemetry-exporter-otlp installed")
except ImportError:
    print("✗ opentelemetry-exporter-otlp NOT installed")
    sys.exit(1)

# Check configuration module
print("\nChecking configuration module...")
try:
    from otel import setup_from_env, get_tracer, get_meter
    print("✓ otel module found and valid")
except ImportError as e:
    print(f"✗ otel module error: {e}")
    sys.exit(1)

# Check environment variables
print("\nEnvironment Configuration:")
print(f"  Service Name: {os.getenv('OTEL_SERVICE_NAME', 'baiiab')}")
print(f"  Service Version: {os.getenv('OTEL_SERVICE_VERSION', '1.0.0')}")
print(f"  Console Exporter: {os.getenv('OTEL_CONSOLE_EXPORTER', 'true')}")
print(f"  OTLP Endpoint: {os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT', 'Not configured')}")
print(f"  Environment: {os.getenv('ENVIRONMENT', 'development')}")

# Initialize telemetry
print("\nInitializing OpenTelemetry...")
try:
    tracer, meter = setup_from_env()
    if tracer and meter:
        print("✓ Tracer and Meter initialized successfully")
    else:
        print("⚠️  Tracer/Meter returned None (telemetry may be disabled)")
except Exception as e:
    print(f"✗ Initialization error: {e}")
    sys.exit(1)

# Test creating a span
if tracer:
    print("\nTesting span creation...")
    try:
        with tracer.start_as_current_span("test_span") as span:
            span.set_attribute("test", "value")
            span.set_attribute("number", 42)
            print("✓ Created test span with attributes")
    except Exception as e:
        print(f"✗ Span creation error: {e}")
        sys.exit(1)

# Test creating metrics
if meter:
    print("\nTesting metric creation...")
    try:
        test_counter = meter.create_counter(
            "test.counter",
            description="Test counter",
            unit="1"
        )
        test_counter.add(1, {"test": "attribute"})
        print("✓ Created and incremented test counter")
        
        test_histogram = meter.create_histogram(
            "test.histogram",
            description="Test histogram",
            unit="ms"
        )
        test_histogram.record(123.45, {"test": "attribute"})
        print("✓ Created and recorded test histogram")
    except Exception as e:
        print(f"✗ Metric creation error: {e}")
        sys.exit(1)

# Check if console output is enabled
console_enabled = os.getenv("OTEL_CONSOLE_EXPORTER", "true").lower() == "true"
if console_enabled:
    print("\n✓ Console exporter is ENABLED")
    print("  You should see span output above or within 60 seconds")
else:
    print("\n⚠️  Console exporter is DISABLED")
    print("   Telemetry is being sent to OTLP endpoint only")

# Check OTLP endpoint
otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
if otlp_endpoint:
    print(f"\n✓ OTLP exporter configured: {otlp_endpoint}")
    print("  Telemetry will be sent to this endpoint")
else:
    print("\n⚠️  OTLP endpoint not configured")
    print("   Set OTEL_EXPORTER_OTLP_ENDPOINT to send to observability backend")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("✓ OpenTelemetry is properly configured!")
print("\nNext steps:")
print("  1. Run: python3 simulator.py")
print("  2. Navigate the menu and select items")
if console_enabled:
    print("  3. Watch the console for span and metric output")
else:
    print("  3. Check your observability backend for traces and metrics")
print("\nFor more information, see:")
print("  - docs/opentelemetry-quickstart.md")
print("  - docs/opentelemetry.md")
print("=" * 70)
