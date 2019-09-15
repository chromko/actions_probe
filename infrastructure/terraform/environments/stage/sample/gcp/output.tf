output instances_addr {
  value = google_compute_instance.gcp-test[*].network_interface.0.access_config.0.nat_ip
}
