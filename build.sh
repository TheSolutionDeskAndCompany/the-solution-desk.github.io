#!/bin/bash
# Exit on error
set -e

# Default Python version if not specified
PYTHON_VERSION=${PYTHON_VERSION:-3.11.6}
PYTHON_CMD=python3

# Determine Python command based on version
if [ -f "/opt/render/project/src/.python-version" ]; then
    PYTHON_CMD="$(cat /opt/render/project/src/.python-version | xargs which python3)"
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD=python3.11
elif command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    echo "Python 3.6+ is required"
    exit 1
fi

echo "-----> Using $($PYTHON_CMD --version)"

# Install pip if not already installed
if ! command -v pip3 &> /dev/null; then
    echo "-----> Installing pip"
    curl -sS https://bootstrap.pypa.io/get-pip.py | $PYTHON_CMD
fi

# Upgrade pip
$PYTHON_CMD -m pip install --upgrade pip

# Install dependencies
echo "-----> Installing dependencies"
$PYTHON_CMD -m pip install -r requirements.txt

# Install the package in development mode
if [ -f "setup.py" ]; then
    $PYTHON_CMD -m pip install -e .
fi

# Run database migrations if needed
if [ -d "migrations" ]; then
    echo "-----> Running database migrations"
    export FLASK_APP=app.py
    $PYTHON_CMD -m flask db upgrade
fi

echo "-----> Build completed successfully"
