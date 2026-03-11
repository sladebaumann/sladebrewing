# Slade Brewing Website - Beer Management with Admin Panel

## Overview

Since Untappd has restricted API access, you now have a **simple admin panel** to manage your beers.json file directly through a web interface. No more manual JSON editing!

## Key Features

✅ **Easy Beer Management** - Add, edit, and delete beers through a web interface
✅ **No Manual Editing** - No need to touch JSON files directly
✅ **Real-time Updates** - Changes appear on your website immediately
✅ **Data Validation** - Required fields are enforced
✅ **Duplicate Prevention** - Can't accidentally add the same beer twice
✅ **Mobile Friendly** - Admin panel works on phones and tablets

## Quick Start

### 1. Start the Server

```bash
cd /home/slade/dev/sladebrewing
python3 server.py
```

### 2. Access the Admin Panel

Open your browser to: **http://localhost:8000/admin**

### 3. Manage Your Beers

**To Add a Beer:**
1. Fill in the form on the left
2. Click "Save Beer"
3. The beer appears in the list immediately
4. Refresh your main website to see it

**To Edit a Beer:**
1. Click "Edit" on any beer in the list
2. Modify the details
3. Click "Save Beer"

**To Delete a Beer:**
1. Click "Delete" on any beer
2. Confirm deletion
3. Beer is removed from the website

## What Fields Can You Edit?

| Field | Required | Example |
|-------|----------|---------|
| Beer Name | Yes | Doe Brand |
| Style | Yes | Lager - American Pre-Prohibition |
| Description | Yes | A simple, clean lager brewed with corn... |
| ABV (%) | Yes | 5.1 |
| IBU | Yes | 30 |
| Release Date | Yes | 2025-11-07 |
| Logo Image Path | No | images/untappd-logos/beer-name.png |
| Untappd URL | No | https://untappd.com/b/slade-brewing-beer-name/123456 |
| Currently Available | No | ✓ Checked = Yes |
| Featured Beer | No | ✓ Checked = Yes |

## Understanding the Data

### beers.json Structure

Your data is stored in `beers.json` in this format:

```json
{
  "Doe Brand": {
    "description": "A simple, clean lager...",
    "logo": "images/untappd-logos/Doe Brand - Pre-Prohibition Lager Untappd Image.png",
    "untappd": "https://untappd.com/b/slade-brewing-doe-brand/6483546",
    "abv": 5.1,
    "ibu": 30,
    "style": "Lager - American Pre-Prohibition",
    "releaseDate": "2025-11-07",
    "currentlyAvailable": true,
    "featured": false
  }
}
```

### What's Stored

- **description** - Your beer description (shown on website)
- **logo** - Path to beer label image
- **untappd** - Link to Untappd page (if your beer is on Untappd)
- **abv** - Alcohol by volume percentage
- **ibu** - International Bittering Units (bitterness)
- **style** - Beer style/type
- **releaseDate** - When the beer was released
- **currentlyAvailable** - Is it available now?
- **featured** - Should it be highlighted as featured?

## Using the Admin Panel

### Adding a New Beer

1. Go to http://localhost:8000/admin
2. Fill in all required fields (marked with *)
3. Optionally add:
   - Logo image path
   - Untappd URL
   - Check "Currently Available" if it's in stock
   - Check "Featured" to highlight it
4. Click "Save Beer"
5. The beer appears in your list and on your website

### Example: Adding "Doe Brand"

```
Beer Name: Doe Brand
Style: Lager - American Pre-Prohibition
Description: A simple, clean lager brewed with corn and 6-row with cluster hops and novalager yeast. Hopefully as good as my Dad's go-to beverage of choice!
ABV: 5.1
IBU: 30
Release Date: 2025-11-07
Logo: images/untappd-logos/Doe Brand - Pre-Prohibition Lager Untappd Image.png
Untappd URL: https://untappd.com/b/slade-brewing-doe-brand/6483546
Currently Available: ✓
Featured: ☐
```

### Editing a Beer

1. Go to http://localhost:8000/admin
2. Find the beer in the list on the right
3. Click "Edit" button
4. Change whatever you need
5. Click "Save Beer"
6. Updates appear immediately

### Deleting a Beer

1. Go to http://localhost:8000/admin
2. Find the beer in the list
3. Click "Delete"
4. Confirm deletion
5. Beer is removed from your website

## API Endpoints (Advanced)

If you want to manage beers programmatically:

### Get All Beers
```
GET http://localhost:8000/api/beers
```

### Get Single Beer
```
GET http://localhost:8000/api/beers/Doe%20Brand
```

### Add Beer
```
POST http://localhost:8000/api/beers/add
Content-Type: application/json

{
  "name": "Doe Brand",
  "style": "Lager - American Pre-Prohibition",
  "description": "...",
  "abv": 5.1,
  "ibu": 30,
  "releaseDate": "2025-11-07",
  "logo": "images/untappd-logos/Doe Brand - Pre-Prohibition Lager Untappd Image.png",
  "untappd": "https://untappd.com/b/slade-brewing-doe-brand/6483546",
  "currentlyAvailable": true,
  "featured": false
}
```

### Update Beer
```
POST http://localhost:8000/api/beers/update
Content-Type: application/json

{
  "oldName": "Doe Brand",
  "name": "Doe Brand",
  "style": "Lager - American Pre-Prohibition",
  ...
}
```

### Delete Beer
```
POST http://localhost:8000/api/beers/delete
Content-Type: application/json

{
  "name": "Doe Brand"
}
```

## Troubleshooting

### The admin panel won't load
- Make sure the server is running: `python3 server.py`
- Check http://localhost:8000/admin in your browser
- Try http://127.0.0.1:8000/admin if localhost doesn't work

### Changes not showing on the website
- Refresh your browser (Ctrl+F5 or Cmd+Shift+R)
- The website loads beers.json automatically

### "Beer already exists" error
- You already have a beer with that name
- Edit the existing beer instead, or use a different name

### Logo image not showing
- Check that the image path is correct
- Images should be in the `images/` folder
- Use paths like: `images/untappd-logos/beer-name.png`

### How do I backup my beers?
- Simply copy the `beers.json` file to keep a backup
- The file is in your project root directory

## File Locations

```
/home/slade/dev/sladebrewing/
├── server.py              # Run this to start the server
├── beers.json            # Your beer data (auto-managed by admin panel)
├── index.html            # Your website homepage
├── assets/
│   ├── css/style.css
│   └── js/script.js
└── images/
    ├── Slade Brewing - Main Logo.png
    ├── engin-akyurt-3ORoQEJY9LA-unsplash.jpg
    └── untappd-logos/    # Store beer label images here
```

## Advanced: Scheduling Server Startup

If you want the server to start automatically:

**macOS (using LaunchAgent):**
Create `~/Library/LaunchAgents/com.sladebrewing.server.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sladebrewing.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/sladebrewing/server.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

Then run:
```bash
launchctl load ~/Library/LaunchAgents/com.sladebrewing.server.plist
```

## Next Steps

1. Start the server: `python3 server.py`
2. Open http://localhost:8000/admin
3. Add your three beers using the admin panel
4. Visit http://localhost:8000 to see your website
5. Make changes anytime by opening the admin panel

That's it! You now have a simple, user-friendly way to manage your beers without touching JSON files. 🍺

---

## What About the Other Files?

- **enrich_beers.py** - No longer needed (Untappd API access restricted)
- **UNTAPPD_SETUP.md** - No longer applicable
- **QUICK_START.md** - No longer applicable

You can delete these if you want, or keep them for reference.
