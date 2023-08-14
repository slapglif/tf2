
        # Terraform configuration for networking
        resource "aws_internet_gateway" "igw" {
          vpc_id = var.vpc_id
        }

        resource "aws_route_table" "rtb" {
          vpc_id = var.vpc_id
        }

        resource "aws_subnet" "subnet" {
          vpc_id     = var.vpc_id
          cidr_block = var.cidr_block
        }

        resource "aws_vpc" "vpc" {
          cidr_block = var.cidr_block
        }
        