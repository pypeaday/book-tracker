#!/usr/bin/env python3
"""
Script to create a default admin user for the Book Tracking application.
This script can be used standalone or during container startup.

Environment variables:
- ADMIN_EMAIL: Email for the admin user (default: admin@example.com)
- ADMIN_PASSWORD: Password for the admin user (default: adminpassword)
"""

import os
import sys
from datetime import datetime
from sqlalchemy.orm import Session

# Get admin credentials from environment variables or use defaults
EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
PASSWORD = os.environ.get("ADMIN_PASSWORD", "adminpassword")

# Import app modules
try:
    from app.database import SessionLocal
    from app.models import User
    from app.auth import get_password_hash
except ImportError:
    # If running from a different directory, add the app directory to the path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from app.database import SessionLocal
    from app.models import User
    from app.auth import get_password_hash


def create_default_admin(quiet=False):
    """
    Create a default admin user with the given email and password.

    Args:
        quiet (bool): If True, suppress output messages

    Returns:
        bool: True if admin was created or updated successfully, False otherwise
    """
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == EMAIL).first()
        if existing_user:
            if not quiet:
                print(f"User with email {EMAIL} already exists.")

            # If user exists but is not admin, update role to admin
            if existing_user.role != "admin":
                existing_user.role = "admin"
                db.commit()
                if not quiet:
                    print(f"Updated user {EMAIL} to admin role.")
            else:
                if not quiet:
                    print(f"User {EMAIL} is already an admin.")

            return True

        # Create new admin user
        hashed_password = get_password_hash(PASSWORD)
        new_user = User(
            email=EMAIL,
            hashed_password=hashed_password,
            is_active=True,
            created_at=datetime.utcnow(),
            role="admin",
        )

        db.add(new_user)
        db.commit()
        if not quiet:
            print(f"Default admin user created successfully!")
            print(f"Login with: {EMAIL} / {PASSWORD}")

        return True

    except Exception as e:
        db.rollback()
        if not quiet:
            print(f"Error creating admin user: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    # Parse command line arguments
    import argparse

    parser = argparse.ArgumentParser(description="Create a default admin user")
    parser.add_argument("--quiet", action="store_true", help="Suppress output messages")
    parser.add_argument("--email", help="Override the admin email")
    parser.add_argument("--password", help="Override the admin password")

    args = parser.parse_args()

    # Override defaults if provided
    if args.email:
        EMAIL = args.email
    if args.password:
        PASSWORD = args.password

    success = create_default_admin(quiet=args.quiet)
    sys.exit(0 if success else 1)
