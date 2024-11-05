#!/bin/bash

# Configuration variables
PROJECT_NAME="geokapti_project"
IMAGE_NAME="geokapti_image"
VERSION_TAG="v0.2.0"

# Building the Docker image
echo "Building the Docker image..."
docker build -t $IMAGE_NAME:$VERSION_TAG .

# Function to deploy in Azure
deploy_azure() {
    echo "Getting started with Azure deployment..."

    # Azure Resource Group y App Service Plan
    AZURE_RESOURCE_GROUP="geokapti-resource-group"
    AZURE_APP_PLAN="geokapti-app-plan"
    AZURE_APP_NAME="geokapti-app"

    # Create resource group and App Service plan if it does not exist
    az group create --name $AZURE_RESOURCE_GROUP --location "East US"
    az appservice plan create --name $AZURE_APP_PLAN --resource-group $AZURE_RESOURCE_GROUP --sku B1 --is-linux

    # Create the we application
    az webapp create --resource-group $AZURE_RESOURCE_GROUP --plan $AZURE_APP_PLAN --name $AZURE_APP_NAME --deployment-container-image-name $IMAGE_NAME:$VERSION_TAG

    # Push image to Azure Container Registry and deploy
    az acr login --name $AZURE_APP_NAME
    docker tag $IMAGE_NAME:$VERSION_TAG $AZURE_APP_NAME.azurecr.io/$IMAGE_NAME:$VERSION_TAG
    docker push $AZURE_APP_NAME.azurecr.io/$IMAGE_NAME:$VERSION_TAG
    az webapp config container set --name $AZURE_APP_NAME --resource-group $AZURE_RESOURCE_GROUP --docker-custom-image-name $AZURE_APP_NAME.azurecr.io/$IMAGE_NAME:$VERSION_TAG

    echo "Deployment in Azure completed."
}

# Function to deploy on AWS
deploy_aws() {
    echo "Iniciando la implementación en AWS..."

    # AWS ECR Repository and ECS configuration
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    AWS_REGION="us-east-1"
    AWS_ECR_REPO="$PROJECT_NAME-repo"
    AWS_CLUSTER_NAME="geokapti-cluster"
    AWS_SERVICE_NAME="geokapti-service"

    # Create repository in ECR if it does not exist
    aws ecr create-repository --repository-name $AWS_ECR_REPO --region $AWS_REGION || echo "El repositorio ya existe."

    # Log in ECR, image push and set up EC
    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
    docker tag $IMAGE_NAME:$VERSION_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$AWS_ECR_REPO:$VERSION_TAG
    docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$AWS_ECR_REPO:$VERSION_TAG

    # Create a new service in ECS if it does not exist.
    aws ecs create-cluster --cluster-name $AWS_CLUSTER_NAME || echo "El cluster ya existe."
    aws ecs create-service --cluster $AWS_CLUSTER_NAME --service-name $AWS_SERVICE_NAME --task-definition $IMAGE_NAME:$VERSION_TAG --desired-count 1 --launch-type FARGATE

    echo "Deployment on AWS completed."
}

# Functionality to deploy in Google Cloud
deploy_gcloud() {
    echo "Getting started with Google Clou implementation..."

    # Google Cloud Artifact Registry and Cloud Run
    GCP_PROJECT_ID=$(gcloud config get-value project)
    GCP_REGION="us-central1"
    GCP_ARTIFACT_REPO="geokapti-repo"
    GCP_SERVICE_NAME="geokapti-service"

    # Create a repository in the Artifact Registry if it does not exist.
    gcloud artifacts repositories create $GCP_ARTIFACT_REPO --repository-format=docker --location=$GCP_REGION || echo "The repository already exists."

    # Log into Artifact Registry, push image and deploy to Cloud Run
    gcloud auth configure-docker $GCP_REGION-docker.pkg.dev
    docker tag $IMAGE_NAME:$VERSION_TAG $GCP_REGION-docker.pkg.dev/$GCP_PROJECT_ID/$GCP_ARTIFACT_REPO/$IMAGE_NAME:$VERSION_TAG
    docker push $GCP_REGION-docker.pkg.dev/$GCP_PROJECT_ID/$GCP_ARTIFACT_REPO/$IMAGE_NAME:$VERSION_TAG

    # Deploy to Cloud Run
    gcloud run deploy $GCP_SERVICE_NAME --image $GCP_REGION-docker.pkg.dev/$GCP_PROJECT_ID/$GCP_ARTIFACT_REPO/$IMAGE_NAME:$VERSION_TAG --platform managed --region $GCP_REGION --allow-unauthenticated

    echo "Deployment on Google Cloud completed."
}

# Validate user input to select cloud provider
if [ $# -eq 0 ]; then
    echo "Uso: $0 {azure|aws|gcloud}"
    exit 1
fi

case "$1" in
    azure)
        deploy_azure
        ;;
    aws)
        deploy_aws
        ;;
    gcloud)
        deploy_gcloud
        ;;
    *)
        echo "Invalid provider. Select one of the following: azure, aws, gcloud"
        exit 1
        ;;
esac

echo "The $1 deployment has been successfully completed."
