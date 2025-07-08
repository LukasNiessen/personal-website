---
title: "What is GitOps: A Full Example with Code"
summary: "GitOps explained through the evolution of a simple blog deployment - from manual CI to full GitOps with Infrastructure as Code"
date: "Jul 4 2025"
draft: false
repoUrl: "https://github.com/LukasNiessen/gitops-evolution-explained"
xLink: "https://x.com/iamlukasniessen/status/https://x.com/iamlukasniessen/status/1941232040353116431"
linkedInLink: "https://www.linkedin.com/pulse/what-gitops-full-example-code-lukas-nie%C3%9Fen-tttde/?trackingId=KdtvFXKyJhLqTZjG%2BYljUg%3D%3D"
tags:
  - GitOps
  - DevOps
  - CI/CD
  - Infrastructure as Code
  - Kubernetes
  - Continuous Deployment
---

# What is GitOps: A Full Example with Code

This is a short explanation of what GitOps is with a full example where we evolve from _"simple project"_ to _"GitOps project"_.

## What is GitOps?

GitOps means we use Git as the single source of truth for everything. Not just for your code, but also for your infrastructure, configuration, and deployment processes too.

In other words, our repository is everything. When you change something in the repo, your system automatically changes to match.

Let's look at a simple example. If you are not doing continuous deployment or not even continuous delivery, then you're not doing GitOps. The release process is not in your repo, so the repo is not the single source of truth for the system.

Likewise, if you you're not doing Infrastructure as Code (IaC), you're not doing GitOps. For example, if you have a repo with CI/CD but your AWS resources are managed through the web console, then your repo isn't the single source of truth - so it's not GitOps.

**Note:**
I talked only about _the repo_. But of course you can have more than one, e.g. you have separate repos for frontend, backend, and infrastructure. As long as each repo _"is GitOps"_ (the single source of truth for its domain), then you're still doing GitOps.

## Our Simple Example Project

Let's follow the journey of a simple blog website through the evolution of DevOps practices. This blog has:

- A React frontend
- A Node.js API backend
- A PostgreSQL database
- Deployed on Kubernetes

I will admit, a simple blog doesn't usually need a Kubernetes cluster... But it's an example :) We'll start with basic CI and evolve step by step to full GitOps.

## Step 1: Just CI (Continuous Integration)

Developers push code. A GitHub Action runs tests and builds the application.

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  test-and-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: "16"
      - name: Install dependencies
        run: npm install
      - name: Run tests
        run: npm test
      - name: Build application
        run: npm run build
```

The code is only merged into main/master/... if the tests and the build was successful. This is key of CI - this and doing this frequently, ideally daily.

**The Problem:** Great! Tests pass and the app builds. But now what? Someone still needs to manually deploy to production. This takes time and is dangerous. Set a false flag or have a typo somewhere and you're in trouble... (Google _knight capital group cicd_)

So we want to add Continuoues Deployment (deploying automatically when code merges into main) or at least Continuous Delivery (having the artifacts you need to deploy always ready, just not actually deploying).

## Step 2: CI/CD (Continuous Integration/Continuous Deployment)

Now we extend CI to also deploy automatically when tests pass.

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD
on:
  push:
    branches: [main]

jobs:
  test-build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: "16"

      # CI part
      - name: Install dependencies
        run: npm install
      - name: Run tests
        run: npm test
      - name: Build application
        run: npm run build

      # CD part
      - name: Build Docker image
        run: docker build -t myblog:${{ github.sha }} .
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/blog-backend blog-backend=myblog:${{ github.sha }}
```

Better! We're doing CI/CD, our deployments are very frequent and much safer now, that's great.

**The Problem:** But our infrastructure is still managed outside Git. Database configs, Kubernetes manifests, environment variables - they're all managed elsewhere. Our repo is not the single source of truth yet.

## Step 3: Infracture as Code

We now also move our infrastructure in the repo. We use Terraform in this example. Our repository structure now looks like:

