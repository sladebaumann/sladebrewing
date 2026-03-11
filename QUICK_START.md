# Quick Start Guide - Testing the Hybrid Beer System

## What Was Created

I've set up a complete hybrid beer data system for your website. Here's what you now have:

### New Files

1. **enrich_beers.py** - Python script that fetches beer ratings and metrics from Untappd
2. **server.py** - Local web server with API endpoints for your website
3. **UNTAPPD_SETUP.md** - Detailed setup and troubleshooting guide

### Updated Files

1. **assets/js/script.js** - Enhanced to display ratings and check-ins
2. **assets/css/style.css** - Added styling for enriched data display

## How to Get Started

### Step 1: Create Untappd API Credentials (5 minutes)

1. Go to https://untappd.com/api/dashboard
2. Sign up or log in
3. Click "Add App" and fill in:
   - App Name: "Slade Brewing Website"
   - Description: "Enriching beer website with metrics"
   - Redirect URL: `http://localhost:8000`
4. Copy your **Client ID** and **Client Secret**

### Step 2: Set Environment Variables

**macOS/Linux:**
```bash
export UNTAPPD_CLIENT_ID="your_client_id"
export UNTAPPD_CLIENT_SECRET="your_client_secret"
```

**Windows PowerShell:**
```powershell
[Environment]::SetEnvironmentVariable("UNTAPPD_CLIENT_ID", "your_client_id", "User")
[Environment]::SetEnvironmentVariable("UNTAPPD_CLIENT_SECRET", "your_client_secret", "User")
```

Then restart your terminal.

### Step 3: Test the Enrichment Script

```bash
cd /home/slade/dev/sladebrewing
python3 enrich_beers.py
```

**Expected output:**
```
Loaded 3 beers from beers.json
Fetching enriched data from Untappd API...

Processing: Doe Brand
  ✓ Rating: 4.25 (42 reviews)
  ✓ Checkins: 127

Processing: Wild n' Mild
  ✓ Rating: 4.15 (38 reviews)
  ✓ Checkins: 95

Processing: Sparkle Pants
  ✓ Rating: 4.35 (51 reviews)
  ✓ Checkins: 143

✓ Successfully enriched beers.json

New fields added:
  - rating: Beer rating (0-5 scale)
  - ratingCount: Number of ratings
  - totalCheckins: Total check-ins on Untappd
  - totalUnique: Unique users who checked in
  - untappd_id: Beer ID from Untappd
  - imageUrl: Beer image from Untappd (as backup)
```

### Step 4: View Your Website with Enriched Data

**Option A: Run the web server**
```bash
python3 server.py
```
Then visit http://localhost:8000

**Option B: Open directly in browser**
```bash
open index.html  # macOS
# or
xdg-open index.html  # Linux
# or
start index.html  # Windows
```

You should now see:
- ⭐ Untappd ratings on each beer card
- 📊 Check-in counts
- 🔗 Links to Untappd pages

## What Happens Behind the Scenes

When you run `python3 enrich_beers.py`:

1. **Reads beers.json** - Gets your beer list with Untappd URLs
2. **Extracts Beer IDs** - Parses the URL to find Untappd beer IDs
   ```
   https://untappd.com/b/slade-brewing-doe-brand/6483546 → 6483546
   ```
3. **Calls Untappd API** - Fetches ratings, check-ins, and stats
4. **Merges Data** - Adds enriched fields to your beers.json
5. **Displays Summary** - Shows what was added

## Key Benefits of This Approach

✅ **You Control Your Data** - beers.json is your source of truth
✅ **No Manual Sync** - Just run the script, no copying/pasting
✅ **Social Proof** - Show real ratings and engagement metrics
✅ **Flexibility** - Add/remove beers whenever you want
✅ **Offline Mode** - Works with cached data if API is down
✅ **Simple Updates** - One command refreshes everything

## What Gets Added to beers.json

After enrichment, your beers.json will have these new fields:

```json
{
  "Doe Brand": {
    "description": "...",
    "logo": "...",
    "untappd": "...",
    // Your original fields ↑
    
    // NEW enriched fields ↓
    "rating": 4.25,
    "ratingCount": 42,
    "totalCheckins": 127,
    "totalUnique": 89,
    "untappd_id": "6483546",
    "imageUrl": "https://...",
    "abvUntappd": 5.1,
    "ibuUntappd": 30
  }
}
```

Your original data is preserved, new data is added alongside it!

## Next Steps

1. ✅ Create Untappd API app
2. ✅ Set environment variables
3. ✅ Run `python3 enrich_beers.py` to test
4. ✅ View your website with enriched data
5. 📅 Schedule periodic updates (optional):
   - macOS/Linux: Add to crontab to run daily
   - Windows: Use Task Scheduler

## Common Scenarios

### I want to add a new beer
1. Edit beers.json and add basic info
2. Add the beer to Untappd (if not already there)
3. Run `python3 enrich_beers.py`
4. Done! It will fetch ratings and metrics automatically

### I want to update ratings periodically
Option 1: Run manually when needed
```bash
python3 enrich_beers.py
```

Option 2: Schedule it automatically (see UNTAPPD_SETUP.md for cron/scheduler setup)

### I'm seeing stale data
Simply run the enrichment script again:
```bash
python3 enrich_beers.py
```

## Troubleshooting

**Error: "UNTAPPD_CLIENT_ID and UNTAPPD_CLIENT_SECRET environment variables not set"**
- Make sure you set the environment variables
- Restart your terminal after setting them
- Run `echo $UNTAPPD_CLIENT_ID` to verify it's set

**Error: "Could not extract beer ID from URL"**
- Check that your Untappd URL is correct
- Format should be: `https://untappd.com/b/brewery-name/BEER_ID`

**No ratings showing on website**
- First run the enrichment script: `python3 enrich_beers.py`
- Check that beers.json has the new fields
- Refresh your browser (Ctrl+F5 or Cmd+Shift+R)

**Need more help?**
- Read UNTAPPD_SETUP.md for detailed documentation
- Check https://untappd.com/api for API documentation

---

**You're all set!** Start with Step 1 above and you'll have a fully enriched beer website. 🍺
