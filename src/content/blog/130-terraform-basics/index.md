---
title: 'Terraform Basics: Infrastructure as Code Done Right'
summary: 'A comprehensive guide to Terraform fundamentals, from resources to modules to state management'
date: 'August 21 2024'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Terraform
  - Infrastructure
  - DevOps
  - IaC
---

# Terraform Basics & Best Practices: Infrastructure as Code Done Right

I want to walk through some best practices of Terraform (TF) in here, as well as have some sort of a _cheat sheet_ for basic syntax and other basics.

## Best Practices

### 1. Use Remote State with Versioning and Locking

Terraform stores state in a `terraform.tfstate` file. **This file is the source of truth for Terraform!!** It's used for things like comparing current state (in that file) with your _'future plans'_ that you want to apply with `terraform apply`. So it's critically important.

By default, it's stored locally. This is fine for solo projects, but a disaster for teams. If two people try to apply changes at the same time, they can corrupt the state. Plus, if you lose your laptop, you lose the state.

The solution is **Remote State**. For AWS users, the standard pattern is using an S3 bucket for storage and a DynamoDB table for locking.

**Why?**
- **Single Source of Truth:** Everyone works off the same state.
- **Locking:** DynamoDB prevents concurrent updates.
- **Versioning:** S3 bucket versioning allows you to roll back if the state gets corrupted.

**How to set it up:**

First, you need the resources (bucket and table) to exist. You can create them manually or with a separate "bootstrap" Terraform project.

