
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
    