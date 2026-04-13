---
title: "Kubernetes Fundamentals: A Practical Reference"
summary: "Core concepts, objects, commands, and patterns in Kubernetes - written for someone who knows Docker but is new to K8s"
date: "Apr 13 2026"
tags:
  - Kubernetes
  - Docker
  - DevOps
  - Infrastructure
---

# Kubernetes Fundamentals: A Practical Reference

This is a practical reference for Kubernetes. It covers core concepts, the most important objects, common commands, and how things fit together. I'm writing this for someone who already knows Docker but hasn't worked with Kubernetes yet.

## What Is Kubernetes?

Docker runs containers on one machine. Kubernetes (K8s) runs them across a cluster of machines. It handles networking between containers, restarts them when they crash, scales them up and down, and manages configuration and secrets.

The key idea is **declarative configuration**. You describe what you want (e.g., "run 3 copies of my app"), and Kubernetes figures out how to make it happen - which machines, what IPs, when to restart. You declare the desired state, K8s reconciles reality to match.

## Core Architecture

```
Kubernetes Cluster
├── Control Plane (the brain)
│   ├── API Server        (receives all kubectl commands, the single entry point)
│   ├── etcd              (database storing all cluster state)
│   ├── Scheduler         (decides which node runs which pod)
│   └── Controller Manager (runs control loops: "are there enough replicas?")
│
├── Node 1 (a machine that runs pods)
│   ├── kubelet           (agent that talks to API server, manages pods on this node)
│   ├── kube-proxy        (handles networking, routes traffic to pods)
│   ├── Pod: my-app-abc   (your container)
│   └── Pod: my-db-xyz    (another container)
│
├── Node 2
│   ├── kubelet
│   ├── kube-proxy
│   ├── Pod: my-app-def
│   └── Pod: my-cache-123
│
└── Node N...
```

The control plane is the brain. It stores state, makes scheduling decisions, and runs reconciliation loops. The nodes are the workers. Each node runs a `kubelet` (an agent that talks to the API server) and `kube-proxy` (handles networking). Your actual containers live inside pods on these nodes.

In Minikube, the entire cluster - control plane plus one node - runs inside a single Docker container on your local machine.

## Core Objects

Every object in K8s is defined by a YAML manifest with this structure:

```yaml
apiVersion: v1              # Which API version
kind: Pod                   # What type of object
metadata:
  name: my-pod              # Object name
  namespace: default        # Which namespace it lives in
  labels:                   # Key-value tags for grouping/selecting
    app: my-app
spec:                       # The desired state (different per kind)
  containers:
    - name: my-container
      image: nginx:latest
```

Let's go through the most important ones.

### Cluster

The whole system: control plane + all nodes. One cluster can run many applications for many teams. `kubectl` talks to one cluster at a time.

```bash
kubectl cluster-info                # What cluster am I connected to?
kubectl config current-context      # Which cluster context is active?
kubectl config get-contexts         # List all known clusters
kubectl config use-context my-ctx   # Switch to a different cluster
```

### Node

A machine (physical server or VM) that runs pods. In Minikube, there's one node (a Docker container pretending to be a server). In production, you'd have many nodes, say 10 Azure VMs, and K8s distributes pods across them.

```bash
kubectl get nodes                   # List all nodes
kubectl describe node minikube      # Details: CPU, memory, pods running on it
```

### Namespace

A logical partition inside the cluster. Think of it like folders for organizing resources. Pods in namespace A can't accidentally interfere with pods in namespace B (though they can still communicate via Services unless you add NetworkPolicies).

```bash
kubectl get namespaces              # List all namespaces
kubectl create namespace my-app     # Create one
kubectl get pods -n my-app          # List pods in a specific namespace
kubectl get pods -A                 # List pods across ALL namespaces
```

K8s comes with a few built-in namespaces:

- `default`: where things go if you don't specify
- `kube-system`: K8s internal components (DNS, proxy, etc.)
- `kube-public`: publicly readable, rarely used

### Pod

