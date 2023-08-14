
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
        