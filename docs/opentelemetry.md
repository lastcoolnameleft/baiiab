# OpenTelemetry Setup for Baiiab

This guide explains how to use OpenTelemetry to monitor and observe your Baiiab box interactions.

## What's Being Tracked

The instrumentation captures:

### 📊 Metrics
- **API Calls**: Count of OpenAI API calls by model
- **Offline Fallbacks**: Count of times offline responses were used
- **API Duration**: Histogram of API response times (in milliseconds)
- **Errors**: Count of errors by type
- **User Interactions**: Button presses, rotary encoder turns, menu selections
- **Menu Navigation**: Navigation events (clockwise/counter-clockwise)

### 🔍 Traces (Spans)
Each trace includes timing and contextual information:

- **create_oai_chat_completion**: OpenAI API calls with model, temperature, response length, duration
- **get_offline_advice**: Offline fallback responses with topic and subtopic
- **action_callback**: User action selection with topic, subtopic, response source
- **rotary_encoder.clockwise/counter_clockwise**: Encoder interactions
- **button.press**: Button press events
- **simulator interactions**: All simulator navigation and selections

### 🏷️ Attributes Captured
- Topic and subtopic for each request
- Model name and parameters
- Response length and finish reason
- Duration in milliseconds
- Response source (API or offline)
- Error types and exceptions

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `opentelemetry-api` - Core API
- `opentelemetry-sdk` - SDK implementation
- `opentelemetry-exporter-otlp` - Export to observability backends
- `opentelemetry-instrumentation` - Auto-instrumentation tools
- `opentelemetry-instrumentation-requests` - HTTP request instrumentation
- `opentelemetry-instrumentation-logging` - Log correlation

### 2. Configure Environment Variables

Add to your `.env` file:

```bash
# Enable/disable telemetry (default: true)
OTEL_ENABLED=true

# Service identification
OTEL_SERVICE_NAME=baiiab
OTEL_SERVICE_VERSION=1.0.0

# Console exporter (prints to stdout, useful for development)
OTEL_CONSOLE_EXPORTER=true

# OTLP exporter endpoint (optional, for production observability)
# Examples: Jaeger, Prometheus, Grafana Cloud, etc.
# OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Environment
ENVIRONMENT=development
```

## Usage Modes

### Mode 1: Console Output (Development)

**Best for**: Local development and testing

```bash
# Enable console exporter in .env
OTEL_ENABLED=true
OTEL_CONSOLE_EXPORTER=true

# Run the simulator
python3 helpers/simulator.py
```

**Output**: Telemetry data prints to the console, showing spans and metrics every 60 seconds.

### Mode 2: OTLP Export (Production)

**Best for**: Production monitoring with observability platforms

```bash
# Configure OTLP endpoint in .env
OTEL_ENABLED=true
OTEL_CONSOLE_EXPORTER=false
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

Common OTLP backends:
- **Jaeger**: Distributed tracing
- **Prometheus + Grafana**: Metrics and dashboards
- **Grafana Cloud**: Hosted observability
- **Azure Monitor**: Azure-native observability
- **Datadog**: Full observability platform

### Mode 3: Disabled

```bash
# Disable telemetry completely
OTEL_ENABLED=false
```

The code gracefully handles missing OpenTelemetry packages - if not installed, telemetry is automatically disabled.

## Setting Up Observability Backends

### Option 1: Jaeger (Local Tracing)

Run Jaeger locally with Docker:

```bash
docker run -d --name jaeger \
  -p 4317:4317 \
  -p 16686:16686 \
  jaegertracing/all-in-one:latest
```

Configure:
```bash
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

View traces at: http://localhost:16686

### Option 2: Prometheus + Grafana (Metrics)

1. Set up Prometheus to scrape OTLP metrics
2. Configure Grafana to visualize
3. Create dashboards for:
   - API call rates
   - Error rates
   - Response times (p50, p95, p99)
   - User interaction patterns

### Option 3: Grafana Cloud (Easiest)