The smallest deployable unit. A pod wraps one (or rarely more) container(s). Pods are **ephemeral**: they can be killed, restarted, or moved to a different node at any time. Never rely on a pod staying alive or keeping its IP.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  containers:
    - name: my-app
      image: my-app:v1.0
      ports:
        - containerPort: 8080
      env:
        - name: DATABASE_URL
          value: "postgres://db:5432/mydb"
```

You rarely create Pods directly. Instead, you create Deployments, which create and manage Pods for you.

```bash
kubectl get pods                    # List pods in default namespace
kubectl get pods -n my-app          # List pods in a specific namespace
kubectl logs my-pod                 # View pod logs
kubectl logs my-pod --tail=50       # Last 50 lines
kubectl logs -f my-pod              # Follow/stream logs
kubectl exec -it my-pod -- /bin/sh  # Shell into a running pod
kubectl delete pod my-pod           # Kill a pod (Deployment will recreate it)
kubectl describe pod my-pod         # Detailed info (events, errors, status)
```

### Deployment

This is what you'll use most. A Deployment manages pods. You say "I want 3 replicas of this pod" and the Deployment ensures exactly 3 are always running. If one crashes, it creates a replacement. If you change the image tag, it does a rolling update: start new pods, then kill old ones, zero downtime.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: my-namespace
spec:
  replicas: 3                       # Run 3 copies
  selector:
    matchLabels:
      app: my-app                   # "Manage pods with this label"
  template:                         # Pod template (what each replica looks like)
    metadata:
      labels:
        app: my-app                 # Must match selector above
    spec:
      containers:
        - name: my-app
          image: my-app:v2.0
          ports:
            - containerPort: 8080
```

```bash
kubectl get deployments -n my-app
kubectl rollout restart deployment my-app -n my-app    # Restart all pods
kubectl rollout status deployment my-app -n my-app     # Watch rollout progress
kubectl scale deployment my-app --replicas=5 -n my-app # Scale manually
kubectl set image deployment/my-app my-app=my-app:v3.0 # Change image tag
```

Under the hood, a Deployment creates a ReplicaSet, which creates the actual Pods:

```
Deployment "my-app" (desired: 3 replicas)
  └── ReplicaSet "my-app-abc123" (manages the actual pods)
      ├── Pod "my-app-abc123-x1y2z"
      ├── Pod "my-app-abc123-a3b4c"
      └── Pod "my-app-abc123-d5e6f"
```

### ReplicaSet

Sits between a Deployment and its Pods. It ensures the right number of pod replicas are running. You almost never create ReplicaSets directly - Deployments create and manage them for you. When you update a Deployment (e.g., new image tag), it creates a new ReplicaSet and gradually shifts pods from the old one to the new one. That's your rolling update.

```bash
kubectl get replicasets -n my-app   # You'll see one per deployment version
```

### StatefulSet

Like a Deployment, but for **stateful** applications: databases, message queues, that kind of thing. The key differences from a Deployment:

- Pods get stable, predictable names: `my-db-0`, `my-db-1`, `my-db-2` (not random suffixes)
- Pods are created and deleted in order (0 first, then 1, then 2)
- Each pod can have its own persistent storage via a PVC
- Pods keep their identity across restarts

Used for: PostgreSQL, Redis, Kafka, Elasticsearch - anything that stores data.

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: my-db
spec:
  serviceName: my-db        # Required: headless service name
  replicas: 3
  selector:
    matchLabels:
      app: my-db
  template:
    metadata:
      labels:
        app: my-db
    spec:
      containers:
        - name: postgres
          image: postgres:15
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:     # Each pod gets its own PVC
    - metadata:
        name: data
      spec:
        accessModes: [ReadWriteOnce]
        resources:
          requests:
            storage: 10Gi
