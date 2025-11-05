# Example Grafana Dashboard Queries

This file contains example queries for creating Grafana dashboards to visualize Baiiab telemetry.

## Prerequisites

- Prometheus configured to scrape OTLP metrics
- Jaeger or Tempo for traces
- Grafana connected to both data sources

## Dashboard Panels

### 1. API Performance Overview

#### Average API Response Time
```promql
avg(baiiab_api_duration_milliseconds_sum / baiiab_api_duration_milliseconds_count)
```

#### API Call Rate (per minute)
```promql
rate(baiiab_api_calls_total[5m]) * 60
```

#### P95 Response Time
```promql
histogram_quantile(0.95, 
  rate(baiiab_api_duration_milliseconds_bucket[5m])
)
```

#### P99 Response Time
```promql
histogram_quantile(0.99, 
  rate(baiiab_api_duration_milliseconds_bucket[5m])
)
```

### 2. Error Monitoring

#### Error Rate
```promql
rate(baiiab_errors_total[5m])
```

#### Errors by Type
```promql
sum by (error_type) (baiiab_errors_total)
```

#### Error Percentage
```promql
(
  rate(baiiab_errors_total[5m]) / 
  rate(baiiab_api_calls_total[5m])
) * 100
```

### 3. Offline Fallback Monitoring

#### Offline Fallback Count
```promql
baiiab_offline_fallbacks_total
```

#### Offline Fallback Rate
```promql
rate(baiiab_offline_fallbacks_total[5m])
```

#### Offline Fallback Percentage
```promql
(
  sum(baiiab_offline_fallbacks_total) /
  (sum(baiiab_api_calls_total) + sum(baiiab_offline_fallbacks_total))
) * 100
```

### 4. User Interaction Metrics

#### Total Interactions
```promql
baiiab_user_interactions_total
```

#### Interaction Rate (per hour)
```promql
rate(baiiab_user_interactions_total[1h]) * 3600
```

#### Interactions by Type
```promql
sum by (interaction_type) (baiiab_user_interactions_total)
```

#### Most Popular Topics
```promql
topk(5, sum by (topic) (baiiab_user_interactions_total{interaction_type="action_selected"}))
```

#### Most Popular Subtopics
```promql
topk(10, sum by (topic, subtopic) (baiiab_user_interactions_total{interaction_type="action_selected"}))
```

### 5. Menu Navigation

#### Navigation Events
```promql
baiiab_menu_navigation_total
```

#### Clockwise vs Counter-Clockwise
```promql
sum by (direction) (baiiab_menu_navigation_total)
```

### 6. System Health

#### API Success Rate
```promql
(
  (sum(baiiab_api_calls_total) - sum(baiiab_errors_total)) /
  sum(baiiab_api_calls_total)
) * 100
```

#### Uptime (based on interaction activity)
```promql
up{job="baiiab"}
```

## Example Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                        Baiiab Dashboard                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ API Success │  │  Avg Resp   │  │   Total     │            │
│  │    Rate     │  │    Time     │  │ Interactions│            │
│  │   98.5%     │  │   1.2s      │  │    1,234    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
├─────────────────────────────────────────────────────────────────┤
│  API Response Time (P50, P95, P99)                              │
│  [Line graph showing response time percentiles over time]       │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────┐  ┌────────────────────────────┐  │
│  │ User Interactions        │  │  Popular Topics            │  │
│  │ [Time series graph]      │  │  [Bar chart]               │  │
│  └──────────────────────────┘  └────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────┐  ┌────────────────────────────┐  │
│  │ Error Rate               │  │  Offline Fallback %        │  │
│  │ [Time series graph]      │  │  [Gauge]                   │  │
│  └──────────────────────────┘  └────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  Recent Errors                                                  │
│  [Table with timestamp, error_type, message]                   │
└─────────────────────────────────────────────────────────────────┘
```

## Alert Rules

### High Error Rate
```yaml
alert: HighErrorRate
expr: |
  (
    rate(baiiab_errors_total[5m]) /
    rate(baiiab_api_calls_total[5m])
  ) * 100 > 5
for: 5m
labels:
  severity: warning
annotations:
  summary: "High error rate detected"
  description: "Error rate is {{ $value }}% (threshold: 5%)"
```

### Slow API Response
```yaml
alert: SlowAPIResponse
expr: |
  histogram_quantile(0.95,
    rate(baiiab_api_duration_milliseconds_bucket[5m])
  ) > 3000
for: 10m
labels:
  severity: warning
annotations:
  summary: "API response time is slow"
  description: "P95 latency is {{ $value }}ms (threshold: 3000ms)"
```

### High Offline Fallback Rate
```yaml
alert: HighOfflineFallbackRate
expr: |
  (
    sum(baiiab_offline_fallbacks_total) /
    (sum(baiiab_api_calls_total) + sum(baiiab_offline_fallbacks_total))
  ) * 100 > 10
for: 5m
labels:
  severity: warning
annotations:
  summary: "High offline fallback rate"
  description: "{{ $value }}% of responses are using offline fallback"
```

### No Recent Activity
```yaml
alert: NoRecentActivity
expr: |
  rate(baiiab_user_interactions_total[30m]) == 0
for: 1h
labels:
  severity: info
annotations:
  summary: "No user activity detected"
  description: "No interactions in the last hour"
```

## Trace Queries (Jaeger/Tempo)

### Find Slow Requests
```
duration > 3s
```

### Find Failed API Calls
```
service="baiiab" AND span.name="create_oai_chat_completion" AND status="ERROR"
```

### Find Requests by Topic
```
service="baiiab" AND topic="Advice"
```

### Find Offline Fallbacks
```
service="baiiab" AND response_source="offline"
```

### Trace User Journey
```
service="baiiab" AND root.span.name="button.press"
```

## Importing into Grafana

1. Copy these queries into new panels
2. Adjust time ranges and refresh intervals
3. Set appropriate thresholds for alerts
4. Customize colors and visualizations
5. Save and share your dashboard!

## Tips

- Use variables for filtering by topic/subtopic
- Create separate dashboards for development vs production
- Set up email/Slack notifications for critical alerts
- Use annotations to mark deployments or incidents
- Create a mobile-friendly view for on-call monitoring

For more information on Grafana configuration, see:
https://grafana.com/docs/
