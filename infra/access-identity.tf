resource "google_project_service" "api_enable-0" {
  project = var.project_id

  for_each = toset([
    "cloudresourcemanager.googleapis.com"
  ])
  service = each.key

  timeouts {
    create = "30m"
    update = "40m"
  }
}


resource "google_project_service" "api_enable-1" {
  project = var.project_id

  for_each = toset([
    "cloudapis.googleapis.com",
    "iam.googleapis.com",
    "billingbudgets.googleapis.com",

  ])
  service = each.key

  timeouts {
    create = "30m"
    update = "40m"
  }

  depends_on = [
    google_project_service.api_enable-0
  ]
}

resource "google_project_service" "api_enable-2" {
  project = var.project_id

  for_each = toset([
    "pubsub.googleapis.com",
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "artifactregistry.googleapis.com",
    "speech.googleapis.com"

  ])
  service = each.key

  disable_dependent_services = true

  timeouts {
    create = "30m"
    update = "40m"
  }

  depends_on = [
    google_project_service.api_enable-1
  ]
}

resource "google_service_account" "cloud_run_sa" {
  account_id   = var.cloud_run_sa
  display_name = "Cloud Run Service Account"

  depends_on = [
    google_project_service.api_enable-2
  ]
}


# resource "google_project_service_identity" "pubsub_service_agent" {
#   provider = google-beta
#   project  = var.project_id
#   service  = "pubsub.googleapis.com"

#   depends_on = [
#     google_project_service.api_enable-2
#   ]
# }

# resource "google_project_iam_binding" "token_creator_service_agent_member" {
#   project = var.project_id
#   role    = "roles/iam.serviceAccountTokenCreator"
#   members = ["serviceAccount:${google_project_service_identity.pubsub_service_agent.email}"]

#   depends_on = [
#     google_project_service_identity.pubsub_service_agent
#   ]
# }