```

### Service

A stable network address for a group of pods. Pods get random IPs that change on restart. A Service gives them a fixed DNS name (e.g., `my-db`) and load-balances traffic across all matching pods.

There are different types:

| Type                    | What it does                                                                                            |
| ----------------------- | ------------------------------------------------------------------------------------------------------- |
| **ClusterIP** (default) | Internal only. Other pods connect via `my-service:port`. Not reachable from outside.                    |
| **NodePort**            | ClusterIP + opens a port (30000-32767) on every node. Reachable from outside if you can hit the node.   |
| **LoadBalancer**        | NodePort + provisions a cloud load balancer (Azure LB, AWS ELB). The production way to expose services. |
| **ExternalName**        | DNS alias to an external service. No proxying.                                                          |

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app
spec:
  type: ClusterIP            # Internal only (default)
  selector:
    app: my-app              # Route traffic to pods with this label
  ports:
    - port: 80               # Service port (what other pods connect to)
      targetPort: 8080       # Container port (where traffic actually goes)
```

```bash
kubectl get services -n my-app
kubectl get svc -n my-app           # svc is short for services
```

**DNS inside the cluster:** Every Service gets a DNS name: `{service-name}.{namespace}.svc.cluster.local`. Within the same namespace, just `{service-name}` works.

So yes, Services are basically how DNS works in Kubernetes. When your backend code connects to a database, you don't use an IP address. You use the Service name. Here's a concrete example. Suppose you have a PostgreSQL database running as a pod, and a Service in front of it:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-db
  namespace: my-app
spec:
  selector:
    app: my-db
  ports:
    - port: 5432
      targetPort: 5432
```

Now in your backend Deployment, you just set the database URL to `my-db:5432`:

```yaml
env:
  - name: DATABASE_URL
    value: "postgres://user:pass@my-db:5432/mydb"
```

That's it. `my-db` resolves to the Service's cluster IP, which routes traffic to whichever pod has the label `app: my-db`. The backend doesn't need to know the pod's actual IP, doesn't need to care if the pod restarts and gets a new IP, doesn't need to care which node it's on. The Service handles all of that.

### Ingress

Routes external HTTP(S) traffic to Services based on hostnames and paths. Basically a reverse proxy (like nginx) that lives inside your cluster.

An Ingress resource on its own does nothing though. It's just a set of routing rules. You also need an **Ingress Controller** - a pod running in your cluster that reads those rules and actually does the routing. Think of it this way: the Ingress is the configuration, the Ingress Controller is the thing that executes it. It's like writing an nginx config file vs actually running nginx.

K8s doesn't ship with an Ingress Controller out of the box. You have to install one yourself. Common choices:

- **nginx-ingress**: the most popular one, basically nginx running inside K8s and auto-configured by your Ingress resources
- **Traefik**: auto-discovers services, nice dashboard, popular in smaller setups
- **Istio Gateway**: part of the Istio service mesh, more powerful but more complex

In Minikube, you enable one with `minikube addons enable ingress` (this installs nginx-ingress). In production on a cloud provider, you'd typically deploy it via Helm.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
spec:
  ingressClassName: nginx
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-frontend
                port:
                  number: 80
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: my-backend
                port:
                  number: 8080
  tls:
    - hosts:
        - myapp.example.com
      secretName: my-tls-cert
```

### ConfigMap

Stores non-sensitive configuration as key-value pairs. Pods read these as environment variables or mounted files. This decouples configuration from the container image, which is what you want.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
data:
  DATABASE_NAME: "mydb"
  LOG_LEVEL: "info"
  config.yaml: |            # Can also store entire files
    server:
      port: 8080
      debug: false
```

You can use it in a pod in several ways:

```yaml
# As individual env vars:
env:
  - name: DATABASE_NAME
    valueFrom:
      configMapKeyRef:
        name: my-config
        key: DATABASE_NAME

# Or load all keys as env vars:
envFrom:
  - configMapRef:
      name: my-config

# Or mount as a file:
volumeMounts:
  - name: config
    mountPath: /etc/config
volumes:
  - name: config
    configMap:
      name: my-config
```

### Secret

Like ConfigMap, but for sensitive data: passwords, API keys, certificates. Values are base64-encoded (not encrypted by default, but K8s treats them differently - restricted access, not shown in logs, can be encrypted at rest).

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secrets
type: Opaque
stringData:                  # stringData: plain text (K8s base64-encodes it)
  DATABASE_PASSWORD: "s3cret"
  API_KEY: "sk-abc123"
```