```hcl
# backend-resources.tf
resource "aws_s3_bucket" "terraform_state" {
  bucket = "my-company-terraform-state"
 
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "enabled" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

Then, configure your backend in your main Terraform code:

```hcl
terraform {
  backend "s3" {
    bucket         = "my-company-terraform-state"
    key            = "global/s3/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

### 2. Use Workspaces for Multiple Environments

Managing `dev`, `staging`, and `prod` can be tricky. You don't want to copy-paste your entire folder structure three times. Terraform Workspaces allow you to use the same code for multiple environments.

**Why?**
It keeps your code DRY (Don't Repeat Yourself). You write the infrastructure definition once, and deploy it multiple times with different variables.

**How to use it:**

```bash
terraform workspace new dev
terraform workspace new prod
terraform workspace select dev
```

In your code, you can reference `terraform.workspace` to change behavior:

```hcl
resource "aws_instance" "web" {
  instance_type = terraform.workspace == "prod" ? "t3.medium" : "t3.micro"
  
  tags = {
    Name = "web-server-${terraform.workspace}"
  }
}
```

### 3. Prefer `for_each` over `count`

While `count` is simple, it has a major flaw: it relies on the list index. If you remove an item from the middle of the list, every resource after it shifts its index, causing Terraform to destroy and recreate them.

**Why?**
`for_each` uses a map key or a set of strings as a stable identifier. If you remove an item, only that specific resource is destroyed.

**Example:**

Don't do this (risky):
```hcl
variable "users" {
  type    = list(string)
  default = ["alice", "bob", "charlie"]
}

resource "aws_iam_user" "example" {
  count = length(var.users)
  name  = var.users[count.index]
}
```
*If you remove "alice", "bob" becomes index 0 and "charlie" becomes index 1. Terraform will rewrite Bob's user to be Alice's old index, etc.*

Do this instead (safe):
```hcl
resource "aws_iam_user" "example" {
  for_each = toset(var.users)
  name     = each.key
}
```

### 4. Never Commit State Files to Git

This is a critical security rule. The `terraform.tfstate` file contains the **full** configuration of your resources, including sensitive data like database passwords, private keys, and API tokens—even if you defined them as "sensitive" variables.

**Why?**
If you push this file to a public (or even private) repository, anyone with access to the repo has your secrets in plain text.

**What to do:**
Add these to your `.gitignore` immediately:

```gitignore
*.tfstate
*.tfstate.backup
.terraform/
```

Always use a remote backend (like S3) which supports encryption at rest.

### 5. Use Modules for Code Reuse

As your infrastructure grows, a single `main.tf` file becomes unmanageable. Modules allow you to package resources into reusable components.

**Why?**
- **Standardization:** You can enforce best practices (e.g., "all S3 buckets must be encrypted") by baking them into a module.
- **Readability:** Your main configuration becomes a high-level description of *what* you want, rather than *how* to build it.

**Example:**

Instead of defining 50 lines of security group rules every time you need a web server, create a module:

```hcl
module "web_server_sg" {
  source = "./modules/security-group"
  
  name        = "web-server"
  vpc_id      = module.vpc.vpc_id
  open_ports  = [80, 443]
}
```

## Conventions & Folder Structure

How you organize your Terraform code depends heavily on your project size and whether infrastructure is your main product or just a supporting player.

### Scenario 1: The "App Repo" (Non-Dedicated)

If you have a backend service (e.g., a Node.js API) and you want to keep the infrastructure code close to the application code, this is the way to go. This is common for microservices where each service owns its own infrastructure (like an S3 bucket or a DynamoDB table).

**Structure:**

```text
my-app/
├── src/              # Application code
├── package.json
├── ...
└── infrastructure/   # Terraform code lives here
    ├── main.tf       # Resources
    ├── variables.tf  # Input variables
    ├── outputs.tf    # Output values
    ├── providers.tf  # Provider configuration
    └── envs/         # Environment-specific variable files
        ├── dev.tfvars
        └── prod.tfvars
```

**Pros:**
- Developers can change app code and infra in the same PR.
- Context switching is minimized.

**Cons:**
- Harder to manage shared infrastructure (like a VPC) that multiple apps use.

### Scenario 2: The "Infra Repo" (Dedicated)

For shared infrastructure (VPCs, K8s clusters, databases used by multiple apps) or large-scale systems, a dedicated repository is better. This is often managed by a Platform or DevOps team.

**Structure:**

```text
infrastructure-repo/
├── modules/                  # Reusable modules (internal)
│   ├── vpc/
│   └── eks/
├── environments/             # Live environments
│   ├── dev/
│   │   ├── main.tf           # Calls modules
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── prod/
└── README.md
```

**Pros:**
- Clear separation of concerns.
- Safer boundaries between environments (dev changes can't accidentally touch prod state if folders are separate).

**Cons:**
- More repositories to manage.
- "It works on my machine" issues if app devs don't have visibility into infra changes.

## Cheat Sheet

Here a walk through and repetition, or cheat sheet, of syntax and other basics.

### Resources

Resources are the fundamental building blocks in Terraform - they represent infrastructure components like EC2 instances, S3 buckets, or VPCs.

```hcl
resource "aws_instance" "web_server" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t3.micro"
  
  tags = {
    Name = "WebServer"
  }
}
```

Each resource has a type (`aws_instance`) and a local name (`web_server`) that you use to reference it elsewhere in your configuration.

### Data Sources

Data sources allow you to fetch information about existing infrastructure that Terraform doesn't manage directly.

```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
}
```

This fetches the latest Ubuntu AMI and uses it in the EC2 instance resource.

### Variables

Variables make your Terraform configurations reusable and flexible.

```hcl
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "environment" {
  description = "Environment name"
  type        = string
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  
  tags = {
    Environment = var.environment
  }
}
```

You can provide variable values through `.tfvars` files, command line, or environment variables.

### Outputs

Outputs expose information about your infrastructure after it's created.

```hcl
output "instance_ip" {
  description = "Public IP of the web server"
  value       = aws_instance.web.public_ip
}

output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.web.id
}
```

### Locals

Locals are named values that you can reuse throughout your configuration - think of them as internal variables.

```hcl
locals {
  common_tags = {
    Environment = var.environment
    Project     = "WebApp"
    ManagedBy   = "Terraform"
  }
  
  name_prefix = "${var.environment}-webapp"
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  
  tags = local.common_tags
}
```

### Providers

Providers are plugins that interact with APIs of cloud platforms, SaaS providers, and other services.

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
```

### Practical Example: VPC Setup

Here's a common pattern for setting up a VPC (Virtual Private Cloud - AWS's isolated network environment):

```hcl
# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "${local.name_prefix}-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "${local.name_prefix}-igw"
  }
}

# Public Subnet
resource "aws_subnet" "public" {
  count = length(var.availability_zones)
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = var.availability_zones[count.index]
  
  map_public_ip_on_launch = true
  
  tags = {
    Name = "${local.name_prefix}-public-${count.index + 1}"
    Type = "Public"
  }
}

# Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = {
    Name = "${local.name_prefix}-public-rt"
  }
}

