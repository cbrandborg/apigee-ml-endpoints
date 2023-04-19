# module "pubsub-audio-queue" {
#   source  = "terraform-google-modules/pubsub/google"
#   version = "4.0.1"

#   topic      = "billing-alert-slack-topic"
#   project_id = var.project_id



#   push_subscriptions = [
#     {
#       name                       = "push"
#       ack_deadline_seconds       = 600
#       push_endpoint              = google_cloud_run_service.cloud_run_transcriber-service.status[0].url
#       oidc_service_account_email = google_service_account.cloud_run_sa.email
#       x-goog-version             = "v1beta1"
#     }
#   ]

#   depends_on = [
#     google_cloud_run_service.cloud_run_notification_service
#   ]
# }


# module "pubsub-transcription-queue" {
#   source  = "terraform-google-modules/pubsub/google"
#   version = "4.0.1"

#   topic      = "billing-alert-slack-topic"
#   project_id = var.project_id



#   push_subscriptions = [
#     {
#       name                       = "push"
#       ack_deadline_seconds       = 600
#       push_endpoint              = google_cloud_run_service.cloud_run_audio_transcription_orchestrator.status[0].url
#       oidc_service_account_email = google_service_account.cloud_run_sa.email
#       x-goog-version             = "v1beta1"
#     }
#   ]

#   depends_on = [
#     google_cloud_run_service.cloud_run_notification_service
#   ]
# }