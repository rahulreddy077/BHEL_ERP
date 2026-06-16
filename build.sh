#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Convert static assets
python backend/manage.py collectstatic --no-input

# Run migrations
python backend/manage.py migrate
