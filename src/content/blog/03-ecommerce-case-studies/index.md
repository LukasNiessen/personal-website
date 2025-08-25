---
title: "Personal case studies: E-commerce"
summary: "Personal case studies: E-commerce"
date: "April 05 2022"
draft: false
tags:
  - E-Commerce
---

# Personal case studies: E-commerce

This is a short collection of personal _"case studies"_ of projects that I was involved in which centered around e-commerce.

## SocialHubs UG

Note, I was founder and CEO of SocialHubs but it's not written from my PoV but from the company's view.

# Case Study 1

## Merchandise Multi-Shop with Shopify for SocialHubs UG

## About SocialHubs UG

SocialHubs UG, a startup founded in 2020 and based in Cologne, operates six specialized social networks targeting distinct communities, from anime fans to LGBT communities. The company prioritizes building digital communities with a focus on a truly *social* experience and data privacy. To enhance user loyalty and gain customer insights, SocialHubs UG introduced e-commerce shops, enabling users to purchase merchandise such as T-shirts, hoodies, stickers, and caps featuring the logos and symbols of their respective networks.

## The Challenge

SocialHubs UG faced several challenges during implementation:

- **Scalability**: Six (or more) parallel shops needed to be created, each appearing independent but manageable from a shared technical foundation.
- **Community Connection**: Each network has its own brand identity, which needed to be reflected in the look and feel of the shops.
- **Resource Efficiency**: As a young startup, the solution had to be implemented by a small team without external agencies.
- **Centralized Management**: Despite individual shops, the startup wanted to centrally manage orders, inventory, and payment processes.
- **Fast Time-to-Market**: The project was to be completed within a few months.

## Our Solution – In-House Development Without External Partners

The entire project was executed by an internal team of two developers. SocialHubs UG chose Shopify as the platform due to its high flexibility and ease of use.

### Implementation

#### Multi-Shop Structure
A separate Shopify store was set up for each of the six community platforms. While Shopify does not provide a single unified backend out of the box, all stores were built on a shared technical foundation.

#### Code Sharing & Deployment
To avoid duplicating theme code across six stores, the team implemented a Git-based workflow:

- A single private Git repository contained the “base” Shopify theme with shared Liquid templates, CSS/JS, and custom functionality.
- Brand-specific elements (colors, logos, typography) were abstracted into configuration files and Liquid variables rather than hard-coded.
- Store-specific overrides were kept in separate configuration folders (e.g., `config/anime.json`, `config/lgbt.json`) plus a small number of brand-specific assets.
- A lightweight build script bundled the base theme with the correct brand config and deployed it to the matching Shopify store via Shopify CLI/Theme Kit.

This allowed the two-person team to roll out updates to all stores centrally: one code change, six deployments.

#### Design & Branding
Each network’s unique look and feel was achieved through the configuration-driven theme plus Shopify’s built-in theme settings. The checkout flow remained standardized for consistency.

#### Product Management
Shopify itself was used for product data; a multi-store sync app handled stock level synchronization across shops. No separate PIM was needed at this stage given the relatively simple catalog.

#### Payment Processing
PayPal, Klarna, and credit card payments were enabled directly within Shopify’s payment settings, requiring minimal setup effort.

#### Community Features
Exclusive discount codes for logged-in network members were implemented via a lightweight custom app leveraging Shopify’s Discounts API.

#### Automated Logistics (Dropshipping)
Orders were automatically forwarded to fulfillment partners using Shopify’s webhook system. When an order was created, Shopify triggered an `orders/create` webhook to a custom endpoint. This middleware transformed the order data to the partner’s API format and sent it to their system. Tracking info was returned and updated back into Shopify automatically. This avoided manual intervention and allowed seamless dropshipping.

#### No ERP/OMS/PIM Overhead
Given the limited catalog and single fulfillment flow, no dedicated ERP, OMS, or PIM was introduced. Shopify served as the order and product hub; the webhook middleware plus sync app covered all operational needs. Accounting integration was handled via Shopify’s standard exports.

## Success Factors & Results

