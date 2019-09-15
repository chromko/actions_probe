resource "google_project_service" "service" {
  count   = length(var.project_services)
  service = element(var.project_services, count.index)

  # Do not disable the service on destroy. On destroy, we are going to
  # destroy the project, but we need the APIs available to destroy the
  # underlying resources.
  disable_on_destroy = false
}

resource "google_compute_network" "env-vpc" {
  name = "${var.project_name}-${var.project_env}-vpc"
  auto_create_subnetworks = "false"
  provider                = "google-beta"
  project = var.google_project
}

resource "google_compute_subnetwork" "env-subnetwork" {
  name          = "${var.project_name}-${var.project_env}-subnetwork"
  network       = google_compute_network.env-vpc.self_link
  region        = var.google_region
  ip_cidr_range = "10.10.0.0/16"

  private_ip_google_access = true

}
resource "google_compute_instance" "gcp-test" {
  name         = "gcp-test-ip"
  machine_type = "custom-2-2048"
  zone         = "${var.google_region}-c"
  labels = {
    env = var.project_env
    project = var.project_name
    app = var.project_app
    service = var.project_service
    component: "app"
  }
  tags = [var.project_env,var.project_name,var.project_service,"app"]

  boot_disk {
    initialize_params {

     image = "centos-cloud/centos-7"
    }
    auto_delete = true
    // boot = true
  }

  network_interface {
    network = "default"

        access_config {
          // Ephemeral IP
        }
  }

  metadata = {
    ssh-keys = join("\n", [for user, key in var.ssh_keys : "${user}:${key}"])
  }
}


// resource "google_compute_instance_from_template" "service-app-1" {
//   name           = "${var.project_name}-${var.project_env}-${var.project_app}-app-1"
//   source_instance_template = "${google_compute_instance_template.tpl.self_link}"

//   // Override fields from instance template
//   machine_type = var.machine_type
//   allow_stopping_for_update = true
//   labels = {
//     env = var.project_env
//     project = var.project_name
//     app = var.project_app
//     service = var.project_service
//     component: "app"
//   }
//   tags = [var.project_env,var.project_name,var.project_service,"app"]

// }

resource "google_compute_address" "env-public" {
  name = "${var.project_name}-${var.project_env}-appserver-ip"
  address_type = "EXTERNAL"
  region = var.google_region
}

resource "google_compute_forwarding_rule" "default" {
  name       = "website-forwarding-rule"
  target     = "${google_compute_target_pool.default.self_link}"
  port_range = "80"
}

resource "google_compute_target_pool" "default" {
  name = "instance-pool"
  region = var.google_region

  instances = [
    google_compute_instance.gcp-test.self_link
  ]
}


resource "google_compute_firewall" "default" {
  name    = "${var.project_name}-${var.project_env}-allow-internal"
  network       = google_compute_network.env-vpc.self_link

  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  source_ranges  = ["10.0.0.0/8"]
}
