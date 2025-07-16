#!/bin/bash

# Check if RENDER_API_KEY is set
if [ -z "$RENDER_API_KEY" ]; then
  echo "⛔ Error: RENDER_API_KEY environment variable is not set"
  echo "Please set it using: export RENDER_API_KEY='your-api-key'"
  exit 1
fi

# Get the service ID for thesolutiondesk
RESPONSE_FILE="render_services_response.json"
curl -s -H "Authorization: Bearer $RENDER_API_KEY" \
  https://api.render.com/v1/services -o "$RESPONSE_FILE"

if [ ! -s "$RESPONSE_FILE" ]; then
  echo "❌ Failed to get response from Render API. Please check your API key and network connection."
  exit 1
fi

SERVICE_ID=$(jq -r '.[] | select(.name=="thesolutiondesk") | .id' "$RESPONSE_FILE" 2>/dev/null)

if [ -z "$SERVICE_ID" ]; then
  echo "❌ Failed to get service ID for 'thesolutiondesk'. Possible reasons:"
  echo "  1. Service 'thesolutiondesk' doesn't exist yet"
  echo "  2. Invalid API response format"
  echo "  3. API key doesn't have permission"
  echo "Response saved to $RESPONSE_FILE for inspection"
  exit 1
fi

echo "✅ Service ID: $SERVICE_ID"

# Get the latest deploy ID
DEPLOY_ID=$(curl -s -H "Authorization: Bearer $RENDER_API_KEY" \
  "https://api.render.com/v1/services/$SERVICE_ID/deploys?limit=1" | \
  jq -r '.deploys[0].id')

if [ -z "$DEPLOY_ID" ]; then
  echo "❌ Failed to get deploy ID for service $SERVICE_ID"
  exit 1
fi

echo "✅ Latest Deploy ID: $DEPLOY_ID"

echo "Fetching build logs..."
curl -s -H "Authorization: Bearer $RENDER_API_KEY" \
  "https://api.render.com/v1/services/$SERVICE_ID/deploys/$DEPLOY_ID/events?type=LOG" | \
  jq -r '.events[].message' > render-build.log

echo "Logs saved to render-build.log"

echo "Scanning for errors..."
grep -Ei "(error|fail)" render-build.log | head -n 20
