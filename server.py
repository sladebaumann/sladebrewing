#!/usr/bin/env python3
"""
Slade Brewing Website Server with Admin Panel
Serves the website and provides an admin interface to manage beers.json

Run with: python3 server.py
Then visit: http://localhost:8000
Admin panel: http://localhost:8000/admin
"""

import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime

# Configuration
PORT = int(os.environ.get('PORT', 8000))
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))
BEERS_FILE = "beers.json"


class SladBrewingHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler for Slade Brewing site with admin panel."""
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        
        # Admin panel
        if parsed_path.path == "/admin":
            self.serve_admin_panel()
            return
        
        # API endpoint to get beers data
        if parsed_path.path == "/api/beers":
            self.handle_get_beers()
            return
        
        # API endpoint to get single beer
        if parsed_path.path.startswith("/api/beers/"):
            beer_name = parsed_path.path.replace("/api/beers/", "").replace("%20", " ")
            self.handle_get_beer(beer_name)
            return
        
        # Serve static files
        super().do_GET()
    
    def do_POST(self):
        """Handle POST requests for beer management."""
        parsed_path = urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self.send_json_response({"success": False, "error": "Invalid JSON"}, 400)
            return
        
        # Add new beer
        if parsed_path.path == "/api/beers/add":
            self.handle_add_beer(data)
            return
        
        # Update beer
        if parsed_path.path == "/api/beers/update":
            self.handle_update_beer(data)
            return
        
        # Delete beer
        if parsed_path.path == "/api/beers/delete":
            self.handle_delete_beer(data)
            return
        
        self.send_json_response({"success": False, "error": "Unknown endpoint"}, 404)
    
    def serve_admin_panel(self):
        """Serve the admin panel HTML."""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Slade Brewing - Beer Admin Panel</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            color: white;
        }
        
        header h1 {
            font-size: 2.5rem;
        }
        
        .back-btn {
            background: rgba(255,255,255,0.2);
            color: white;
            border: 1px solid white;
            padding: 0.7rem 1.5rem;
            border-radius: 4px;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        .back-btn:hover {
            background: white;
            color: #667eea;
        }
        
        .content {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .panel {
            background: white;
            border-radius: 8px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 2rem;
        }
        
        .panel h2 {
            color: #667eea;
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        label {
            display: block;
            margin-bottom: 0.5rem;
            color: #333;
            font-weight: 600;
            font-size: 0.95rem;
        }
        
        input[type="text"],
        input[type="number"],
        input[type="url"],
        input[type="date"],
        textarea,
        select {
            width: 100%;
            padding: 0.8rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-family: inherit;
            font-size: 0.95rem;
            transition: border-color 0.3s ease;
        }
        
        input:focus,
        textarea:focus,
        select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        textarea {
            resize: vertical;
            min-height: 100px;
        }
        
        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
        
        input[type="checkbox"] {
            width: 18px;
            height: 18px;
            cursor: pointer;
        }
        
        .btn {
            padding: 0.85rem 1.5rem;
            border: none;
            border-radius: 4px;
            font-weight: 600;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
            width: 100%;
        }
        
        .btn-primary:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }
        
        .btn-secondary {
            background: #f0f0f0;
            color: #333;
            width: 100%;
            margin-top: 1rem;
        }
        
        .btn-secondary:hover {
            background: #e0e0e0;
        }
        
        .btn-danger {
            background: #ff6b6b;
            color: white;
            padding: 0.6rem 1rem;
            font-size: 0.9rem;
            width: auto;
        }
        
        .btn-danger:hover {
            background: #ff5252;
        }
        
        .btn-edit {
            background: #51cf66;
            color: white;
            padding: 0.6rem 1rem;
            font-size: 0.9rem;
            margin-right: 0.5rem;
        }
        
        .btn-edit:hover {
            background: #40c057;
        }
        
        .beer-list {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        
        .beer-item {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 6px;
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }
        
        .beer-item:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            background: white;
        }
        
        .beer-item h3 {
            color: #667eea;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }
        
        .beer-item p {
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 0.3rem;
        }
        
        .beer-item-actions {
            margin-top: 1rem;
            display: flex;
            gap: 0.5rem;
        }
        
        .badge {
            display: inline-block;
            padding: 0.3rem 0.7rem;
            border-radius: 20px;
            font-size: 0.8rem;
            margin-right: 0.5rem;
        }
        
        .badge-available {
            background: #d4edda;
            color: #155724;
        }
        
        .badge-unavailable {
            background: #f8d7da;
            color: #721c24;
        }
        
        .badge-featured {
            background: #fff3cd;
            color: #856404;
        }
        
        .message {
            padding: 1rem;
            border-radius: 4px;
            margin-bottom: 1rem;
            display: none;
        }
        
        .message.success {
            display: block;
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .message.error {
            display: block;
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .empty-state {
            text-align: center;
            padding: 3rem 1rem;
            color: #999;
        }
        
        .empty-state p {
            margin-bottom: 1rem;
            font-size: 1.1rem;
        }
        
        @media (max-width: 768px) {
            .content {
                grid-template-columns: 1fr;
            }
            
            header {
                flex-direction: column;
                gap: 1rem;
                text-align: center;
            }
            
            header h1 {
                font-size: 1.8rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🍺 Beer Admin Panel</h1>
            <a href="/" class="back-btn">← Back to Website</a>
        </header>
        
        <div class="content">
            <!-- Add/Edit Beer Form -->
            <div class="panel">
                <h2 id="form-title">Add New Beer</h2>
                <div id="message" class="message"></div>
                
                <form id="beerForm">
                    <div class="form-group">
                        <label for="name">Beer Name *</label>
                        <input type="text" id="name" name="name" required placeholder="e.g., Doe Brand">
                    </div>
                    
                    <div class="form-group">
                        <label for="style">Style *</label>
                        <input type="text" id="style" name="style" required placeholder="e.g., Lager - American Pre-Prohibition">
                    </div>
                    
                    <div class="form-group">
                        <label for="description">Description *</label>
                        <textarea id="description" name="description" required placeholder="Tell us about this beer..."></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="abv">ABV (%) *</label>
                        <input type="number" id="abv" name="abv" required step="0.1" placeholder="5.1">
                    </div>
                    
                    <div class="form-group">
                        <label for="ibu">IBU *</label>
                        <input type="number" id="ibu" name="ibu" required step="1" placeholder="30">
                    </div>
                    
                    <div class="form-group">
                        <label for="releaseDate">Release Date *</label>
                        <input type="date" id="releaseDate" name="releaseDate" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="logo">Logo Image Path</label>
                        <input type="text" id="logo" name="logo" placeholder="images/untappd-logos/beer-name.png">
                    </div>
                    
                    <div class="form-group">
                        <label for="untappd">Untappd URL</label>
                        <input type="url" id="untappd" name="untappd" placeholder="https://untappd.com/b/slade-brewing-beer-name/123456">
                    </div>
                    
                    <div class="checkbox-group">
                        <input type="checkbox" id="currentlyAvailable" name="currentlyAvailable">
                        <label for="currentlyAvailable" style="margin: 0;">Currently Available?</label>
                    </div>
                    
                    <div class="checkbox-group">
                        <input type="checkbox" id="featured" name="featured">
                        <label for="featured" style="margin: 0;">Featured Beer?</label>
                    </div>
                    
                    <button type="submit" class="btn btn-primary">Save Beer</button>
                    <button type="button" class="btn btn-secondary" id="cancelBtn" style="display:none;">Cancel</button>
                </form>
            </div>
            
            <!-- Beer List -->
            <div class="panel">
                <h2>Beer List</h2>
                <div id="beerList" class="beer-list">
                    <div class="empty-state">
                        <p>Loading beers...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const FORM = document.getElementById('beerForm');
        const MESSAGE = document.getElementById('message');
        const BEER_LIST = document.getElementById('beerList');
        const FORM_TITLE = document.getElementById('form-title');
        const CANCEL_BTN = document.getElementById('cancelBtn');
        let editingBeer = null;
        
        // Load beers on page load
        document.addEventListener('DOMContentLoaded', loadBeers);
        
        // Form submission
        FORM.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(FORM);
            const beerData = Object.fromEntries(formData);
            
            // Convert checkboxes to boolean
            beerData.currentlyAvailable = formData.has('currentlyAvailable');
            beerData.featured = formData.has('featured');
            
            // Convert numbers
            beerData.abv = parseFloat(beerData.abv);
            beerData.ibu = parseInt(beerData.ibu);
            
            const endpoint = editingBeer ? '/api/beers/update' : '/api/beers/add';
            if (editingBeer) {
                beerData.oldName = editingBeer;
            }
            
            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(beerData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showMessage(`Beer ${editingBeer ? 'updated' : 'added'} successfully!`, 'success');
                    FORM.reset();
                    editingBeer = null;
                    FORM_TITLE.textContent = 'Add New Beer';
                    CANCEL_BTN.style.display = 'none';
                    loadBeers();
                } else {
                    showMessage(result.error || 'An error occurred', 'error');
                }
            } catch (error) {
                showMessage('Error: ' + error.message, 'error');
            }
        });
        
        CANCEL_BTN.addEventListener('click', () => {
            FORM.reset();
            editingBeer = null;
            FORM_TITLE.textContent = 'Add New Beer';
            CANCEL_BTN.style.display = 'none';
        });
        
        async function loadBeers() {
            try {
                const response = await fetch('/api/beers');
                const result = await response.json();
                
                if (result.success && result.beers) {
                    const beers = Object.entries(result.beers).map(([name, data]) => ({
                        name,
                        ...data
                    }));
                    
                    if (beers.length === 0) {
                        BEER_LIST.innerHTML = '<div class="empty-state"><p>No beers yet. Add one to get started!</p></div>';
                    } else {
                        BEER_LIST.innerHTML = beers.map(beer => `
                            <div class="beer-item">
                                <h3>${beer.name}</h3>
                                <p><strong>${beer.style}</strong></p>
                                <p>${beer.description}</p>
                                <p>
                                    <span class="badge ${beer.currentlyAvailable ? 'badge-available' : 'badge-unavailable'}">
                                        ${beer.currentlyAvailable ? 'Available' : 'Unavailable'}
                                    </span>
                                    ${beer.featured ? '<span class="badge badge-featured">Featured</span>' : ''}
                                </p>
                                <p><strong>ABV:</strong> ${beer.abv}% | <strong>IBU:</strong> ${beer.ibu}</p>
                                <div class="beer-item-actions">
                                    <button class="btn btn-edit" onclick="editBeer('${beer.name}')">Edit</button>
                                    <button class="btn btn-danger" onclick="deleteBeer('${beer.name}')">Delete</button>
                                </div>
                            </div>
                        `).join('');
                    }
                }
            } catch (error) {
                BEER_LIST.innerHTML = '<div class="empty-state"><p>Error loading beers: ' + error.message + '</p></div>';
            }
        }
        
        async function editBeer(beerName) {
            try {
                const response = await fetch('/api/beers/' + encodeURIComponent(beerName));
                const result = await response.json();
                
                if (result.success && result.beer) {
                    const beer = result.beer;
                    document.getElementById('name').value = beer.name;
                    document.getElementById('style').value = beer.style;
                    document.getElementById('description').value = beer.description;
                    document.getElementById('abv').value = beer.abv;
                    document.getElementById('ibu').value = beer.ibu;
                    document.getElementById('releaseDate').value = beer.releaseDate;
                    document.getElementById('logo').value = beer.logo || '';
                    document.getElementById('untappd').value = beer.untappd || '';
                    document.getElementById('currentlyAvailable').checked = beer.currentlyAvailable;
                    document.getElementById('featured').checked = beer.featured;
                    
                    editingBeer = beerName;
                    FORM_TITLE.textContent = 'Edit Beer: ' + beerName;
                    CANCEL_BTN.style.display = 'block';
                    
                    // Scroll to form
                    document.querySelector('.panel').scrollIntoView({ behavior: 'smooth' });
                }
            } catch (error) {
                showMessage('Error loading beer: ' + error.message, 'error');
            }
        }
        
        async function deleteBeer(beerName) {
            if (!confirm(`Are you sure you want to delete "${beerName}"?`)) return;
            
            try {
                const response = await fetch('/api/beers/delete', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name: beerName })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showMessage('Beer deleted successfully!', 'success');
                    loadBeers();
                } else {
                    showMessage(result.error || 'Error deleting beer', 'error');
                }
            } catch (error) {
                showMessage('Error: ' + error.message, 'error');
            }
        }
        
        function showMessage(text, type) {
            MESSAGE.textContent = text;
            MESSAGE.className = 'message ' + type;
            setTimeout(() => {
                MESSAGE.className = 'message';
            }, 5000);
        }
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(html.encode())))
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_get_beers(self):
        """Return all beers as JSON."""
        try:
            with open(BEERS_FILE, 'r') as f:
                beers = json.load(f)
            self.send_json_response({"success": True, "beers": beers}, 200)
        except FileNotFoundError:
            self.send_json_response({"success": False, "error": "beers.json not found"}, 404)
        except json.JSONDecodeError:
            self.send_json_response({"success": False, "error": "Invalid JSON in beers.json"}, 500)
    
    def handle_get_beer(self, beer_name):
        """Return a single beer by name."""
        try:
            with open(BEERS_FILE, 'r') as f:
                beers = json.load(f)
            
            if beer_name in beers:
                beer = beers[beer_name]
                beer['name'] = beer_name
                self.send_json_response({"success": True, "beer": beer}, 200)
            else:
                self.send_json_response({"success": False, "error": "Beer not found"}, 404)
        except Exception as e:
            self.send_json_response({"success": False, "error": str(e)}, 500)
    
    def handle_add_beer(self, data):
        """Add a new beer to beers.json."""
        try:
            # Load existing beers
            try:
                with open(BEERS_FILE, 'r') as f:
                    beers = json.load(f)
            except FileNotFoundError:
                beers = {}
            
            # Validate required fields
            required = ['name', 'style', 'description', 'abv', 'ibu', 'releaseDate']
            if not all(field in data and data[field] for field in required):
                self.send_json_response({"success": False, "error": "Missing required fields"}, 400)
                return
            
            # Check if beer already exists
            if data['name'] in beers:
                self.send_json_response({"success": False, "error": "Beer already exists"}, 409)
                return
            
            # Add the beer
            beers[data['name']] = {
                'description': data['description'],
                'logo': data.get('logo', ''),
                'untappd': data.get('untappd', ''),
                'abv': data['abv'],
                'ibu': data['ibu'],
                'style': data['style'],
                'releaseDate': data['releaseDate'],
                'currentlyAvailable': data.get('currentlyAvailable', True),
                'featured': data.get('featured', False)
            }
            
            # Save updated beers
            with open(BEERS_FILE, 'w') as f:
                json.dump(beers, f, indent=2)
            
            self.send_json_response({"success": True, "message": "Beer added successfully"}, 200)
        except Exception as e:
            self.send_json_response({"success": False, "error": str(e)}, 500)
    
    def handle_update_beer(self, data):
        """Update an existing beer."""
        try:
            with open(BEERS_FILE, 'r') as f:
                beers = json.load(f)
            
            # Validate required fields
            required = ['name', 'oldName', 'style', 'description', 'abv', 'ibu', 'releaseDate']
            if not all(field in data and data[field] for field in required):
                self.send_json_response({"success": False, "error": "Missing required fields"}, 400)
                return
            
            # Check if old beer exists
            if data['oldName'] not in beers:
                self.send_json_response({"success": False, "error": "Beer not found"}, 404)
                return
            
            # If name changed, check if new name doesn't exist
            if data['name'] != data['oldName'] and data['name'] in beers:
                self.send_json_response({"success": False, "error": "Beer with that name already exists"}, 409)
                return
            
            # Update the beer
            old_name = data['oldName']
            new_name = data['name']
            
            beers[new_name] = {
                'description': data['description'],
                'logo': data.get('logo', ''),
                'untappd': data.get('untappd', ''),
                'abv': data['abv'],
                'ibu': data['ibu'],
                'style': data['style'],
                'releaseDate': data['releaseDate'],
                'currentlyAvailable': data.get('currentlyAvailable', True),
                'featured': data.get('featured', False)
            }
            
            # Remove old entry if name changed
            if old_name != new_name:
                del beers[old_name]
            
            # Save updated beers
            with open(BEERS_FILE, 'w') as f:
                json.dump(beers, f, indent=2)
            
            self.send_json_response({"success": True, "message": "Beer updated successfully"}, 200)
        except Exception as e:
            self.send_json_response({"success": False, "error": str(e)}, 500)
    
    def handle_delete_beer(self, data):
        """Delete a beer from beers.json."""
        try:
            with open(BEERS_FILE, 'r') as f:
                beers = json.load(f)
            
            if 'name' not in data:
                self.send_json_response({"success": False, "error": "Beer name required"}, 400)
                return
            
            if data['name'] not in beers:
                self.send_json_response({"success": False, "error": "Beer not found"}, 404)
                return
            
            del beers[data['name']]
            
            with open(BEERS_FILE, 'w') as f:
                json.dump(beers, f, indent=2)
            
            self.send_json_response({"success": True, "message": "Beer deleted successfully"}, 200)
        except Exception as e:
            self.send_json_response({"success": False, "error": str(e)}, 500)
    
    def send_json_response(self, data, status_code=200):
        """Send a JSON response."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        response_text = json.dumps(data)
        self.send_header('Content-Length', str(len(response_text.encode())))
        self.end_headers()
        self.wfile.write(response_text.encode())
    
    def end_headers(self):
        """Add CORS headers to all responses."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


if __name__ == "__main__":
    os.chdir(STATIC_DIR)
    
    # Bind to 0.0.0.0 to accept external connections (required for Render)
    server = HTTPServer(("0.0.0.0", PORT), SladBrewingHandler)
    print(f"Slade Brewing Website with Admin Panel")
    print(f"=" * 50)
    print(f"Starting server on port {PORT}")
    print(f"")
    print(f"Available pages:")
    print(f"  🌐 Website: http://localhost:{PORT}")
    print(f"  🔧 Admin Panel: http://localhost:{PORT}/admin")
    print(f"")
    print(f"Press Ctrl+C to stop")
    print(f"=" * 50)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        server.server_close()
