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

## Project Setup

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
