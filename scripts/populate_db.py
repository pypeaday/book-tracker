#!/usr/bin/env python3
from datetime import datetime, timedelta
import httpx
import asyncio

# Sample books with interesting notes
books = [
    {
        "title": "Project Hail Mary",
        "author": "Andy Weir",
        "status": "completed",
        "notes": "Fascinating exploration of interstellar science. The Astrophage concept was mind-blowing!",
        "start_date": (datetime.now() - timedelta(days=60)).isoformat(),
        "completion_date": (datetime.now() - timedelta(days=30)).isoformat(),
        "rating": 3  # Would recommend
    },
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "status": "reading",
        "notes": "The world-building is incredible. Currently in the middle of Paul's journey through the desert. Loving it so far!",
        "start_date": (datetime.now() - timedelta(days=15)).isoformat(),
        "rating": 3  # Would recommend based on current progress
    },
    {
        "title": "The Three-Body Problem",
        "author": "Cixin Liu",
        "status": "to_read",
        "notes": "Heard great things about this hard sci-fi masterpiece. Planning to start after Dune."
        # No rating for unread books
    },
    {
        "title": "Foundation",
        "author": "Isaac Asimov",
        "status": "completed",
        "notes": "A masterclass in large-scale sci-fi storytelling. Psychohistory is such an intriguing concept.",
        "start_date": (datetime.now() - timedelta(days=120)).isoformat(),
        "completion_date": (datetime.now() - timedelta(days=90)).isoformat(),
        "rating": 2  # Good but not recommendable
    },
    {
        "title": "The Name of the Wind",
        "author": "Patrick Rothfuss",
        "status": "on_hold",
        "notes": "Beautiful prose, but waiting for the third book before continuing. What I've read so far is excellent.",
        "start_date": (datetime.now() - timedelta(days=180)).isoformat(),
        "rating": 2  # Good but hard to recommend due to unfinished series
    },
    {
        "title": "Snow Crash",
        "author": "Neal Stephenson",
        "status": "dnf",
        "notes": "Interesting concepts but couldn't get into the writing style after 100 pages.",
        "start_date": (datetime.now() - timedelta(days=45)).isoformat(),
        "rating": 0  # So bad I didn't finish
    },
    {
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "status": "reading",
        "notes": "Hilarious! Don't forget your towel. The humor is exactly my style.",
        "start_date": (datetime.now() - timedelta(days=5)).isoformat(),
        "rating": 1  # Wouldn't read again
    },
    {
        "title": "Neuromancer",
        "author": "William Gibson",
        "status": "to_read",
        "notes": "Classic cyberpunk novel that coined the term 'cyberspace'. High on my TBR list."
        # No rating for unread books
    },
    {
        "title": "The Left Hand of Darkness",
        "author": "Ursula K. Le Guin",
        "status": "completed",
        "notes": "A profound exploration of gender and society. The winter journey sequence was particularly moving.",
        "start_date": (datetime.now() - timedelta(days=90)).isoformat(),
        "completion_date": (datetime.now() - timedelta(days=60)).isoformat(),
        "rating": 3  # Would recommend
    },
    {
        "title": "The Way of Kings",
        "author": "Brandon Sanderson",
        "status": "reading",
        "notes": "Epic fantasy with incredible world-building. The Stormlight magic system is fascinating.",
        "start_date": (datetime.now() - timedelta(days=20)).isoformat(),
        "rating": 3  # Would recommend based on current progress
    }
]

async def populate_db():
    # API endpoint
    base_url = "http://localhost:8082/api"
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            # Get existing books
            response = await client.get(f"{base_url}/books/")
            response.raise_for_status()
            existing_books = response.json()
            
            # Delete existing books
            for book in existing_books:
                response = await client.delete(f"{base_url}/books/{book['id']}")
                response.raise_for_status()
                print(f"Deleted book: {book['title']}")
            
            # Add new books
            for book in books:
                response = await client.post(
                    f"{base_url}/books/",
                    json=book
                )
                response.raise_for_status()
                print(f"Added book: {book['title']}")
            
            print(f"\nSuccessfully added {len(books)} sample books!")
            
        except httpx.HTTPError as e:
            print(f"Error: {e}")
            print("Make sure the application is running on http://localhost:8082")

if __name__ == "__main__":
    asyncio.run(populate_db())
