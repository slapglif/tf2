terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.66.1"
    }
  }
  backend "s3" {
    bucket = "terraform-state-eu-west-1-id-music-prod"
    key    = "terraform.tfstate"
    region = "eu-west-1"
  }
}

provider "aws" {
  region = "eu-west-1"
}

# Create a VPC
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr_block
}

# Create subnets in different Availability Zones
resource "aws_subnet" "main" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.subnet_cidr_blocks[count.index]
  availability_zone = var.availability_zones[count.index]
}

# Create an Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}

# Create a route table
resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}

# Associate the route table with the subnet
resource "aws_route_table_association" "main" {
  count          = length(var.availability_zones)
  subnet_id      = aws_subnet.main[count.index].id
  route_table_id = aws_route_table.main.id
}

# Create a DB subnet group
resource "aws_db_subnet_group" "keycloak_db_subnet_group" {
  name       = "keycloak-db-subnet-group"
  subnet_ids = aws_subnet.main[*].id
}

# Create a DB instance
resource "aws_db_instance" "keycloak_db" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "postgres"
  engine_version       = var.db_engine_version
  instance_class       = "db.t2.medium"
  username             = "keycloak"
  password             = "password"
  parameter_group_name = "default.postgres14"
  skip_final_snapshot  = true
  vpc_security_group_ids = [aws_security_group.keycloak_db_sg.id]
  db_subnet_group_name = aws_db_subnet_group.keycloak_db_subnet_group.name
}

# Create a security group for the DB instance
resource "aws_security_group" "keycloak_db_sg" {
  vpc_id = aws_vpc.main.id
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create an ECS cluster
resource "aws_ecs_cluster" "keycloak_cluster" {
  name = "keycloak-cluster"
}

# Define the ECS task definition
resource "aws_ecs_task_definition" "keycloak" {
  family                = "keycloak"
  container_definitions = file("keycloak-container-definition.json")
}

# Create an ECS service
resource "aws_ecs_service" "keycloak_service" {
  name            = "keycloak-service"
  cluster         = aws_ecs_cluster.keycloak_cluster.id
  task_definition = aws_ecs_task_definition.keycloak.arn
  desired_count   = 2
  launch_type     = "EC2"
  load_balancer {
    target_group_arn = aws_lb_target_group.keycloak_tg.arn
    container_name   = "keycloak"
    container_port   = 8080
  }
}

# Create a load balancer
resource "aws_lb" "keycloak_lb" {
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.keycloak_lb_sg.id]
  subnets            = aws_subnet.main[*].id
}

# Create a target group for the load balancer
resource "aws_lb_target_group" "keycloak_tg" {
  port     = 8080
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
}

# Create a security group for the load balancer
resource "aws_security_group" "keycloak_lb_sg" {
  vpc_id = aws_vpc.main.id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
# Request an ACM certificate for the domain if it doesn't exist
resource "aws_acm_certificate" "auth_id_music_cert" {
  domain_name       = "auth.id.music"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

# Check if the domain exists
data "aws_route53_zone" "id_music" {
  name         = "auth.id.music"
  private_zone = false
}

# DNS validation record for the ACM certificate
resource "aws_route53_record" "auth_id_music_cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.auth_id_music_cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
    if dvo.domain_name == "auth.id.music"
  }

  name    = each.value.name
  type    = each.value.type
  records = [each.value.record]
  ttl     = 60

  zone_id = data.aws_route53_zone.id_music.zone_id
}

resource "aws_acm_certificate_validation" "auth_id_music_cert_validation" {
  for_each = aws_route53_record.auth_id_music_cert_validation

  certificate_arn         = aws_acm_certificate.auth_id_music_cert.arn
  validation_record_fqdns = [each.value.fqdn]
}

# Create or update the Route 53 record for auth.id.music
resource "aws_route53_record" "auth_id_music" {
  zone_id = data.aws_route53_zone.id_music.zone_id # Reference to the defined zone
  name    = "auth.id.music"
  type    = "A"
  alias {
    name                   = aws_lb.keycloak_lb.dns_name
    zone_id                = aws_lb.keycloak_lb.zone_id
    evaluate_target_health = false
  }
}



# Create a load balancer listener with the ACM certificate
resource "aws_lb_listener" "keycloak_listener" {
  load_balancer_arn = aws_lb.keycloak_lb.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = aws_acm_certificate.auth_id_music_cert.arn
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.keycloak_tg.arn
  }

  depends_on = [aws_lb.keycloak_lb, aws_lb_target_group.keycloak_tg] # Ensure correct order
}

# Create a load balancer listener with a redirect to HTTPS
resource "aws_lb_listener" "keycloak_listener_redirect" {
  load_balancer_arn = aws_lb.keycloak_lb.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type             = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }

  depends_on = [aws_lb.keycloak_lb] # Ensure correct order
}

# Create a load balancer target group attachment
resource "aws_lb_target_group_attachment" "keycloak_tg_attachment" {
  target_group_arn = aws_lb_target_group.keycloak_tg.arn
  target_id        = aws_ecs_service.keycloak_service.id
  port             = 8080
}

# Create a load balancer listener rule
resource "aws_lb_listener_rule" "keycloak_listener_rule" {
  listener_arn = aws_lb_listener.keycloak_listener.arn
  priority     = 100
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.keycloak_tg.arn
  }
  condition {
    path_pattern {
      values = ["/auth*"]
    }
  }
}
