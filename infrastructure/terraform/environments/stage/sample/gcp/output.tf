output instances_db_addr {
  value = google_compute_instance.gcp-test-db[*].network_interface.0.access_config.0.nat_ip
}

output instances_app_addr {
  value = google_compute_instance.gcp-test[*].network_interface.0.access_config.0.nat_ip
}
