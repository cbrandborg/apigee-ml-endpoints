resource "google_artifact_registry_repository" "ar_asr_services" {
  project       = var.project_id
  location      = var.location
  repository_id = var.artifact_registry
  description   = "Repository for billing projects related to clients"
  format        = "DOCKER"

  depends_on = [
    google_project_service.api_enable-2
  ]
}