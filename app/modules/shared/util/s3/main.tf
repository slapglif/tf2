
    # Terraform configuration for S3
    resource "aws_s3_bucket" "bucket" {
      bucket = var.bucket_name
      acl    = "private"

      tags = {
        Name        = var.bucket_name
        Environment = var.environment
      }
    }
    