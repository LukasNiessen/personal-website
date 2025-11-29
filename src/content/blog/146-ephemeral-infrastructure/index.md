---
title: 'Ephemeral Infrastructure: Why Short-Lived is a Good Thing'
summary: 'Understanding ephemeral infrastructure and why designing systems to be disposable makes them more reliable'
date: 'Nov 29 2025'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Infrastructure
  - DevOps
  - Kubernetes
  - Cloud
---

# Ephemeral Infrastructure: Why Short-Lived is a Good Thing

## What Does Ephemeral Mean?

The word "ephemeral" means short-lived or temporary. In the context of infrastructure and DevOps, it describes components that are designed to exist only for as long as they're needed, then disappear.

Think of it like hotel rooms versus apartments. An apartment is yours - you move in, customize it, fix things when they break, and stay for years. A hotel room is ephemeral - you use it for a few nights, and when you leave, housekeeping resets it to a clean state for the next guest.

**Ephemeral infrastructure** treats servers, containers, and other resources like hotel rooms, not apartments.

## Examples of Ephemeral Resources

Here are some common examples from different contexts:

**Kubernetes Pods**: When you deploy an app, Kubernetes spins up pods. These pods might live for hours, days, or weeks, but they're designed to be killed and replaced at any moment. If a node fails, pods disappear. When you deploy a new version, old pods get terminated.

**CI/CD Runners**: GitHub Actions or GitLab CI runners spin up a fresh environment for each job. Your tests run, the job finishes, and the runner is destroyed. Next job? Brand new runner.

**Lambda Functions**: AWS Lambda containers exist only for the duration of your function execution. Once done, they're gone (or at least recycled).

**Auto-scaling Instances**: When traffic spikes, new EC2 instances appear. When traffic drops, they disappear. They're not pets with names - they're cattle.

## Why Does This Matter?

You might be thinking: "Why would I want my infrastructure to disappear? Isn't stability about keeping things running?"

Actually, no. Ephemeral infrastructure makes systems *more* stable, not less. Here's why.

### 1. Forces Stateless Design

If your pods can disappear at any moment, you can't store important data on them. This forces you to properly separate state from compute.

**Bad (stateful)**:
```
Pod stores user sessions in memory
Pod crashes → all sessions lost → users get logged out
```

**Good (stateless)**:
```
Pod stores user sessions in Redis
Pod crashes → new pod starts → users stay logged in
```

This is exactly what you want. You're forced to do the right thing.

### 2. Self-Healing by Default

With ephemeral infrastructure, recovery is automatic. When something goes wrong, the system doesn't try to fix it - it just replaces it.

Traditional approach: Server crashes → Someone needs to SSH in → Debug for hours → Maybe fix it

Ephemeral approach: Pod crashes → Kubernetes notices → Starts new pod → Done in seconds

There's no "fixing" because there's nothing to fix. You just get a fresh, working copy.

### 3. Eliminates Configuration Drift

Remember that server where someone manually installed a package "just this once" three years ago, and now nobody knows why it's there? That doesn't happen with ephemeral infrastructure.

Every new pod starts from the same image. No accumulated changes. No mystery configurations. No "it works on server A but not server B."

### 4. Makes Scaling Trivial

Need more capacity? Spin up more pods. Need less? Kill some pods. Since everything is disposable and identical, scaling is just a number.

Compare this to traditional servers where you need to carefully provision, configure, and maintain each new instance.

## Kubernetes and Ephemeral Pods

The most common place you'll encounter ephemeral infrastructure is Kubernetes. And a common question is: "Wait, if pods are ephemeral, how do I keep my data?"

The answer is: **Pods are ephemeral. Data is not.**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: app
        image: my-app:v1.2.3
        volumeMounts:
        - name: data
          mountPath: /data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: my-pvc  # Data lives here, not in the pod