# Route Table Association
resource "aws_route_table_association" "public" {
  count = length(aws_subnet.public)
  
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}
```

### For Loops and Dynamic Blocks

Terraform provides several ways to iterate and create multiple similar resources.

#### Count

```hcl
resource "aws_instance" "web" {
  count = 3
  
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public[count.index].id
  
  tags = {
    Name = "${local.name_prefix}-web-${count.index + 1}"
  }
}
```

#### for_each

More flexible than count, especially when you need to reference resources by key:

```hcl
variable "environments" {
  default = {
    dev  = "t3.micro"
    prod = "t3.small"
  }
}

resource "aws_instance" "app" {
  for_each = var.environments
  
  ami           = data.aws_ami.ubuntu.id
  instance_type = each.value
  
  tags = {
    Name        = "${each.key}-app"
    Environment = each.key
  }
}
```

**How does `each.key` work?** 

When using `for_each` with a map, Terraform iterates over each key-value pair:
- `each.key` = the map key ("dev", "prod")  
- `each.value` = the map value ("t3.micro", "t3.small")

So `"${each.key}-app"` becomes "dev-app" and "prod-app" respectively.

#### Dynamic Blocks

For creating nested blocks dynamically:

```hcl
resource "aws_security_group" "web" {
  name   = "${local.name_prefix}-web-sg"
  vpc_id = aws_vpc.main.id
  
  dynamic "ingress" {
    for_each = var.ingress_ports
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
}
```

### Modules

Modules are reusable Terraform configurations. Think of them as functions - they take inputs (variables) and produce outputs. This is arguably the most important concept for scaling Terraform usage across teams and projects.

**Why modules matter:** Instead of copying and pasting the same VPC configuration across 10 projects, you create a VPC module once and reuse it everywhere. When you need to add a security group rule to all VPCs, you update the module once instead of 10 separate configurations.

#### Creating a Module

A module is just a directory containing `.tf` files. Here's a simple web server module:

```hcl
# modules/web-server/main.tf
resource "aws_instance" "this" {
  ami                    = var.ami_id
  instance_type         = var.instance_type
  subnet_id             = var.subnet_id
  vpc_security_group_ids = [aws_security_group.this.id]
  
  tags = var.tags
}

resource "aws_security_group" "this" {
  name   = "${var.name}-sg"
  vpc_id = var.vpc_id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# modules/web-server/variables.tf
variable "name" {
  description = "Name prefix for resources"
  type        = string
}

variable "ami_id" {
  description = "AMI ID for the instance"
  type        = string
}

variable "instance_type" {
  description = "Instance type"
  type        = string
  default     = "t3.micro"
}

variable "subnet_id" {
  description = "Subnet ID"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}

# modules/web-server/outputs.tf
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.this.id
}

output "public_ip" {
  description = "Public IP of the instance"
  value       = aws_instance.this.public_ip
}
```

#### Using the Module

```hcl
module "web_server" {
  source = "./modules/web-server"
  
  name          = "my-web-app"
  ami_id        = data.aws_ami.ubuntu.id
  instance_type = "t3.small"
  subnet_id     = aws_subnet.public[0].id
  vpc_id        = aws_vpc.main.id
  
  tags = local.common_tags
}

output "web_server_ip" {
  value = module.web_server.public_ip
}
```

### Essential Commands

#### terraform init
Initializes a Terraform working directory. Downloads providers and modules.

```bash
terraform init
```

#### terraform plan
Shows what Terraform will do without actually doing it. Always run this before apply.

```bash
terraform plan
terraform plan -out=tfplan  # Save plan to file
```

#### terraform apply
Creates, updates, or deletes infrastructure to match your configuration.

```bash
terraform apply
terraform apply tfplan      # Apply saved plan
terraform apply -auto-approve  # Skip confirmation
```

#### terraform destroy
Destroys all resources managed by the configuration.

```bash
terraform destroy
terraform destroy -target=aws_instance.web  # Destroy specific resource
```

#### terraform fmt
Formats Terraform files to a canonical style.

```bash
terraform fmt
terraform fmt -recursive  # Format all files in subdirectories
```

#### terraform validate
Validates the configuration syntax.

```bash
terraform validate
```

### State Management

#### Terraform State File

Terraform stores information about your infrastructure in a state file (`.tfstate`). This file maps your configuration to the real world and tracks resource metadata.

**Important:** Never edit the state file manually. Use Terraform commands instead.

#### Remote State

For team environments, store state remotely:

```hcl
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}
```

#### State Lock

The `.terraform.lock.hcl` file locks dependency versions to ensure consistent builds across team members and environments.

```hcl
# .terraform.lock.hcl (auto-generated)
provider "registry.terraform.io/hashicorp/aws" {
  version     = "5.17.0"
  constraints = "~> 5.0"
  hashes = [
    "h1:U+EDfeUqefebA1h7KyBMD1xH2dPdGcYfgEUvDU6gT7w=",
    # ... more hashes
  ]
}
```

**Never delete this file.** Commit it to version control.

## Terraform vs Other IaC Tools

### Terraform vs CloudFormation

**Terraform Pros:**
- Multi-cloud support
- More intuitive HCL syntax
- Better state management
- Larger ecosystem of providers
- Plan functionality shows exact changes

**Terraform Cons:**
- State file management complexity
- Learning curve for HCL
- Requires separate tooling for some AWS-specific features

**CloudFormation Pros:**
- Native AWS integration
- No state file to manage
- Tight integration with AWS services
- Automatic rollback on failure

**CloudFormation Cons:**
- AWS-only
- JSON/YAML can be verbose
- Slower to support new AWS features
- Limited preview capabilities

### Terraform vs Pulumi

**Terraform Pros:**
- Declarative approach
- Mature ecosystem
- Large community
- Domain-specific language (HCL)

**Terraform Cons:**
- Limited programming constructs
- State management complexity

**Pulumi Pros:**
- Use familiar programming languages (Python, TypeScript, Go, etc.)
- Better for complex logic and calculations
- Native testing frameworks
- Object-oriented approach

**Pulumi Cons:**
- Smaller ecosystem
- Steeper learning curve for traditional ops teams
- Can lead to over-engineered infrastructure code

### Terraform vs Ansible

These tools serve different purposes but sometimes overlap:

**Terraform Pros:**
- Purpose-built for infrastructure provisioning
- Better state management for infrastructure
- Declarative approach ideal for infrastructure

**Terraform Cons:**
- Not designed for configuration management
- Limited post-deployment capabilities

**Ansible Pros:**
- Excellent for configuration management
- Agentless architecture
- Great for application deployment
- Imperative approach good for complex workflows

**Ansible Cons:**
- Weaker infrastructure provisioning
- No native state tracking
- Can be slower for large-scale operations

## Best Practices

1. **Always use version control** for your Terraform configurations
2. **Use remote state** for team environments
3. **Pin provider versions** to avoid unexpected changes
4. **Use modules** for reusable components
5. **Run terraform plan** before every apply
6. **Use consistent naming conventions** and tagging
7. **Separate environments** (dev, staging, prod) into different state files
8. **Never commit secrets** to version control - use variables or secret management tools

## Conclusion

Terraform strikes an excellent balance between simplicity and power. Its declarative approach, multi-cloud support, and mature ecosystem make it the de facto standard for infrastructure as code. While it has a learning curve, the investment pays off quickly in terms of reproducibility, version control, and team collaboration.

I personally prefer Terraform over proprietary IaC like CloudFormation or ARM templates since it's multiplatform and very widely known. Also, Terraform wins in maturity (also against Pulumi & co IMO) and the provider ecosystem is amazing.