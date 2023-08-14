# Define variables specific to the prod environment
variable "aws_region" {
  description = "AWS region for the infrastructure"
  type        = string
  default     = "eu-west-1"
}

variable "load_balancer_subnets" {
  description = "List of subnets for the load balancer"
  type        = list(string)
  default     = []
}

variable "load_balancer_security_groups" {
  description = "List of security groups for the load balancer"
  type        = list(string)
  default     = []
}

variable "ssl_certificate_arn" {
  description = "ARN of the SSL certificate to use for the load balancer"
  type        = string
  default     = ""
}

variable "vpc_id" {
  description = "VPC ID for the load balancer and target group"
  type        = string
  default     = ""
}
