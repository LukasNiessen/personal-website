---
title: 'Infrastructure as Code is a MUST have'
summary: 'Very simple recap of what Infrastructure as Code is and why it matters.'
date: 'Jan 01 2025'
draft: false
repoUrl: 'https://github.com/LukasNiessen/iac-explained'
xLink: 'https://x.com/iamlukasniessen/status/'
linkedInLink: 'https://www.linkedin.com/pulse//'
tags:
  - IaC
  - Infrastructure
  - Terraform
---

# Infrastructure as Code

Infrastructure as Code (IaC) certainly has become a buzzword so this serves as a quick guide or reminder of why IaC is so important.

## Super short: What is IaC?

IaC is what the name says, defining your infrastructure as code. Meaning, all of these things are defined simply as code:

- How many servers do we have?
- Where are the servers?
- Do we use load balancing and if so, what kind?
- Do we expose IP addresses or do we use a gateway?

That code could be a JSON file for example. That's it.

## Why IaC is a Must have

First of all, the ability to just code your infrastructure is a big deal. A very big deal. Before the cloud age of AWS, Azure, GCP and the like, companies had their own servers. When you needed more CPU, more servers, more RAM or things like that, you would need to request that from the operations department. Then hardware would be ordered and installed. The entire thing could take weeks or even months.

But now, we just click a button in the AWS console and have 10 new servers in Asia and 7 more in Europe. Of whatever size etc we want. This changes the game.

However, instead of clicking things manually in the console, it's much better to have the configurations stored somewhere, ideally in a moduralized and reusable way. This is what IaC brings us. When we put these IaC files under source control, we get even more benefits like simple rollbacks and knowing how the servers looked 6 months ago.

So the main benefits are:

- Reusable
- Rollbacks are easy
- We know how the infrastructure looked at any given time
- Reproducing is easy

But the benefits go further. If you use Terraform for example, a very popular tool for doing IaC, you also get faster deployment since it parallelizes what can be parallelized, and it checks for errors before applying any change.

## Negatives?

There aren't really any. Of course there is a learning curve and arguably some overhead. So if your team is not familiar with IaC and Terraform at all, it will take some time for them to learn it. I would argue that even for small projects it's good to always use IaC. The benefits are just too big. Consider the following phenomena of a _snowflake server_.

## Snowflake Server

Snowflake servers are servers that are difficult to reproduce. For example, it was set up and configured once by someone, but getting it the exact same way again... nobody really knows if they can do it. So everyone is scared to touch the server. What do you do then we you need more resources? Or make other infrastructure changes? You will have to touch it and that's a dangerous game. (Read more [here](https://martinfowler.com/bliki/SnowflakeServer.html))

Not with IaC though. With IaC you know exactly how the server is set up, also if someone else did that 3 years ago. You also know how it was set up last week or last christmas. When you make a change, it's as transparent as it gets. And when something breaks, just roll it back. So no more snowflake servers.

## Terraform Examples

Here are some simple examples of how to define infrastructure using Terraform for different cloud providers:

### AWS Example

```hcl
# Configure the AWS Provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

# Create a VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "main-vpc"
  }
}

# Create an EC2 instance
resource "aws_instance" "web" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t2.micro"

  tags = {
    Name = "web-server"
  }
}
```

### Azure Example

```hcl
# Configure the Azure Provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Create a resource group
resource "azurerm_resource_group" "main" {
  name     = "rg-terraform-example"
  location = "West Europe"
}

# Create a virtual machine
resource "azurerm_linux_virtual_machine" "main" {
  name                = "vm-terraform-example"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = "Standard_B1s"
  admin_username      = "adminuser"

  network_interface_ids = [
    azurerm_network_interface.main.id,
  ]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }
}
```

### Google Cloud Platform (GCP) Example

```hcl
# Configure the Google Cloud Provider
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = "my-project-id"
  region  = "us-central1"
  zone    = "us-central1-c"
}

# Create a Compute Engine instance
resource "google_compute_instance" "vm_instance" {
  name         = "terraform-instance"
  machine_type = "e2-micro"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"
    access_config {
      // Ephemeral public IP
    }
  }

  tags = ["web", "dev"]
}

# Create a Cloud Storage bucket
resource "google_storage_bucket" "static_site" {
  name     = "my-terraform-bucket-example"
  location = "US"
}
```

### Alibaba Cloud Example

```hcl
# Configure the Alibaba Cloud Provider
terraform {
  required_providers {
    alicloud = {
      source  = "aliyun/alicloud"
      version = "~> 1.0"
    }
  }
}

provider "alicloud" {
  region = "cn-hangzhou"
}

# Create a VPC
resource "alicloud_vpc" "vpc" {
  vpc_name   = "tf_test_vpc"
  cidr_block = "172.16.0.0/16"
}

# Create an ECS instance
resource "alicloud_instance" "instance" {
  availability_zone = "cn-hangzhou-b"
  security_groups   = [alicloud_security_group.group.id]

  instance_type              = "ecs.n4.large"
  system_disk_category       = "cloud_efficiency"
  system_disk_name           = "test_system_disk"
  system_disk_description    = "test_system_disk_description"
  image_id                   = "ubuntu_18_04_64_20G_alibase_20190624.vhd"
  instance_name              = "test_instance"
  vswitch_id                 = alicloud_vswitch.vsw.id
  internet_max_bandwidth_out = 10
}

# Create a security group
resource "alicloud_security_group" "group" {
  name   = "terraform-test-group"
  vpc_id = alicloud_vpc.vpc.id
}
```

## Bottom Line

These examples show how simple it is to define infrastructure across different cloud providers using Terraform. The syntax is clean, readable, and version-controllable. Once you have these files, you can deploy, modify, or destroy your infrastructure with simple commands like `terraform apply` or `terraform destroy`.

Remember: Infrastructure as Code isn't just a nice-to-have anymore—it's essential for modern, scalable, and maintainable systems.
