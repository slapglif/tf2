# Environment Class
class Environment:
    def __init__(self, name, aws_region = 'eu-west-1'):
        self.name = name
        self.aws_region = aws_region

    def __str__(self):
        return f'Environment: {self.name}, AWS Region: {self.aws_region}'

# id-music Usage
prod_env = Environment('prod')
print(prod_env)

# Deployment Script (local_run_sample.sh)
deployment_script = """
#!/bin/bash
echo 'Starting deployment for environment: $1'
terraform init
terraform apply -var 'env=$1'
echo 'Deployment completed for environment: $1'
"""

# Writing the script to a file
with open('local_run_sample.sh', 'w') as file:
    file.write(deployment_script)

# Main Configuration (main.tf)
main_configuration = """
provider "aws" {
  region = var.aws_region
}

module "infrastructure" {
  source = "./modules/infrastructure"
}
"""

# Writing the main configuration to a file
with open('main.tf', 'w') as file:
    file.write(main_configuration)

# Variable Definitions (variables.tf)
variable_definitions = """
variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "eu-west-1"
}

variable "env" {
  description = "Environment (prod, staging, qa, dev)"
  type        = string
}
"""

# Writing the variable definitions to a file
with open('variables.tf', 'w') as file:
    file.write(variable_definitions)

# Infrastructure Modules (modules/infrastructure)
infrastructure_module = """
resource "aws_instance" "id-music" {
  ami           = var.ami
  instance_type = var.instance_type
}
"""

# Writing the infrastructure module to a file
with open('modules/infrastructure/main.tf', 'w') as file:
    file.write(infrastructure_module)

# Generate Script (generate.py)
from jinja2 import Environment, FileSystemLoader


def generate_files(env_name):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('main.tf.j2')
    output = template.render(env=env_name)
    with open(f'{env_name}/main.tf', 'w') as file:
        file.write(output)

# id-music Usage
generate_files('prod')

# Integrating deploy-envs.tf
deploy_envs = """
# Define the environments to deploy
variable \"environments\" {
  type    = list(string)
  default = [\"dev\", \"prod\", \"qa\", \"staging\"]
}
"""

# Writing the deploy environments to a file
with open('deploy-envs.tf', 'w') as file:
    file.write(deploy_envs)

# Integrating local_run_sample.sh from old folder
local_run_sample_script = """
#!/bin/bash

# Sample shell script for local run
echo \"Running Terraform locally...\"
terraform init
terraform plan
terraform apply
"""

# Writing the local run sample script to a file
with open('local_run_sample.sh', 'w') as file:
    file.write(local_run_sample_script)

# Integrating main.tf from old folder
main_old_configuration = """
# Main Terraform configuration file
provider \"aws\" {
  region = var.aws_region
}

module \"cognito_user_pool\" {
  source  = \"lgallard/cognito-user-pool/aws\"
  name                       = \"id-domain-user-pool\"
  admin_create_user          = true
  admin_create_user_password = true
  admin_create_user_profile  = true
  domain                     = \"auth.id.music\"
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes       = [\"openid\", \"email\"]
}

module \"cognito_identity_pool\" {
  source  = \"corpit-consulting-public/cognito-identity-pool/aws\"
  identity_pool_name = \"id-domain-identity-pool\"
  cognito_user_pool_id = module.cognito_user_pool.user_pool_id
}

module \"keycloak\" {
  source  = \"mrparkers/keycloak\"
  keycloak_url = \"auth.id.music\"
  realms       = var.environments
}

module \"load_balancer\" {
  source  = \"terraform-aws-modules/alb/aws\"
  name            = \"id-domain-load-balancer\"
  subnets         = var.load_balancer_subnets
  security_groups = var.load_balancer_security_groups
  region          = \"eu-west-1\"
  ssl_certificate_arn = var.ssl_certificate_arn
}

resource \"aws_lb_listener\" \"front_end\" {
  load_balancer_arn = module.load_balancer.this.arn
  port              = \"443\"
  protocol          = \"HTTPS\"
  ssl_policy        = \"ELBSecurityPolicy-2016-08\"
  certificate_arn   = var.ssl_certificate_arn

  default_action {
    type             = \"forward\"
    target_group_arn = aws_lb_target_group.keycloak.arn
  }
}
"""

