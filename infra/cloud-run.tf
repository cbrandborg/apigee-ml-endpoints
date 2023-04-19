# resource "google_cloud_run_service" "cloud_run_audio_transcription_orchestrator" {
#   name     = "cloudrun-audio-transcription-request-orchestrator"
#   location = var.location

#   template {
#     spec {

#       service_account_name = google_service_account.cloud_run_sa.email
#       containers {
#         image = "europe-west1-docker.pkg.dev/prj-dtdk-client-billing/client-billing/notification-slack-service:latest"
#       }
#     }
#   }

#   traffic {
#     percent         = 100
#     latest_revision = true
#   }

#   depends_on = [
#     google_project_iam_binding.token_creator_service_agent_member
#   ]
# }


# module "cloud_run_asr_services" {
#   source  = "GoogleCloudPlatform/cloud-run/google"
#   version = "~> 0.2.0"

#   # Required variables
#   service_name           = "cloudrun-asr-"
#   project_id             = var.project_id
#   location               = var.location
#   image                  = "gcr.io/cloudrun/hello"
#   traffic_split          = [
#                               {
#                                 "latest_revision": true,
#                                 "percent": 100,
#                                 "revision_name": "v1-0-0",
#                                 "tag": null
#                               }
#                             ]
#   #env_vars
#   service_account_email   = "${var.cloud_run_sa}@${var.project_id}.iam.gserviceaccount.com"
#   members                 = ["${var.cloud_run_sa}@${var.project_id}.iam.gserviceaccount.com"]

#   depends_on = [
#     google_project_iam_binding.token_creator_service_agent_member
#   ]

# }