```
my-blog/
├── apps/
│   └── backend/
│       ├── src/
│       ├── Dockerfile
│       └── package.json
├── infrastructure/
│   ├── kubernetes/
│   │   ├── namespace.yaml
│   │   ├── backend-deployment.yaml
│   │   └── database.yaml
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── helm/
│       └── values.yaml
├── config/
│   ├── production.yaml
│   ├── staging.yaml
│   └── development.yaml
└── .github/
    └── workflows/
        └── gitops.yml
```

**The GitOps Workflow:**

```yaml
# .github/workflows/gitops.yml
name: GitOps
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      # Build and push images
      - name: Build and push Docker images
        run: |
          docker build -t myblog-backend:${{ github.sha }} ./apps/backend
          docker push myblog-backend:${{ github.sha }}

      # Update infrastructure
      - name: Deploy infrastructure with Terraform
        run: |
          cd infrastructure/terraform
          terraform init
          terraform plan
          terraform apply -auto-approve

      # Update Kubernetes manifests
      - name: Update image tags in K8s manifests
        run: |
          sed -i 's|image: myblog-backend:.*|image: myblog-backend:${{ github.sha }}|' \
            infrastructure/kubernetes/backend-deployment.yaml

      # Apply all changes
      - name: Apply Kubernetes manifests
        run: |
          kubectl apply -f infrastructure/kubernetes/
```

Now everything is in our repo. There is only one issue left. What if someone goes and changes something without using the repo? For example manually changing the kubernetes configs. Then our repo becomes outdated and incorrect.

## Drift

What I have described above is called _"drift"_. The actual system _"drifted"_ from our repo because someone made manual changes. This means we no longer have GitOps in this case: the repo is not actually the single source of truth.

This is why things like ArgoCD and Flux exist. I will explain at a very high level how they solve this issue in a second.

**However**, if you can ensure that no one changes the system manually or in any other way besides Git, then it is still GitOps. It's just hard to really ensure that. But if you can, that's GitOps. It's called _push-based GitOps_. However, note that some people disagree, they say that push-based GitOps is not actually GitOps.

## ArgoCD: Pull-Based GitOps

ArgoCD (and Flux) solve the drift problem by constantly watching your Git repository and automatically syncing your cluster to match what's in Git. Instead of _pushing_ changes to your cluster, ArgoCD _pulls_ changes from your repo.

Here's how it works: ArgoCD runs inside your Kubernetes cluster and continuously monitors your Git repository. Every few minutes, it checks if what's actually running in your cluster matches what's defined in your Git repo. If there's a difference, ArgoCD automatically fixes it.

**The Problem with Push-Based GitOps:**

```yaml
# Someone runs this manually - oh no!
kubectl scale deployment blog-backend --replicas=10
```

Now your cluster has 10 replicas, but your Git repo still says 3 replicas. Your system has drifted from Git.

**The Solution with Pull-Based GitOps:**
ArgoCD notices the drift and automatically scales back to 3 replicas because that's what Git says. This is called _"self-healing"_.

Let's set up ArgoCD for our blog:

```yaml
# argocd/application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: blog-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-username/my-blog
    targetRevision: HEAD
    path: infrastructure/kubernetes
  destination:
    server: https://kubernetes.default.svc
    namespace: blog
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

Now we just remove the `kubectl apply` from our pipeline - ArgoCD takes care of that.

And that's it! Now we have _real_ GitOps. ArgoCD automatically detects the change in Git and deploys the new image. If someone manually changes something in the cluster, ArgoCD will revert it back to match Git within minutes. Your cluster is always in sync with Git, no matter what.

## The GitOps Advantages

Here a few advantages.

**1. Single Source of Truth**
Everything is in Git. Want to know what's running in production? Check the main branch.

**2. Rollback is Just Git**

Rolling back is just executing a few git commands.

**3. Audit Trail**
Every change is tracked. Who changed what, when, and why. Perfect for compliance and debugging.

**4. Declarative Infrastructure**
Your infrastructure is code. It's testable, reviewable, and repeatable.

**5. Self-Healing**
With pull-based GitOps, your system automatically fixes drift. Someone manually changes something? It gets reverted automatically.

**6. Enhanced Security**
Your cluster doesn't need external access for deployments. ArgoCD runs inside the cluster and pulls changes, reducing the attack surface.
