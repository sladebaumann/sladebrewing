# Slade Brewing Website - Hybrid Beer Data System

## Overview

This website uses a **hybrid approach** to manage beer data:
- **beers.json** contains the primary beer information (name, ABV, IBU, style, description, Untappd links)
- **enrich_beers.py** fetches additional data from the Untappd API (ratings, check-ins, popularity metrics)
- The frontend displays both your local data and enriched Untappd data

## Benefits of This Approach

1. **No Manual Sync** - You maintain control of your beer list locally
2. **Enriched Content** - Ratings, check-in counts, and social proof from Untappd
3. **Always Available** - Works even if Untappd API is temporarily down (uses cached data)
4. **Simple Updates** - Just run the enrichment script periodically to refresh metrics

## Setup Instructions

### Step 1: Create an Untappd API App

1. Go to [https://untappd.com/api](https://untappd.com/api)
2. Sign in with your account (create one if needed)
3. Click "Add App" to register a new application
4. Fill in the application details:
   - **App Name**: "Slade Brewing Website"
   - **App Description**: "Enriching our website with beer metrics"
   - **Redirect URL**: `http://localhost:8000` (for local testing)
5. After creation, you'll receive:
   - **Client ID** (your API Key)
   - **Client Secret**

### Step 2: Set Environment Variables

Store your Untappd credentials securely:

```bash
# On macOS/Linux, add to ~/.bash_profile or ~/.zshrc
export UNTAPPD_CLIENT_ID="your_client_id_here"
export UNTAPPD_CLIENT_SECRET="your_client_secret_here"

# Reload your shell
source ~/.bash_profile  # or ~/.zshrc
```

**For Windows (PowerShell):**
```powershell
[Environment]::SetEnvironmentVariable("UNTAPPD_CLIENT_ID", "your_client_id_here", "User")
[Environment]::SetEnvironmentVariable("UNTAPPD_CLIENT_SECRET", "your_client_secret_here", "User")
# Restart PowerShell after setting
```

### Step 3: Run the Enrichment Script

#### Option A: Manual Enrichment (Recommended for Local Development)

```bash
python3 enrich_beers.py
```

This will:
1. Read your `beers.json` file
2. Extract the Untappd beer IDs from the URLs
3. Fetch ratings, check-ins, and other metrics from Untappd
4. Update `beers.json` with the new data
5. Display a summary of what was added

#### Option B: Web Server with API Endpoint (For Production)

Start the local development server:

```bash
python3 server.py
```

Then you can:
- Visit http://localhost:8000 to browse your website
- GET http://localhost:8000/api/beers - View current beer data as JSON
- GET http://localhost:8000/api/enrich-beers - Trigger enrichment via API

## beers.json Structure

### Original Fields (maintained by you)
```json
{
  "Beer Name": {
    "description": "Your beer description",
    "logo": "images/untappd-logos/beer-image.png",
    "untappd": "https://untappd.com/b/slade-brewing-beer-name/BEER_ID",
    "abv": "5.1",
    "ibu": "30",
    "style": "Lager - American Pre-Prohibition",
    "releaseDate": "2025-11-07",
    "currentlyAvailable": true,
    "featured": false
  }
}
```

### Enriched Fields (added by enrich_beers.py)
```json
{
  "rating": 4.25,              // Untappd rating (0-5 scale)
  "ratingCount": 42,           // Number of ratings on Untappd
  "totalCheckins": 127,        // Total check-ins
  "totalUnique": 89,           // Unique users who checked in
  "untappd_id": "6483546",     // Beer ID from Untappd
  "imageUrl": "https://...",   // Beer label image from Untappd (backup)
  "abvUntappd": 5.1,          // Untappd's recorded ABV (may differ)
  "ibuUntappd": 30            // Untappd's recorded IBU (may differ)
}
```

## How It Works

### Enrichment Process

1. **Extract Beer IDs**: Parse Untappd URLs to get beer IDs
   ```
   https://untappd.com/b/slade-brewing-doe-brand/6483546
                                               ↑
                                            ID: 6483546
   ```

2. **API Call**: Fetch beer data from Untappd
   ```
   GET https://api.untappd.com/v4/beer/info/6483546?client_id=X&client_secret=Y
   ```

3. **Merge Data**: Add enriched fields to your `beers.json`

4. **Display**: Frontend shows ratings and check-ins on beer cards

### Frontend Display

The website automatically displays enriched data on beer cards:
- **Rating Stars**: Shows Untappd rating and review count
- **Check-ins Counter**: Shows total number of check-ins
- **View on Untappd**: Link to the beer's Untappd page

## Updating Your Beer Data

### To Add a New Beer

1. Edit `beers.json` and add the new beer with basic info:
   ```json
   "New Beer": {
     "description": "...",
     "logo": "images/untappd-logos/new-beer.png",
     "untappd": "https://untappd.com/b/slade-brewing-new-beer/BEER_ID",
     "abv": "5.5",
     "ibu": "35",
     "style": "IPA",
     "releaseDate": "2026-03-01",
     "currentlyAvailable": true,
     "featured": false
   }
   ```

2. Run the enrichment script:
   ```bash
   python3 enrich_beers.py
   ```

### To Update Metrics

Run the enrichment script periodically to refresh all metrics:
```bash
python3 enrich_beers.py
```

**Recommendation**: Set up a cron job (macOS/Linux) or scheduled task (Windows) to run this daily or weekly.

#### Cron Job Example (macOS/Linux)

```bash
# Open crontab editor
crontab -e

# Add this line to run enrichment daily at 2 AM
0 2 * * * cd /path/to/sladebrewing && python3 enrich_beers.py >> enrich.log 2>&1
```

## Troubleshooting

### Error: "UNTAPPD_CLIENT_ID and UNTAPPD_CLIENT_SECRET environment variables not set"

**Solution**: Check that your environment variables are set:
```bash
echo $UNTAPPD_CLIENT_ID
echo $UNTAPPD_CLIENT_SECRET
```

If empty, set them again and reload your terminal.

### Error: "Could not extract beer ID from URL"

**Solution**: Ensure your Untappd URLs are correct format:
- ✅ Correct: `https://untappd.com/b/slade-brewing-beer-name/6483546`
- ❌ Wrong: `https://untappd.com/beer/6483546` (missing brewery slug)

### Script Times Out or Fails

**Solution**: Check your internet connection and Untappd API status.
- Untappd has a rate limit of **100 calls/hour** per API key
- With 3 beers, each enrichment uses 3 API calls
- If you have many beers, you may need to wait or request higher limits

### Ratings Don't Show Up

**Possible reasons**:
1. The beer has no ratings yet on Untappd
2. The beer was just added to Untappd (needs time to accumulate ratings)
3. Your local beer name doesn't match Untappd's exactly

**Solution**: Check the beer on Untappd.com directly to verify ratings exist.

## File Structure

```
sladebrewing/
├── beers.json                 # Your beer data (local primary source)
├── enrich_beers.py            # Enrichment script
├── server.py                  # Development web server
├── index.html                 # Homepage
├── news.html                  # News/blog page
├── assets/
│   ├── css/
│   │   └── style.css          # Includes styles for enriched data
│   └── js/
│       └── script.js          # Loads and displays enriched data
└── images/
    ├── Slade Brewing - Main Logo.png
    ├── engin-akyurt-3ORoQEJY9LA-unsplash.jpg
    └── untappd-logos/
        ├── Doe Brand - Pre-Prohibition Lager Untappd Image.png
        ├── Wild n' Mild Untappd Image.png
        └── Sparkle Pants Witbier Untappd Image.png
```

## API Rate Limits

Untappd API has a **100 calls/hour limit** per API key. Since each beer enrichment uses 1 API call:
- 3 beers = 3 calls (well within limit)
- 20 beers = 20 calls (still fine)
- 100+ beers = approaching limit (consider batching or requesting higher limits from Untappd)

## Future Enhancements

Possible improvements to this system:

1. **Admin Dashboard** - Web UI to manage beers without editing JSON
2. **Database Backend** - Store beer data in a database instead of JSON
3. **Webhook Integration** - Auto-refresh when beers are updated on Untappd
4. **Beer Reviews** - Display recent Untappd reviews on your site
5. **Analytics** - Track which beers are most checked-in
6. **Caching** - Store enriched data with TTL to reduce API calls

## Questions or Issues?

For problems with this setup, check:
1. **Untappd Docs**: https://untappd.com/api/docs
2. **Your Untappd App Dashboard**: https://untappd.com/api
3. **API Explorer**: https://untappd.com/api/explorer (test API calls)

---

**Happy brewing!** 🍺