1. Sign up for free tier at grafana.com
2. Get your OTLP endpoint and credentials
3. Configure:

```bash
OTEL_EXPORTER_OTLP_ENDPOINT=https://otlp-gateway-prod-us-east-0.grafana.net/otlp
# Add auth headers as needed
```

## Viewing Telemetry Data

### Console Output Example

```
{
    "name": "create_oai_chat_completion",
    "kind": "INTERNAL",
    "start_time": "2025-11-04T12:34:56.789Z",
    "end_time": "2025-11-04T12:34:58.123Z",
    "attributes": {
        "model": "gpt-4",
        "temperature": 1.3,
        "duration_ms": 1334.5,
        "response_length": 156,
        "finish_reason": "stop"
    },
    "status": "OK"
}
```

### Key Queries

Once data is in your observability platform:

**API Performance**:
```
# Average API response time
avg(baiiab_api_duration) by (model)

# 95th percentile latency
histogram_quantile(0.95, baiiab_api_duration)
```

**Error Rates**:
```
# Error rate over time
rate(baiiab_errors[5m])

# Errors by type
sum(baiiab_errors) by (error_type)
```

**User Behavior**:
```
# Most popular topics
sum(baiiab_user_interactions) by (topic)

# Interaction rate
rate(baiiab_user_interactions[1h])
```

**Offline Fallback Rate**:
```
# Percentage of offline responses
sum(baiiab_offline_fallbacks) / sum(baiiab_api_calls) * 100
```

## Testing Your Setup

### 1. Test with Simulator

```bash
python3 helpers/simulator.py
```

Navigate through menus and select actions. With `OTEL_CONSOLE_EXPORTER=true`, you'll see spans printed to the console.

### 2. Verify Traces

Look for spans like:
- `simulator.navigation.next`
- `simulator.action_callback`
- `create_oai_chat_completion`
- `get_offline_advice`

### 3. Verify Metrics

After 60 seconds, you should see metrics exported:
- `baiiab.api_calls`
- `baiiab.api_duration`
- `baiiab.simulator_interactions`

## Troubleshooting

### No telemetry output?

1. Check `OTEL_ENABLED=true` in `.env`
2. Verify OpenTelemetry packages are installed: `pip list | grep opentelemetry`
3. Check logs for "OpenTelemetry initialized" message

### Import errors?

```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Can't connect to OTLP endpoint?

1. Verify endpoint URL is correct
2. Check if backend is running: `curl http://localhost:4317`
3. Review firewall/network settings

### Too much console output?

```bash
# Disable console exporter
OTEL_CONSOLE_EXPORTER=false
```

## Production Recommendations

1. **Use OTLP Exporter**: Send to a proper observability backend
2. **Set Environment**: `ENVIRONMENT=production` for filtering
3. **Monitor Key Metrics**:
   - API error rate (alert if > 5%)
   - API latency (alert if p95 > 3 seconds)
   - Offline fallback rate (alert if > 10%)
4. **Set Up Alerts**: Configure alerts for anomalies
5. **Create Dashboards**: Build views for:
   - Real-time usage
   - Error tracking
   - Performance trends
   - User behavior patterns

## Example Dashboard Panels

### API Performance
- Line graph: API response time over time
- Gauge: Current API success rate
- Histogram: Response time distribution

### User Interactions
- Counter: Total interactions today
- Bar chart: Popular topics
- Heatmap: Usage by hour

### System Health
- Line graph: Error rate over time
- Table: Recent errors with stack traces
- Gauge: Offline fallback percentage

## Additional Resources

- [OpenTelemetry Python Documentation](https://opentelemetry.io/docs/instrumentation/python/)
- [OTLP Specification](https://opentelemetry.io/docs/reference/specification/protocol/)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)

## Next Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Configure `.env` file with telemetry settings
3. Test with simulator: `python3 helpers/simulator.py`
4. Set up an observability backend (Jaeger, Grafana, etc.)
5. Create dashboards and alerts
6. Deploy to production with monitoring enabled!
