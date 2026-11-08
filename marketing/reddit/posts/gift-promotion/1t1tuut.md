```json
{
  "id": "1t1tuut",
  "author": "trolleid",
  "category": "gift-promotion",
  "subreddit": "openshift",
  "created_utc": 1777737748.0,
  "created_at": "2026-05-02T18:02:28+02:00",
  "permalink": "https://www.reddit.com/r/openshift/comments/1t1tuut/i_added_special_openshit_support_to_this/",
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
  "title_sha256": "0e295cded69b7a5c1f65fbcae76d6981fd571d56db01758c79707f9894875a8f",
  "body_sha256": "e3fe097cfd469514d860c842b4fc2addf931816f334fd3dbfb81e12d7ac24b9f",
  "body_characters": 2025
}
```

# Original title

I added special Openshit support to this Kubernetes Skill (Claude Code and Codex)

## Original body

I added dedicated OpenShift support to KubeShark.

**Mini recap:**

KubeShark is my Kubernetes skill for Claude Code and Codex.

It helps AI agents generate, review, and refactor Kubernetes manifests without falling into the usual LLM traps: missing security contexts, deprecated API versions, broken selectors, wildcard RBAC, unsafe probes, missing resource requests, and rollout configs that look okay but fail under real traffic.

The important part is that KubeShark is failure-mode-first. It does not just tell the model “write good Kubernetes”. It forces the model to reason about what can go wrong before it generates YAML, and then return validation and rollback guidance as part of the answer.

That matters a lot with Kubernetes, because many bad manifests are accepted by the API server and only fail later at runtime.

Repo: [https://github.com/LukasNiessen/kubernetes-skill](https://github.com/LukasNiessen/kubernetes-skill)

\---

**Now what’s new:**

KubeShark now has special dedicated OpenShift support.

When the task involves OpenShift, OKD, ROSA, ARO, Routes, SCCs, OLM, ImageStreams, or `oc`, KubeShark switches into OpenShift-aware guidance.

This matters because OpenShift is Kubernetes, but with important platform behavior that generic Kubernetes YAML often ignores.

Common LLM mistakes include:

* hardcoding `runAsUser: 1000`
* assuming root-capable images will run
* telling users to edit default SCCs
* granting `anyuid` or `privileged` too broadly
* using Ingress-controller annotations on OpenShift Routes
* forgetting to validate with `oc`

Example guidance KubeShark now keeps in mind:

    apiVersion: route.openshift.io/v1
    kind: Route
    metadata:
      name: app
    spec:
      to:
        kind: Service
        name: app
      tls:
        termination: edge

It also knows to treat OpenShift Routes, SCCs, arbitrary UID containers, and OLM-managed resources as first-class concerns.

So instead of generic Kubernetes advice, you get OpenShift-aware manifest generation and review.
