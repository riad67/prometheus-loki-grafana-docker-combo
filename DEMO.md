# Demo and presentation guide

## Before recording

1. Start the stack and verify the dashboard, Loki query, Prometheus targets, and the alert flow on your machine. Allow time for five-minute rate windows. Resolve failures before recording; do not imply an untested feature worked.
2. Use only generated data. Close unrelated tabs, hide passwords and notifications, and keep the browser at a readable zoom. Do not show `.env`, private host paths, or real customer data.
3. Capture at 1080p or higher with clear audio. Use a consistent cursor and pause on each result. Prepare a brief architecture slide or display the README diagram.

## Suggested 4–5 minute storyboard

| Time | Visual | Narration / evidence |
| --- | --- | --- |
| 0:00–0:30 | Title and architecture | State the problem, the synthetic dataset and the single-host lab scope. |
| 0:30–1:15 | Compose services and diagram | Trace generator → collector → Loki → Grafana and the independent exporter → Prometheus path. |
| 1:15–2:15 | Grafana dashboard | Explain rates, HTTP status distribution and response bytes. Point out that status codes alone do not establish an attack. |
| 2:15–3:15 | Grafana Explore | Run `{job="generated-logs"} | json`; inspect a line and compare a LogQL rate with a dashboard view. |
| 3:15–4:15 | Alert state | Show a previously verified missing-log alert and recovery. If the wait is edited, disclose the elapsed time and demonstrate the actual timestamps. |
| 4:15–5:30 | Architecture and limitations | Discuss the trust boundaries, no external notification, local-only configuration, single-host failure domain and collector and dependency maintenance. |

## Questions to prepare for

- How are labels selected, and what happens if high-cardinality values are indexed?
- What happens when a collector, exporter, object store or host fails? Which data is replayed or lost?
- Which trust boundaries need authentication, encryption, authorization and audit logs?
- How would you evaluate security detection against a labeled baseline, and report false positives and detection delay?
- How would retention, privacy, cost and incident-response requirements affect design?

