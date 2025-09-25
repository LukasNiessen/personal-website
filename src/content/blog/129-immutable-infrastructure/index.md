---
title: 'Immutable Infrastructure: Why You Should Replace, Not Patch'
summary: 'A discussion of immutable infrastructure, why it matters, and how to implement it'
date: 'Sep 25 2025'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Infrastructure
  - DevOps
  - Cloud
  - Terraform
---

# Immutable Infrastructure: Why You Should Replace, Not Patch

## What is Immutable Infrastructure?

Think of it like this: instead of renovating your house every time you want to change something, you build a new house exactly how you want it and move in. That's immutable infrastructure. While this may sound crazy, let's entertain that idea for a bit.

By building from scratch always we have many benefits, such as:

- We know exactly what we're getting. No surprises. That's not the case otherwise, if the tenants living in the house broke a few things that we don't know about, or the list is just too long, then we might make our changes, but the end result doesn't really work as we want - and we wouldn't even know why exactly. This does not happen when building a new house.
- If we mess up our changes, no problem! We just send the tenants back to the old house, and as soon as fixed, they come back. Easy.

Okay, let's get realistic again. Nobody will do this of course because it's too expensive. But if we replace _house_ by _servers_ or other things, then it's a very interesting idea.

Here the IT version: **Immutable infrastructure treats servers and infrastructure components as unchangeable once deployed. Instead of updating existing systems in-place, you replace them entirely with new, pre-configured instances.**

Here's the key difference:

**Traditional (Mutable) Approach:**
```
Deploy server → Apply patches → Update configs → Install packages → Hope nothing breaks
```

**Immutable Approach:**
```
Build new image → Deploy new instances → Route traffic → Destroy old instances
```

## Is This Already Standard?

You're probably thinking: "Wait, isn't this how we already do things?" And you might be right.

If you're doing something like:
1. Build service image (NEW) in CI/CD pipeline
2. Push it to Artifactory/ECR
3. Kubernetes deploys it via ArgoCD
4. Old pods get replaced with new ones

Then yes, that's a perfect example of immutable infrastructure. This workflow is indeed fairly standard in modern cloud-native environments.

The thing is, while container-based deployments have made immutable infrastructure more common, not everyone fully embraces it. I've still seen teams SSH into running containers to "fix" things quickly, or manually patch servers "just this once".

## Why Immutable Infrastructure Matters

### 1. Predictability

When you deploy the exact same image you tested, there are no surprises. No "it works on my machine" problems, no configuration drift, no mysterious patches that somehow broke something else.

### 2. Atomic Deployments

Traditional deployments are like surgery - you're operating on a living system, and things can go wrong mid-operation. Immutable deployments are like assembly lines - you build the complete product and then swap it in.

If something goes wrong during image creation, no production systems are affected. The deployment either succeeds completely or fails completely. No partial states, no "deployment got stuck halfway".

### 3. Trivial Rollbacks

Since you're preserving history (or should at least), rollbacks become very simple, just deploy the previous image. This can even be automated. The same process you use to deploy forward works for rolling back.

### 4. Forces Good Practices

Here's a side benefit I didn't expect: immutable infrastructure forces you to do things properly.

**Centralized logging:** You can't SSH into servers to check logs because they might not exist tomorrow. This pushes you toward proper observability.

**Configuration management:** All configuration needs to be externalized and version-controlled because you can't just edit files on the server.

**State separation:** You're forced to clearly separate stateful components (databases) from stateless ones (application servers).

## The Downsides

There are definitely downsides.

### Slower Deployments
Building a complete new image takes longer than just copying new code to an existing server. However, this can be mitigated with layered images and caching strategies.

And this is also where _building a Docker image_ and _building a house_ differs quite a bit pricewise ;)

### External Dependencies
If you're installing packages during image build and apt/yum repositories are slow or down, your deployment fails. One can try to tackle this with building base images ahead of time and keeping dependencies in your own registries.

### Storage Overhead
Keeping multiple versions of images around takes more storage space. But storage is cheap, and you can implement retention policies.

### Initial Complexity
Setting up the automation and tooling requires more upfront investment. But the payoff is immediate and compounds over time.

## A Practical Example with Terraform

Here's how you might implement immutable infrastructure for a web application using Terraform and AWS:

```hcl
# Build a new AMI for each deployment
data "aws_ami" "app_ami" {
  most_recent = true
  owners      = ["self"]
  
  filter {
    name   = "name"
    values = ["my-app-${var.app_version}"]
  }
}

# Launch configuration with the new AMI
resource "aws_launch_template" "app_template" {
  name_prefix   = "my-app-${var.app_version}-"
  image_id      = data.aws_ami.app_ami.id
  instance_type = "t3.medium"
  
  vpc_security_group_ids = [aws_security_group.app_sg.id]
  
  user_data = base64encode(templatefile("user_data.sh", {
    app_version = var.app_version
  }))
  
  lifecycle {
    create_before_destroy = true
  }
}

# Auto Scaling Group that replaces instances
resource "aws_autoscaling_group" "app_asg" {
  name                = "my-app-${var.app_version}"
  vpc_zone_identifier = var.private_subnet_ids
  target_group_arns   = [aws_lb_target_group.app_tg.arn]
  
  min_size         = 2
  max_size         = 10
  desired_capacity = var.desired_capacity
  
  launch_template {
    id      = aws_launch_template.app_template.id
    version = "$Latest"
  }
  
  # Replace instances gradually
  instance_refresh {
    strategy = "Rolling"
    preferences {
      min_healthy_percentage = 50
    }
  }
  
  lifecycle {
    create_before_destroy = true
  }
  
  tag {
    key                 = "Name"
    value               = "my-app-${var.app_version}"
    propagate_at_launch = true
  }
}
```

The deployment process would be:
1. Build new AMI with Packer (with new app version)
2. Update `app_version` variable
3. Run `terraform apply`
4. Terraform creates new launch template and triggers instance refresh
5. ASG gradually replaces old instances with new ones
6. Once healthy, old instances are terminated

## Container-Native Approach

If you're using Kubernetes, it's even simpler:

```yaml
# Deployment with new image
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
        version: "v1.2.3"  # New version
    spec:
      containers:
      - name: my-app
        image: my-registry/my-app:v1.2.3  # New immutable image
        ports:
        - containerPort: 8080
```

With ArgoCD or similar GitOps tools, you just update the image tag in Git, and the system handles the immutable deployment automatically.

## My Take

Immutable infrastructure is a fundamental mindset shift.

It eliminates entire categories of problems:
- Less _snowflaky servers_
- Less "it worked yesterday" mysteries  
- Less fear of deploying on Fridays
- Less manual debugging sessions on production servers

## Enterprises

However, **immutable isn't always an option**, especially in large enterprises. Most enterprises take considerable time to migrate to new architectures, and it's often necessary to keep some mutable servers around until you can properly architect an atomic, blue-green deployment process.

This is still very much true in 2025:

**Legacy Systems:** Complex applications with undocumented dependencies and custom patches can't be made immutable overnight.

**Gradual Migration:** Organizations need to incrementally modernize, running hybrid environments where new services are immutable but legacy components remain mutable.

**Cost & Risk:** Rebuilding infrastructure requires significant investment and extensive testing phases that can take months or years.

**Complex Dependencies:** Making one system immutable might break integration points with systems that expect long-lived, addressable servers.

**My take:** Don't let perfect be the enemy of good. Making your web tier immutable while keeping databases mutable is still a huge win. Progress over perfection.

Have a migration strategy and make conscious decisions about what stays mutable and for how long.