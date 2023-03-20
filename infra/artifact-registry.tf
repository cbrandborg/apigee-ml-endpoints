resource "google_artifact_registry_repository" "ar_orchestrator_service" {
  project       = var.project_id
  repository_id = "${var.artifact_registry}-orchestration"
  description   = "Repository for billing projects related to clients"
  format        = "DOCKER"

  depends_on = [
    google_project_service.api_enable-2
  ]
}

resource "google_artifact_registry_repository" "ar_transcription_service" {
  location      = var.location
  project       = var.project_id
  repository_id = "${var.artifact_registry}-transcriber"
  description   = "Repository for billing projects related to clients"
  format        = "DOCKER"

  depends_on = [
    google_project_service.api_enable-2
  ]
}