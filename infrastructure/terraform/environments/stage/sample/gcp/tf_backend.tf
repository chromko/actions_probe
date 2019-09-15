terraform {
  backend "gcs" {
    bucket  = "chromko-tmp-bucket"
    prefix    = "stage/sample/gcp"
  }
}