# Writing the main old configuration to a file
with open('main_old.tf', 'w') as file:
    file.write(main_old_configuration)

# Integrating variables.tf from old folder
variables_old_configuration = """
# Define variables used in the Terraform configuration
variable \"aws_region\" {
  description = \"AWS region for the infrastructure\"
  type        = string
  default     = \"eu-west-1\"
}

variable \"environments\" {
  description = \"List of environments\"
  type        = list(string)
  default     = [\"dev\", \"prod\", \"qa\", \"staging\"]
}

variable \"load_balancer_subnets\" {
  description = \"List of subnets for the load balancer\"
  type        = list(string)
  default     = []
}

variable \"load_balancer_security_groups\" {
  description = \"List of security groups for the load balancer\"
  type        = list(string)
  default     = []
}

variable \"ssl_certificate_arn\" {
  description = \"ARN of the SSL certificate to use for the load balancer\"
  type        = string
  default     = \"\"\"
}

variable \"vpc_id\" {
  description = \"VPC ID for the load balancer and target group\"
  type        = string
  default     = \"\"\"
}
"""

# Writing the variables old configuration to a file
with open('variables_old.tf', 'w') as file:
    file.write(variables_old_configuration)

# Integrating deploy-envs.tf
deploy_envs = """
# Define the environments to deploy
variable \"environments\" {
  type    = list(string)
  default = [\"dev\", \"prod\", \"qa\", \"staging\"]
}
"""

# Writing the deploy environments configuration to a file
with open('deploy-envs.tf', 'w') as file:
    file.write(deploy_envs)

# Integrating local_run_sample.sh
local_run_sample = """
#!/bin/bash

# Sample shell script for local run
echo \"Running Terraform locally...\"
terraform init
terraform plan
terraform apply
"""

# Writing the local run sample script to a file
with open('local_run_sample.sh', 'w') as file:
    file.write(local_run_sample)

# Integrating main.tf from old folder
main_old = """
# Main Terraform configuration file
provider \"aws\" {
  region = var.aws_region
}

module \"cognito_user_pool\" {
  source  = \"lgallard/cognito-user-pool/aws\"
  name                       = \"id-domain-user-pool\"
  admin_create_user          = true
  admin_create_user_password = true
  admin_create_user_profile  = true
  domain                     = \"auth.id.music\"
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes       = [\"openid\", \"email\"]
}

module \"cognito_identity_pool\" {
  source  = \"corpit-consulting-public/cognito-identity-pool/aws\"
  identity_pool_name = \"id-domain-identity-pool\"
  cognito_user_pool_id = module.cognito_user_pool.user_pool_id
}

module \"keycloak\" {
  source  = \"mrparkers/keycloak\"
  keycloak_url = \"auth.id.music\"
  realms       = [\"prod\"]
}

module \"load_balancer\" {
  source  = \"corpit-consulting-public/load-balancer/aws\"
  name    = \"load-balancer\"
  subnets = var.load_balancer_subnets
  security_groups = var.load_balancer_security_groups
}
"""

# Writing the main configuration from old folder to a file
with open('main_old.tf', 'w') as file:
    file.write(main_old)

# Integrating variables.tf from old folder
variables_old = """
# Define variables used in the Terraform configuration
variable \"aws_region\" {
  description = \"AWS region for the infrastructure\"
  type        = string
  default     = \"eu-west-1\"
}

variable \"environments\" {
  description = \"List of environments\"
  type        = list(string)
  default     = [\"dev\", \"prod\", \"qa\", \"staging\"]
}

variable \"load_balancer_subnets\" {
  description = \"List of subnets for the load balancer\"
  type        = list(string)
  default     = []
}

variable \"load_balancer_security_groups\" {
  description = \"List of security groups for the load balancer\"
  type        = list(string)
  default     = []
}

variable \"ssl_certificate_arn\" {
  description = \"ARN of the SSL certificate to use for the load balancer\"
  type        = string
  default     = \"\"\"
}

variable \"vpc_id\" {
  description = \"VPC ID for the infrastructure\"
  type        = string
  default     = \"\"\"
}
"""

