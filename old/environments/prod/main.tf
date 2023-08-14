
# Terraform configuration for the prod environment
module "cognito_user_pool" {
  source  = "../../../modules/cognito-user-pool/aws"
  

  name                       = "id-domain-user-pool-prod"
  admin_create_user          = true
  admin_create_user_password = true
  admin_create_user_profile  = true
domain                     = "auth.id.music"
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes       = ["openid", "email"]
}

module "cognito_identity_pool" {
  source  = "../../../modules/cognito-identity-pool/aws"    
  

  identity_pool_name = "id-domain-identity-pool-prod"
  cognito_user_pool_id = module.cognito_user_pool.user_pool_id
}

module "keycloak" {
  source  = "../../../modules/keycloak"
  

  keycloak_url = "auth.id.music"
  realms       = ["prod"]
}

module "load_balancer" {
  source  = "../../../modules/load-balancer/aws"
  

  name            = "id-domain-load-balancer-prod"
  subnets         = var.load_balancer_subnets
  security_groups = var.load_balancer_security_groups
  region          = "eu-west-1"
  ssl_certificate_arn = var.ssl_certificate_arn
}
