#!/bin/bash

# 🚀 Deploy to Render.com
# Prerequisites: Bash, cURL, jq, Render API key

set -e  # Exit on error

# Enable debug logging if DEBUG is set
[ -n "$DEBUG" ] && set -x

# Constants
SERVICE_NAME="thesolutiondesk"
REPO_URL="https://github.com/TheSolutionDeskAndCompany/the-solution-desk.github.io.git"
REGION="oregon"
PLAN="free"

# Logging function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required commands
for cmd in curl jq; do
    if ! command_exists "$cmd"; then
        log "❌ Error: $cmd is required but not installed"
        exit 1
    fi
done

# Check environment variables
for var in RENDER_API_KEY DATABASE_URL JWT_SECRET; do
    if [ -z "${!var}" ]; then
        log "⚠️  Warning: $var is not set"
        if [ "$var" = "JWT_SECRET" ] && [ -f .env ]; then
            # Try to get JWT_SECRET from .env
            JWT_SECRET=$(grep -E '^(JWT_SECRET|SECRET_KEY)=' .env | cut -d '=' -f2- | tr -d "'\"")
            if [ -n "$JWT_SECRET" ]; then
                log "ℹ️  Found $var in .env file"
                continue
            fi
        fi
        log "❌ Error: $var is required"
        exit 1
    fi
done

# API base URL
API_BASE="https://api.render.com/v1"

# Check if service exists
log "🔍 Checking if service '$SERVICE_NAME' exists..."
SERVICE_RESPONSE=$(curl -s -H "Authorization: Bearer $RENDER_API_KEY" \
    "$API_BASE/services?name=$SERVICE_NAME" 2>/dev/null)

SERVICE_ID=$(echo "$SERVICE_RESPONSE" | jq -r '.[0].service.id // empty')

if [ -n "$SERVICE_ID" ]; then
    log "🔄 Service '$SERVICE_NAME' found (ID: $SERVICE_ID), updating..."
    
    # Update existing service
    UPDATE_RESPONSE=$(curl -s -X PATCH "$API_BASE/services/$SERVICE_ID" \
        -H "Authorization: Bearer $RENDER_API_KEY" \
        -H "Content-Type: application/json" \
        -d @- <<EOF
{
    "autoDeploy": "yes",
    "envVars": [
        {"key":"DATABASE_URL","value":"$DATABASE_URL"},
        {"key":"JWT_SECRET","value":"$JWT_SECRET"},
        {"key":"FLASK_ENV","value":"production"}
    ]
}
EOF
    )
    
    if echo "$UPDATE_RESPONSE" | jq -e '.id' >/dev/null 2>&1; then
        log "✅ Service updated successfully"
    else
        log "❌ Failed to update service. Response:"
        echo "$UPDATE_RESPONSE" | jq .
        exit 1
    fi
else
    # Create new service
    log "🆕 Service '$SERVICE_NAME' not found, creating new service..."
    
    # Get owner ID from user endpoint
    OWNER_RESPONSE=$(curl -s -H "Authorization: Bearer $RENDER_API_KEY" \
        "$API_BASE/account" 2>/dev/null)
    OWNER_ID=$(echo "$OWNER_RESPONSE" | jq -r '.id // empty')
    
    if [ -z "$OWNER_ID" ]; then
        log "❌ Failed to get owner ID. Please check your API key"
        exit 1
    fi
    
    CREATE_RESPONSE=$(curl -s -X POST "$API_BASE/services" \
        -H "Authorization: Bearer $RENDER_API_KEY" \
        -H "Content-Type: application/json" \
        -d @- <<EOF
{
    "type": "web_service",
    "name": "$SERVICE_NAME",
    "ownerId": "$OWNER_ID",
    "repo": "$REPO_URL",
    "branch": "main",
    "region": "$REGION",
    "plan": "$PLAN",
    "buildCommand": "pip install -r requirements.txt && cd frontend && npm install && npm run build",
    "startCommand": "gunicorn app:app --preload --bind 0.0.0.0:\$PORT --workers 3",
    "envVars": [
        {"key":"DATABASE_URL","value":"$DATABASE_URL"},
        {"key":"JWT_SECRET","value":"$JWT_SECRET"},
        {"key":"FLASK_ENV","value":"production"}
    ]
}
EOF
    )
    
    SERVICE_ID=$(echo "$CREATE_RESPONSE" | jq -r '.id // empty')
    
    if [ -z "$SERVICE_ID" ]; then
        log "❌ Failed to create service. Response:"
        echo "$CREATE_RESPONSE" | jq .
        exit 1
    fi
    
    log "✅ Service created with ID: $SERVICE_ID"
fi

# Trigger deployment
log "🚀 Triggering deployment..."
DEPLOY_RESPONSE=$(curl -s -X POST "$API_BASE/services/$SERVICE_ID/deploys" \
    -H "Authorization: Bearer $RENDER_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"clearCache": "clear"}' 2>/dev/null)

DEPLOY_ID=$(echo "$DEPLOY_RESPONSE" | jq -r '.id // empty')

if [ -n "$DEPLOY_ID" ]; then
    DEPLOY_URL="https://dashboard.render.com/web/$SERVICE_ID/deploys/$DEPLOY_ID"
    log "✅ Deployment triggered successfully!"
    log "📊 Check deployment status at: $DEPLOY_URL"
    log "🌐 Your service will be available at: https://$SERVICE_NAME.onrender.com"
    
    # Simple health check
    log "⏳ Waiting for service to be healthy..."
    until curl -sSf "https://$SERVICE_NAME.onrender.com/health" >/dev/null 2>&1; do
        echo -n "."
        sleep 5
    done
    echo ""
    log "✅ Service is healthy!"
else
    log "❌ Failed to trigger deployment. Response:"
    echo "$DEPLOY_RESPONSE" | jq .
    exit 1
fi

log "
📋 Deployment Summary:"
log "🔗 Service URL: https://$SERVICE_NAME.onrender.com"
log "📊 Dashboard: https://dashboard.render.com/services/$SERVICE_ID/deploys"
log "
🔍 To verify the health of your backend, run:"
log "-----------------------------------------------------------"
log "until curl -sSf https://$SERVICE_NAME.onrender.com/health; do"
log "  echo \"⏳ Waiting for backend…\""
log "  sleep 5"
log "done"
log "echo \"🚀 Backend is live!\""
log "-----------------------------------------------------------"
echo "done"
echo "echo "🚀 Backend is live!""
echo "-----------------------------------------------------------"
