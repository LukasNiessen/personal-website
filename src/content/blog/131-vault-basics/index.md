---
title: 'HashiCorp Vault Basics: Secrets Management Done Right'
summary: 'A comprehensive guide to HashiCorp Vault fundamentals, from secret engines to authentication methods'
date: 'Feb 26 2024'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Vault
  - Security
  - DevOps
  - HashiCorp
---

# HashiCorp Vault Basics: Secrets Management Done Right

HashiCorp Vault is a secrets management platform that provides secure storage, dynamic secrets generation, and encryption services. Instead of hardcoding passwords in your applications or storing them in plain text files, Vault centralizes secrets management with robust access controls and audit logging.

## What Problems Does Vault Solve?

**The Traditional Approach:**
- Passwords stored in configuration files
- Database credentials hardcoded in applications
- API keys committed to version control
- SSH keys shared via email or Slack
- No audit trail of who accessed what when

**The Vault Approach:**
- Centralized secret storage with encryption at rest
- Dynamic secrets that are generated on-demand and automatically rotated
- Fine-grained access policies
- Complete audit logging
- Secret versioning and rollback capabilities

## The Big Picture: How Vault Actually Works

Before diving into commands and concepts, let's understand **what Vault actually is** and how it fits into your infrastructure.

### Vault is a Server

**Vault is a standalone server application** that you run as part of your infrastructure. Think of it like running a database server, Redis, or any other service.

```bash
# Vault runs as a server process
vault server -config=/etc/vault/vault.hcl
```

**Deployment options:**
- **Docker container:** `docker run vault:latest vault server -config=/vault/config`
- **AWS ECS/Fargate:** Deploy Vault container with persistent storage
- **Kubernetes:** Deploy as StatefulSet with persistent volumes
- **VMs:** Install Vault binary and run as systemd service
- **Managed service:** HashiCorp Cloud Platform (HCP) Vault

### The Architecture Flow

Here's how your applications actually interact with Vault:

```
┌─────────────────┐    HTTP API     ┌─────────────────┐    Backend     ┌─────────────────┐
│                 │   (REST/JSON)   │                 │   Storage      │                 │
│  Your App       ├────────────────►│  Vault Server   ├───────────────►│  Consul/etcd/   │
│  (Docker/ECS)   │                 │  (Port 8200)    │                │  S3/PostgreSQL  │
│                 │◄────────────────┤                 │                │                 │
└─────────────────┘                 └─────────────────┘                └─────────────────┘
```

**Step-by-step flow:**
1. **Vault server runs** on infrastructure (ECS, Kubernetes, VMs)
2. **Your application starts up** and needs secrets
3. **App authenticates** to Vault using HTTP API
4. **App requests secrets** via HTTP calls to Vault
5. **Vault returns secrets** as JSON responses
6. **App uses secrets** to connect to databases, APIs, etc.

### Concrete Docker/ECS Example

**Vault Server Container:**
```dockerfile
# Dockerfile for Vault server
FROM vault:1.15.2

COPY vault.hcl /vault/config/
COPY policies/ /vault/policies/

EXPOSE 8200
EXPOSE 8201

CMD ["vault", "server", "-config=/vault/config/vault.hcl"]
```

**Application Container:**
```dockerfile
# Your application Dockerfile
FROM python:3.9

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

# App connects to Vault at runtime via HTTP
ENV VAULT_ADDR=http://vault-server:8200

CMD ["python", "app.py"]
```

**ECS Task Definition:**
```json
{
  "family": "my-app-stack",
  "taskDefinition": {
    "containerDefinitions": [
      {
        "name": "vault-server",
        "image": "vault:1.15.2",
        "portMappings": [{"containerPort": 8200}],
        "environment": [
          {"name": "VAULT_DEV_ROOT_TOKEN_ID", "value": "dev-token"}
        ]
      },
      {
        "name": "my-app",
        "image": "my-app:latest",
        "environment": [
          {"name": "VAULT_ADDR", "value": "http://localhost:8200"}
        ],
        "dependsOn": [{"containerName": "vault-server"}]
      }
    ]
  }
}
```

### How Applications Authenticate to Vault

This is the key question: **How does your app prove its identity to Vault?**

