  GNU nano 7.2                      deploy.sh                               #!/bin/bash

TAG=${1:-latest} #default to latest if no tag is provided

echo "Deploying backend and frontend with tag: $TAG"

export BACKEND_TAG=$TAG
export FRONTEND_TAG=$TAG

#pulling latest image
docker-compose pull

echo "Restarting containers..."
docker-compose up -d