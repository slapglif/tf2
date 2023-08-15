
# Define the environments to deploy
variable "environments" {
  type    = list(string)
  default = ["dev", "prod", "qa", "staging"]
}