# Writing the variables configuration from old folder to a file
with open('variables_old.tf', 'w') as file:
    file.write(variables_old)

# dev.tfvars
dev_tfvars = """
# Variables specific to the dev environment
aws_region = \"eu-west-1\"
"""

# Writing the dev environment variables to a file
with open('dev/dev.tfvars', 'w') as file:
    file.write(dev_tfvars)

# main.tf for dev environment
dev_main_tf = """
# Terraform configuration for the dev environment
module \"cognito_user_pool\" {
  source  = \"../../../modules/cognito-user-pool/aws\"
  name                       = \"id-domain-user-pool-dev\"
  admin_create_user          = true
  admin_create_user_password = true
  admin_create_user_profile  = true
  domain                     = \"auth.id.music\"
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes       = [\"openid\", \"email\"]
}

module \"cognito_identity_pool\" {
  source  = \"../../../modules/cognito-identity-pool/aws\"
  identity_pool_name = \"id-domain-identity-pool-dev\"
  cognito_user_pool_id = module.cognito_user_pool.user_pool_id
}

module \"keycloak\" {
  source  = \"../../../modules/keycloak\"
  keycloak_url = \"auth.id.music\"
  realms       = [\"dev\"]
}

module \"load_balancer\" {
  source  = \"../../../modules/load-balancer/aws\"
  name    = \"load-balancer-dev\"
  subnets = var.load_balancer_subnets
  security_groups = var.load_balancer_security_groups
}
"""

# Writing the main configuration for dev environment to a file
with open('dev/main.tf', 'w') as file:
    file.write(dev_main_tf)

# outputs.tf for dev environment
dev_outputs_tf = """
# Define outputs for the dev environment
output \"output\" {
  value = \"This is the dev environment output\"
}
"""

# Writing the outputs configuration for dev environment to a file
with open('dev/outputs.tf', 'w') as file:
    file.write(dev_outputs_tf)

# Adding environments variable definition to variables.tf
environments_variable_definition = """
variable \"environments\" {
  type    = list(string)
  default = [\"dev\", \"prod\", \"qa\", \"staging\"]
}
"""

# Appending the environments variable definition to the existing variables.tf file
with open('variables.tf', 'a') as file:
    file.write(environments_variable_definition)

# variables.tf for dev environment
dev_variables_tf = """
# Define variables specific to the dev environment
variable \"aws_region\" {
  description = \"AWS region for the infrastructure\"
  type        = string
  default     = \"eu-west-1\"
}

variable \"load_balancer_subnets\" {
  description = \"List of subnets for the load balancer\"
  type        = list(string)
  default     = []
}

variable \"load_balancer_security_groups\" {
  description = \"List of security groups for the load balancer\"
  type        = list(string)
  default     = []
}

variable \"ssl_certificate_arn\" {
  description = \"ARN of the SSL certificate to use for the load balancer\"
  type        = string
  default     = \"\"\"
}

variable \"keycloak_container_name\" {
  type = string
  default = \"keycloak-dev\"
}

variable \"keycloak_admin\" {
  type = string
  default = \"admin\"
}
"""

# Writing the variables configuration for dev environment to a file
with open('dev/variables.tf', 'w') as file:
    file.write(dev_variables_tf)

# Updated Deployment Script (local_run.sh)
updated_deployment_script = """
#!/bin/bash
echo 'Running Terraform locally for environment: $1...'
cd $1
terraform init
terraform plan -var 'env=$1'
terraform apply -var 'env=$1'
echo 'Deployment completed for environment: $1'
"""

# Writing the updated deployment script to a file
with open('local_run.sh', 'w') as file:
    file.write(updated_deployment_script)