**Option 1: AWS IAM Authentication (ECS/EC2)**
```python
import hvac
import boto3

# App running on ECS with IAM role
client = hvac.Client(url='http://vault-server:8200')

# Authenticate using AWS IAM role
aws_auth = client.auth.aws
aws_auth.iam_login(
    access_key=boto3.Session().get_credentials().access_key,
    secret_key=boto3.Session().get_credentials().secret_key,
    session_token=boto3.Session().get_credentials().token,
    role='my-ecs-role'
)
```

**Option 2: Kubernetes Service Account (K8s)**
```python
import hvac

# App running in Kubernetes pod
client = hvac.Client(url='http://vault-service:8200')

# Read service account token from pod
with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as f:
    jwt = f.read()

# Authenticate using Kubernetes service account
client.auth.kubernetes.login(role='my-k8s-role', jwt=jwt)
```

**Option 3: AppRole (Generic)**
```python
import hvac
import os

client = hvac.Client(url=os.environ['VAULT_ADDR'])

# Authenticate using AppRole (role_id from config, secret_id from startup)
client.auth.approle.login(
    role_id=os.environ['VAULT_ROLE_ID'],
    secret_id=os.environ['VAULT_SECRET_ID']
)
```

### Real Application Example

Here's how a Python web app actually uses Vault:

```python
import hvac
import os
import psycopg2
from flask import Flask

app = Flask(__name__)

class VaultClient:
    def __init__(self):
        # Connect to Vault server
        self.client = hvac.Client(url=os.environ['VAULT_ADDR'])
        
        # Authenticate (using AWS IAM in this example)
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate to Vault using AWS IAM"""
        try:
            # This works when running on EC2/ECS with proper IAM role
            import boto3
            session = boto3.Session()
            credentials = session.get_credentials()
            
            self.client.auth.aws.iam_login(
                access_key=credentials.access_key,
                secret_key=credentials.secret_key,
                session_token=credentials.token,
                role='webapp-role'  # Configured in Vault
            )
            print("Successfully authenticated to Vault")
        except Exception as e:
            print(f"Failed to authenticate to Vault: {e}")
            raise
    
    def get_db_connection(self):
        """Get database connection using Vault-managed credentials"""
        # Request fresh database credentials from Vault
        response = self.client.secrets.database.generate_credentials(
            name='postgres-readonly'  # Role configured in Vault
        )
        
        creds = response['data']
        
        # Use the temporary credentials
        return psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            user=creds['username'],      # Generated by Vault
            password=creds['password']    # Generated by Vault
        )

# Initialize Vault client when app starts
vault_client = VaultClient()

@app.route('/data')
def get_data():
    # Get fresh DB connection with Vault-managed credentials
    conn = vault_client.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    conn.close()
    return {'users': result}

if __name__ == '__main__':
    app.run()
```

### Infrastructure Setup Summary

**What you actually deploy:**
1. **Vault server** (Docker container, VM, or managed service)
2. **Your applications** that make HTTP calls to Vault
3. **Storage backend** for Vault (Consul, PostgreSQL, S3, etc.)
4. **Network connectivity** between apps and Vault
5. **IAM roles/service accounts** for authentication

**The HTTP API is everything:**
- All Vault operations happen via HTTP REST API
- Applications use HTTP client libraries (hvac for Python, etc.)
- Authentication, secret retrieval, token renewal - all HTTP calls
- Vault CLI commands are just wrappers around HTTP API calls

## Core Concepts

### Secrets Engines

Secrets engines are components that store, generate, or encrypt data. Each engine is mounted at a specific path and handles requests for that path.

**Key-Value (KV) Engine:**
The simplest engine - stores arbitrary key-value pairs.

```bash
# Enable KV v2 engine
vault secrets enable -path=secret kv-v2

# Store a secret
vault kv put secret/myapp/db username=admin password=supersecret

# Read a secret  
vault kv get secret/myapp/db

# Get specific field
vault kv get -field=password secret/myapp/db
```

**Database Engine:**
Generates dynamic database credentials with automatic rotation.

```bash
# Enable database engine
vault secrets enable database

# Configure database connection
vault write database/config/my-mysql-database \
    plugin_name=mysql-database-plugin \
    connection_url="{{username}}:{{password}}@tcp(localhost:3306)/" \
    allowed_roles="my-role" \
    username="vaultadmin" \
    password="vaultpass"

# Create a role
vault write database/roles/my-role \
    db_name=my-mysql-database \
    creation_statements="CREATE USER '{{name}}'@'%' IDENTIFIED BY '{{password}}';GRANT SELECT ON *.* TO '{{name}}'@'%';" \
    default_ttl="1h" \
    max_ttl="24h"

# Generate credentials
vault read database/creds/my-role
```

