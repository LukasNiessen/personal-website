```json
{
  "id": "1t1u3pg",
  "author": "trolleid",
  "category": "project-showcase",
  "subreddit": "devops",
  "created_utc": 1777738313.0,
  "created_at": "2026-05-02T18:11:53+02:00",
  "permalink": "https://www.reddit.com/r/devops/comments/1t1u3pg/claude_caude_codex_agent_skill_for_kubernetes/",
  "link_url": "https://github.com/LukasNiessen/kubernetes-skill",
  "is_self": false,
  "crosspost_parent": null,
  "removed_by_category": "moderator",
  "body_state": "intact",
  "eligible_for_voice": true,
  "archive_only": false,
  "reference_use": "historical_voice_only",
  "retrieved_on": "2026-11-08",
  "source": "Reddit authenticated submitted listing",
  "title_sha256": "f22fe0e62b7695ac2f95c19e0189ff2e3d9eaed06c330b0f09325faa2c50edbe",
  "body_sha256": "5d59ea7ead1826b44d67db5d31e1b24aa7b3b11e29e43bb50b694bf96cab4eee",
  "body_characters": 4437
}
```

# Original title

Claude Caude / Codex Agent Skill for Kubernetes

## Original body

I built KubeShark, a Kubernetes skill for Claude Code and Codex.

The idea is simple: LLMs hallucinate a lot when writing Kubernetes.

They generate deprecated API versions, forget security contexts, create Services that select no pods, add wildcard RBAC, misconfigure probes, omit resource requests, and produce rollout configs that look fine but fail under real traffic.

And Kubernetes is especially unforgiving here, because many mistakes are not rejected immediately. A wrong Service selector applies successfully. A broken NetworkPolicy applies successfully. A bad liveness probe applies successfully, and then restarts your pods forever.

So KubeShark is not just a big Kubernetes prompt or a dumped best-practices document. It is a failure-mode-first workflow for AI agents.

Before generating YAML, the agent has to reason about what can go wrong:

* insecure workload defaults
* resource starvation
* network exposure
* privilege sprawl
* fragile rollouts
* API drift

Only after that does it generate manifests, Helm charts, Kustomize overlays, RBAC, NetworkPolicies, policies, or validation steps.

That matters a lot in Claude Code / Codex times, because AI agents are very good at generating plausible infrastructure code, but they are also very good at skipping the boring operational details that make the difference between “applies” and “works”. KubeShark tries to make those details unavoidable.

It defaults to secure workload settings, thinks about Pod Security Standards, checks cross-resource consistency, watches label/selector/port alignment, avoids deprecated APIs, and includes validation and rollback guidance.

It is also intentionally token-lean. Most skills become huge walls of text very quickly. KubeShark does the opposite.

The main `SKILL.md` stays compact and procedural. The deeper knowledge lives in focused reference files that are loaded only when relevant. So a task about probes does not need to load RBAC guidance. A task about Helm does not need to load NetworkPolicy guidance. A plain Deployment review does not need to load every cloud provider’s quirks.

This is especially important for Kubernetes, because the ecosystem is huge: workloads, networking, storage, security, GitOps, policy engines, observability stacks, cloud-specific controllers, and so on. If you load everything, you don’t just waste tokens. You also increase the chance that the agent mixes concepts that do not belong together.

KubeShark is designed to avoid that.

Repo: [https://github.com/LukasNiessen/kubernetes-skill](https://github.com/LukasNiessen/kubernetes-skill)

A few examples of what KubeShark is meant to catch:

* a Service selector that does not match the Deployment labels
* an Ingress using an API version removed in modern Kubernetes
* a Deployment running as root with no security context
* a liveness probe checking an external database
* a ClusterRoleBinding where a RoleBinding would be enough
* a StatefulSet that assumes PVCs disappear on scale-down
* a Helm template that renders valid YAML with the wrong Kubernetes API
* a Kustomize patch that silently targets the wrong resource

The goal is not to make the agent sound more Kubernetes-fluent. The goal is to make the output safer.

Valid YAML is not enough. Production-ready Kubernetes needs security defaults, resource discipline, rollout safety, policy awareness, and validation. That is what KubeShark is built for.

I’ve also added special dedicated support for the platform/tooling contexts where generic Kubernetes advice usually breaks down:

* AWS / EKS
* Azure / AKS
* Google Cloud / GKE
* OpenShift
* GitOps with Argo CD and Flux
* observability stacks like Prometheus Operator, OpenTelemetry, Loki, Grafana, Tempo, and Datadog-style agents

This uses something I call Conditional Reference Retrieval.

Basically: KubeShark detects signals like `IRSA`, `Karpenter`, `Azure Workload Identity`, `GKE Autopilot`, `OpenShift Routes`, `ApplicationSet`, `HelmRelease`, `ServiceMonitor`, or `OpenTelemetry Collector`, and then loads the matching specialized reference.

So instead of generic Kubernetes advice, you get EKS-aware, AKS-aware, GKE-aware, OpenShift-aware, GitOps-aware, or observability-aware manifest generation and review. But only when that context is actually relevant.

Very curious for feedback, especially from platform engineers, SREs, DevOps engineers, and anyone using Claude Code or Codex for Kubernetes work.
