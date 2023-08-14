import os

def create_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def create_directory(directory_path):
    os.makedirs(directory_path, exist_ok=True)

def create_terraform_files():
    # Create top-level files
    create_file('deploy-envs.tf', '''
# Define the environments to deploy
variable "environments" {
  type    = list(string)
  default = ["dev", "prod", "qa", "staging"]
}
''')

    create_file('local_run_sample.sh', '''
#!/bin/bash

# Sample shell script for local run
echo "Running Terraform locally..."
terraform init
terraform plan
terraform apply
''')

    create_file('main.tf', '''
# Main Terraform configuration file
provider "aws" {
  region = var.aws_region
}

module "cognito_user_pool" {
  source  = "lgallard/cognito-user-pool/aws"
  

  name                       = "id-domain-user-pool"
  admin_create_user          = true
  admin_create_user_password = true
  admin_create_user_profile  = true
  domain                     = "auth.id.music"
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes       = ["openid", "email"]
}

module "cognito_identity_pool" {
  source  = "corpit-consulting-public/cognito-identity-pool/aws"
  

  identity_pool_name = "id-domain-identity-pool"
  cognito_user_pool_id = module.cognito_user_pool.user_pool_id
}

module "keycloak" {
  source  = "mrparkers/keycloak"
  

  keycloak_url = "auth.id.music"
  realms       = var.environments
}

module "load_balancer" {
  source  = "terraform-aws-modules/alb/aws"
  

  name            = "id-domain-load-balancer"
  subnets         = var.load_balancer_subnets
  security_groups = var.load_balancer_security_groups
  region          = "eu-west-1"
  ssl_certificate_arn = var.ssl_certificate_arn
}

resource "aws_lb_listener" "front_end" {
  load_balancer_arn = module.load_balancer.this.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.ssl_certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.keycloak.arn
  }
}

resource "aws_lb_target_group" "keycloak" {
  name     = "keycloak"
  port     = 8443
  protocol = "HTTPS"
  vpc_id   = var.vpc_id
}
''')

    create_file('variables.tf', '''
# Define variables used in the Terraform configuration
variable "aws_region" {
  description = "AWS region for the infrastructure"
  type        = string
  default     = "eu-west-1"
}

variable "environments" {
  description = "List of environments"
  type        = list(string)
  default     = ["dev", "prod", "qa", "staging"]
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
''')

    # Create environments directory
    create_directory('environments')

    for environment in ['dev', 'prod', 'qa', 'staging']:
        create_directory(f'environments/{environment}')
        create_file(f'environments/{environment}/{environment}.tfvars', f'''
# Variables specific to the {environment} environment
aws_region = "eu-west-1"
''')
        create_file(f'environments/{environment}/main.tf', f'''
# Terraform configuration for the {environment} environment
module "cognito_user_pool" {{
  source  = "../../../modules/cognito-user-pool/aws"
  

  name                       = "id-domain-user-pool-{environment}"
  admin_create_user          = true
  admin_create_user_password = true
  admin_create_user_profile  = true
domain                     = "auth.id.music"
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes       = ["openid", "email"]
}}

module "cognito_identity_pool" {{
  source  = "../../../modules/cognito-identity-pool/aws"    
  

  identity_pool_name = "id-domain-identity-pool-{environment}"
  cognito_user_pool_id = module.cognito_user_pool.user_pool_id
}}

module "keycloak" {{
  source  = "../../../modules/keycloak"
  

  keycloak_url = "auth.id.music"
  realms       = ["{environment}"]
}}

module "load_balancer" {{
  source  = "../../../modules/load-balancer/aws"
  

  name            = "id-domain-load-balancer-{environment}"
  subnets         = var.load_balancer_subnets
  security_groups = var.load_balancer_security_groups
  region          = "eu-west-1"
  ssl_certificate_arn = var.ssl_certificate_arn
}}
'''
                    )
        create_file(
            f'environments/{environment}/outputs.tf', f'''
        # Define outputs for the {environment} environment
        output "output" {{
          value = "This is the {environment} environment output"
        }}
        '''
            )
        create_file(
            f'environments/{environment}/variables.tf', f'''
        # Define variables specific to the {environment} environment
        variable "variable" {{
          type    = string
          default = "variable"
        }}
        '''
            )

    # Create infrastructure directory
    create_directory('infrastructure')

    # Create networking directory
    create_directory('infrastructure/networking')
    create_file(
        'infrastructure/networking/main.tf', '''
        # Terraform configuration for networking
        resource "aws_internet_gateway" "igw" {
          vpc_id = var.vpc_id
        }

        resource "aws_route_table" "rtb" {
          vpc_id = var.vpc_id
        }

        resource "aws_subnet" "subnet" {
          vpc_id     = var.vpc_id
          cidr_block = var.cidr_block
        }

        resource "aws_vpc" "vpc" {
          cidr_block = var.cidr_block
        }
        '''
        )
    create_file(
        'infrastructure/networking/variables.tf', '''
        # Define variables for networking
        variable "vpc_id" {
          type = string
        }

        variable "cidr_block" {
          type = string
        }
        '''
        )

    # Create modules directory
    create_directory('modules')

    # Create cognito-user-pool module files
    create_directory('modules/cognito-user-pool')
    create_file(
        'modules/cognito-user-pool/main.tf', '''
        # Terraform configuration for the Cognito User Pool module
        resource "aws_cognito_user_pool" "user_pool" {
          name = var.user_pool_name
        }
        '''
        )
    create_file(
        'modules/cognito-user-pool/variables.tf', '''
        # Define variables for the Cognito User Pool module
        variable "user_pool_name" {
          type    = string
          default = "id-domain-user-pool"
        }
        '''
        )

    # Create cognito-identity-pool module files
    create_directory('modules/cognito-identity-pool')
    create_file(
        'modules/cognito-identity-pool/main.tf', '''
        # Terraform configuration for the Cognito Identity Pool module
        resource "aws_cognito_identity_pool" "identity_pool" {
          identity_pool_name = var.identity_pool_name
          allow_unauthenticated_identities = true

          cognito_identity_providers {
            client_id = var.cognito_user_pool_client_id
            provider_name = var.cognito_user_pool_provider_name
          }
        }
        '''
        )
    create_file(
        'modules/cognito-identity-pool/variables.tf', '''
        # Define variables for the Cognito Identity Pool module
        variable "identity_pool_name" {
          type    = string
          default = "id-domain-identity-pool"
        }

        variable "cognito_user_pool_id" {
          type    = string
          default = ""
        }

        variable "cognito_user_pool_client_id" {
          type = string
        }

        variable "cognito_user_pool_provider_name" {
          type = string
        }
        '''
        )

    # Create keycloak module files
    # Create keycloak module files
    create_directory('modules/keycloak')
    create_file(
        'modules/keycloak/main.tf', '''
        # Terraform configuration for the Keycloak module
        resource "aws_instance" "keycloak" {
          ami           = var.ami
          instance_type = var.instance_type

          provisioner "remote-exec" {
            inline = [
              "sudo apt-get update",
              "sudo apt-get install -y docker.io",
              "sudo docker run -d --name ${var.keycloak_container_name} -p 8443:8443 -e KEYCLOAK_ADMIN=${var.keycloak_admin} -e KEYCLOAK_ADMIN_PASSWORD=${var.keycloak_admin_password} quay.io/keycloak/keycloak:latest"
            ]
          }
        }
        '''
    )
    create_file(
        'modules/keycloak/variables.tf', '''
        # Define variables for the Keycloak module
        variable "keycloak_url" {
          type    = string
          default = "auth.id.music"
        }

        variable "realms" {
          type    = list(string)
          default = []
        }

        variable "ami" {
          type = string
        }

        variable "instance_type" {
          type = string
        }

        variable "keycloak_container_name" {
          type = string
        }

        variable "keycloak_admin" {
          type = string
        }

        variable "keycloak_admin_password" {
          type = string
        }
        '''
    )
    for environment in ['dev', 'prod', 'qa', 'staging']:
        ...
        create_file(
            f'environments/{environment}/variables.tf', f'''
        # Define variables specific to the {environment} environment
        variable "aws_region" {{
          description = "AWS region for the infrastructure"
          type        = string
          default     = "eu-west-1"
        }}

        variable "load_balancer_subnets" {{
          description = "List of subnets for the load balancer"
          type        = list(string)
          default     = []
        }}

        variable "load_balancer_security_groups" {{
          description = "List of security groups for the load balancer"
          type        = list(string)
          default     = []
        }}

        variable "ssl_certificate_arn" {{
          description = "ARN of the SSL certificate to use for the load balancer"
          type        = string
          default     = ""
        }}

        variable "keycloak_container_name" {{
          type = string
          default = "keycloak-{environment}"
        }}

        variable "keycloak_admin" {{
          type = string
          default = "admin"
        }}

        variable "keycloak_admin_password" {{
          type = string
          default = "password"
        }}
        '''
        )

    # Create shared module directory
    create_directory('modules/shared')

    # Create shared db directory
    create_directory('modules/shared/db')
    create_directory('modules/shared/db/dynamodb')
    # Create shared db rds directory
    create_directory('modules/shared/db/rds')

    # Create rds module files
    create_file(
        'modules/shared/db/rds/main.tf', '''
    # Terraform configuration for RDS
    resource "aws_db_instance" "instance" {
      allocated_storage    = 20
      storage_type         = "gp2"
      engine               = "postgres"
      engine_version       = "12.4"
      instance_class       = "db.t2.micro"
      name                 = var.instance_name
      username             = "admin"
      password             = "password"
      parameter_group_name = "default.postgres12"
    }
    '''
        )
    create_file(
        'modules/shared/db/rds/variables.tf', '''
    # Define variables for RDS
    variable "instance_name" {
      type    = string
      default = "rds-instance"
    }
    '''
        )

    # Create shared util directory
    create_directory('modules/shared/util')

    # Create shared util s3 directory
    create_directory('modules/shared/util/s3')

    # Create s3 module files
    create_file(
        'modules/shared/util/s3/main.tf', '''
    # Terraform configuration for S3
    resource "aws_s3_bucket" "bucket" {
      bucket = var.bucket_name
      acl    = "private"

      tags = {
        Name        = var.bucket_name
        Environment = var.environment
      }
    }
    '''
        )
    create_file(
        'modules/shared/util/s3/variables.tf', '''
    # Define variables for S3
    variable "bucket_name" {
      type    = string
      default = "s3-bucket"
    }

    variable "environment" {
      type    = string
      default = "dev"
    }
    '''
        )

    # Create shared util sqs directory
    create_directory('modules/shared/util/sqs')

    # Create sqs module files
    create_file(
        'modules/shared/util/sqs/main.tf', '''
    # Terraform configuration for SQS
    resource "aws_sqs_queue" "queue" {
      name                      = var.queue_name
      delay_seconds             = 0
      message_retention_seconds = 86400
    }
    '''
        )
    create_file(
        'modules/shared/util/sqs/variables.tf', '''
    # Define variables for SQS
    variable "queue_name" {
      type    = string
      default = "sqs-queue"
    }
    '''
        )

    # Create shared util sns directory
    create_directory('modules/shared/util/sns')

    # Create sns module files
    create_file(
        'modules/shared/util/sns/main.tf', '''
    # Terraform configuration for SNS
    resource "aws_sns_topic" "topic" {
      name = var.topic_name
    }
    '''
        )
    create_file(
        'modules/shared/util/sns/variables.tf', '''
    # Define variables for SNS
    variable "topic_name" {
      type    = string
      default = "sns-topic"
    }
    '''
        )

# Run the function to create the files and folders
create_terraform_files()