This creates temporary database users that automatically expire.

### Authentication Methods

Authentication methods (auth methods) are how clients prove their identity to Vault.

**Token Authentication:**
The default method. Every client needs a valid token.

```bash
# Create a token
vault token create

# Create token with specific policies
vault token create -policy=myapp-policy

# Look up token info
vault token lookup <token>
```

**Userpass Authentication:**
Username and password authentication.

```bash
# Enable userpass auth
vault auth enable userpass

# Create a user
vault write auth/userpass/users/john \
    password=mypassword \
    policies=dev-policy

# Login as user
vault auth -method=userpass username=john password=mypassword
```

**AWS IAM Authentication:**
Authenticate using AWS IAM credentials.

```bash
# Enable AWS auth
vault auth enable aws

# Configure AWS auth
vault write auth/aws/config/client \
    access_key=<access_key> \
    secret_key=<secret_key> \
    region=us-east-1

# Create role for EC2 instances
vault write auth/aws/role/dev-role \
    auth_type=iam \
    bound_iam_principal_arn=arn:aws:iam::123456789012:role/MyRole \
    policies=dev-policy \
    ttl=1h
```

**Kubernetes Authentication:**
Authenticate using Kubernetes service account tokens.

```bash
# Enable Kubernetes auth
vault auth enable kubernetes

# Configure Kubernetes auth
vault write auth/kubernetes/config \
    token_reviewer_jwt="<service-account-jwt>" \
    kubernetes_host="https://kubernetes.default.svc" \
    kubernetes_ca_cert=@ca.crt
```

### Policies

Policies define what actions are allowed on which paths. They're written in HashiCorp Configuration Language (HCL).

```hcl
# Example policy: myapp-policy.hcl
# Allow reading secrets under secret/myapp/*
path "secret/data/myapp/*" {
  capabilities = ["read"]
}

# Allow creating/updating secrets under secret/myapp/dev/*
path "secret/data/myapp/dev/*" {
  capabilities = ["create", "update", "read"]
}

# Allow generating database credentials
path "database/creds/my-role" {
  capabilities = ["read"]
}

# Deny access to admin secrets
path "secret/data/admin/*" {
  capabilities = ["deny"]
}
```

Apply the policy:
```bash
vault policy write myapp-policy myapp-policy.hcl
```

Capabilities include:
- `create` - Create new data
- `read` - Read data  
- `update` - Update existing data
- `delete` - Delete data
- `list` - List keys
- `sudo` - Admin operations
- `deny` - Explicitly deny access

### Tokens

Tokens are the core authentication mechanism. Every request to Vault must include a valid token.

**Token Properties:**
- **TTL (Time To Live):** How long the token is valid
- **Policies:** What the token is allowed to do
- **Renewable:** Whether the token can be refreshed
- **Parent Token:** Tokens can create child tokens

```bash
# Create token with specific TTL
vault token create -ttl=1h

# Create renewable token
vault token create -renewable=true

# Renew a token
vault token renew <token>

# Revoke a token
vault token revoke <token>
```

## Practical Example: Application Integration

Here's how you might integrate Vault into a web application:

### 1. Setup Vault

```bash
# Start Vault in dev mode (for testing only!)
vault server -dev

# Set environment variables
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='<root-token-from-dev-server>'

# Enable KV engine
vault secrets enable -path=secret kv-v2

# Store database credentials
vault kv put secret/webapp/prod \
    db_username=produser \
    db_password=prodpass123 \
    api_key=abc123xyz
```

### 2. Create Policy

```hcl
# webapp-policy.hcl
path "secret/data/webapp/prod" {
  capabilities = ["read"]
}

path "auth/token/renew-self" {
  capabilities = ["update"]
}
```

```bash
vault policy write webapp-policy webapp-policy.hcl
```

### 3. Application Code (Python Example)

