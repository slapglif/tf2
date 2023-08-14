
        # Terraform configuration for the Cognito Identity Pool module
        resource "aws_cognito_identity_pool" "identity_pool" {
          identity_pool_name = var.identity_pool_name
          allow_unauthenticated_identities = true

          cognito_identity_providers {
            client_id = var.cognito_user_pool_client_id
            provider_name = var.cognito_user_pool_provider_name
          }
        }
        