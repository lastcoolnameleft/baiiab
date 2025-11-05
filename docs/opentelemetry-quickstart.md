# OpenTelemetry Quick Start

Get started with OpenTelemetry monitoring in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and ensure these lines are present:

```bash
OTEL_ENABLED=true
OTEL_CONSOLE_EXPORTER=true  # This will be auto-disabled in simulator
```

## Step 3: Run the Simulator

```bash
python3 helpers/simulator.py
```

**Note**: The simulator automatically redirects telemetry output to `logs/simulator_telemetry.log` to prevent interference with the LCD display. The telemetry status is shown at the top of the screen.

## Step 4: Interact and Watch

1. Navigate the menu using `w`/`s` or arrow keys
2. Select an item with `e` or Enter
3. Watch the telemetry output in your console!

You'll see spans like:

```json
{
    "name": "simulator.navigation.next",
    "context": {...},
    "kind": "SpanKind.INTERNAL",
    "start_time": "2025-11-04T12:34:56.789Z",
    "end_time": "2025-11-04T12:34:56.792Z"
}
```

And metrics exported every 60 seconds:

```
baiiab.simulator_interactions: 5
baiiab.api_calls: 2
baiiab.api_duration: [1234.5, 2456.7]
```

## What You're Seeing

### Traces (Spans)
- **Navigation events**: When you move through the menu
- **Selection events**: When you select an action
- **API calls**: When OpenAI is called, including timing and response details
- **Offline fallbacks**: When offline responses are used

### Metrics
- **Interaction counters**: How many times each action was taken
- **API metrics**: Call counts, durations, error rates
- **Offline fallback rate**: How often API calls failed

## Next Steps

### Option A: Try with Real API Calls

Configure your Azure OpenAI credentials in `.env`, then select a menu item. You'll see:

```json
{
    "name": "create_oai_chat_completion",
    "attributes": {
        "model": "gpt-4",
        "temperature": 1.3,
        "duration_ms": 1234.5,
        "response_length": 156,
        "finish_reason": "stop"
    }
}
```

### Option B: Set Up Jaeger for Visual Traces

Run Jaeger:

```bash
docker run -d --name jaeger \
  -p 4317:4317 \
  -p 16686:16686 \
  jaegertracing/all-in-one:latest
```

Update `.env`:

```bash
OTEL_CONSOLE_EXPORTER=false
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

View traces at: http://localhost:16686

### Option C: Read Full Documentation

See `docs/opentelemetry.md` for:
- Complete configuration options
- Production setup guides
- Dashboard examples
- Troubleshooting tips
- Query examples

## Disable Telemetry

To turn off telemetry:

```bash
OTEL_ENABLED=false
```

Or simply don't install the OpenTelemetry packages - the code will gracefully degrade.

## Troubleshooting

**No output?**
- Check `OTEL_ENABLED=true` in `.env`
- Verify packages installed: `pip list | grep opentelemetry`

**Import errors?**
- Run `pip install -r requirements.txt` again

**Too verbose?**
- Metrics export every 60 seconds by default
- Set `OTEL_CONSOLE_EXPORTER=false` to disable console output

## Success! 🎉

You now have full observability into your Baiiab interactions, including:
- ⏱️ Response times
- 📊 Usage patterns
- 🐛 Error tracking
- 🔄 Offline fallback rates
- 👤 User interaction flows

For production deployment and advanced configurations, see the full documentation in `docs/opentelemetry.md`.