The implementation brought clear benefits for SocialHubs UG:

- **Strong Community Connection**: Members identify with their platforms and can proudly showcase this through merchandise.
- **Rapid Implementation**: All six shops were launched within 2 months.
- **Efficiency**: Centralized code and management allow resource-efficient handling of orders, products, and marketing campaigns.
- **International Scalability**: Shopify enables the addition of new languages and markets without significant technical barriers.

## Outlook

SocialHubs UG plans to expand the shops with print-on-demand products, allowing community members to order custom-designed items. Additionally, they plan to expand into more markets and provide more personalization.


# Case Study 2

This is not really a case study in the traditional sense as I was only involved in the presales process, it's more a _solution brief_.

# Optimizing MACH Architecture Performance for E-commerce Retailer

## The Challenge

A mid-market fashion retailer came to us as an inbound lead after struggling with their MACH e-commerce setup. They were running Shopify Plus with a microservices backend but experiencing significant performance issues - response times hitting 3+ seconds during peak traffic and timeout errors causing cart abandonment.

Their main pain points included chatty services requiring multiple API calls for simple operations, difficulty tracing errors across their distributed system, and failed distributed transactions due to poor service boundaries.

## Pre-Sales Process & My Role

### Sales Cycle

**Week 1: Initial Discovery**
- Inbound lead qualified by our BDR team
- I joined the Account Executive for technical discovery calls
- Reviewed their current architecture diagrams, architecture decision records, and identified bottlenecks
- Scoped the engagement around performance optimization and observability

**Week 2-3: Technical Deep Dive** 
- Conducted architecture review sessions with their engineering team
- Analyzed their service communication patterns - found 10 services involved in checkout flow
- Partnered with our Shopify specialist and built technical proposal focusing on service consolidation and async patterns

**Week 4: Workshop & Closing**
- Designed 1-day architecture workshop to demonstrate our approach
- Collaborated with AE on commercial terms while I handled technical objections
- SOW and closing was done by sales team

## The Solution

### Architecture Workshop
I facilitated a hands-on workshop covering:
- Service boundary partially redesigned using DDD and event storming among other techniques
- Implementing distributed tracing for better debugging  
- Shopify Plus API optimization strategies

### Key Technical Changes
Working with our Shopify specialist, we:
- **Consolidated services**: Reduced checkout flow from 10 to 5 services
- **Added observability**: Implemented distributed tracing across all services
- **Introduced async patterns**: Used event streaming for non-critical operations
- **Optimized Shopify integration**: Batched API calls and implemented caching using Redis

## Results (PoC)
- Heavy load response times improved from 3s to 1.2s
- Cart abandonment reduced by 12%
- Error debugging time cut from hours to minutes
- System uptime increased to 99.8%

## Key Insights

The engagement highlighted how many companies adopt MACH architectures without proper service design principles. Microservices is a hype topic to a degree. Success required combining deep microservices knowledge with platform-specific expertise - which is why our collaborative Solution Architecture approach proved essential.


# Case Study 3

## Expanding Beyond Marketplaces

## About Odoma
Odoma is a small retailer that initially sold exclusively on eBay and Amazon, with a simple WordPress homepage serving as their “digital business card.” While marketplaces drove most sales, Odoma wanted an additional sales channel they fully controlled — both to reduce dependency on platform fees and policies, and to build direct customer relationships.

## Challenge

- Heavy reliance on eBay/Amazon fees and rules
- No direct customer data or branding opportunities
- Needed an online store quickly without replacing their existing WordPress site

## Solution: WooCommerce on WordPress

WooCommerce was the natural fit because:
- Seamless WordPress Integration: Odoma’s site already ran on WordPress; WooCommerce adds full e-commerce functionality without rebuilding the site.
- Low Cost & Flexibility: Open-source and extensible with plugins; ideal for a small business on a budget.

## Outcome
Odoma launched their WooCommerce shop quickly and gained an owned sales channel alongside eBay/Amazon. This improved margins and gave them direct access to customer data for marketing and loyalty initiatives.