---
title: "KubeShark: Kubernetes Guardrails for Claude Code and Codex"
summary: "Why I built an open-source Kubernetes skill that makes AI diagnose security, rollout, networking, RBAC, resource, and API drift risks before it writes YAML."
date: "May 02 2026"
repoUrl: "https://github.com/LukasNiessen/kubernetes-skill"
tags:
  - Kubernetes
  - AI
  - Claude Code
  - Codex
  - Open Source
  - DevOps
---

# KubeShark: Agent Skill for Claude Code and Codex, Kubernetes Skill

I use coding agents a lot. Claude Code, Codex, sometimes other tools. For normal application code, the experience is often great. Not perfect, but genuinely useful.

Kubernetes is different.

With Kubernetes, the problem is not only that the model can be wrong. The bigger problem is that the output can look correct, pass a quick review, and still be dangerous. A manifest can be valid YAML, use a valid `apiVersion`, apply successfully, and still route no traffic, restart every pod in a loop, expose things that should not be exposed, or run everything as root.

That being said: LLMs **love** to hallucinate when it comes to K8s.

So I built [KubeShark](https://github.com/LukasNiessen/kubernetes-skill), an open-source Kubernetes skill for Claude Code and Codex. The goal is simple: make AI-generated Kubernetes work, eliminate hallucinations and still don't burn all your tokens.

## Why Kubernetes Is Such a Good Trap

Kubernetes is declarative. You describe what you want and the control plane tries to make reality match. This is a great model, but it also means mistakes can be subtle.

Let's get concrete.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
        version: v2
    spec:
      containers:
        - name: web
          image: ghcr.io/example/web:latest
          ports:
            - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector:
    app: web
    version: v1
  ports:
    - port: 80
      targetPort: 8080
```

This is the kind of thing an LLM can easily generate when refactoring labels. The Service selector says `version: v1`, but the pods have `version: v2`.

Kubernetes accepts this. No dramatic error. No big red warning. The Service simply has no endpoints and traffic goes nowhere.

And this is just one example. Other common ones:

- no `securityContext`, so containers run as root by default
- no resource requests, so the scheduler has no useful information
- liveness probes checking a database, causing cascading restarts
- `cluster-admin` bound to a normal application service account
- `extensions/v1beta1` Ingress from old training data
- `:latest` image tags, making rollback and auditing painful

These are not theoretical problems. This is exactly the kind of YAML coding agents produce when you just say "create a production-ready Deployment".

## What KubeShark Is

KubeShark is not a Kubernetes tutorial. LLMs already know the basic syntax. They do not need another explanation of what a Deployment is.

The missing part is judgment.

So KubeShark is built as a workflow plus targeted references. The core `SKILL.md` is intentionally small. It tells the agent how to approach Kubernetes work:

```text
capture context
-> diagnose failure modes
-> load only relevant references
-> propose fix path with risk controls
-> generate manifests or charts
-> validate
-> return assumptions, tradeoffs, tests, and rollback notes
```

That second step is the important one: **diagnose before generating**.

Without that step, the model tends to jump straight into YAML. With that step, it first asks: what can go wrong here? Is this mostly a security context problem? A rollout problem? An RBAC problem? A cloud-provider-specific storage issue? A Helm issue?

That framing changes the output.

## The Six Failure Modes

KubeShark organizes Kubernetes risk into six failure modes:

1. **Insecure workload defaults** - missing security contexts, host access, Pod Security Standard violations
2. **Resource starvation** - missing requests and limits, no PDB, bad scheduling assumptions
3. **Network exposure** - missing NetworkPolicies, wrong Service types, broken selectors, DNS issues
4. **Privilege sprawl** - wildcard RBAC, `cluster-admin`, leaked secrets, too many service account rights
5. **Fragile rollouts** - bad probes, mutable tags, unsafe update strategies, no graceful shutdown
6. **API drift** - deprecated APIs, wrong `apiVersion`, schema mistakes, Helm/Kustomize structure problems

This is the core design choice. Instead of organizing the skill like a Kubernetes book, it is organized around the ways LLM-generated Kubernetes fails.

That sounds like a small difference, but it matters. If the task is "review this Deployment", I don't want the model to load every possible Kubernetes concept. I want it to check the failure modes that usually make Deployments dangerous.

## Token Efficiency

I care a lot about token usage here.

A skill that improves output but burns massive context is not good enough. Coding agents already need room for the repo, manifests, logs, previous messages, tool output, and tests. If the skill itself eats too much, the model gets worse in a different way.

So KubeShark uses what I call Conditional Reference Retrieval, or CRR.

The idea is simple:

- the main skill stays small and procedural
- detailed content lives in focused reference files
- the agent loads only what matches the task
- EKS, GKE, AKS, OpenShift, GitOps, and observability stack guidance stay out of context unless detected

For example, a plain Deployment hardening task does not need AKS Workload Identity guidance. A Kustomize overlay review does not need StatefulSet storage patterns. A GKE Autopilot task does need GKE-specific constraints.

That is the point of CRR: keep common work lean, but still have depth when the task actually needs it.

## What The Skill Pushes The Agent To Do

Suppose you ask:

```text
Create a production-ready Deployment, Service, Ingress, HPA, and NetworkPolicy for my API.
```

A generic response often jumps into a big YAML file. It might include some good pieces, but it will also often miss something important.

With KubeShark, the agent should first establish assumptions:

- Kubernetes version floor
- namespace and environment
- ingress controller
- whether Pod Security Admission is enforced
- whether NetworkPolicies are supported by the CNI
- whether the app can run with a read-only root filesystem
- expected ports and health endpoints

Then it should select likely failure modes:

- insecure workload defaults
- resource starvation
- network exposure
- fragile rollouts
- API drift

Only then should it generate YAML.

The generated output should include things like:

```yaml
securityContext:
  runAsNonRoot: true
  seccompProfile:
    type: RuntimeDefault
containers:
  - name: api
    image: ghcr.io/example/api:v1.2.3
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
          - ALL
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        memory: 256Mi
    readinessProbe:
      httpGet:
        path: /readyz
        port: http
    livenessProbe:
      httpGet:
        path: /healthz
        port: http
```

And just as important, it should tell you how to validate it:

```bash
kubectl diff -f k8s/
kubectl apply --dry-run=server -f k8s/
kubeconform -strict -summary k8s/
kubectl get endpoints web -n my-namespace
kubectl rollout status deployment/web -n my-namespace
```

This does not make Kubernetes safe by magic. But it changes the default from "here is YAML, good luck" to "here is YAML, these are my assumptions, these are the risks, here is how you check it, and here is how to roll back."

That's a very different interaction.

## Claude Code And Codex

KubeShark works with Claude Code because Claude Code has a skill system. You can clone it into your skills directory or install it through the Claude plugin marketplace.

For Codex, there is no global skill system in the same way. But the skill is plain Markdown, so it still works well. You clone it into a project and reference it from `AGENTS.md`.

That is actually one thing I like about this approach. There is no magic runtime. The core value is in a compact operating procedure and curated reference files. Any agent that can read files and follow instructions can benefit from it.

## How To Use It

For Claude Code:

```bash
git clone https://github.com/LukasNiessen/kubernetes-skill.git ~/.claude/skills/kubernetes-skill
```

For Codex, clone it into your repo:

```bash
git clone https://github.com/LukasNiessen/kubernetes-skill.git .kubernetes-skill
```

Then add something like this to `AGENTS.md`:

```markdown
## Kubernetes

When working with Kubernetes manifests, Helm charts, or Kustomize overlays,
follow the workflow in `.kubernetes-skill/SKILL.md`.
Load references from `.kubernetes-skill/references/` as needed.
```

After that, ask naturally:

```text
Review my Helm chart for security and rollout issues.
```

or:

```text
Create a production-ready Deployment, Service, HPA, and NetworkPolicy for this API.
```

## Closing

Kubernetes is powerful, but it is also very easy to get almost right. And "almost right" is exactly where LLMs are most dangerous.

KubeShark is my attempt to make AI Kubernetes work more boring, more explicit, and less hallucinated. It is open source, MIT licensed, and works with Claude Code, Codex, and basically any agent that can follow Markdown instructions.

The repo is here: [https://github.com/LukasNiessen/kubernetes-skill](https://github.com/LukasNiessen/kubernetes-skill)
