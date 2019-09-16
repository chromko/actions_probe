#################################
# Google Cloud Provider variables
#################################

variable "google_project" {
  description = "The ID of the project"
}

variable "google_region" {
  default     = "europe-west1"
  description = "The region to operate under"
}


variable "project_name" {
  description = "platform"
}
variable "project_env" {
  description = "test"
}

variable "project_service" {
  description = "test"
}

variable "ssh_keys" {
  description = "test"
  default = {}
  type = map(string)
}

variable "project_app" {
  description = "test"
}

variable "machine_type" {
  description = "test"
}

variable "project_services" {
  type = list(string)
  default = [
    "cloudkms.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "container.googleapis.com",
    "compute.googleapis.com",
    "iam.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com",
  ]
  description = "List of services to enable on the project."
}
