```json
{
  "id": "1t1tofo",
  "author": "trolleid",
  "category": "gift-promotion",
  "subreddit": "aws",
  "created_utc": 1777737356.0,
  "created_at": "2026-05-02T17:55:56+02:00",
  "permalink": "https://www.reddit.com/r/aws/comments/1t1tofo/i_added_special_aws_support_to_this_kubernetes/",
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
  "title_sha256": "9d6c9f8cb0c744bd9cfa765da9034b4b2d08283ec0fe6a8e2c47a0dfca4c061a",
  "body_sha256": "05bfc6d65647d0a91f9927709cf81e42f821d6dfcfda335abd530d22adc721e0",
  "body_characters": 2174
}
```

# Original title

I added special AWS support to this Kubernetes Skill (Claude Code and Codex)

## Original body

I added dedicated AWS / EKS support to KubeShark.

**Mini recap:**

KubeShark is my Kubernetes skill for Claude Code and Codex.

It helps AI agents generate, review, and refactor Kubernetes manifests without falling into the usual LLM traps: missing security contexts, deprecated API versions, broken selectors, wildcard RBAC, unsafe probes, missing resource requests, and rollout configs that look okay but fail under real traffic.

The important part is that KubeShark is failure-mode-first. It does not just tell the model “write good Kubernetes”. It forces the model to reason about what can go wrong before it generates YAML, and then return validation and rollback guidance as part of the answer.

That matters a lot with Kubernetes, because many bad manifests are accepted by the API server and only fail later at runtime.

Repo: [https://github.com/LukasNiessen/kubernetes-skill](https://github.com/LukasNiessen/kubernetes-skill)

\---

**Now what’s new:**

KubeShark now has special dedicated AWS / EKS support.

When the task involves EKS, AWS, IRSA, EKS Pod Identity, AWS Load Balancer Controller, EBS/EFS CSI, AWS VPC CNI, or Karpenter, KubeShark switches into EKS-aware guidance.

That matters because EKS is “just Kubernetes” until identity, load balancing, storage, pod networking, and node provisioning enter the picture.

Common LLM mistakes include:

* putting AWS access keys into Kubernetes Secrets
* mixing IRSA and EKS Pod Identity assumptions
* using nginx annotations with AWS Load Balancer Controller
* treating EBS like ReadWriteMany storage
* recommending Karpenter while omitting resource requests
* assuming NetworkPolicy works without checking the CNI/policy engine

Example guidance KubeShark now keeps in mind:

    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: app
      namespace: payments
      annotations:
        eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/payments-app

It also knows that EBS is usually RWO and zone-sensitive, EFS is the RWX option, and Karpenter depends heavily on good workload requests.

So instead of generic Kubernetes advice, you get EKS-aware manifest generation and review.
