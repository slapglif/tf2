
        # Terraform configuration for the Cognito User Pool module
        resource "aws_cognito_user_pool" "user_pool" {
          name = var.user_pool_name
        }
        