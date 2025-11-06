#!/usr/bin/env python3
"""
Generate test metrics to verify Grafana dashboard is working.
This script creates the same metrics that the application generates.
"""
import sys
import time
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from otel import setup_from_env, get_tracer, get_meter

print("=" * 70)
print("Generating Test Metrics for Grafana")
print("=" * 70)

print("\nInitializing OpenTelemetry...")
tracer, meter = setup_from_env()

if not meter:
    print("ERROR: Meter not initialized")
    sys.exit(1)

print("✓ OpenTelemetry initialized")

# Create the same metrics that the application uses
print("\nCreating application metrics...")
api_call_counter = meter.create_counter(
    "baiiab.api_calls",
    description="Number of API calls",
    unit="1"
)

api_duration = meter.create_histogram(
    "baiiab.api_duration",
    description="API call duration",
    unit="milliseconds"
)

interaction_counter = meter.create_counter(
    "baiiab.simulator_interactions",
    description="Simulator interactions",
    unit="1"
)

error_counter = meter.create_counter(
    "baiiab.errors",
    description="Error count",
    unit="1"
)

print("✓ Metrics created")

print("\nGenerating test data...")
# Simulate some API calls with realistic labels
topics = ["joke", "advice", "recipe", "insult", "cocktail"]
subtopics = ["funny", "dad", "tasty", "silly", "absurd"]
for i in range(10):
    # API metrics
    api_call_counter.add(1, {"model": "gpt-4", "status": "success"})
    api_duration.record(150.5 + (i * 10), {"model": "gpt-4"})
    
    # Interaction metrics with correct labels
    topic = topics[i % len(topics)]
    subtopic = subtopics[i % len(subtopics)]
    interaction_counter.add(1, {
        "interaction_type": "action_selected", 
        "topic": topic,
        "subtopic": subtopic
    })
    
    # No errors in test
    if i % 2 == 0:
        error_counter.add(0, {"error_type": "none"})
    
    print(f"  ✓ Generated metric batch {i+1}/10 (topic={topic}, subtopic={subtopic})")
    time.sleep(0.5)

print("\n" + "=" * 70)
print("Waiting for metrics to be exported...")
print("=" * 70)
print("\nMetrics are exported every 60 seconds to the OTel Collector.")
print("Progress: ", end="", flush=True)

# Wait for the periodic export (60 seconds)
for i in range(60):
    time.sleep(1)
    if i % 5 == 0:
        print(".", end="", flush=True)

print("\n\n" + "=" * 70)
print("✓ Test metrics generated and exported!")
print("=" * 70)

print("\nNext steps:")
print("  1. Open Grafana: http://localhost:3000")
print("  2. Login with admin/admin")
print("  3. Open the 'Baiiab - AI in a Box' dashboard")
print("  4. You should now see data in the panels:")
print("     - API Call Rate")
print("     - Average API Response Time")
print("     - Interactions")
print("     - Error Rate")
print("\nIf you don't see data, check:")
print("  - Prometheus: http://localhost:9090")
print("  - Search for 'baiiab' to see available metrics")
print("=" * 70)
