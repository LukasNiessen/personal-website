```json
{
  "id": "1t1tu0g",
  "author": "trolleid",
  "category": "gift-promotion",
  "subreddit": "ArgoCD",
  "created_utc": 1777737696.0,
  "created_at": "2026-05-02T18:01:36+02:00",
  "permalink": "https://www.reddit.com/r/ArgoCD/comments/1t1tu0g/i_added_special_argocd_support_to_this_kubernetes/",
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
  "title_sha256": "0de9e9ddecce8dc88a20503620dad612cd0ec62f4f1f4ada0f9d5ac08a743088",
  "body_sha256": "37aaaef66d6ffbafa717b054d7d8ebd5daf2e19f7118c08c3bc11714e9088c94",
  "body_characters": 2246
}
```

# Original title

I added special ArgoCD support to this Kubernetes Skill (Claude Code and Codex)

## Original body

I added dedicated GitOps support to KubeShark.

**Mini recap:**

KubeShark is my Kubernetes skill for Claude Code and Codex.

It helps AI agents generate, review, and refactor Kubernetes manifests without falling into the usual LLM traps: missing security contexts, deprecated API versions, broken selectors, wildcard RBAC, unsafe probes, missing resource requests, and rollout configs that look okay but fail under real traffic.

The important part is that KubeShark is failure-mode-first. It does not just tell the model “write good Kubernetes”. It forces the model to reason about what can go wrong before it generates YAML, and then return validation and rollback guidance as part of the answer.

That matters a lot with Kubernetes, because many bad manifests are accepted by the API server and only fail later at runtime.

Repo: [https://github.com/LukasNiessen/kubernetes-skill](https://github.com/LukasNiessen/kubernetes-skill)

\---

**Now what’s new:**

KubeShark now has special dedicated GitOps support for Argo CD and Flux.

When the task involves Argo CD, ApplicationSet, sync waves, Flux, GitRepository, Kustomization, HelmRelease, or GitOps reconciliation, KubeShark switches into GitOps-aware guidance.

Why this matters:

GitOps changes the risk model.

A manifest applied once with `kubectl apply` is very different from a manifest continuously reconciled by a controller with pruning, self-healing, generated applications, and sync ordering.

Common LLM mistakes include:

* enabling auto-prune without ownership boundaries
* assuming Argo CD sync waves order separate Applications
* using broad `ignoreDifferences` to hide real drift
* confusing Flux `Kustomization` CRs with `kustomization.yaml`
* forgetting `dependsOn` in Flux
* putting plaintext secrets in Git

Example guidance KubeShark now keeps in mind:

    apiVersion: kustomize.toolkit.fluxcd.io/v1
    kind: Kustomization
    metadata:
      name: app
    spec:
      dependsOn:
        - name: platform-crds
      prune: true
      interval: 10m

It also knows to reason about reconciliation, pruning, drift, ordering, and rollback before suggesting GitOps resources.

So instead of generic Kubernetes advice, you get GitOps-aware manifest generation and review.
