resource "google_cloud_run_service" "cloud_run_audio_transcription_orchestrator" {
  name     = "cloudrun-audio-transcription-request-orchestrator"
  location = var.location

  template {
    spec {

      service_account_name = google_service_account.cloud_run_sa.email
      containers {
        image = "europe-west1-docker.pkg.dev/prj-dtdk-client-billing/client-billing/notification-slack-service:latest"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [
    google_project_iam_binding.token_creator_service_agent_member
  ]
}


resource "google_cloud_run_service" "cloud_run_transcriber-service" {
  name     = "cloudrun-audio-transcriber"
  location = var.location

  template {
    spec {

      service_account_name = google_service_account.cloud_run_sa.email
      containers {
        image = "europe-west1-docker.pkg.dev/prj-dtdk-client-billing/client-billing/notification-slack-service:latest"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [
    google_project_iam_binding.token_creator_service_agent_member
  ]
}