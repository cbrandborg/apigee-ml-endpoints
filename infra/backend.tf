terraform {
  backend "gcs" {
    bucket  = "bkt-asr-tf-statefiles"
    prefix  = "terraform/state"
  }
}
