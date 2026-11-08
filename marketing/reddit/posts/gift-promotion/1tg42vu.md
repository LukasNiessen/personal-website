```json
{
  "id": "1tg42vu",
  "author": "trolleid",
  "category": "gift-promotion",
  "subreddit": "AZURE",
  "created_utc": 1779057270.0,
  "created_at": "2026-05-18T00:34:30+02:00",
  "permalink": "https://www.reddit.com/r/AZURE/comments/1tg42vu/i_added_special_azure_support_to_this_kubernetes/",
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
  "title_sha256": "afc9abcfc23b23225548b5739d8beb41fbab76a24bc9c0c501b3261c74a38ffb",
  "body_sha256": "c6daf15cb160fa474277821d19abf049d3d72abfad07b24566d6999ae039ef51",
  "body_characters": 2346
}
```

# Original title

I added special Azure support to this Kubernetes Skill (Claude Code and Codex)

## Original body

I added dedicated Azure / AKS support to KubeShark

**Mini recap:**

KubeShark is my Kubernetes skill for Claude Code and Codex.

It helps AI agents generate, review, and refactor Kubernetes manifests without falling into the usual LLM traps: missing security contexts, deprecated API versions, broken selectors, wildcard RBAC, unsafe probes, missing resource requests, and rollout configs that look okay but fail under real traffic.

The important part is that KubeShark is failure-mode-first. It does not just tell the model “write good Kubernetes”. It forces the model to reason about what can go wrong before it generates YAML, and then return validation and rollback guidance as part of the answer.

That matters a lot with Kubernetes, because many bad manifests are accepted by the API server and only fail later at runtime.

Repo: [https://github.com/LukasNiessen/kubernetes-skill](https://github.com/LukasNiessen/kubernetes-skill)

\---

**Now what’s new:**

KubeShark now has special dedicated Azure / AKS support.

When the task involves AKS, Azure Kubernetes Service, Microsoft Entra Workload ID, Azure CNI, Azure CNI Overlay, AGIC, Azure Disk CSI, Azure Files CSI, or Azure Blob CSI, KubeShark switches into AKS-aware guidance.

This is important because AKS has several places where generic Kubernetes advice is not enough.

Common LLM mistakes include:

* using deprecated pod-managed identity for new AKS work
* forgetting the required workload identity pod label
* mixing nginx annotations into AGIC-managed Ingress
* recommending kubenet for new long-lived clusters
* treating Azure Disk as shared RWX storage
* inventing StorageClass names instead of checking the cluster

Example guidance KubeShark now keeps in mind:

    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: app
      namespace: payments
      annotations:
        azure.workload.identity/client-id: "<client-id>"
    ---
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: app
    spec:
      template:
        metadata:
          labels:
            azure.workload.identity/use: "true"

It also knows to prefer Microsoft Entra Workload ID, capture the AKS network plugin, and choose Azure Disk/File/Blob CSI based on access pattern.

So instead of generic Kubernetes advice, you get AKS-aware manifest generation and review.