# Main Terraform Configuration (main.tf)
main_configuration = """
# Main Terraform configuration file
provider \"aws\" {
  region = var.aws_region
}

module \"cognito_user_pool\" {
  source  = \"lgallard/cognito-user-pool/aws\"
  name                       = \"id-domain-user-pool\"
  admin_create_user          = true
  admin_create_user_password = true
  admin_create_user_profile  = true
  domain                     = \"auth.id.music\"
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes       = [\"openid\", \"email\"]
}

module \"cognito_identity_pool\" {
  source  = \"corpit-consulting-public/cognito-identity-pool/aws\"
  identity_pool_name = \"id-domain-identity-pool\"
  cognito_user_pool_id = module.cognito_user_pool.user_pool_id
}

module \"keycloak\" {
  source  = \"mrparkers/keycloak\"
  keycloak_url = \"auth.id.music\"
  realms       = var.environments
}

module \"load_balancer\" {
  source  = \"terraform-aws-modules/alb/aws\"
  name            = \"id-domain-load-balancer\"
  subnets         = var.load_balancer_subnets
  security_groups = var.load_balancer_security_groups
  region          = \"eu-west-1\"
  ssl_certificate_arn = var.ssl_certificate_arn
}

resource \"aws_lb_listener\" \"front_end\" {
  load_balancer_arn = module.load_balancer.this.arn
  port              = \"443\"
  protocol          = \"HTTPS\"
  ssl_policy        = \"ELBSecurityPolicy-2016-08\"
  certificate_arn   = var.ssl_certificate_arn

  default_action {
    type             = \"forward\"
    target_group_arn = aws_lb_target_group.keycloak.arn
  }
}

resource \"aws_lb_target_group\" \"keycloak\" {
  name     = \"keycloak\"
  port     = 8443
  protocol = \"HTTPS\"
  vpc_id   = var.vpc_id
}
"""

# Writing the main configuration to a file
with open('main.tf', 'w') as file:
    file.write(main_configuration)

# Additional Variable Definitions for variables.tf
additional_variable_definitions = """
variable \"aws_region\" {
  description = \"AWS region for the infrastructure\"
  type        = string
  default     = \"eu-west-1\"
}

variable \"load_balancer_subnets\" {
  description = \"List of subnets for the load balancer\"
  type        = list(string)
  default     = []
}

variable \"load_balancer_security_groups\" {
  description = \"List of security groups for the load balancer\"
  type        = list(string)
  default     = []
}

variable \"ssl_certificate_arn\" {
  description = \"ARN of the SSL certificate to use for the load balancer\"
  type        = string
  default     = \"\""
}

variable \"vpc_id\" {
  description = \"VPC ID for the load balancer and target group\"
  type        = string
  default     = \"\""
}
"""

# Appending the additional variable definitions to the existing variables.tf file
with open('variables.tf', 'a') as file:
    file.write(additional_variable_definitions)

# AWS Amplify Configuration (amplify.tf)
amplify_configuration = """
resource "aws_amplify_app" "id-music" {
  name = "id-music-app"
  repository = var.repository_url
}
"""

# Writing the AWS Amplify configuration to a file
with open('amplify.tf', 'w') as file:
    file.write(amplify_configuration)

# Next.js with SSR Configuration (nextjs.tf)
nextjs_configuration = """
# Assuming Next.js is deployed as a containerized application on AWS ECS
resource "aws_ecs_service" "nextjs" {
  name            = "nextjs-service"
  cluster         = aws_ecs_cluster.id-music.id
  task_definition = aws_ecs_task_definition.nextjs.arn
  desired_count   = 2
  launch_type     = "FARGATE"
}
"""

# Writing the Next.js configuration to a file
with open('nextjs.tf', 'w') as file:
    file.write(nextjs_configuration)

# Keycloak for OIDC SSO Identity Provider Configuration (keycloak.tf)
keycloak_configuration = """
resource "aws_rds_instance" "keycloak_db" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "postgres"
  engine_version       = "12.4"
  instance_class       = "db.t2.micro"
  name                 = "keycloakdb"
  username             = "keycloak"
  password             = var.keycloak_db_password
  parameter_group_name = "default.postgres12"
  skip_final_snapshot  = true
}
"""

