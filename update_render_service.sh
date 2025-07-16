#!/bin/bash

# 🚀 Update existing Render service
# Prerequisites: Bash, cURL, Render API key

# Check if RENDER_API_KEY is set
if [ -z "$RENDER_API_KEY" ]; then
  echo "⛔ Error: RENDER_API_KEY environment variable is not set"
  echo "Please set it using: export RENDER_API_KEY='your-api-key'"
  exit 1
fi

# Service details
SERVICE_ID="srv-d1of3bur433s73c9qvqg"
SERVICE_NAME="thesolutiondesk"

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
  echo "❌ DATABASE_URL environment variable is not set"
  exit 1
fi

# Check if JWT_SECRET is set
if [ -z "$JWT_SECRET" ]; then
  echo "⚠️ Warning: JWT_SECRET environment variable is not set"
  echo "Attempting to use SECRET_KEY from .env file"
  if [ -f .env ]; then
    JWT_SECRET=$(grep JWT_SECRET .env | cut -d '=' -f2)
    if [ -z "$JWT_SECRET" ]; then
      JWT_SECRET=$(grep SECRET_KEY .env | cut -d '=' -f2)
      echo "Found JWT_SECRET (from SECRET_KEY) in .env file"
    else
      echo "Found JWT_SECRET in .env file"
    fi
  fi
  
  if [ -z "$JWT_SECRET" ]; then
    echo "❌ JWT_SECRET not found. Please set it in your environment or .env file"
    exit 1
  fi
fi

echo "🚀 Updating service $SERVICE_NAME (ID: $SERVICE_ID)..."

# Update the service configuration
RESPONSE=$(curl -X PATCH "https://api.render.com/v1/services/$SERVICE_ID" \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "envVars": [
      {"key":"DATABASE_URL","value":"'$DATABASE_URL'"},
      {"key":"JWT_SECRET","value":"'$JWT_SECRET'"},
      {"key":"FLASK_ENV","value":"production"}
    ]
  }' 2>/dev/null)

echo "🔧 Service update response:"
echo "$RESPONSE"

echo "🚀 Triggering new deployment..."
DEPLOY_RESPONSE=$(curl -X POST "https://api.render.com/v1/services/$SERVICE_ID/deploys" \
  -H "Authorization: Bearer $RENDER_API_KEY" 2>/dev/null)

echo "📦 Deployment response:"
echo "$DEPLOY_RESPONSE"

echo "\n✅ Update initiated for $SERVICE_NAME"
echo "🌐 Your service will be updated at: https://$SERVICE_NAME.onrender.com"
echo "📊 Check deployment status at: https://dashboard.render.com/web/$SERVICE_ID"
