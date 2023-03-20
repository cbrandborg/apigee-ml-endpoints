export AUTH="Authorization: Bearer $(gcloud auth print-access-token)"
export PROJECT_ID=devo-ruben-sandbox
export ENV_GROUP_HOSTNAME=$(curl -H "$AUTH" https://apigee.googleapis.com/v1/organizations/$PROJECT_ID/envgroups -s | jq -r '.environmentGroups[0].hostnames[0]')
export INTERNAL_LOAD_BALANCER_IP=$(curl -H "$AUTH" https://apigee.googleapis.com/v1/organizations/$PROJECT_ID/instances -s | jq -r '.instances[0].host')
