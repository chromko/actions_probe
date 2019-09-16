// Configure the Google Cloud provider
provider "google" {
  version = "~> 2.13.0"

  project = var.google_project
  region  = var.google_region
  zone = "${var.google_region}-c"
}
