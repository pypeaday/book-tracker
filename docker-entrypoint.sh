#!/bin/sh

# Create data directory if it doesn't exist
mkdir -p /app/data
chmod 777 /app/data

# Ensure database tables are created
echo "Initializing database..."
python -c '
from app.database import engine
from app.models import Base
Base.metadata.create_all(bind=engine)
print("Database tables created successfully")
'

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Create default admin user
echo "Creating default admin user..."
python create_default_admin.py

# Start the application
echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
