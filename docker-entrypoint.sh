#!/bin/sh

# Create data directory if it doesn't exist
mkdir -p /app/data

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
