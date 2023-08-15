
        # Define variables specific to the dev environment
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

        variable "keycloak_container_name" {
          type = string
          default = "keycloak-dev"
        }

        variable "keycloak_admin" {
          type = string
          default = "admin"
        }

        variable "keycloak_admin_password" {
          type = string
          default = "password"
        }
        