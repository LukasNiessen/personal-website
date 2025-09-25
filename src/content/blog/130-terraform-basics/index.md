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

# Terraform Basics: Infrastructure as Code Done Right

Terraform is HashiCorp's Infrastructure as Code (IaC) tool that lets you define and provision infrastructure using declarative configuration files. Instead of clicking through AWS consoles or running shell scripts, you describe your desired infrastructure state, and Terraform makes it happen.

## Core Concepts

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

## Practical Example: VPC Setup

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

## For Loops and Dynamic Blocks

Terraform provides several ways to iterate and create multiple similar resources.

### Count

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

### for_each

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

### Dynamic Blocks

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

## Modules

Modules are reusable Terraform configurations. Think of them as functions - they take inputs (variables) and produce outputs. This is arguably the most important concept for scaling Terraform usage across teams and projects.

**Why modules matter:** Instead of copying and pasting the same VPC configuration across 10 projects, you create a VPC module once and reuse it everywhere. When you need to add a security group rule to all VPCs, you update the module once instead of 10 separate configurations.

### Creating a Module

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

### Using the Module

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

## Essential Commands

### terraform init
Initializes a Terraform working directory. Downloads providers and modules.

```bash
terraform init
```

### terraform plan
Shows what Terraform will do without actually doing it. Always run this before apply.

```bash
terraform plan
terraform plan -out=tfplan  # Save plan to file
```

### terraform apply
Creates, updates, or deletes infrastructure to match your configuration.

```bash
terraform apply
terraform apply tfplan      # Apply saved plan
terraform apply -auto-approve  # Skip confirmation
```

### terraform destroy
Destroys all resources managed by the configuration.

```bash
terraform destroy
terraform destroy -target=aws_instance.web  # Destroy specific resource
```

### terraform fmt
Formats Terraform files to a canonical style.

```bash
terraform fmt
terraform fmt -recursive  # Format all files in subdirectories
```

### terraform validate
Validates the configuration syntax.

```bash
terraform validate
```

## State Management

### Terraform State File

Terraform stores information about your infrastructure in a state file (`.tfstate`). This file maps your configuration to the real world and tracks resource metadata.

**Important:** Never edit the state file manually. Use Terraform commands instead.

### Remote State

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

### State Lock

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