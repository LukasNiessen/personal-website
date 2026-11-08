```json
{
  "id": "1t1tsb7",
  "author": "trolleid",
  "category": "gift-promotion",
  "subreddit": "googlecloud",
  "created_utc": 1777737606.0,
  "created_at": "2026-05-02T18:00:06+02:00",
  "permalink": "https://www.reddit.com/r/googlecloud/comments/1t1tsb7/i_added_special_gcp_support_to_this_kubernetes/",
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
  "title_sha256": "8e720dfce85313eb023cc218932aa43f3559f1181f95a384da01fc0e6270d311",
  "body_sha256": "3287b01e5d2ddddd7d3ea110bd4b99b0681c57d6585a06c1978044c9bf694c58",
  "body_characters": 2721
}
```

# Original title

I added special GCP support to this Kubernetes Skill (Claude Code and Codex)

## Original body

I added dedicated Google Cloud / GKE support to KubeShark.

**Mini recap:**

KubeShark is my Kubernetes skill for Claude Code and Codex.

It helps AI agents generate, review, and refactor Kubernetes manifests without falling into the usual LLM traps: missing security contexts, deprecated API versions, broken selectors, wildcard RBAC, unsafe probes, missing resource requests, and rollout configs that look okay but fail under real traffic.

The important part is that KubeShark is failure-mode-first. It does not just tell the model “write good Kubernetes”. It forces the model to reason about what can go wrong before it generates YAML, and then return validation and rollback guidance as part of the answer.

That matters a lot with Kubernetes, because many bad manifests are accepted by the API server and only fail later at runtime.

Repo: [https://github.com/LukasNiessen/kubernetes-skill](https://github.com/LukasNiessen/kubernetes-skill)

\---

**Now what’s new:**

KubeShark now has special dedicated Google Cloud / GKE support.

When the task involves GKE, Autopilot, Workload Identity Federation for GKE, Dataplane V2, GCE Ingress, Cloud Load Balancing, Persistent Disk CSI, Filestore CSI, or Config Sync, KubeShark switches into GKE-aware guidance.

Why this matters:

GKE Standard and GKE Autopilot have very different assumptions.

A manifest that is fine in a self-managed cluster may be rejected or mutated in Autopilot. A NetworkPolicy that seems correct may break workload identity if metadata server egress is blocked. A generic Ingress annotation copied from nginx or AWS may be meaningless for GCE Ingress.

Common LLM mistakes include:

* recommending service account JSON keys instead of Workload Identity Federation
* generating privileged or node-level workloads for Autopilot without compatibility checks
* mixing nginx or AWS ALB annotations into GCE Ingress
* forgetting metadata-server egress when restrictive NetworkPolicies and GCP auth are both present
* treating zonal Persistent Disks as freely movable across zones
* assuming Gateway API support without confirming the installed controller and CRDs

Example guidance KubeShark now keeps in mind:

    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: app
      namespace: payments
      annotations:
        iam.gke.io/gcp-service-account: payments-app@project.iam.gserviceaccount.com

It also knows to prefer Workload Identity Federation over JSON keys, avoid privileged/node-level assumptions in Autopilot, treat Persistent Disk and Filestore differently, and account for Dataplane V2 behavior when validating NetworkPolicy.

So instead of generic Kubernetes advice, you get GKE-aware manifest generation and review.
