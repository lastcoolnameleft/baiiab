# OpenTelemetry Instrumentation Map

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Baiiab System                                │
│                                                                      │
│  ┌────────────────────┐         ┌──────────────────────┐           │
│  │   Physical Box     │         │     Simulator        │           │
│  │   (service.py)     │         │   (simulator.py)     │           │
│  └────────────────────┘         └──────────────────────┘           │
│           │                               │                          │
│           │ Rotary Encoder               │ Keyboard Input           │
│           │ Button Press                 │ (w/s/e keys)             │
│           │                               │                          │
│           ├─ SPAN: rotary_encoder.*      ├─ SPAN: simulator.navigation.*
│           ├─ SPAN: button.press          ├─ SPAN: simulator.select
│           ├─ METRIC: menu_navigation     ├─ METRIC: simulator_interactions
│           └─ METRIC: user_interactions   │
│                      │                    │
│                      └────────┬───────────┘
│                               │
│                               ▼
│                    ┌──────────────────────┐
│                    │   action_callback    │
│                    │  (topic + subtopic)  │
│                    └──────────────────────┘
│                               │
│                               │ SPAN: action_callback
│                               │ METRIC: user_interactions
│                               │
│                               ▼
│                    ┌──────────────────────┐
│                    │    Baiiab Class      │
│                    │   (Baiiab.py)        │
│                    └──────────────────────┘
│                         │           │
│               ┌─────────┴───────────┴─────────┐
│               │                                │
│               ▼                                ▼
│    ┌────────────────────┐         ┌────────────────────┐
│    │  OpenAI API Call   │         │  Offline Fallback  │
│    │  (Azure OpenAI)    │         │   (JSON files)     │
│    └────────────────────┘         └────────────────────┘
│               │                                │
│               │ SPAN: create_oai_chat_*       │ SPAN: get_offline_advice
│               │ METRIC: api_calls             │ METRIC: offline_fallbacks
│               │ METRIC: api_duration          │
│               │ METRIC: errors                │
│               │                                │
│               └────────────┬───────────────────┘
│                            │
│                            ▼
│                    ┌──────────────┐
│                    │   Response   │
│                    └──────────────┘
│                            │
│                            ▼
│                    ┌──────────────┐
│                    │  Print/Display│
│                    └──────────────┘
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────┐
         │     OpenTelemetry Exporters          │
         ├──────────────────────────────────────┤
         │  Console Exporter → stdout            │
         │  OTLP Exporter → Observability Backend│
         └──────────────────────────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────┐
         │   Observability Platforms            │
         ├──────────────────────────────────────┤
         │  • Jaeger (traces)                   │
         │  • Prometheus (metrics)              │
         │  • Grafana (visualization)           │
         │  • Azure Monitor                     │
         │  • Datadog                           │
         │  • Grafana Cloud                     │
         └──────────────────────────────────────┘
```

## Metrics Collected

### Counters (cumulative totals)
```
baiiab.api_calls                    # OpenAI API requests
baiiab.offline_fallbacks            # Offline response usage
baiiab.errors                       # Errors by type
baiiab.user_interactions            # User actions
baiiab.menu_navigation              # Menu movements
baiiab.simulator_interactions       # Simulator usage
```

### Histograms (distributions)
```
baiiab.api_duration                 # API response times (ms)
```

## Spans Collected (with timing)

### User Interactions
- `rotary_encoder.clockwise` - Physical knob turn right
- `rotary_encoder.counter_clockwise` - Physical knob turn left
- `button.press` - Physical button press
- `simulator.navigation.next` - Simulator down navigation
- `simulator.navigation.previous` - Simulator up navigation
- `simulator.select` - Simulator selection

### Business Logic
- `action_callback` - Full action execution flow
  - Attributes: topic, subtopic, response_source
- `simulator.action_callback` - Simulator action execution
  - Attributes: topic, subtopic, mode

### API & Data Operations
- `create_oai_chat_completion` - OpenAI API call
  - Attributes: model, temperature, duration_ms, response_length, finish_reason
  - Records: timing, success/failure, exception details
- `get_offline_advice` - Offline fallback retrieval
  - Attributes: topic, subtopic, response_length

## Trace Context Flow

```
Root Span: button.press (234ms)
  └─ Child: action_callback (232ms)
      ├─ Child: create_oai_chat_completion (1234ms)
      │   └─ Attributes: {
      │       model: "gpt-4",
      │       duration_ms: 1234.5,
      │       response_length: 156,
      │       status: "OK"
      │     }
      └─ Result: printed to device
```

Or with fallback:

```
Root Span: simulator.select (45ms)
  └─ Child: simulator.action_callback (44ms)
      ├─ Child: create_oai_chat_completion (FAILED - 3000ms timeout)
      │   └─ Exception: TimeoutError
      └─ Child: get_offline_advice (2ms)
          └─ Attributes: {
              topic: "Advice",
              subtopic: "Good",
              response_length: 87
            }
```

## Attributes By Span Type

### Navigation Spans
- `direction`: "clockwise" | "counter_clockwise"
- `interaction_type`: "navigation_up" | "navigation_down" | "select"

### Action Spans
- `topic`: e.g., "Advice", "Joke", "Insult"
- `subtopic`: e.g., "Good", "Bad", "Silly"
- `response_source`: "api" | "offline"
- `mode`: "physical" | "simulator"

### API Spans
- `model`: Azure OpenAI deployment name
- `temperature`: Model temperature setting
- `max_tokens`: Token limit
- `system_prompt`: First 100 chars of system prompt
- `duration_ms`: Call duration in milliseconds
- `response_length`: Length of response text
- `finish_reason`: "stop" | "length" | "content_filter"
- `error_type`: Exception class name if failed

### Offline Spans
- `topic`: Content category
- `subtopic`: Specific type
- `response_length`: Length of response text

## Example Queries

### Find Slow API Calls
```
duration_ms > 3000 AND span.name = "create_oai_chat_completion"
```

### Most Popular Topics
```
GROUP BY topic COUNT(*) FROM span.name = "action_callback" ORDER BY count DESC
```

### Error Analysis
```
status = "ERROR" GROUP BY error_type
```

### User Journey
```
TRACE WHERE root.span.name = "button.press" AND duration > 5000ms
```

This visualization shows every point where telemetry data is collected, making it easy to understand what's being tracked and where!
