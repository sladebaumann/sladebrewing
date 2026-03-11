#!/usr/bin/env python3
"""
Enrich beers.json with data from Untappd API
This script fetches beer ratings, stats, and other details from Untappd
and merges them with your local beers.json file.

Setup:
1. Create an Untappd app at https://untappd.com/api
2. Set your credentials as environment variables:
   export UNTAPPD_CLIENT_ID="your_client_id"
   export UNTAPPD_CLIENT_SECRET="your_client_secret"
3. Run: python3 enrich_beers.py
"""

import json
import os
import re
import requests
from urllib.parse import urlparse, parse_qs

# Configuration
UNTAPPD_API_BASE = "https://api.untappd.com/v4"
CLIENT_ID = os.getenv("UNTAPPD_CLIENT_ID")
CLIENT_SECRET = os.getenv("UNTAPPD_CLIENT_SECRET")
BEERS_FILE = "beers.json"

# Default user agent (required by Untappd)
USER_AGENT = "Slade Brewing Website (CLIENT_ID)"


def extract_beer_id(untappd_url):
    """Extract the beer ID from an Untappd URL."""
    match = re.search(r'/b/[^/]+/(\d+)', untappd_url)
    if match:
        return match.group(1)
    return None


def fetch_beer_data(beer_id):
    """Fetch beer data from Untappd API."""
    if not CLIENT_ID or not CLIENT_SECRET:
        print("ERROR: UNTAPPD_CLIENT_ID and UNTAPPD_CLIENT_SECRET environment variables not set")
        print("See instructions at the top of this file.")
        return None
    
    url = f"{UNTAPPD_API_BASE}/beer/info/{beer_id}"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "compact": "true"  # Only return beer info, not full details
    }
    headers = {
        "User-Agent": USER_AGENT
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("response", {}).get("status") == 200:
            return data.get("response", {}).get("beer", {})
        else:
            print(f"WARNING: Untappd API returned status {data.get('response', {}).get('status')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"ERROR fetching data for beer {beer_id}: {e}")
        return None


def enrich_beers():
    """Load beers.json and enrich with Untappd data."""
    
    # Load existing beers
    with open(BEERS_FILE, 'r') as f:
        beers = json.load(f)
    
    print(f"Loaded {len(beers)} beers from {BEERS_FILE}")
    print("Fetching enriched data from Untappd API...\n")
    
    enriched_beers = {}
    
    for beer_name, beer_data in beers.items():
        print(f"Processing: {beer_name}")
        
        # Extract beer ID from Untappd URL
        untappd_url = beer_data.get("untappd")
        beer_id = extract_beer_id(untappd_url)
        
        if not beer_id:
            print(f"  ✗ Could not extract beer ID from URL: {untappd_url}")
            enriched_beers[beer_name] = beer_data
            continue
        
        # Fetch data from Untappd
        untappd_data = fetch_beer_data(beer_id)
        
        if untappd_data:
            # Merge data, keeping local data as primary
            enriched_data = {
                **beer_data,
                "untappd_id": beer_id,
                "rating": untappd_data.get("rating", 0),
                "ratingCount": untappd_data.get("rating_count", 0),
                "totalCheckins": untappd_data.get("total_checkins", 0),
                "totalUnique": untappd_data.get("total_user_count", 0),
                "abvUntappd": untappd_data.get("abv"),
                "ibuUntappd": untappd_data.get("ibu"),
                "styleUntappd": untappd_data.get("style"),
                "imageUrl": untappd_data.get("beer_label", ""),
            }
            enriched_beers[beer_name] = enriched_data
            print(f"  ✓ Rating: {untappd_data.get('rating', 'N/A')} ({untappd_data.get('rating_count', 0)} reviews)")
            print(f"  ✓ Checkins: {untappd_data.get('total_checkins', 0)}")
        else:
            # Keep original data if fetch fails
            enriched_beers[beer_name] = beer_data
            print(f"  ✗ Could not fetch Untappd data, keeping original data")
        
        print()
    
    # Save enriched data
    with open(BEERS_FILE, 'w') as f:
        json.dump(enriched_beers, f, indent=2)
    
    print(f"✓ Successfully enriched {BEERS_FILE}")
    print("\nNew fields added:")
    print("  - rating: Beer rating (0-5 scale)")
    print("  - ratingCount: Number of ratings")
    print("  - totalCheckins: Total check-ins on Untappd")
    print("  - totalUnique: Unique users who checked in")
    print("  - untappd_id: Beer ID from Untappd")
    print("  - imageUrl: Beer image from Untappd (as backup)")


if __name__ == "__main__":
    try:
        enrich_beers()
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        exit(1)