Using in a pod:

```yaml
env:
  - name: DATABASE_PASSWORD
    valueFrom:
      secretKeyRef:
        name: my-secrets
        key: DATABASE_PASSWORD
```

```bash
kubectl get secrets -n my-app
kubectl describe secret my-secrets -n my-app  # Shows keys but NOT values
```

### Where Do All These YAML Files Live?

This is worth addressing because it's not obvious when you're starting out. You've now seen Deployments, Services, ConfigMaps, Secrets, and more - all defined as YAML manifests. But where do these files actually go? Are they in your repo? How do they get applied?

**Most manifests go into version control.** Deployments, Services, Ingresses, ConfigMaps, NetworkPolicies, HPAs - all of these belong in your Git repo, typically in a folder like `k8s/` or `infrastructure/kubernetes/`. You apply them with `kubectl apply -f` or, better yet, through a GitOps tool like ArgoCD that syncs your repo to the cluster automatically.

**Secrets are the exception.** You should never commit actual passwords or API keys to Git. So how do you handle them? A few common approaches:

- **Create them manually with kubectl:**
  
  ```bash
  kubectl create secret generic my-secrets \
    --from-literal=DATABASE_PASSWORD=s3cret \
    --from-literal=API_KEY=sk-abc123 \
    -n my-app
  ```
  
  Simple, but now there's no record of it anywhere. Someone has to remember what secrets exist and what values they have.

- **Sealed Secrets (Bitnami):** You write a Secret manifest, encrypt it with a tool called `kubeseal`, and commit the *encrypted* version to Git. Only the cluster can decrypt it. This way you get the benefits of version control without exposing the actual values.

- **External secret stores:** Tools like External Secrets Operator sync secrets from AWS Secrets Manager, Azure Key Vault, or HashiCorp Vault into your cluster. The secret values live in the vault, and K8s pulls them in at runtime. This is the most common approach in production.

So the general rule: everything goes in Git except actual secret values. For those, use one of the approaches above.

### PersistentVolumeClaim (PVC)

Requests storage, like a virtual disk. K8s finds or creates a PersistentVolume (PV) that satisfies the request. The pod mounts it as a directory.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-data
spec:
  accessModes:
    - ReadWriteOnce          # One pod can write at a time
  resources:
    requests:
      storage: 10Gi
  storageClassName: standard # Depends on cloud provider
```

Access modes:

- `ReadWriteOnce` (RWO): one pod reads/writes. Most common, works with block storage.
- `ReadOnlyMany` (ROX): many pods read, none write.
- `ReadWriteMany` (RWX): many pods read/write. Requires special storage like NFS or Azure Files.

There's also **emptyDir**, a simpler alternative: temporary storage that dies with the pod. No PVC needed, but data is lost on restart.

```yaml
volumes:
  - name: temp-data
    emptyDir: {}             # Temporary, dies with the pod
  - name: persistent-data
    persistentVolumeClaim:
      claimName: my-data     # Survives pod restarts
```

### Job and CronJob

A Job runs a container to completion, then stops. Unlike Deployments (which keep pods running forever), Jobs are for one-time tasks.

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migrate
spec:
  template:
    spec:
      restartPolicy: OnFailure
      containers:
        - name: migrate
          image: my-app:v2.0
          command: ["python", "-m", "alembic", "upgrade", "head"]
  backoffLimit: 3            # Retry up to 3 times on failure
```

Common uses: database migrations, batch processing, data imports.

A **CronJob** is a Job on a schedule:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: nightly-cleanup
spec:
  schedule: "0 2 * * *"     # 2 AM every night
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
            - name: cleanup
              image: my-app:v2.0
              command: ["python", "cleanup.py"]
