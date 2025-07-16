#!/bin/bash
# Exit on error
set -e

# Install the specified Python version
echo "-----> Installing Python 3.11.14"
python3.11 --version

# Install pip
echo "-----> Installing pip"
curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py

# Install dependencies
echo "-----> Installing dependencies"
pip install -r requirements.txt

# Run database migrations if needed
echo "-----> Running database migrations"
flask db upgrade

echo "-----> Build completed successfully"
