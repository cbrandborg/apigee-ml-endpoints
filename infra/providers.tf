terraform {

  # cloud {
  #   organization = "cbrandborg"

  #   workspaces {
  #     name = "billing-slack-notification-service"
  #   }
  # }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.62.0"
    }
  }
}

provider "google" {
  credentials = file("../prj-dvt-asr-apis-6055ff07b2f7.json")
  project = var.project_id
  region  = var.location
}
