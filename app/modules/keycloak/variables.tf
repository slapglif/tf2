
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
        