# Writing the Keycloak configuration to a file
with open('keycloak.tf', 'w') as file:
    file.write(keycloak_configuration)

# Cognito using Identity Pool for Keycloak OIDC SSO Configuration (cognito.tf)
cognito_configuration = """
resource "aws_cognito_identity_pool" "id-music" {
  identity_pool_name               = "id-music-identity-pool"
  allow_unauthenticated_identities = false

  cognito_identity_providers {
    client_id             = var.keycloak_client_id
    provider_name         = var.keycloak_provider_name
    server_side_token_check = false
  }
}
"""

# Writing the Cognito configuration to a file
with open('cognito.tf', 'w') as file:
    file.write(cognito_configuration)

# AWS Load Balancer (ALB/ELB) with OpenAPI/Swagger Support Configuration (load_balancer.tf)
load_balancer_configuration = """
resource "aws_lb" "id-music" {
  name               = "id-music-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.id-music.id]
  subnets            = aws_subnet.id-music.*.id
}
"""

# Writing the Load Balancer configuration to a file
with open('load_balancer.tf', 'w') as file:
    file.write(load_balancer_configuration)

# DynamoDB for Amplify Lambdas Backend Configuration (dynamodb.tf)
dynamodb_configuration = """
resource "aws_dynamodb_table" "id-music" {
  name           = "id-music-table"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"
  attribute {
    name = "id"
    type = "S"
  }
}
"""

# Writing the DynamoDB configuration to a file
with open('dynamodb.tf', 'w') as file:
    file.write(dynamodb_configuration)

# Main Terraform File (main.tf)
main_terraform_file = """
provider "aws" {
  region = var.aws_region
}

module "amplify" {
  source = "./amplify"
}

module "nextjs" {
  source = "./nextjs"
}

module "keycloak" {
  source = "./keycloak"
}

module "cognito" {
  source = "./cognito"
}

module "load_balancer" {
  source = "./load_balancer"
}

module "dynamodb" {
  source = "./dynamodb"
}
"""

# Writing the main Terraform file to a file
with open('main.tf', 'w') as file:
    file.write(main_terraform_file)

# Importing required libraries
from jinja2 import Environment, FileSystemLoader
import os


# Function to generate Terraform files for a specific environment
def generate_terraform_files(environment, variables):
    """
    this function generates Terraform files for a specific environment
    :param environment:
    :param variables:
    """
    # Setting up the Jinja2 environment
    env = Environment(loader=FileSystemLoader('./templates'))

    # Creating the output directory for the environment
    output_dir = f'./output/{environment}'
    os.makedirs(output_dir, exist_ok=True)

    # Iterating through the Terraform templates
    for template_name in env.list_templates():
        # Loading the template
        template = env.get_template(template_name)

        # Rendering the template with the provided variables
        rendered_template = template.render(variables)

        # Writing the rendered template to the output directory
        with open(f'{output_dir}/{template_name}', 'w') as file:
            file.write(rendered_template)

    print(f'{environment.capitalize()} environment files generated successfully.')

# id-music usage
generate_terraform_files('prod', { 'aws_region': 'eu-west-1' })

# Creating Terraform Templates Directory
#
# Writing the main Terraform template
# with open('./templates/main.tf.j2', 'w') as file:
#     file.write(main_terraform_file)
#
# # Writing the individual component templates
# component_templates = {
#     'amplify.tf.j2': amplify_configuration,
#     'nextjs.tf.j2': nextjs_configuration,
#     'keycloak.tf.j2': keycloak_configuration,
#     'cognito.tf.j2': cognito_configuration,
#     'load_balancer.tf.j2': load_balancer_configuration,
#     'dynamodb.tf.j2': dynamodb_configuration
# }
#
# for template_name, content in component_templates.items():
#     with open(f'./templates/{template_name}', 'w') as file:
#         file.write(content)

print('Terraform templates created successfully.')
# AWS Amplify Configuration
amplify_configuration = """
resource \"aws_amplify_app\" \"id-music\" {
  name = \"id-music-app\"
}
"""

