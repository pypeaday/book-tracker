# Book Tracking

A modern, mobile-friendly application to track your reading progress and manage your book collection. Built with FastAPI and HTMX for a smooth, interactive experience.

## Features

Track books with different statuses:
- To Read
- Currently Reading
- Completed
- On Hold
- Did Not Finish (DNF)

### User Experience
- Mobile-optimized interface
- Real-time updates without page reloads
- Easy drag-and-drop organization
- Instant search and filtering
- Undo/redo actions
- Clean, modern design

## Technology Stack

- Backend: FastAPI with SQLite database
- Frontend: HTMX + Tailwind CSS
- Templates: Jinja2

## Setup

### Using Docker (Recommended)

1. Using Docker Compose:
```bash
# Build and start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

The application will be available at `http://localhost:8082` (mapped from port 8000 inside the container)

2. Using Docker directly:
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

### Admin User

A default admin user is automatically created when the application starts:
- Email: admin@example.com
- Password: adminpassword

You can customize the admin credentials by setting the following environment variables:
- `ADMIN_EMAIL`: Custom email for the admin user
- `ADMIN_PASSWORD`: Custom password for the admin user

The admin dashboard is accessible at `/admin/dashboard` after logging in with admin credentials.

Admin features include:
- User management (view, activate/deactivate, change roles)
- System statistics
- Book usage analytics

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

### Loading Sample Data

To populate the database with sample books:

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

# Run the populate script
python scripts/populate_db.py
```

This will add 10 sample books across different reading statuses with notes and dates, including:
- Currently reading books (Dune, The Way of Kings)
- Completed books with reviews
- Books on the to-read list
- Books on hold or DNF with explanations

The script uses the application's API endpoints, so it requires the app to be running at http://localhost:8082.

## Features

### Book Management
- Add new books with title, author, and status
- Track reading progress with start and completion dates
- Add personal notes and thoughts
- Organize books by reading status
- Quick edit and delete options

### User Interface
- Responsive grid layout
- Status-based organization
- Hover actions for quick edits
- Toast notifications for actions
- Form validation and error handling

## Development

The application uses:
- HTMX for dynamic content updates
- Tailwind CSS for styling
- SQLite database for data storage
- Jinja2 templates for server-side rendering

No build process required - just run the server and start using the application!
