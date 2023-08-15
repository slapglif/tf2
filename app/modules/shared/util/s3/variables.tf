
    # Define variables for S3
    variable "bucket_name" {
      type    = string
      default = "s3-bucket"
    }

    variable "environment" {
      type    = string
      default = "dev"
    }
    