# Next.js with SSR Configuration
nextjs_configuration = """
resource \"aws_ecs_service\" \"id-music\" {
  name            = \"id-music\"
  cluster         = aws_ecs_cluster.id-music.id
  task_definition = aws_ecs_task_definition.id-music.arn
  desired_count   = 2
}
"""

# Keycloak for OIDC SSO Identity Provider Configuration
keycloak_configuration = """
resource \"aws_rds_instance\" \"keycloak_db\" {
  allocated_storage    = 20
  storage_type         = \"gp2\"
  engine               = \"postgres\"
  engine_version       = \"12.4\"
  instance_class       = \"db.t2.micro\"
  name                 = \"keycloakdb\"
  username             = \"keycloak\"
  password             = var.keycloak_db_password
  parameter_group_name = \"default.postgres12\"
  skip_final_snapshot  = true
}
"""

# Cognito using Identity Pool for Keycloak OIDC SSO Configuration
cognito_configuration = """
resource \"aws_cognito_identity_pool\" \"id-music\" {
  identity_pool_name               = \"id-music-identity-pool\"
  allow_unauthenticated_identities = false
}
"""

# AWS Load Balancer (ALB/ELB) with OpenAPI/Swagger Support Configuration
load_balancer_configuration = """
resource \"aws_lb\" \"id-music\" {
  name               = \"id-music-lb\"
  internal           = false
  load_balancer_type = \"application\"
  security_groups    = [aws_security_group.id-music.id]
  subnets            = aws_subnet.id-music.*.id
}
"""

# DynamoDB for Amplify Lambdas Backend Configuration
dynamodb_configuration = """
resource \"aws_dynamodb_table\" \"id-music\" {
  name           = \"id-music-table\"
  billing_mode   = \"PAY_PER_REQUEST\"
  hash_key       = \"id\"
  attribute {
    name = \"id\"
    type = \"S\"
  }
}
"""

# Main Terraform File
main_terraform_file = """
provider \"aws\" {
  region = var.aws_region
}
module \"amplify\" {
  source = \"./amplify\"
}
module \"nextjs\" {
  source = \"./nextjs\"
}
module \"keycloak\" {
  source = \"./keycloak\"
}
module \"cognito\" {
  source = \"./cognito\"
}
module \"load_balancer\" {
  source = \"./load_balancer\"
}
module \"dynamodb\" {
  source = \"./dynamodb\"
}
"""

0# Creating Terraform Templates Directory
os.makedirs('./templates', exist_ok=True)

# Writing the main Terraform template
with open('./templates/main.tf.j2', 'w') as file:
    file.write(main_terraform_file)

# Writing the individual component templates
component_templates = {
    'amplify.tf.j2': amplify_configuration,
    'nextjs.tf.j2': nextjs_configuration,
    'keycloak.tf.j2': keycloak_configuration,
    'cognito.tf.j2': cognito_configuration,
    'load_balancer.tf.j2': load_balancer_configuration,
    'dynamodb.tf.j2': dynamodb_configuration
}

for template_name, content in component_templates.items():
    with open(f'./templates/{template_name}', 'w') as file:
        file.write(content)

print('Terraform templates created successfully.')

# Jinja2 Environment Setup
file_loader = FileSystemLoader('./templates')
env = Environment(loader=file_loader)

# Environments Configuration
environments = ['prod', 'staging', 'qa', 'dev']
aws_region = 'eu-west-1'

# Generating Terraform Files for Each Environment
for environment in environments:
    os.makedirs(f'./{environment}', exist_ok=True)

    # Rendering Main Terraform File
    main_template = env.get_template('main.tf.j2')
    main_output = main_template.render(aws_region=aws_region)
    with open(f'./{environment}/main.tf', 'w') as file:
        file.write(main_output)

    # Rendering Component Templates
    for template_name in component_templates:
        template = env.get_template(template_name)
        output = template.render()
        with open(f'./{environment}/{template_name[:-3]}', 'w') as file:
            file.write(output)

    print(f'{environment.capitalize()} environment Terraform files generated successfully.')
