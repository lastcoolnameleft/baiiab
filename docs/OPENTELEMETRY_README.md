# OpenTelemetry Integration

The Baiiab project now includes comprehensive OpenTelemetry instrumentation for monitoring and observability!

## What's New

🔍 **Distributed Tracing** - Track every interaction from button press to response  
📊 **Metrics Collection** - Monitor API performance, error rates, and user behavior  
🐛 **Error Tracking** - Automatic exception recording with full context  
⏱️ **Performance Monitoring** - Measure API latency, response times, and system performance  

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Add to your `.env` file:
```bash
OTEL_ENABLED=true
OTEL_CONSOLE_EXPORTER=true
```

### 3. Test It
```bash
python3 helpers/test_otel.py        # Verify setup
python3 helpers/simulator.py        # Run with telemetry
```

### 4. See Telemetry
Watch your console for traces and metrics!

## What Gets Tracked

### User Interactions
- Rotary encoder turns (clockwise/counter-clockwise)
- Button presses
- Menu navigation
- Action selections

### API Performance
- OpenAI API calls with timing
- Request/response details
- Error rates and types
- Offline fallback usage

### System Metrics
- API response times (P50, P95, P99)
- Success/failure rates
- Popular topics and subtopics
- User engagement patterns

## Documentation

- **Quick Start**: `docs/opentelemetry-quickstart.md` - Get running in 5 minutes
- **Full Guide**: `docs/opentelemetry.md` - Complete setup and configuration
- **Architecture**: `docs/opentelemetry-architecture.md` - What's tracked and where
- **Summary**: `OPENTELEMETRY_SUMMARY.md` - Implementation details

## Configuration

All configuration via environment variables:

```bash
# Enable/disable telemetry
OTEL_ENABLED=true

# Service identification
OTEL_SERVICE_NAME=baiiab
OTEL_SERVICE_VERSION=1.0.0

# Export to console (development)
OTEL_CONSOLE_EXPORTER=true

# Export to observability backend (production)
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Environment tag
ENVIRONMENT=development
```

## Observability Backends

Works with popular platforms:
- **Jaeger** - Distributed tracing
- **Prometheus + Grafana** - Metrics and dashboards
- **Grafana Cloud** - Hosted observability
- **Azure Monitor** - Azure-native monitoring
- **Datadog** - Full observability platform

## Example: Run with Jaeger

```bash
# Start Jaeger
docker run -d --name jaeger \
  -p 4317:4317 \
  -p 16686:16686 \
  jaegertracing/all-in-one:latest

# Configure in .env
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
OTEL_CONSOLE_EXPORTER=false

# Run simulator
python3 helpers/simulator.py

# View traces at http://localhost:16686
```

## Benefits

### For Development
- Debug performance bottlenecks
- Understand user interaction flows
- Test error handling scenarios
- Optimize API usage

### For Operations
- Monitor system health 24/7
- Set up alerts for anomalies
- Track SLA compliance
- Capacity planning with real data

### For Product
- Understand usage patterns
- Identify popular features
- Track user engagement
- Measure feature adoption

## Zero Breaking Changes

The implementation is:
- ✅ **Optional** - Works with or without OpenTelemetry installed
- ✅ **Non-invasive** - No changes to existing functionality
- ✅ **Configurable** - Enable/disable via environment variables
- ✅ **Backward compatible** - Existing code works unchanged

## Files Added

- `otel_config.py` - OpenTelemetry configuration
- `helpers/test_otel.py` - Setup verification script
- `.env.example` - Environment template
- `docs/opentelemetry.md` - Complete guide
- `docs/opentelemetry-quickstart.md` - Quick start
- `docs/opentelemetry-architecture.md` - Architecture diagram
- `OPENTELEMETRY_SUMMARY.md` - Implementation summary

## Example Output

When running with console exporter:

```json
{
  "name": "create_oai_chat_completion",
  "attributes": {
    "model": "gpt-4",
    "temperature": 1.3,
    "duration_ms": 1234.5,
    "response_length": 156,
    "finish_reason": "stop"
  },
  "status": "OK"
}
```

Metrics every 60 seconds:
```
baiiab.api_calls: 3
baiiab.api_duration: [1234.5, 2345.6, 987.3]
baiiab.user_interactions: 12
baiiab.offline_fallbacks: 1
```

## Support

For questions or issues:
1. Check the documentation in `docs/`
2. Run `python3 helpers/test_otel.py` to verify setup
3. Review logs for "OpenTelemetry initialized" message

## Learn More

- [OpenTelemetry Python Docs](https://opentelemetry.io/docs/instrumentation/python/)
- [OTLP Specification](https://opentelemetry.io/docs/reference/specification/protocol/)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)

---

Ready to get full visibility into your Baiiab interactions? Start with `docs/opentelemetry-quickstart.md`! 🚀
