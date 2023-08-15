
# Terraform configuration for the dev environment
variable "cognito_user_pool_id" {
  default = "id-domain-user-pool-dev"
}
module "cognito_user_pool" {
  source  = "../../../modules/cognito-user-pool/aws"
  
  user_pool_id               = var.cognito_user_pool_id
  name                       = "id-domain-user-pool-dev"
  admin_create_user          = true
  admin_create_user_password = true
  admin_create_user_profile  = true
  domain                     = "auth.id.music"
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes       = ["openid", "email"]
}

variable "environment" {
  default = "dev"
}
variable "identity_pool_id" {
  default = "id-domain-identity-pool-dev"
}
module "cognito_identity_pool" {
  source  = "../../../modules/cognito-identity-pool/aws"    
  

    identity_pool_name = "id-domain-identity-pool-${var.environment}"
    identity_pool_id   = "id-domain-identity-pool-${var.environment}"
    cognito_user_pool_id = var.cognito_user_pool_id
    allowed_oauth_scopes = ["openid", "email"]
    allowed_oauth_flows = ["implicit"]
    allowed_oauth_flows_user_pool_client = true
    allow_unauthenticated_identities = true
}

module "keycloak" {
  source  = "../../../modules/keycloak"
  

  keycloak_url = "auth.id.music"
  realms       = ["dev"]
}

module "load_balancer" {
  source  = "../../../modules/load-balancer/aws"
  

  name            = "id-domain-load-balancer-dev"
  subnets         = var.load_balancer_subnets
  security_groups = var.load_balancer_security_groups
  region          = "eu-west-1"
  ssl_certificate_arn = var.ssl_certificate_arn
}
