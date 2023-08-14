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
  user_pool_name = ""
}

module "cognito_identity_pool" {
  source  = "corpit-consulting-public/cognito-identity-pool/aws"


  identity_pool_name = "id-domain-identity-pool"
  cognito_user_pool_id = module.cognito_user_pool.user_pool_id
}

module "keycloak" {
  source  = "github.com/mrparkers/keycloak.git"


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
