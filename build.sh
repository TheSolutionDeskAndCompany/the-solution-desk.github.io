#!/bin/bash
# Exit on error
set -e

echo "-----> Starting build process"

# Set Python version (should match runtime.txt)
PYTHON_VERSION=3.11.4
echo "-----> Using Python ${PYTHON_VERSION}"

# Install Python version if not already installed
echo "-----> Setting up Python ${PYTHON_VERSION}"
apt-get update && apt-get install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-dev

# Set Python command
PYTHON_CMD=python${PYTHON_VERSION}

# Ensure pip is installed
echo "-----> Ensuring pip is installed"
if ! command -v ${PYTHON_CMD} -m pip &> /dev/null; then
    echo "-----> Installing pip"
    curl -sS https://bootstrap.pypa.io/get-pip.py | ${PYTHON_CMD}
fi

# Upgrade pip
echo "-----> Upgrading pip"
${PYTHON_CMD} -m pip install --upgrade pip

# Install dependencies
echo "-----> Installing dependencies"
${PYTHON_CMD} -m pip install -r requirements.txt

# Install the package in development mode
if [ -f "setup.py" ]; then
    echo "-----> Installing application in development mode"
    ${PYTHON_CMD} -m pip install -e .
fi

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=production

# Run database migrations if needed
if [ -d "migrations" ]; then
    echo "-----> Running database migrations"
    ${PYTHON_CMD} -m flask db upgrade
fi

echo "-----> Build completed successfully"