```

### DaemonSet

Ensures one pod runs on **every node** in the cluster. When a new node joins, K8s automatically adds a pod to it. When a node is removed, the pod is garbage collected.

Used for things like log collectors (Fluentd), monitoring agents (Prometheus node-exporter), and network plugins (Calico, Cilium).

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: log-collector
spec:
  selector:
    matchLabels:
      app: log-collector
  template:
    metadata:
      labels:
        app: log-collector
    spec:
      containers:
        - name: fluentd
          image: fluentd:latest
          volumeMounts:
            - name: varlog
              mountPath: /var/log
      volumes:
        - name: varlog
          hostPath:
            path: /var/log
```

### NetworkPolicy

Firewall rules for pods. By default, all pods can talk to all other pods. NetworkPolicies restrict this.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-only-backend
  namespace: my-app
spec:
  podSelector:
    matchLabels:
      app: my-db              # Apply to database pods
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: my-backend  # Only backend pods can connect
      ports:
        - port: 5432
```

### HorizontalPodAutoscaler (HPA)

Automatically scales the number of pod replicas based on metrics like CPU or memory usage.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70   # Scale up when CPU > 70%
```

```bash
kubectl get hpa -n my-app
kubectl describe hpa my-app-hpa -n my-app
```

### ServiceAccount, Roles, and RBAC

A **ServiceAccount** is an identity for pods. When a pod needs to talk to the Kubernetes API (e.g., an operator), it uses a ServiceAccount. Also used for cloud identity (Azure Workload Identity, AWS IRSA).

**Role** and **RoleBinding** control what a ServiceAccount can do. Role defines permissions, RoleBinding assigns them.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-manager
  namespace: my-app
