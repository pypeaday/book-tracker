#!/usr/bin/env python3
from datetime import datetime, timedelta
import httpx
import asyncio
import argparse
import os

# Admin credentials (can be overridden with command line arguments)
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "adminpassword")

# Sample books with interesting notes
books = [
    {
        "title": "Project Hail Mary",
        "author": "Andy Weir",
        "status": "completed",
        "notes": "Fascinating exploration of interstellar science. The Astrophage concept was mind-blowing!",
        "start_date": (datetime.now() - timedelta(days=60)).isoformat(),
        "completion_date": (datetime.now() - timedelta(days=30)).isoformat(),
        "rating": 3,  # Would recommend
    },
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "status": "reading",
        "notes": "The world-building is incredible. Currently in the middle of Paul's journey through the desert. Loving it so far!",
        "start_date": (datetime.now() - timedelta(days=15)).isoformat(),
        "rating": 3,  # Would recommend based on current progress
    },
    {
        "title": "The Three-Body Problem",
        "author": "Cixin Liu",
        "status": "to_read",
        "notes": "Heard great things about this hard sci-fi masterpiece. Planning to start after Dune.",
        # No rating for unread books
    },
    {
        "title": "Foundation",
        "author": "Isaac Asimov",
        "status": "completed",
        "notes": "A masterclass in large-scale sci-fi storytelling. Psychohistory is such an intriguing concept.",
        "start_date": (datetime.now() - timedelta(days=120)).isoformat(),
        "completion_date": (datetime.now() - timedelta(days=90)).isoformat(),
        "rating": 2,  # Good but not recommendable
    },
    {
        "title": "The Name of the Wind",
        "author": "Patrick Rothfuss",
        "status": "on_hold",
        "notes": "Beautiful prose, but waiting for the third book before continuing. What I've read so far is excellent.",
        "start_date": (datetime.now() - timedelta(days=180)).isoformat(),
        "rating": 2,  # Good but hard to recommend due to unfinished series
    },
    {
        "title": "Snow Crash",
        "author": "Neal Stephenson",
        "status": "dnf",
        "notes": "Interesting concepts but couldn't get into the writing style after 100 pages.",
        "start_date": (datetime.now() - timedelta(days=45)).isoformat(),
        "rating": 0,  # So bad I didn't finish
    },
    {
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "status": "reading",
        "notes": "Hilarious! Don't forget your towel. The humor is exactly my style.",
        "start_date": (datetime.now() - timedelta(days=5)).isoformat(),
        "rating": 1,  # Wouldn't read again
    },
    {
        "title": "Neuromancer",
        "author": "William Gibson",
        "status": "to_read",
        "notes": "Classic cyberpunk novel that coined the term 'cyberspace'. High on my TBR list.",
        # No rating for unread books
    },
    {
        "title": "The Left Hand of Darkness",
        "author": "Ursula K. Le Guin",
        "status": "completed",
        "notes": "A profound exploration of gender and society. The winter journey sequence was particularly moving.",
        "start_date": (datetime.now() - timedelta(days=90)).isoformat(),
        "completion_date": (datetime.now() - timedelta(days=60)).isoformat(),
        "rating": 3,  # Would recommend
    },
    {
        "title": "The Way of Kings",
        "author": "Brandon Sanderson",
        "status": "reading",
        "notes": "Epic fantasy with incredible world-building. The Stormlight magic system is fascinating.",
        "start_date": (datetime.now() - timedelta(days=20)).isoformat(),
        "rating": 3,  # Would recommend based on current progress
    },
]


async def login_admin(client, base_url, email, password):
    """Login as admin and return the access token"""
    print(f"Logging in as {email}...")

    # Get token using the token endpoint
    response = await client.post(
        f"{base_url}/token",
        data={"username": email, "password": password},  # OAuth2 expects username field
    )
    response.raise_for_status()
    token_data = response.json()

    print(f"Successfully logged in as {email}")
    return token_data["access_token"]


async def populate_db(
    email=ADMIN_EMAIL, password=ADMIN_PASSWORD, base_url="http://localhost:8082"
):
    """Populate the database with sample books for the admin user"""
    api_url = f"{base_url}/api"

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            # Login as admin to get token
            token = await login_admin(client, base_url, email, password)

            # Set authorization header for all subsequent requests
            headers = {"Authorization": f"Bearer {token}"}

            # Get existing books for the admin user
            response = await client.get(f"{api_url}/books/", headers=headers)
            response.raise_for_status()
            existing_books = response.json()

            # Delete existing books
            for book in existing_books:
                response = await client.delete(
                    f"{api_url}/books/{book['id']}", headers=headers
                )
                response.raise_for_status()
                print(f"Deleted book: {book['title']}")

            # Add new books
            for book in books:
                response = await client.post(
                    f"{api_url}/books/", json=book, headers=headers
                )
                response.raise_for_status()
                print(f"Added book: {book['title']}")

            print(f"\nSuccessfully added {len(books)} sample books for {email}!")

        except httpx.HTTPError as e:
            print(f"Error: {e}")
            print(f"Make sure the application is running on {base_url}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Populate the database with sample books for the admin user"
    )
    parser.add_argument(
        "--email", default=ADMIN_EMAIL, help=f"Admin email (default: {ADMIN_EMAIL})"
    )
    parser.add_argument(
        "--password",
        default=ADMIN_PASSWORD,
        help=f"Admin password (default: {ADMIN_PASSWORD})",
    )
    parser.add_argument(
        "--url",
        default="http://localhost:8082",
        help="Base URL of the application (default: http://localhost:8082)",
    )

    args = parser.parse_args()

    asyncio.run(populate_db(args.email, args.password, args.url))
