```json
{
  "id": "1t1twu3",
  "author": "trolleid",
  "category": "gift-promotion",
  "subreddit": "PrometheusMonitoring",
  "created_utc": 1777737870.0,
  "created_at": "2026-05-02T18:04:30+02:00",
  "permalink": "https://www.reddit.com/r/PrometheusMonitoring/comments/1t1twu3/i_added_special_prometheus_support_to_this/",
  "link_url": "https://github.com/LukasNiessen/kubernetes-skill",
  "is_self": false,
  "crosspost_parent": null,
  "removed_by_category": "reddit",
  "body_state": "intact",
  "eligible_for_voice": true,
  "archive_only": false,
  "reference_use": "historical_voice_only",
  "retrieved_on": "2026-11-08",
  "source": "Reddit authenticated submitted listing",
  "title_sha256": "a4ee1114c52bf6526aea1252bf1a7aea7c294ace3d4e435577a89a09179fe796",
  "body_sha256": "d4082efd0baeba3dd7292a1cd21d15c542a56428c0e811a25bd61382443feb27",
  "body_characters": 2428
}
```

# Original title

I added special Prometheus support to this Kubernetes Skill (Claude Code and Codex)

## Original body

I added dedicated observability-stack support to KubeShark.

**Mini recap:**

KubeShark is my Kubernetes skill for Claude Code and Codex.

It helps AI agents generate, review, and refactor Kubernetes manifests without falling into the usual LLM traps: missing security contexts, deprecated API versions, broken selectors, wildcard RBAC, unsafe probes, missing resource requests, and rollout configs that look okay but fail under real traffic.

The important part is that KubeShark is failure-mode-first. It does not just tell the model “write good Kubernetes”. It forces the model to reason about what can go wrong before it generates YAML, and then return validation and rollback guidance as part of the answer.

That matters a lot with Kubernetes, because many bad manifests are accepted by the API server and only fail later at runtime.

Repo: [https://github.com/LukasNiessen/kubernetes-skill](https://github.com/LukasNiessen/kubernetes-skill)

\---

**Now what’s new:**

KubeShark now has special dedicated observability-stack support.

When the task involves Prometheus Operator, ServiceMonitor, PodMonitor, PrometheusRule, OpenTelemetry Collector, Loki, Grafana, Tempo, Datadog-style agents, metrics, logs, traces, or telemetry pipelines, KubeShark switches into observability-aware guidance.

This matters because observability resources often apply successfully while doing nothing.

Common LLM mistakes include:

* creating a ServiceMonitor that matches Deployment labels instead of Service labels
* referencing a numeric port when the monitor expects a named Service port
* forgetting that Prometheus must select the monitor
* deploying OpenTelemetry receivers in duplicate
* choosing Loki monolithic mode for serious production volume
* creating high-cardinality log labels
* putting datasource credentials in ConfigMaps

Example guidance KubeShark now keeps in mind:

    apiVersion: monitoring.coreos.com/v1
    kind: ServiceMonitor
    metadata:
      name: app
      labels:
        release: kube-prometheus-stack
    spec:
      selector:
        matchLabels:
          app.kubernetes.io/name: app
      endpoints:
        - port: metrics

It also knows to check the boring but critical details: selectors, named ports, CRD presence, scrape discovery, telemetry pipelines, durable storage, and alert hygiene.

So instead of generic Kubernetes advice, you get observability-aware manifest generation and review.