rules:
  - apiGroups: [""]
    resources: ["pods", "services"]
    verbs: ["get", "list", "create", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: operator-can-manage-pods
  namespace: my-app
subjects:
  - kind: ServiceAccount
    name: my-operator
roleRef:
  kind: Role
  name: pod-manager
  apiGroup: rbac.authorization.k8s.io
```

**ClusterRole / ClusterRoleBinding** is the same thing but cluster-wide instead of namespaced.

### CustomResourceDefinition (CRD)

CRDs teach K8s a new resource type. After applying a CRD, you can create instances of that type just like built-in resources.

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: widgets.example.com
spec:
  group: example.com
  names:
    kind: Widget
    plural: widgets
    singular: widget
    shortNames: [wg]
  scope: Namespaced
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                color:
                  type: string
                size:
                  type: integer
```

Now you can do:

```yaml
apiVersion: example.com/v1
kind: Widget
metadata:
  name: my-widget
spec:
  color: blue
  size: 42
```

But CRDs alone don't do anything. You need an **operator** - a program running in the cluster that watches for these custom resources and acts on them. More on that next.

## Operators

An operator is a program (typically Go, sometimes Python) running as a pod in your cluster. It watches for changes to custom resources and creates, updates, or deletes other resources in response.

The pattern:

1. Define CRDs (what your custom resources look like)
2. Write an operator (what to do when CRs are created/changed/deleted)
3. Deploy the operator as a Deployment in the cluster
4. Users create CRs, the operator reacts

Here's a concrete example. Imagine a database operator. You create a CR like:

```yaml
kind: Database
spec:
  engine: postgres
  version: "15"
  storage: 50Gi
```

The operator sees this and creates: a StatefulSet, a Service, a PVC, a Secret with generated credentials, and runs initial setup. You didn't write any of those manifests. The operator did it all from one small CR.

Popular frameworks for writing operators:

- **Kubebuilder** (Go): most common, production-grade
- **Kopf** (Python): simpler, great for learning
- **Operator SDK** (Go/Ansible/Helm): Red Hat's framework

## Manifests

A manifest is a YAML file describing one or more K8s resources. It's not code, it's a declaration: "I want this to exist." You apply it with `kubectl apply -f` and K8s makes it happen.

A single file can contain multiple resources separated by `---`:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: my-app
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: my-app
spec:
  # ...
---
apiVersion: v1
kind: Service
metadata:
  name: my-app
  namespace: my-app
spec:
  # ...
```

**Important:** `kubectl apply -f my-file.yaml` sends the YAML to the K8s API server, which stores it in etcd. From that point on, the file on disk doesn't matter. If you edit the file but don't run `kubectl apply` again, nothing changes in the cluster. K8s works from etcd, not from your filesystem.

```bash
kubectl apply -f my-file.yaml      # Create or update resources from a file
kubectl apply -f ./k8s/            # Apply all YAML files in a directory
kubectl delete -f my-file.yaml     # Delete the resources defined in a file
kubectl diff -f my-file.yaml       # Show what would change without applying
```

## kubectl

The CLI for interacting with Kubernetes. Every command talks to the API server.

### Command Structure

```bash
kubectl <verb> <resource-type> <name> -n <namespace> <flags>
```

### Common Verbs

| Verb              | What it does                                  |
| ----------------- | --------------------------------------------- |
| `get`             | List resources                                |
| `describe`        | Detailed info about a specific resource       |
| `apply -f`        | Create or update from a YAML file             |
| `delete`          | Delete a resource                             |
| `logs`            | View pod logs                                 |
| `exec`            | Run a command inside a pod                    |
| `port-forward`    | Tunnel a port from localhost to a pod/service |
| `rollout restart` | Restart all pods in a deployment              |
| `scale`           | Change replica count                          |

### Common Flags

| Flag                | Short           | What it does                     |
| ------------------- | --------------- | -------------------------------- |
| `--namespace my-ns` | `-n my-ns`      | Target a specific namespace      |
| `--all-namespaces`  | `-A`            | All namespaces                   |
| `--output yaml`     | `-o yaml`       | Output in YAML format            |
| `--output json`     | `-o json`       | Output in JSON format            |
| `--selector app=x`  | `-l app=x`      | Filter by label                  |
| `--watch`           | `-w`            | Watch for changes (live updates) |
| `--tail=50`         |                 | Last N log lines                 |
| `--follow`          | `-f` (in logs)  | Stream logs in real-time         |
| `--filename`        | `-f` (in apply) | Read from file                   |

Note that `-f` means different things in different contexts: in `kubectl logs` it means "follow," in `kubectl apply` it means "file."

### Resource Short Names

| Full name                 | Short  |
| ------------------------- | ------ |
| pods                      | po     |
| services                  | svc    |
| deployments               | deploy |
| namespaces                | ns     |
| configmaps                | cm     |
| persistentvolumeclaims    | pvc    |
| horizontalpodautoscalers  | hpa    |
| customresourcedefinitions | crd    |

### Common Workflows

```bash
# See everything in a namespace
kubectl get all -n my-app

# Debug a pod that won't start
kubectl describe pod my-pod -n my-app   # Look at "Events" section at bottom
kubectl logs my-pod -n my-app           # Check application logs
kubectl get events -n my-app            # Cluster events (scheduling, pulling, etc.)

# See what K8s has stored (regardless of what's on disk)
kubectl get deployment my-app -n my-app -o yaml

# Watch pods in real-time
kubectl get pods -n my-app -w

# Quick port access to a service
kubectl port-forward svc/my-app 8080:80 -n my-app
# Now http://localhost:8080 reaches the service

# Run a one-off debug container
kubectl run debug --rm -it --image=busybox -- /bin/sh
```

## Minikube

Minikube runs a single-node Kubernetes cluster on your local machine inside a Docker container. It's for development and testing.

```bash
# Lifecycle
minikube start --driver=docker --cpus=4 --memory=8192
minikube stop                        # Pause (preserves state)
minikube delete                      # Destroy everything

# Status
minikube status
minikube ip                          # Node IP (internal to Docker on Windows)

# Images
minikube image load my-app:v1        # Copy image from host Docker into Minikube
minikube image rm my-app:v1          # Remove image from Minikube
minikube image list                  # List images inside Minikube

# Access
minikube service my-svc -n my-ns     # Open a tunnel + browser to a service
minikube tunnel                      # Expose LoadBalancer services on localhost

# Addons
minikube addons list                 # Available addons
minikube addons enable ingress       # Enable nginx ingress controller
minikube addons enable metrics-server # Enable HPA metrics
```

### Two Separate Docker Daemons

This trips people up. Your host machine runs Docker Desktop. Minikube runs its own Docker inside its container. They don't share images.

```
Host Docker (your terminal):
  - docker build creates images HERE
  - docker image ls shows host images

Minikube Docker (inside the cluster):
  - K8s pulls images from HERE
  - minikube image list shows these images
```

To get images from host into Minikube:

```bash
# Option 1: load from host
docker build -t my-app:v1 .
minikube image load my-app:v1

# Option 2: build directly inside Minikube
eval $(minikube docker-env)     # Point docker CLI at Minikube's daemon
docker build -t my-app:v1 .    # Built inside Minikube directly
eval $(minikube docker-env -u)  # Reset back to host Docker
```

When using locally loaded images, set `imagePullPolicy: Never` in your manifests. Otherwise K8s tries to pull from Docker Hub and fails.

### Minikube on Windows with Docker Driver

On Windows, the Minikube node is a Docker container on an internal network (`192.168.49.2`). It's not directly reachable from your browser. To access services:

```bash
# Option 1: port-forward (temporary, lives as long as terminal is open)
kubectl port-forward svc/my-app 3000:80 -n my-app

# Option 2: minikube service (auto-tunnels and opens browser)
minikube service my-app -n my-app

# Option 3: minikube tunnel (for LoadBalancer type services)
minikube tunnel
```

## How Things Fit Together

Let me walk through a complete example. Suppose we're deploying a web app with a frontend, backend API, background workers, a database, and a cache.

### The Resources

```
Namespace: my-app
│
├── Deployment: frontend (2 replicas)
│   └── Pods running nginx serving static files
│
├── Deployment: backend-api (3 replicas)
│   └── Pods running Python/FastAPI
│
├── Deployment: workers (2 replicas)
│   └── Pods running background job consumers
│
├── StatefulSet: database (1 replica)
│   └── Pod running PostgreSQL with persistent storage
│
├── Deployment: cache (1 replica)
│   └── Pod running Redis
│
├── Service: frontend (ClusterIP, port 80)
├── Service: backend-api (ClusterIP, port 8000)
├── Service: database (ClusterIP, port 5432)
├── Service: cache (ClusterIP, port 6379)
│
├── Ingress: routes myapp.com -> frontend, myapp.com/api -> backend-api
│
├── ConfigMap: app-config (non-sensitive settings)
├── Secret: app-secrets (database password, API keys)
│
├── HPA: backend-api (scale 3-10 pods on CPU > 70%)
├── HPA: workers (scale 2-20 pods on queue depth)
│
└── NetworkPolicy: database only accepts connections from backend-api and workers
```

### The Request Flow

```
User browser
    │
    ▼
Ingress Controller (nginx)
    │
    ├── myapp.com/ ──────────> Service: frontend ──> frontend pods (nginx)
    │
    └── myapp.com/api/ ──────> Service: backend-api ──> backend pods (FastAPI)
                                    │
                                    ├──> Service: database ──> PostgreSQL pod
                                    ├──> Service: cache ──> Redis pod
                                    └──> RPUSH job to Redis
                                              │
                                              ▼
                                         worker pods (BLPOP from Redis, process jobs)
                                              │
                                              └──> external APIs, database writes, etc.
```

# 

## Key Concepts Summary

| Concept                      | What it means                                                                                                                       |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Declarative**              | You describe WHAT you want, K8s figures out HOW                                                                                     |
| **Reconciliation**           | K8s constantly compares desired state vs actual state and fixes differences                                                         |
| **Labels & Selectors**       | Labels are tags on resources. Selectors filter by tags. This is how Deployments find their Pods, Services find their backends, etc. |
| **Rolling updates**          | New pods start, health checks pass, old pods terminate. Zero downtime.                                                              |
| **Self-healing**             | Pod crashes? Deployment creates a new one. Node dies? Pods get rescheduled elsewhere.                                               |
| **Immutable infrastructure** | Don't SSH into pods and change things. Build a new image, roll it out.                                                              |
| **12-factor**                | Config via env vars, logs to stdout, stateless processes, backing services as attached resources. K8s is designed around this.      |
