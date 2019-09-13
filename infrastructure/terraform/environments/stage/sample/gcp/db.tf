resource "google_compute_instance_template" "tpl" {
  name = "${var.project_name}-${var.project_env}-${var.project_app}-db-tpl"
  machine_type = "g1-small"
  region           = var.google_region
  project          = var.google_project

  disk {
    // source_image = "centos-7/centos-7-v20190729"
    source_image = "centos-cloud/centos-7"
    auto_delete = true
    boot = true
  }

  network_interface {
    access_config {}
  }

  metadata = {
    ssh-keys = join("\n", [for user, key in var.ssh_keys : "${user}:${key}"])
  }

}


resource "google_compute_instance_from_template" "service-app-1" {
  name           = "${var.project_name}-${var.project_env}-${var.project_app}-app-1"
  source_instance_template = "${google_compute_instance_template.tpl.self_link}"

  // Override fields from instance template
  machine_type = var.machine_type
  allow_stopping_for_update = true
  labels = {
    env = var.project_env
    project = var.project_name
    app = var.project_app
    service = var.project_service
    component: "app"
  }
  tags = [var.project_env,var.project_name,var.project_service,"app"]

}
