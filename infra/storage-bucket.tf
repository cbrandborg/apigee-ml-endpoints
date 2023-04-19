module "asr_audio_file_bkt" {
  source  = "terraform-google-modules/cloud-storage/google//modules/simple_bucket"
  version = "~> 4.0"

  name                  = var.storage_bucket
  project_id            = var.project_id
  location              = var.location
  lifecycle_rules = [{
    action = {
      type = "Delete"
    }
    condition = {
      age            = 30
    }
  }]

   depends_on = [
    google_project_service.api_enable-2
  ]
}