#!/bin/bash

# Check if RENDER_API_KEY is set
if [ -z "$RENDER_API_KEY" ]; then
  echo "Error: RENDER_API_KEY environment variable is not set"
  echo "Please set it using: export RENDER_API_KEY='your-api-key'"
  exit 1
fi

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
  echo "Warning: DATABASE_URL environment variable is not set"
  echo "Using default value from .env file"
  # Extract from .env if available
  if [ -f .env ]; then
    DATABASE_URL=$(grep DATABASE_URL .env | cut -d '=' -f2)
  fi
fi

# Check if JWT_SECRET is set
if [ -z "$JWT_SECRET" ]; then
  echo "Warning: JWT_SECRET environment variable is not set"
  echo "Using SECRET_KEY from .env file"
  # Extract from .env if available
  if [ -f .env ]; then
    JWT_SECRET=$(grep SECRET_KEY .env | cut -d '=' -f2)
  fi
fi

echo "Creating Render web service..."
RESPONSE=$(curl -X POST https://api.render.com/v1/services \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "serviceType": "web",
    "name": "ow-backend",
    "repo": "https://github.com/TheSolutionDeskAndCompany/the-solution-desk.github.io.git",
    "branch": "main",
    "envVars": [
      {"key":"DATABASE_URL","value":"'"$DATABASE_URL"'"},
      {"key":"JWT_SECRET","value":"'"$JWT_SECRET"'"},
      {"key":"FLASK_ENV","value":"production"}
    ],
    "buildCommand": "pip install -r requirements.txt",
    "startCommand": "gunicorn app:app --preload --bind 0.0.0.0:$PORT --workers 3"
  }')

echo "$RESPONSE"

# Extract the service ID
SERVICE_ID=$(echo $RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)

if [ -z "$SERVICE_ID" ]; then
  echo "Failed to get service ID. Please check the response above for errors."
  exit 1
fi

echo "Service ID: $SERVICE_ID"

echo "Triggering initial deploy..."
DEPLOY_RESPONSE=$(curl -X POST "https://api.render.com/v1/services/$SERVICE_ID/deploys" \
  -H "Authorization: Bearer $RENDER_API_KEY")

echo "$DEPLOY_RESPONSE"

echo "Deployment initiated. The service URL will be: https://ow-backend.onrender.com"
echo "You can verify the health by running:"
echo "until curl -sSf https://ow-backend.onrender.com/health; do echo 'Waiting for backend…'; sleep 5; done; echo 'Backend is live!'"
