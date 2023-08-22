variable "region" {
  description = "AWS region"
  default     = "eu-west-1"
}

variable "availability_zones" {
  description = "List of Availability Zones"
  type        = list(string)
  default     = ["eu-west-1a", "eu-west-1b"]
}

variable "vpc_cidr_block" {
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "subnet_cidr_blocks" {
  description = "CIDR blocks for the subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "db_engine_version" {
  description = "PostgreSQL engine version"
  default     = "14.6.1"
}

variable "domain_name" {
  description = "Domain name for the ACM certificate and Route 53 record"
  default     = "auth.id.music"
}

variable "wildcard_domain_name" {
  description = "Wildcard domain name for the ACM certificate"
  default     = "*.id.music"
}
