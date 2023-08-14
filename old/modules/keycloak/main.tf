
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
        