# Simulator Display Fix - Telemetry Separation

## Problem
When running the simulator with OpenTelemetry enabled, the telemetry console output (spans and metrics) was interfering with the LCD display rendering, causing a garbled screen when navigating the menu.

## Solution
Separated telemetry output from the LCD display by:

1. **Custom File Exporters**: Created `FileSpanExporter` and `FileMetricExporter` classes that write telemetry directly to JSON log files
2. **Automatic File Export**: Simulator automatically uses file exporters instead of console exporters
3. **Enhanced display layout**: LCD display now has a clear border and dedicated telemetry status area
4. **Visual separation**: Added distinct sections for telemetry status, LCD display, and controls

## Changes Made

### 1. Custom File Exporters (`otel_config.py`)
- **`FileSpanExporter`**: Custom OpenTelemetry span exporter that writes spans to JSON log file
- **`FileMetricExporter`**: Custom metric exporter that writes metrics to JSON log file
- Enhanced `setup_telemetry()` with `use_file_exporter` and `file_path` parameters
- Each span logged as JSON with timestamp, name, trace_id, duration, attributes, status

### 2. Telemetry File Export (`helpers/simulator.py`)
- Automatically uses file exporters instead of console exporters
- Writes telemetry to `logs/simulator_telemetry.log` in JSON format
- Shows telemetry status with file path at top of screen
- No console output to interfere with LCD display

### 2. Enhanced Display Layout
**Before:**
```
┌────────────────────┐
│ LCD content        │
└────────────────────┘

Controls:
  [w] or [↑] - Previous
  ...
```

**After:**
```
╔══════════════════════════════════════════════════════════════════════════════╗
║ [Telemetry: ENABLED] → logs/simulator_telemetry.log                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

╔════════════════════╗
║   LCD DISPLAY      ║
╠════════════════════╣
║ Welcome to         ║
║ BAIIAB Simulator   ║
║ > Advice           ║
║   Fake Facts       ║
╚════════════════════╝

────────────────────────────────────────────────────────────────────────────────
CONTROLS:
  [w] or [↑] - Turn knob counter-clockwise (previous item)
  [s] or [↓] - Turn knob clockwise (next item)
  [e] or [Enter] - Press knob (select)
  [q] - Quit simulator
────────────────────────────────────────────────────────────────────────────────

Command: 
```

### 3. Updated `.gitignore`
Added telemetry log files to gitignore:
```
# OpenTelemetry logs
logs/simulator_telemetry.log
logs/*.log
```

### 4. Updated Documentation
- Updated `docs/opentelemetry-quickstart.md` to mention automatic telemetry redirection
- Noted that simulator shows telemetry status at top of screen

## Benefits

✅ **Clean LCD Display**: No interference from telemetry output  
✅ **Visible Telemetry Status**: Always know if telemetry is enabled and where logs go  
✅ **Full Telemetry Data**: All telemetry still captured, just in a log file  
✅ **Better UX**: Clear visual separation of different UI elements  
✅ **Professional Look**: Enhanced borders and layout  

## Viewing Telemetry While Using Simulator

### Option 1: Tail the log file (recommended)
In a separate terminal, watch telemetry in real-time:
```bash
tail -f logs/simulator_telemetry.log
```

Each span is logged as JSON:
```json
{"timestamp": "2025-11-04T12:34:56.789", "name": "simulator.navigation.next", "trace_id": "abc123...", "span_id": "def456...", "start_time": 1730000000, "end_time": 1730000001, "duration_ms": 1.23, "attributes": {"interaction_type": "navigation_down"}, "status": "OK"}
```

### Option 2: Pretty-print with jq
```bash
tail -f logs/simulator_telemetry.log | jq '.'
```

### Option 3: View log file after session
```bash
cat logs/simulator_telemetry.log | jq '.'
```

### Option 4: Use an observability backend
Configure OTLP endpoint in `.env` and view in Jaeger, Grafana, etc. The file export and OTLP export can run simultaneously.

## Files Modified
- `helpers/simulator.py` - Added telemetry redirection and enhanced display
- `.gitignore` - Added log file exclusions
- `docs/opentelemetry-quickstart.md` - Updated documentation

## Testing

Run the simulator and navigate through menus:
```bash
python3 helpers/simulator.py
```

The display should be clean with:
- Telemetry status at top
- LCD display in the middle (with box border)
- Controls at bottom
- No garbled output when navigating

To see telemetry data:
```bash
tail -f logs/simulator_telemetry.log
```

## Notes

- The `OTEL_CONSOLE_EXPORTER` setting is temporarily disabled only for the simulator
- Physical hardware service (`service.py`) is unaffected and uses configured settings
- Telemetry data is still fully captured, just written to a file instead of stdout
- The log file location is shown at the top of the simulator screen
