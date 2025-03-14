# Book Tracking - Developer Guide

This document contains technical information for developers working on the Book Tracking application.

## Technology Stack

- Backend: FastAPI with SQLite database
- Frontend: HTMX + Tailwind CSS
- Templates: Jinja2

## Setup Options

### Using Docker (Recommended)

#### 1. Using Docker Compose:
```bash
# Build and start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

The application will be available at `http://localhost:8082` (mapped from port 8000 inside the container)

#### 2. Using Docker directly:
```bash
# Build the image
docker build -t book-tracker .

# Run the container
docker run -d \
  -p 8082:8000 \
  -v book_tracking_data:/app/data \
  -e DATABASE_URL=sqlite:///data/books.db \
  -e ADMIN_EMAIL=admin@example.com \
  -e ADMIN_PASSWORD=adminpassword \
  --name book-tracker \
  book-tracker
```

The application will be available at `http://localhost:8082` (mapped from port 8000 inside the container)

### Local Development Setup

1. Create and activate a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload --port 8082 --host 0.0.0.0
```

The application will be available at `http://localhost:8082`

## Environment Variables

You can customize the application behavior using the following environment variables:
- `DATABASE_URL`: Database connection string (default: sqlite:///data/books.db)
- `ADMIN_EMAIL`: Custom email for the admin user (default: admin@example.com)
- `ADMIN_PASSWORD`: Custom password for the admin user (default: adminpassword)

## Loading Sample Data

To populate the database with sample books for the admin user:

1. First, make sure the application is running:
```bash
uvicorn app.main:app --reload --port 8082 --host 0.0.0.0
```

2. Then in another terminal, run the populate script:
```bash
# Make sure your virtual environment is activated first
source venv/bin/activate  # On Linux/Mac

# Install dependencies if needed
pip install -r requirements.txt

# Run the populate script (uses default admin credentials)
python scripts/populate_db.py

# Or specify custom admin credentials
python scripts/populate_db.py --email admin@example.com --password adminpassword
```

This will add 10 sample books across different reading statuses with notes and dates.

The script uses the application's API endpoints, so it requires the app to be running at http://localhost:8082. It will:
1. Log in as the admin user
2. Delete any existing books for that user
3. Add the sample books to the admin's collection

## Development Notes

The application uses:
- HTMX for dynamic content updates without page reloads
- Tailwind CSS for styling
- SQLite database for data storage
- Jinja2 templates for server-side rendering

No build process required - just run the server and start developing!