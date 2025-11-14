# OpenTelemetry File-Based Export for Raspberry Pi

This document explains how to use file-based telemetry export on resource-constrained devices like the Raspberry Pi Zero W.

## Why File-Based Export?

Real-time OTLP export can cause performance issues on the Raspberry Pi Zero W:
- HTTP/network overhead during I2C operations causes timing issues
- CPU cycles spent on serialization and network I/O
- Can lead to I2C bus errors with LCD displays

**Solution:** Write telemetry to a file, then upload it separately using a background service.

## Configuration

### Main Application (.env)

```bash
# Enable telemetry with file export
OTEL_ENABLED=true
OTEL_CONSOLE_EXPORTER=false
OTEL_FILE_EXPORTER=true
OTEL_FILE_PATH=/home/pi/baiiab/logs/telemetry.jsonl

# Disable direct OTLP export from main app
# (Comment out or leave blank)
#OTEL_EXPORTER_OTLP_ENDPOINT=
```

### Upload Service (.env)

```bash
# Upload service configuration
OTEL_UPLOAD_ENABLED=true
OTEL_UPLOAD_INTERVAL=60  # Upload every 60 seconds
OTEL_EXPORTER_OTLP_ENDPOINT=your-endpoint:443
OTEL_EXPORTER_OTLP_HEADERS=Authorization=ApiKey xxx
OTEL_RESOURCE_ATTRIBUTES=service.name=baiiab,service.version=1.0
```

## Installation on Raspberry Pi

### 1. Copy the service file

```bash
sudo cp misc/otel-upload.service /etc/systemd/system/
```

### 2. Update the service file paths

Edit `/etc/systemd/system/otel-upload.service` if your paths differ from defaults.

### 3. Enable and start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable otel-upload.service
sudo systemctl start otel-upload.service
```

### 4. Check service status

```bash
sudo systemctl status otel-upload.service
```

### 5. View logs

```bash
# Live logs
sudo journalctl -u otel-upload.service -f

# Recent logs
sudo journalctl -u otel-upload.service -n 50
```

## How It Works

1. **Main Application** (Baiiab.py/service.py):
   - Creates traces and metrics as normal
   - Writes them to `logs/telemetry.jsonl` file
   - Minimal overhead - just file I/O

2. **Upload Service** (helpers/otel_upload_service.py):
   - Runs continuously in background
   - Every 60 seconds (configurable):
     - Reads telemetry file
     - Uploads to OTLP endpoint
     - Archives the file
   - Keeps last 10 archives for debugging

3. **Telemetry reaches Elastic Cloud**:
   - Slightly delayed (up to 60 seconds)
   - No performance impact on main application
   - Reliable delivery with retry logic

## File Format

The telemetry file uses JSON Lines format (`.jsonl`):
- One JSON object per line
- Spans and metrics stored together
- Easy to parse and debug

Example:
```json
{"timestamp": "2025-11-11T10:00:00", "name": "user_interaction", "trace_id": "..."}
{"timestamp": "2025-11-11T10:00:01", "name": "api_call", "trace_id": "..."}
```

## Troubleshooting

### Service won't start

```bash
# Check service status
sudo systemctl status otel-upload.service

# Check for errors in logs
sudo journalctl -u otel-upload.service -n 100
```

### No data being uploaded

1. Check file exists: `ls -lh /home/pi/baiiab/logs/telemetry.jsonl`
2. Check file has data: `head /home/pi/baiiab/logs/telemetry.jsonl`
3. Check upload service is running: `sudo systemctl status otel-upload.service`
4. Check endpoint configuration: `grep OTEL_EXPORTER_OTLP_ENDPOINT .env`

### Too many archive files

The service keeps the last 10 archives. To clean up manually:
```bash
rm /home/pi/baiiab/logs/telemetry.jsonl.*
```

## Switching Back to Real-Time Export

To switch back to real-time export (e.g., on more powerful hardware):

```bash
# In .env
OTEL_FILE_EXPORTER=false
OTEL_EXPORTER_OTLP_ENDPOINT=your-endpoint:443
OTEL_EXPORTER_OTLP_HEADERS=Authorization=ApiKey xxx

# Stop upload service
sudo systemctl stop otel-upload.service
sudo systemctl disable otel-upload.service
```

## Performance Impact

**File-based export:**
- ✅ Minimal CPU overhead (just file writes)
- ✅ No network I/O during critical operations
- ✅ No timing issues with I2C/LCD
- ⚠️ Slight delay in data visibility (up to 60 seconds)

**Real-time export:**
- ⚠️ Network I/O during telemetry calls
- ⚠️ Can cause timing issues on Pi Zero W
- ⚠️ Higher CPU usage
- ✅ Immediate data visibility
