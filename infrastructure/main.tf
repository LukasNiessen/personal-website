terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "website_bucket" {
  bucket        = "www.lukasniessen.com"
  force_destroy = false
  tags          = {}
}

resource "aws_s3_bucket_policy" "website_bucket_policy" {
  bucket = aws_s3_bucket.website_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.website_bucket.arn}/*"
      }
    ]
  })
}

resource "aws_s3_bucket_server_side_encryption_configuration" "website_bucket_encryption" {
  bucket = aws_s3_bucket.website_bucket.id

  rule {
    bucket_key_enabled = true

    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "website_bucket_versioning" {
  bucket = aws_s3_bucket.website_bucket.id

  versioning_configuration {
    status = "Disabled"
  }
}

resource "aws_s3_bucket_website_configuration" "website_bucket_website" {
  bucket = aws_s3_bucket.website_bucket.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "404.html"
  }
}

resource "aws_acm_certificate" "website_cert" {
  domain_name               = "lukasniessen.com"
  subject_alternative_names = ["www.lukasniessen.com"]
  validation_method         = "DNS"
  tags                      = {}

  options {
    certificate_transparency_logging_preference = "ENABLED"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_cloudfront_distribution" "website_cdn" {
  aliases = [
    "lukasniessen.com",
    "www.lukasniessen.com",
  ]
  enabled         = true
  is_ipv6_enabled = true
  price_class     = "PriceClass_All"
  tags            = {}

  origin {
    domain_name = aws_s3_bucket_website_configuration.website_bucket_website.website_endpoint
    origin_id   = aws_s3_bucket_website_configuration.website_bucket_website.website_endpoint

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols = [
        "SSLv3",
        "TLSv1",
        "TLSv1.1",
        "TLSv1.2",
      ]
    }
  }

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = aws_s3_bucket_website_configuration.website_bucket_website.website_endpoint
    viewer_protocol_policy = "redirect-to-https"
    compress               = true
    cache_policy_id        = "658327ea-f89d-4fab-a63d-7e88639e58f6"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.website_cert.arn
    minimum_protocol_version = "TLSv1.2_2021"
    ssl_support_method       = "sni-only"
  }
}
