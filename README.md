# Book Tracking

I replaced this with [great-reads](https://www.github.com/pypeaday/great-reads)


## What is Book Tracking?

Book Tracking helps you organize your reading life by keeping track of books you want to read, are currently reading, or have finished. With an intuitive interface designed to work on both desktop and mobile devices, you can manage your entire book collection from anywhere.

## Features

### Track Your Reading Journey
- **Multiple Reading Statuses**: Organize books as "To Read," "Currently Reading," "Completed," "On Hold," or "Did Not Finish"
- **Reading Progress**: Record when you start and finish books
- **Personal Notes**: Add thoughts and reflections for each book

### User-Friendly Experience
- **Mobile-Optimized**: Use on any device with a responsive design
- **Real-Time Updates**: Changes appear instantly without page reloads
- **Easy Organization**: Drag and drop books between different status categories
- **Quick Search**: Find books in your collection instantly
- **Clean Design**: Enjoy a modern, distraction-free interface

## Getting Started

### Installation

The easiest way to run Book Tracking is with Docker:

```bash
# Start the application
docker compose up -d
```

The application will be available at `http://localhost:8080`

*For developers: See [DEVELOPER.md](DEVELOPER.md) for detailed setup instructions and technical information.*

### Creating an Account

1. Visit `http://localhost:8080` in your browser
2. Click "Register" and create your account
3. Log in with your new credentials

### Adding Books

1. After logging in, click the "+" button to add a new book
2. Enter the book title, author, and select a status
3. Optionally add notes or dates
4. Click "Save" to add the book to your collection

### Managing Your Books

- **Change Status**: Drag books between status columns or use the edit button
- **Add Notes**: Click on a book to add thoughts or reflections
- **Track Progress**: Update start and completion dates as you read
- **Search**: Use the search bar to quickly find books in your collection

## Admin Access

A default admin account is created when you first run the application:
- Email: admin@example.com
- Password: adminpassword

The admin dashboard (accessible at `/admin/dashboard`) allows you to:
- Manage users
- View system statistics
- Access book usage analytics

*Note: For security in production environments, change the default admin credentials using environment variables.*

## Sample Data

Want to see how the app works with books already added? Run:

```bash
python scripts/populate_db.py
```

This adds sample books across different reading statuses to the admin account.

## Need Help?

For technical issues or development questions, please refer to [DEVELOPER.md](DEVELOPER.md) or open an issue on our repository.

Happy reading!