```

The pod is ephemeral - it can be killed and recreated at any moment. But the data lives on a PersistentVolume, which survives pod restarts.

### When Pods Get Replaced

Pods are ephemeral by design. They get replaced all the time:

- **Rolling updates**: Deploy new version → old pods get terminated, new ones appear
- **Node maintenance**: Drain a node → all pods move to other nodes
- **Resource pressure**: Node runs out of memory → evict pods
- **Failed health checks**: Pod becomes unhealthy → kill it, start fresh
- **Scale down**: Too much capacity → remove pods

This happens constantly in production Kubernetes clusters. And that's fine - in fact, it's exactly what you want.

## The Mental Shift

It is a mindset change. In the older days (and sometimes still today), we have treated servers as precious things that need care and feeding. Ephemeral infrastructure flips this.

**Old mindset**: This server is important. If it breaks, we need to fix it carefully.

**New mindset**: This pod is disposable. If it breaks, kill it and get a new one.

## What About Databases?

Databases are inherently stateful, they *are* the state. You can't just kill a database and start fresh without losing all your data. So with databases it's a different story, are (usually) **not** ephemeral.

That said, you can still apply ephemeral principles around databases:

**The compute is ephemeral, the storage is not:**
```
Database Pod (ephemeral) → PersistentVolume (permanent)
```

The pod itself can be replaced, but it reconnects to the same storage. This is what StatefulSets in Kubernetes do.

**Managed databases:**
Cloud providers (RDS, Cloud SQL, etc.) abstract away the server entirely. You don't care about the underlying compute - it's ephemeral from your perspective. You just have a database endpoint.

**Replicas are ephemeral:**
In database clusters, replica nodes can be ephemeral. The primary handles writes (stateful), but read replicas can come and go as needed.

## Ephemeral vs Immutable

I addressed this briefly in [my article on immutable infrastructure](https://lukasniessen.com/blog/129-immutable-infrastructure/), but it's worth clarifying again because these terms get mixed up constantly.

**Ephemeral = Short-lived by design**
- A CI runner that exists for 2 minutes
- A Lambda function that runs for 100ms
- A Kubernetes pod that lives for a few hours

**Immutable = Unchangeable once created**
- A Docker image that never gets modified
- An EC2 instance you replace rather than patch
- A configuration file that gets versioned, not edited in place

A resource can be both ephemeral and immutable (like a Kubernetes pod from an immutable image), but they're different concepts.

### Ephemeral Resources Are Usually Immutable

However: **ephemeral resources are typically immutable by design**.

If your pod only lives for a few hours and then gets replaced, why would you modify it? You wouldn't SSH in to install a package or change a config file. You'd just build a new image and redeploy. So _ephemeral_ and _immutable_ are different things, but in practice they usually go hand in hand.

This is why ephemeral infrastructure naturally pushes you toward immutability:

**Exception**: Of course there are exceptions. For example, a temporary VM spun up for a specific task could theoretically be modified while it's running. But in practice, modern ephemeral infrastructure is almost always immutable too.

## Practical Example: Web Application

Let's look at a concrete example. Suppose you're running a web application.

**Traditional (long-lived) approach:**
```
Deploy EC2 instances
→ Install application
→ Configure it
→ It runs for months
→ Apply patches when needed
→ SSH in to debug issues
→ Eventually, "it works, don't touch it"
```

**Ephemeral approach:**
```
Build Docker image with app
→ Push to registry
→ Kubernetes pulls image and starts pods
→ Pods run for hours/days
→ Deploy new version → old pods die, new pods start
→ Problems? Just restart the pod
→ No SSH access needed or wanted
```

The ephemeral version is simpler, more reliable, and easier to reason about.

## The Downsides

Of course, ephemeral infrastructure isn't free. There are trade-offs.

### Startup Time

Ephemeral resources need to start up frequently. If your application takes 5 minutes to start, that's a problem. This pushes you toward faster startup times, which is good, but it takes effort.

### Debugging Can Be Harder

When a pod crashes and gets replaced, you lose the ability to SSH in and poke around. You need proper logging and observability instead. This is actually better in the long run, but it requires upfront investment.

### Stateful Workloads Are Tricky

As we discussed with databases, not everything can be ephemeral. Stateful services require more careful design.

## In Practice

Nowadays most modern systems are already partially ephemeral, it's almost a default in cloud native environments at least:

- Your Kubernetes cluster? Ephemeral pods.
- Your CI/CD pipeline? Ephemeral runners.
- Your serverless functions? Ephemeral by definition.
- Your auto-scaling group? Ephemeral instances.

The question isn't "should I use ephemeral infrastructure?" but rather "how much of my system should be ephemeral?"

**My answer**: Make everything ephemeral except the parts that absolutely need to be stateful (databases, message queues, etc.). And even then, make the compute ephemeral while keeping only the storage persistent.
