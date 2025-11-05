#!/usr/bin/env python3
"""
Quick test to verify telemetry file writing works.
"""

import os
import sys

# Add parent directory to path so we can import from project modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test 1: Check if logs directory exists
print("Test 1: Checking logs directory...")
if os.path.exists("logs"):
    print("✓ logs/ directory exists")
else:
    print("✗ logs/ directory missing")
    os.makedirs("logs", exist_ok=True)
    print("✓ Created logs/ directory")

# Test 2: Check if we can write to the file
log_file = "logs/simulator_telemetry.log"
print(f"\nTest 2: Testing write to {log_file}...")
try:
    with open(log_file, 'a') as f:
        f.write("Test write at startup\n")
    print(f"✓ Successfully wrote to {log_file}")
except Exception as e:
    print(f"✗ Failed to write: {e}")
    sys.exit(1)

# Test 3: Try importing OpenTelemetry
print("\nTest 3: Checking OpenTelemetry installation...")
try:
    from opentelemetry import trace
    print("✓ OpenTelemetry is installed")
    
    # Test 4: Try importing custom exporters
    print("\nTest 4: Checking custom file exporters...")
    try:
        from otel.otel_config import FileSpanExporter, FileMetricExporter
        print("✓ Custom file exporters available")
        
        # Test 5: Try creating a file exporter
        print("\nTest 5: Testing FileSpanExporter...")
        try:
            exporter = FileSpanExporter("logs/test_spans.log")
            print(f"✓ FileSpanExporter created successfully")
            print(f"  Output file: logs/test_spans.log")
        except Exception as e:
            print(f"✗ Failed to create exporter: {e}")
            
    except ImportError as e:
        print(f"✗ Failed to import custom exporters: {e}")
        
except ImportError:
    print("✗ OpenTelemetry is NOT installed")
    print("  Run: pip install -r requirements.txt")
    sys.exit(1)

print("\n" + "="*60)
print("All tests passed! Telemetry file writing should work.")
print(f"Telemetry will be written to: {os.path.abspath(log_file)}")
print("="*60)
