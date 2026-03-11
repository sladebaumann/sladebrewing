# Slade Brewing Website

A modern, responsive website for **Slade Brewing** - a craft brewery based in Minneapolis, MN. Features a beautiful design showcasing your beer lineup with an easy-to-use admin panel for managing beer data.

## 🍺 Features

- **Modern Design** - Clean, professional website with teal color scheme
- **Responsive Layout** - Works perfectly on desktop, tablet, and mobile
- **Beer Management** - Admin panel to add, edit, and delete beers
- **Easy Updates** - No coding required - manage beers through web interface
- **Real-time Changes** - Updates appear on your website instantly
- **Hero Section** - Beautiful parallax background with beer mug imagery
- **Featured Beer** - Highlight your latest or best-selling beer
- **Beer Cards** - Display ABV, IBU, style, and Untappd links for each beer
- **Contact Section** - Get in touch with visitors

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [How to Manage Beers](#how-to-manage-beers)
- [File Structure](#file-structure)
- [Website Pages](#website-pages)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)

## 🚀 Quick Start

### Prerequisites
- Python 3 (comes pre-installed on most systems)
- A web browser

### Starting the Website

1. **Open a terminal and navigate to the project directory:**
   ```bash
   cd /path/to/sladebrewing
   ```

2. **Start the web server:**
   ```bash
   python3 server.py
   ```

3. **Open your browser:**
   - Website: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

4. **Stop the server:**
   - Press `Ctrl+C` in the terminal

That's it! Your website is now running.

## 🍻 How to Manage Beers

### Overview

Your beer data is stored in `beers.json`. You can update it in two ways:

1. **Admin Panel** (Recommended) - Easy web interface, no technical knowledge needed
2. **Direct Editing** - Edit beers.json file manually (advanced)

### Method 1: Using the Admin Panel (Recommended)

The admin panel is the easiest way to manage your beers. No coding knowledge required!

#### Accessing the Admin Panel

1. Start the server: `python3 server.py`
2. Open your browser to: **http://localhost:8000/admin**
3. You should see a beautiful interface with two sections:
   - **Left side:** Form to add/edit beers
   - **Right side:** List of all your current beers

#### Adding a New Beer

**Step 1: Fill in the Beer Details**

In the form on the left, enter:

1. **Beer Name** (required)
   - Example: "Doe Brand"
   - This is the main name that appears on your website
   - Must be unique (can't have two beers with same name)

2. **Style** (required)
   - Example: "Lager - American Pre-Prohibition"
   - Describes the type of beer
   - Examples: IPA, Pale Ale, Stout, Wheat Beer, etc.

3. **Description** (required)
   - Example: "A simple, clean lager brewed with corn and 6-row with cluster hops and novalager yeast. Hopefully as good as my Dad's go-to beverage of choice!"
   - This appears on your website, so make it appealing
   - Can be as long as you want

4. **ABV (%)** (required)
   - Example: 5.1
   - Alcohol by volume
   - Enter just the number (the % sign is added automatically)
   - Decimal values OK (5.1, 4.25, etc.)

5. **IBU** (required)
   - Example: 30
   - International Bittering Units (measures bitterness)
   - Enter a whole number
   - Higher = more bitter

6. **Release Date** (required)
   - Example: 2025-11-07
   - Click the date field, a calendar appears
   - Choose when this beer was released or will be released

7. **Logo Image Path** (optional)
   - Example: `images/untappd-logos/Doe Brand - Pre-Prohibition Lager Untappd Image.png`
   - Path to the beer label image
   - Should be in the `images/` folder
   - Leave blank if you don't have an image yet

8. **Untappd URL** (optional)
   - Example: `https://untappd.com/b/slade-brewing-doe-brand/6483546`
   - Link to your beer on Untappd
   - Leave blank if your beer isn't on Untappd

9. **Currently Available** (optional checkbox)
   - ✓ Check if the beer is available now
   - ☐ Uncheck if it's out of stock or seasonal
   - This doesn't affect the website appearance, just for your info

10. **Featured Beer** (optional checkbox)
    - ✓ Check to highlight this as your featured beer
    - ☐ Uncheck for regular beers
    - Featured beer appears in a special section on the homepage

**Step 2: Save the Beer**

Click the blue **"Save Beer"** button at the bottom of the form.

You should see a green success message: "Beer added successfully!"

The beer immediately appears in the beer list on the right.

**Step 3: Verify on Website**

1. Open http://localhost:8000 in a new tab
2. Scroll down to see your beer in the "Our Full Lineup" section
3. The beer card shows: name, style, ABV, IBU, description, and links

#### Editing an Existing Beer

**Step 1: Find the Beer**

In the beer list on the right, find the beer you want to edit.

**Step 2: Click Edit**

Click the green **"Edit"** button on the beer.

**Step 3: Make Changes**

The form on the left now shows the beer's current details. Change whatever you need:
- Name
- Style
- Description
- ABV
- IBU
- Release date
- Logo
- Untappd URL
- Availability/Featured status

**Step 4: Save Changes**

Click **"Save Beer"** again.

You'll see: "Beer updated successfully!"

The beer list updates immediately, and changes appear on your website.

#### Deleting a Beer

**Step 1: Find the Beer**

In the beer list on the right, find the beer you want to delete.

**Step 2: Click Delete**

Click the red **"Delete"** button on the beer.

**Step 3: Confirm**

A confirmation popup appears: "Are you sure you want to delete [beer name]?"

Click "OK" to confirm deletion.

**Step 4: Done**

The beer is removed from the list and your website immediately.

### Real-World Example: Adding "Wild n' Mild"

Let's say you want to add a new beer called "Wild n' Mild":

1. Open http://localhost:8000/admin
2. Fill in the form:
   ```
   Beer Name:          Wild n' Mild
   Style:              Mild - Dark
   Description:        An easy drinking, low abv dark mild brewed with 
                       a pound of northern MN wild rice!
   ABV:                2.8
   IBU:                20
   Release Date:       2025-11-07
   Logo:               images/untappd-logos/Wild n' Mild Untappd Image.png
   Untappd URL:        https://untappd.com/b/slade-brewing-wild-n-mild/6483539
   Currently Available: ✓ (checked)
   Featured:           ☐ (unchecked)
   ```
3. Click "Save Beer"
4. Green success message appears
5. Beer appears in list on right
6. Refresh http://localhost:8000 to see it on your website

### Method 2: Direct Editing (Advanced)

If you prefer to edit `beers.json` directly, you can. This requires basic JSON knowledge.

#### Opening beers.json

1. Use a text editor (VS Code, Sublime Text, Notepad++, etc.)
2. Open the file at: `/home/slade/dev/sladebrewing/beers.json`

#### Understanding the Format

The file looks like this:

```json
{
  "Doe Brand": {
    "description": "A simple, clean lager brewed with corn and 6-row...",
    "logo": "images/untappd-logos/Doe Brand - Pre-Prohibition Lager Untappd Image.png",
    "untappd": "https://untappd.com/b/slade-brewing-doe-brand/6483546",
    "abv": 5.1,
    "ibu": 30,
    "style": "Lager - American Pre-Prohibition",
    "releaseDate": "2025-11-07",
    "currentlyAvailable": true,
    "featured": false
  },
  "Wild n' Mild": {
    "description": "An easy drinking, low abv dark mild...",
    ...
  }
}
```

#### Adding a Beer Manually

Add a new entry following this template:

```json
{
  "Your Beer Name": {
    "description": "Description of your beer",
    "logo": "images/untappd-logos/beer-image.png",
    "untappd": "https://untappd.com/b/slade-brewing-beer-name/123456",
    "abv": 5.1,
    "ibu": 30,
    "style": "Beer Style",
    "releaseDate": "YYYY-MM-DD",
    "currentlyAvailable": true,
    "featured": false
  }
}
```

**Important Notes:**
- Beer name must be unique
- Use double quotes for all text values
- Numbers (abv, ibu) don't need quotes
- Boolean values (true/false) are lowercase, no quotes
- Release date format: YYYY-MM-DD (e.g., 2025-11-07)
- Add a comma after each beer entry except the last one

#### Editing a Beer Manually

Find the beer name and update any fields:

```json
"Doe Brand": {
  "description": "Updated description here",
  "abv": 5.2,        // Changed from 5.1
  "ibu": 32,         // Changed from 30
  "featured": true,  // Changed from false
  ...
}
```

#### Deleting a Beer Manually

Remove the entire beer entry:

```json
{
  "Doe Brand": { ... },      // Keep this
  "Wild n' Mild": { ... },   // Delete this entire section
  "Sparkle Pants": { ... }   // Keep this
}
```

#### Saving Changes

Save the file. If you're running the server, refresh your browser to see changes.

**Important:** Make sure the JSON is valid. One missing comma or quote will break the file!

### Comparing the Two Methods

| Feature | Admin Panel | Direct Editing |
|---------|------------|-----------------|
| Ease of Use | ⭐⭐⭐⭐⭐ Easy | ⭐⭐ Requires JSON knowledge |
| Error Prevention | ✅ Prevents mistakes | ❌ Easy to make syntax errors |
| Time to Add Beer | 2 minutes | 5 minutes |
| Time to Edit Beer | 1 minute | 3 minutes |
| Validation | ✅ Built-in | ❌ Manual |
| Recommended | ✅ Yes | ❌ No (only if needed) |

## 📁 File Structure

```
sladebrewing/
├── README.md                           # This file
├── ADMIN_PANEL.md                      # Admin panel documentation
├── beers.json                          # Your beer data (managed by admin panel)
├── index.html                          # Homepage
├── news.html                           # News/blog page
├── elements.html                       # Element showcase page
├── server.py                           # Web server (run this!)
├── LICENSE                             # License information
├── TODO.md                             # Development todo list
│
├── assets/
│   ├── css/
│   │   └── style.css                   # Website styling
│   │
│   └── js/
│       └── script.js                   # Website functionality
│
└── images/
    ├── Slade Brewing - Main Logo.png   # Navbar logo
    ├── engin-akyurt-3ORoQEJY9LA-unsplash.jpg  # Hero background
    │
    └── untappd-logos/
        ├── Doe Brand - Pre-Prohibition Lager Untappd Image.png
        ├── Wild n' Mild Untappd Image.png
        └── Sparkle Pants Witbier Untappd Image.png
```

## 📄 Website Pages

### Home Page (index.html)

The main landing page featuring:

- **Navigation Bar** - Links to beers, news, and contact
- **Hero Section** - Beautiful header with beer mug background
- **About Section** - Description of Slade Brewing
- **Stats Section** - Key brewery facts (founded 2019, 3 beers, etc.)
- **Featured Beer** - Highlight of your latest beer
- **Beer Lineup** - Grid of all your beers
- **Contact Section** - Get in touch form

### News Page (news.html)

Blog/news section for announcements, events, and updates.

### Elements Page (elements.html)

Design showcase page demonstrating all HTML/CSS elements.

## 🎨 Customization

### Changing Colors

The website uses a teal color scheme. To change it:

1. Open `assets/css/style.css`
2. Find the `:root` section at the top:
   ```css
   :root {
       --primary-color: #5a9fb5;      /* Main teal color */
       --accent-color: #4a8fa5;       /* Darker teal */
       ...
   }
   ```
3. Change the hex colors to your preference
4. Save and refresh your browser

### Changing the Logo

1. Replace `images/Slade Brewing - Main Logo.png` with your logo
2. Keep the same filename, or update the reference in `index.html` line 15

### Changing the Hero Image

1. Replace `images/engin-akyurt-3ORoQEJY9LA-unsplash.jpg` with your image
2. The image is referenced in `assets/css/style.css` around line 171

### Adding New Pages

1. Create a new `.html` file
2. Copy the structure from `index.html`
3. Add a link in the navigation bar
4. Update `assets/css/style.css` if needed

## 🐛 Troubleshooting

### Website won't load / Can't access http://localhost:8000

**Problem:** "Cannot connect to server"

**Solutions:**
1. Make sure the server is running: `python3 server.py`
2. Try http://127.0.0.1:8000 instead of localhost
3. Check if port 8000 is in use by another application
4. Restart your terminal and try again

### Admin panel won't load / http://localhost:8000/admin gives error

**Problem:** Admin panel page is blank or shows error

**Solutions:**
1. Make sure you're using Python 3: `python3 --version`
2. Restart the server: Stop with Ctrl+C, then `python3 server.py`
3. Try refreshing the page (Ctrl+F5 or Cmd+Shift+R)
4. Clear your browser cache

### Changes to beers.json don't show up

**Problem:** Added a beer but it's not appearing on website

**Solutions:**
1. If using admin panel: Wait 1-2 seconds for success message
2. If editing beers.json directly: Save the file
3. Refresh your browser (Ctrl+F5 or Cmd+Shift+R)
4. Make sure beers.json has valid JSON (use a JSON validator)

### "Beer already exists" error

**Problem:** Can't add a beer - getting error message

**Solution:** You already have a beer with that exact name. Either:
- Use a different name, or
- Edit the existing beer instead of adding a new one

### Beer images aren't showing

**Problem:** Beer label images display as broken images

**Solutions:**
1. Check the image file actually exists: `ls images/untappd-logos/`
2. Verify the path in the admin panel is correct
3. Make sure file extension is correct (.png, .jpg, etc.)
4. Try using the exact filename from the images folder

### beers.json says "Invalid JSON"

**Problem:** Admin panel won't load or shows JSON error

**Solutions:**
1. Use a JSON validator: https://jsonlint.com/
2. Common mistakes:
   - Missing comma after a beer entry
   - Missing quotes around text values
   - Extra commas (before closing brace)
   - Apostrophes in beer names need escaping
3. If you can't fix it, restore from backup and re-add beers

### Website looks weird on mobile

**Problem:** Layout is broken on phone/tablet

**Solutions:**
1. This shouldn't happen - website is responsive
2. Try restarting the server
3. Clear browser cache
4. Try a different browser

## 📚 Additional Resources

### Full Documentation

- **ADMIN_PANEL.md** - Detailed admin panel guide
- **TODO.md** - Development roadmap
- **LICENSE** - License information

### External Resources

- [HTML5 UP Templates](https://html5up.net/) - Original template
- [Unsplash](https://unsplash.com/) - Free images
- [JSON Formatter](https://jsonformatter.org/) - Validate/format JSON

## 🔧 For Developers

### Running in Development Mode

```bash
python3 server.py
```

This starts a local development server on http://localhost:8000

### Project Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript (vanilla)
- **Backend:** Python 3 (simple HTTP server)
- **Data:** JSON (beers.json)
- **Styling:** Modern CSS with flexbox and grid

### Key Files for Developers

| File | Purpose |
|------|---------|
| `server.py` | Python web server with admin panel endpoints |
| `index.html` | Homepage HTML structure |
| `assets/css/style.css` | All styling (979 lines) |
| `assets/js/script.js` | Website interactivity |
| `beers.json` | Beer data storage |

### Making Code Changes

1. Edit HTML/CSS/JS files
2. Refresh browser (Ctrl+F5) to see changes
3. No need to restart server unless changing Python code
4. If you modify server.py, restart with Ctrl+C then `python3 server.py`

## 📞 Support

For issues or questions:

1. Check the **Troubleshooting** section above
2. Read **ADMIN_PANEL.md** for detailed help
3. Use a JSON validator if you're editing beers.json directly
4. Check browser console for errors (F12 → Console tab)

---

## Image Credits

- **Hero Background:** Photo by [engin akyurt](https://unsplash.com/@enginakyurt?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/photos/clear-glass-beer-mug-with-beer-3ORoQEJY9LA?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
- **Original Template:** [Massively by HTML5 UP](https://html5up.net)

## License

Free for personal and commercial use under the CCA 3.0 license ([html5up.net/license](http://html5up.net/license))

---

**Happy brewing!** 🍺

Last Updated: March 2026
