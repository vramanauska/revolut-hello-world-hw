#!/bin/bash

# Variables
AWS_REGION="your_aws_region"
AWS_PROFILE="your_aws_profile"
ECR_REPO_NAME="birthday-reminder"
APP_IMAGE_TAG="v1"
APP_PORT=80
APP_NAMESPACE="birthday-reminder"
PRIMARY_DB_ENDPOINT="primary_db_endpoint"
STANDBY_DB_ENDPOINT="standby_db_endpoint"

# Build and push Docker image to ECR
$(aws ecr get-login --no-include-email --region $AWS_REGION --profile $AWS_PROFILE)
docker build -t $ECR_REPO_NAME:$APP_IMAGE_TAG .
docker tag $ECR_REPO_NAME:$APP_IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:$APP_IMAGE_TAG
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:$APP_IMAGE_TAG

# Create or update Kubernetes deployment
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $ECR_REPO_NAME
  namespace: $APP_NAMESPACE
spec:
  replicas: 1
  selector:
    matchLabels:
      app: $ECR_REPO_NAME
  template:
    metadata:
      labels:
        app: $ECR_REPO_NAME
    spec:
      containers:
      - name: $ECR_REPO_NAME
        image: $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:$APP_IMAGE_TAG
        ports:
        - containerPort: $APP_PORT
        env:
        - name: PRIMARY_DB_ENDPOINT
          value: $PRIMARY_DB_ENDPOINT
        - name: STANDBY_DB_ENDPOINT
          value: $STANDBY_DB_ENDPOINT
---
apiVersion: v1
kind: Service
metadata:
  name: $ECR_REPO_NAME
  namespace: $APP_NAMESPACE
spec:
  type: LoadBalancer
  selector:
    app: $ECR_REPO_NAME
  ports:
  - protocol: TCP
    port: $APP_PORT
    targetPort: $APP_PORT
EOF