```python
import hvac
import os

class VaultClient:
    def __init__(self):
        self.client = hvac.Client(
            url=os.environ['VAULT_ADDR'],
            token=os.environ['VAULT_TOKEN']
        )
    
    def get_secret(self, path):
        """Get secret from Vault"""
        try:
            response = self.client.secrets.kv.v2.read_secret_version(
                path=path
            )
            return response['data']['data']
        except Exception as e:
            print(f"Error reading secret: {e}")
            return None
    
    def get_db_credentials(self):
        """Get database credentials"""
        secrets = self.get_secret('webapp/prod')
        if secrets:
            return {
                'username': secrets['db_username'],
                'password': secrets['db_password']
            }
        return None

# Usage
vault_client = VaultClient()
db_creds = vault_client.get_db_credentials()

if db_creds:
    # Use credentials to connect to database
    connection_string = f"mysql://{db_creds['username']}:{db_creds['password']}@localhost/mydb"
```

### 4. Token Management

For production applications, you should:

1. **Use short-lived tokens** with automatic renewal
2. **Authenticate using appropriate auth methods** (not root tokens)
3. **Handle token expiration gracefully**

```python
def renew_token_if_needed(self):
    """Renew token if it's close to expiring"""
    try:
        token_info = self.client.auth.token.lookup_self()
        ttl = token_info['data']['ttl']
        
        # Renew if less than 5 minutes remaining
        if ttl < 300:  
            self.client.auth.token.renew_self()
            print("Token renewed successfully")
    except Exception as e:
        print(f"Error renewing token: {e}")
```

## Dynamic Secrets Example

Dynamic secrets are generated on-demand and automatically expire. Here's a PostgreSQL example:

### 1. Configure Database Connection

```bash
# Enable database engine
vault secrets enable database

# Configure PostgreSQL connection
vault write database/config/postgresql \
    plugin_name=postgresql-database-plugin \
    connection_url="postgresql://{{username}}:{{password}}@localhost:5432/postgres?sslmode=disable" \
    allowed_roles="readonly" \
    username="vaultadmin" \
    password="vaultpass"
```

### 2. Create Database Role

```bash
vault write database/roles/readonly \
    db_name=postgresql \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
    default_ttl="1h" \
    max_ttl="24h"
```

### 3. Generate Credentials

```bash
# Generate temporary database credentials
vault read database/creds/readonly

# Output:
# Key                Value
# ---                -----
# lease_id           database/creds/readonly/abc123
# lease_duration     1h
# lease_renewable    true
# password           A1a-randompassword123
# username           v-token-readonly-xyz789
```

These credentials automatically expire after 1 hour and the database user is automatically cleaned up.

## Essential Vault Commands

### Server Operations

```bash
# Start Vault server
vault server -config=vault.hcl

# Initialize Vault (first time only)
vault operator init

# Unseal Vault (after restart)
vault operator unseal <unseal-key>

# Check status
vault status
```

### Secret Operations

```bash
# List secret engines
vault secrets list

# List secrets at path
vault kv list secret/

# Get secret metadata
vault kv metadata get secret/myapp/db

# Delete secret version
vault kv delete secret/myapp/db

# Undelete secret version
vault kv undelete -versions=1 secret/myapp/db
```

### Authentication

```bash
# List auth methods
vault auth list

# Login with different methods
vault auth -method=userpass username=john
vault auth -method=aws role=dev-role

# Create service token
vault token create -policy=myapp-policy -period=24h
```

### Policy Management

```bash
# List policies
vault policy list

# Read policy
vault policy read myapp-policy

# Delete policy
vault policy delete myapp-policy
```

## Vault Architecture

### Seal/Unseal Process

Vault starts in a "sealed" state where it cannot decrypt data. Unsealing requires threshold number of keys.

**Why sealing matters:** If someone gains access to the Vault server, they can't read encrypted data without unsealing it first.

```bash
# Check seal status
vault status

# Unseal (requires threshold number of key shares)
vault operator unseal <key-1>
vault operator unseal <key-2>
vault operator unseal <key-3>
```

### Storage Backend

Vault encrypts data before storing it in the backend. Common backends:

- **Consul:** Highly available, supports clustering
- **etcd:** Kubernetes-native option
- **File:** Simple filesystem storage (development only)
- **S3:** AWS object storage
- **PostgreSQL:** Relational database storage

Example configuration:
```hcl
# vault.hcl
storage "consul" {
  address = "127.0.0.1:8500"
  path    = "vault/"
}

listener "tcp" {
  address = "0.0.0.0:8200"
  tls_disable = 1
}

ui = true
```

## High Availability and Clustering

Vault Enterprise supports active-passive clustering:

