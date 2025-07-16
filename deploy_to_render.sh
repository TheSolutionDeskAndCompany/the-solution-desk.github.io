#!/bin/bash

# 🚀 Deploy Backend to Render.com
# Prerequisites: Bash, cURL, Render API key

# Check if RENDER_API_KEY is set
if [ -z "$RENDER_API_KEY" ]; then
  echo "⛔ Error: RENDER_API_KEY environment variable is not set"
  echo "Please set it using: export RENDER_API_KEY='your-api-key'"
  exit 1
fi

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
  echo "❌ DATABASE_URL environment variable is not set"
  exit 1
fi

# Check if JWT_SECRET is set
if [ -z "$JWT_SECRET" ]; then
  echo "⚠️ Warning: JWT_SECRET environment variable is not set"
  echo "Attempting to use SECRET_KEY from .env file"
  # Extract from .env if available
  if [ -f .env ]; then
    # Try to get JWT_SECRET first, then try SECRET_KEY
    JWT_SECRET=$(grep JWT_SECRET .env | cut -d '=' -f2)
    if [ -z "$JWT_SECRET" ]; then
      JWT_SECRET=$(grep SECRET_KEY .env | cut -d '=' -f2)
      echo "Found JWT_SECRET (from SECRET_KEY) in .env file"
    else
      echo "Found JWT_SECRET in .env file"
    fi
  else
    echo "No .env file found with JWT_SECRET"
    echo "Please export JWT_SECRET='your-secret'"
    exit 1
  fi
fi

# Get owner ID
ACCOUNT_RESPONSE_FILE="render_account_response.json"
curl -s -H "Authorization: Bearer $RENDER_API_KEY" \
  https://api.render.com/v2/user -o "$ACCOUNT_RESPONSE_FILE"

if [ ! -s "$ACCOUNT_RESPONSE_FILE" ]; then
  echo "❌ Failed to get account response. Please check your API key and network connection."
  exit 1
fi

OWNER_ID=$(jq -r '.user.id' "$ACCOUNT_RESPONSE_FILE" 2>/dev/null)

if [ -z "$OWNER_ID" ]; then
  echo "❌ Failed to get owner ID. Possible reasons:"
  echo "  1. Invalid API response format"
  echo "  2. API key doesn't have permission"
  echo "Response saved to $ACCOUNT_RESPONSE_FILE for inspection"
  exit 1
fi

echo "🔧 Creating Render web service..."
RESPONSE=$(curl -X POST https://api.render.com/v1/services \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "serviceType": "web",
    "ownerId": "'$OWNER_ID'",
    "name": "thesolutiondesk",
    "repo": "https://github.com/TheSolutionDeskAndCompany/the-solution-desk.github.io.git",
    "branch": "main",
    "envVars": [
      {"key":"DATABASE_URL","value":"'"$DATABASE_URL"'"},
      {"key":"JWT_SECRET","value":"'"$JWT_SECRET"'"},
      {"key":"FLASK_ENV","value":"production"}
    ],
    "buildCommand": "pip install -r requirements.txt && cd frontend && npm install && npm run build && cd ..",
    "startCommand": "gunicorn app:app --preload --bind 0.0.0.0:$PORT --workers 3"
  }')

echo "$RESPONSE"

# Extract the service ID
SERVICE_ID=$(echo $RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)

if [ -z "$SERVICE_ID" ]; then
  echo "❌ Failed to get service ID. Please check the response above for errors."
  exit 1
fi

echo "✅ Service created with ID: $SERVICE_ID"
echo "🌐 Your service will be live at: https://thesolutiondesk.onrender.com"

echo "🚀 Triggering initial deploy..."
DEPLOY_RESPONSE=$(curl -X POST "https://api.render.com/v1/services/$SERVICE_ID/deploys" \
  -H "Authorization: Bearer $RENDER_API_KEY")

echo "$DEPLOY_RESPONSE"

echo "
📋 Deployment Summary:"
echo "🔗 Service URL: https://thesolutiondesk.onrender.com"
echo "📊 Dashboard: https://dashboard.render.com/services/$SERVICE_ID/deploys"
echo "
🔍 To verify the health of your backend, run:"
echo "-----------------------------------------------------------"
echo "until curl -sSf https://thesolutiondesk.onrender.com/health; do"
echo "  echo "⏳ Waiting for backend…""
echo "  sleep 5"
echo "done"
echo "echo "🚀 Backend is live!""
echo "-----------------------------------------------------------"
