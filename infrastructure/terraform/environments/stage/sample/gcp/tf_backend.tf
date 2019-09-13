terraform {
  backend "gcs" {
    bucket  = "tf-states"
    prefix    = "stage/sample/gcp"
  }
}
