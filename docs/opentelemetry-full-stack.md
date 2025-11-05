# OpenTelemetry Full Stack Setup (Traces + Metrics)

This guide shows how to collect both traces and metrics from your Baiiab application.

## Architecture

```
Baiiab App → OpenTelemetry Collector → Jaeger (traces) + Prometheus (metrics)
```

## Quick Start

### 1. Stop existing Jaeger container
```bash
docker stop jaeger
docker rm jaeger
```

### 2. Start the full observability stack
```bash
docker-compose -f docker-compose-otel.yaml up -d
```

This starts:
- **Jaeger** (port 16686) - Trace visualization
- **OpenTelemetry Collector** (ports 4317/4318) - Receives traces + metrics
- **Prometheus** (port 9090) - Metrics storage and querying
- **Grafana** (port 3000) - Dashboards and visualization

### 3. Update your .env file
```bash
# Change these settings:
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
OTEL_TRACES_ONLY=false
```

### 4. Run your application
```bash
python3 helpers/simulator.py
# or
python3 service.py
```

## Access UIs

- **Grafana (Dashboards)**: http://localhost:3000 (admin/admin)
- **Jaeger (Traces)**: http://localhost:16686
- **Prometheus (Metrics)**: http://localhost:9090

## Viewing Your Data

### Dashboards in Grafana (Recommended)
1. Open http://localhost:3000
2. Login: `admin` / `admin`
3. Go to Dashboards → "Baiiab - AI in a Box"
4. View real-time metrics:
   - API call rates
   - Response times
   - Error rates
   - Offline fallbacks

The dashboard auto-refreshes every 5 seconds and shows the last 30 minutes of data.

### Traces in Jaeger
1. Open http://localhost:16686
2. Select service: `baiiab`
3. Click "Find Traces"
4. In Grafana, you can also explore traces by clicking on trace IDs

### Metrics in Prometheus
1. Open http://localhost:9090
2. Go to Graph tab
3. Try these queries:
   ```promql
   # API call rate
   rate(baiiab_api_calls_total[1m])
   
   # Average API duration
   rate(baiiab_api_duration_sum[1m]) / rate(baiiab_api_duration_count[1m])
   
   # Error rate
   rate(baiiab_errors_total[1m])
   
   # Offline fallback count
   baiiab_offline_fallbacks_total
   ```

## Available Metrics

The application exports these metrics:

- `baiiab.api_calls` - Number of API calls made
- `baiiab.offline_fallbacks` - Number of offline fallback responses  
- `baiiab.api_duration` - API call duration histogram (ms)
- `baiiab.errors` - Number of errors encountered
- `baiiab.rotary_actions` - Rotary encoder interactions (from service.py)
- `baiiab.button_presses` - Button press events (from service.py)

## Troubleshooting

### Ports already in use
If port 4317 or 4318 is busy:
```bash
# Find what's using the port
lsof -i :4317
lsof -i :4318

# Stop the process or change the port in docker-compose-otel.yaml
```

### Not seeing metrics in Prometheus
1. Check OpenTelemetry Collector logs:
   ```bash
   docker logs otel-collector
   ```

2. Verify metrics endpoint:
   ```bash
   curl http://localhost:8889/metrics
   ```

3. Check Prometheus targets:
   - Open http://localhost:9090/targets
   - Ensure `otel-collector` target is UP

### Not seeing traces in Jaeger
1. Check if traces are reaching collector:
   ```bash
   docker logs otel-collector | grep -i trace
   ```

2. Check Jaeger logs:
   ```bash
   docker logs jaeger
   ```

## Switching Back to Traces-Only Mode

If you only want traces (Jaeger only, no Prometheus):

1. Update `.env`:
   ```bash
   OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
   OTEL_TRACES_ONLY=true
   ```

2. Stop full stack and run Jaeger only:
   ```bash
   docker-compose -f docker-compose-otel.yaml down
   docker run -d --name jaeger \
     -p 16686:16686 \
     -p 4317:4317 \
     -e COLLECTOR_OTLP_ENABLED=true \
     jaegertracing/all-in-one:latest
   ```

## Production Considerations

For production deployments, consider:

1. **Grafana** - Better visualization than Prometheus UI
2. **Persistent storage** - Configure volumes for Prometheus data
3. **Authentication** - Add security to Jaeger/Prometheus UIs
4. **Resource limits** - Set memory/CPU limits in docker-compose
5. **Sampling** - Configure trace sampling for high-volume apps
6. **Alerting** - Set up Prometheus alerting rules

## Next Steps

- Add Grafana for dashboards: https://grafana.com/docs/grafana/latest/getting-started/
- Configure alerting: https://prometheus.io/docs/alerting/latest/overview/
- Explore OpenTelemetry Collector processors: https://opentelemetry.io/docs/collector/configuration/