```hcl
# vault.hcl for clustered setup
storage "consul" {
  address = "127.0.0.1:8500"
  path    = "vault/"
}

listener "tcp" {
  address = "0.0.0.0:8200"
  cluster_address = "0.0.0.0:8201"
  tls_cert_file = "/opt/vault/tls/vault.crt"
  tls_key_file = "/opt/vault/tls/vault.key"
}

api_addr = "https://vault-1.company.com:8200"
cluster_addr = "https://vault-1.company.com:8201"
```

Only one node is active at a time; others are on standby and automatically take over if the active node fails.

## Security Best Practices

### 1. Never Use Root Tokens in Production

Root tokens have unlimited access. Create service-specific tokens instead:

```bash
# Bad: Using root token
export VAULT_TOKEN="s.roottoken123"

# Good: Create limited token
vault token create -policy=myapp-policy -period=24h
```

### 2. Use Short-Lived Tokens

Minimize blast radius by using tokens with short TTLs:

```bash
# Create token with 1-hour TTL
vault token create -ttl=1h -renewable=true
```

### 3. Implement Proper Access Policies

Follow principle of least privilege:

```hcl
# Too permissive
path "*" {
  capabilities = ["read", "write"]
}

# Better: Specific paths and capabilities
path "secret/data/myapp/*" {
  capabilities = ["read"]
}
```

### 4. Enable Audit Logging

Track all Vault operations:

```bash
# Enable file audit logging
vault audit enable file file_path=/vault/logs/audit.log

# Enable syslog audit logging
vault audit enable syslog
```

### 5. Use Auto-Unseal

For production, use auto-unseal to avoid manual intervention:

```hcl
seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "alias/vault-unseal-key"
}
```

## Vault vs Other Secret Management Tools

### Vault vs AWS Secrets Manager

**Vault Pros:**
- Multi-cloud and on-premise support
- Dynamic secrets generation
- More flexible authentication methods
- Better integration with non-AWS services
- More granular access controls

**Vault Cons:**
- Higher operational overhead
- Requires separate infrastructure
- More complex setup

**AWS Secrets Manager Pros:**
- Native AWS integration
- Managed service (no ops overhead)
- Automatic rotation for supported services
- Simple setup

**AWS Secrets Manager Cons:**
- AWS-only
- Limited dynamic secret capabilities
- Less flexible access controls
- Higher cost for large-scale usage

### Vault vs Azure Key Vault

**Vault Pros:**
- Multi-cloud support
- Dynamic secrets
- More authentication methods
- Better programmatic access
- More flexible policies

**Azure Key Vault Pros:**
- Native Azure integration
- Hardware Security Module (HSM) support
- Managed service
- Certificate management

### Vault vs Kubernetes Secrets

**Vault Pros:**
- Encryption at rest by default
- Dynamic secrets
- Audit logging
- Fine-grained access controls
- Secret rotation capabilities

**Kubernetes Secrets Pros:**
- Native Kubernetes integration
- No additional infrastructure
- Simple for basic use cases

**Kubernetes Secrets Cons:**
- Base64 encoding, not encryption
- No audit logging
- Limited access controls
- No secret rotation
- Stored in etcd (potential security risk)

## Production Deployment Considerations

### 1. High Availability Setup

```bash
# Multiple Vault nodes with Consul backend
vault-1.company.com (active)
vault-2.company.com (standby)
vault-3.company.com (standby)
```

### 2. Backup and Recovery

```bash
# Backup Vault data (Consul example)
consul snapshot save backup.snap

# Create disaster recovery token
vault operator generate-root -dr-token
```

### 3. Monitoring

Key metrics to monitor:
- Token usage and expiration
- Secret access patterns
- Seal/unseal events
- Authentication failures
- Storage backend health

### 4. Network Security

- Use TLS everywhere
- Restrict network access to Vault ports
- Use VPN or private networks
- Implement WAF for HTTP endpoints

## Conclusion

HashiCorp Vault is a powerful secrets management platform that addresses critical security challenges in modern infrastructure. Its dynamic secrets, fine-grained access controls, and extensive audit capabilities make it suitable for enterprise environments.

The key is to start simple with basic KV secrets and gradually adopt advanced features like dynamic secrets and multiple auth methods as your requirements grow. Proper planning around high availability, backup strategies, and operational procedures is essential for production deployments.

Remember: Vault is only as secure as the infrastructure and processes around it. Invest time in proper setup, monitoring, and operational procedures to get the full benefit of centralized secrets management.