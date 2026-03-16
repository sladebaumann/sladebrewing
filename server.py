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
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime

# Configuration
PORT = int(os.environ.get('PORT', 8000))
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))
BEERS_FILE = "beers.json"
NEWS_FILE = "news.json"

# Admin authentication - set via environment variable for security
# Default password for development only - override in production!
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'devpassword123')


class SladBrewingHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler for Slade Brewing site with admin panel."""
    
    def check_auth(self):
        """Verify Basic authentication."""
        auth_header = self.headers.get("Authorization", "")
        if not auth_header.startswith("Basic "):
            return False
        
        try:
            import base64
            encoded = auth_header[6:]
            decoded = base64.b64decode(encoded).decode("utf-8")
            username, password = decoded.split(":", 1)
            return password == ADMIN_PASSWORD
        except Exception:
            return False
    
    def require_auth(self):
        """Send 401 if not authenticated."""
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Admin"')
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"success": False, "error": "Authentication required"}).encode())
        return False
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        
        # Ignore favicon requests
        if parsed_path.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        
        # Admin panel
        if parsed_path.path == "/admin":
            if not self.check_auth():
                self.send_response(401)
                self.send_header("WWW-Authenticate", 'Basic realm="Admin Area"')
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"<html><body><h1>401 Unauthorized</h1><p>Authentication required.</p></body></html>")
                return
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
        
        # API endpoint to get all news
        if parsed_path.path == "/api/news":
            self.handle_get_news()
            return
        
        # API endpoint to get single news
        if parsed_path.path.startswith("/api/news/"):
            news_id = parsed_path.path.replace("/api/news/", "").replace("%20", " ")
            self.handle_get_news_item(news_id)
            return
        
        # Serve static files
        super().do_GET()
    
    def do_POST(self):
        """Handle POST requests for beer management."""
        
        # Require auth for all POST requests (add/update/delete)
        if not self.check_auth():
            self.require_auth()
            return
            
        parsed_path = urlparse(self.path)
        
        # Handle multipart form data for file uploads
        content_type = self.headers.get('Content-Type', '')
        if 'multipart/form-data' in content_type:
            self.handle_file_upload(parsed_path)
            return
        
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
        
        # Add news
        if parsed_path.path == "/api/news/add":
            self.handle_add_news(data)
            return
        
        # Update news
        if parsed_path.path == "/api/news/update":
            self.handle_update_news(data)
            return
        
        # Delete news
        if parsed_path.path == "/api/news/delete":
            self.handle_delete_news(data)
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
            background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
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
            color: #2563eb;
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
            color: #2563eb;
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
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
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
            background: #2563eb;
            color: white;
            width: 100%;
        }
        
        .btn-primary:hover {
            background: #1e40af;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(37, 99, 235, 0.3);
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
            border-left: 4px solid #2563eb;
            transition: all 0.3s ease;
        }
        
        .beer-item:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            background: white;
        }
        
        .beer-item h3 {
            color: #2563eb;
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
        
        .tabs {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 2rem;
        }
        
        .tab-btn {
            padding: 1rem 2rem;
            background: rgba(255,255,255,0.2);
            border: 2px solid transparent;
            color: white;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            border-radius: 4px;
            transition: all 0.3s ease;
        }
        
        .tab-btn:hover {
            background: rgba(255,255,255,0.3);
        }
        
        .tab-btn.active {
            background: white;
            color: #2563eb;
            border-color: white;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
            background: white;
            border-radius: 8px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 2rem;
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
            <h1>🍺 Slade Admin Panel</h1>
            <a href="/" class="back-btn">← Back to Website</a>
        </header>
        
        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('beers')">Beers</button>
            <button class="tab-btn" onclick="switchTab('news')">News</button>
        </div>
        
        <!-- Beers Tab -->
        <div id="beers-tab" class="tab-content active">
            <div class="content">
            <!-- Add/Edit Beer Form -->
            <div class="panel">
                <h2 id="form-title">Add New Beer</h2>
                <div id="message" class="message"></div>
                
                    <form id="beerForm" enctype="multipart/form-data">
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
                        <label for="logo">Logo Image (PNG)</label>
                        <input type="file" id="logo" name="logo" accept="image/png,image/jpeg,image/jpg">
                        <small style="color: #666;">Upload a PNG image or leave blank to keep existing</small>
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
        
        <!-- News Tab -->
        <div id="news-tab" class="tab-content">
            <div class="content">
                <!-- Add/Edit News Form -->
                <div class="panel">
                    <h2 id="news-form-title">Add News Item</h2>
                    <div id="news-message" class="message"></div>
                    
                    <form id="newsForm">
                        <div class="form-group">
                            <label for="newsId">News ID *</label>
                            <input type="text" id="newsId" name="id" required placeholder="e.g., new-website-2025">
                            <small style="color: #666;">URL-friendly identifier (no spaces)</small>
                        </div>
                        
                        <div class="form-group">
                            <label for="newsTitle">Title *</label>
                            <input type="text" id="newsTitle" name="title" required placeholder="e.g., Welcome to the New Website">
                        </div>
                        
                        <div class="form-group">
                            <label for="newsDate">Date *</label>
                            <input type="date" id="newsDate" name="date" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="newsSummary">Summary</label>
                            <textarea id="newsSummary" name="summary" placeholder="Short description for homepage (optional)"></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="newsContent">Full Content</label>
                            <textarea id="newsContent" name="content" rows="4" placeholder="Full news article content..."></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="newsImage">Image URL</label>
                            <input type="text" id="newsImage" name="image" placeholder="images/news/image-name.jpg (optional)">
                        </div>
                        
                        <div class="checkbox-group">
                            <input type="checkbox" id="newsFeatured" name="featured">
                            <label for="newsFeatured" style="margin: 0;">Show on Homepage?</label>
                        </div>
                        
                        <button type="submit" class="btn btn-primary">Save News</button>
                        <button type="button" class="btn btn-secondary" id="newsCancelBtn" style="display:none;">Cancel</button>
                    </form>
                </div>
                
                <!-- News List -->
                <div class="panel">
                    <h2>News List</h2>
                    <div id="newsList" class="beer-list">
                        <div class="empty-state">
                            <p>Loading news...</p>
                        </div>
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
        
        // Event delegation for edit/delete buttons
        document.addEventListener('click', (e) => {
            const editBtn = e.target.closest('[data-beer-name]');
            const deleteBtn = e.target.closest('[data-beer-name-delete]');
            
            if (editBtn) {
                const beerName = decodeURIComponent(editBtn.dataset.beerName);
                editBeer(beerName);
            }
            if (deleteBtn) {
                const beerName = decodeURIComponent(deleteBtn.dataset.beerNameDelete);
                deleteBeer(beerName);
            }
        });
        
        // Load beers on page load
        document.addEventListener('DOMContentLoaded', loadBeers);
        
        // Form submission
        FORM.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(FORM);
            
            // Convert checkboxes to boolean
            const beerData = {
                name: formData.get('name'),
                style: formData.get('style'),
                description: formData.get('description'),
                abv: parseFloat(formData.get('abv')),
                ibu: parseInt(formData.get('ibu')),
                releaseDate: formData.get('releaseDate'),
                untappd: formData.get('untappd') || '',
                currentlyAvailable: formData.has('currentlyAvailable'),
                featured: formData.has('featured'),
                logo: ''
            };
            
            // Handle logo file upload
            const logoFile = formData.get('logo');
            if (logoFile && logoFile.size > 0) {
                try {
                    const uploadFormData = new FormData();
                    uploadFormData.append('logo', logoFile);
                    
                    const uploadResponse = await fetch('/api/upload-logo', {
                        method: 'POST',
                        body: uploadFormData
                    });
                    const uploadResult = await uploadResponse.json();
                    
                    if (uploadResult.success) {
                        beerData.logo = uploadResult.path;
                    } else {
                        showMessage('Error uploading logo: ' + uploadResult.error, 'error');
                        return;
                    }
                } catch (error) {
                    showMessage('Error uploading logo: ' + error.message, 'error');
                    return;
                }
            } else {
                // Keep existing logo if no new file uploaded
                const logoInput = document.getElementById('logo');
                if (logoInput.dataset.existingLogo) {
                    beerData.logo = logoInput.dataset.existingLogo;
                }
            }
            
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
                                    <button class="btn btn-edit" data-beer-name="${encodeURIComponent(beer.name)}">Edit</button>
                                    <button class="btn btn-danger" data-beer-name-delete="${encodeURIComponent(beer.name)}">Delete</button>
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
                    document.getElementById('logo').value = '';
                    document.getElementById('logo').dataset.existingLogo = beer.logo || '';
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
        
        // Tab switching
        function switchTab(tabName) {
            console.log('Switching to tab:', tabName);
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            document.querySelector(`[onclick="switchTab('${tabName}')"]`).classList.add('active');
            document.getElementById(`${tabName}-tab`).classList.add('active');
            
            if (tabName === 'news') {
                console.log('Loading news...');
                loadNews();
            }
        }
        
        // News management
        const NEWS_FORM = document.getElementById('newsForm');
        const NEWS_MESSAGE = document.getElementById('news-message');
        const NEWS_LIST = document.getElementById('newsList');
        const NEWS_FORM_TITLE = document.getElementById('news-form-title');
        const NEWS_CANCEL_BTN = document.getElementById('newsCancelBtn');
        let editingNews = null;
        
        NEWS_FORM.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(NEWS_FORM);
            const newsData = Object.fromEntries(formData);
            
            newsData.featured = formData.has('featured');
            
            const endpoint = editingNews ? '/api/news/update' : '/api/news/add';
            if (editingNews) {
                newsData.oldId = editingNews;
            }
            
            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(newsData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showNewsMessage(`News item ${editingNews ? 'updated' : 'added'} successfully!`, 'success');
                    NEWS_FORM.reset();
                    editingNews = null;
                    NEWS_FORM_TITLE.textContent = 'Add News Item';
                    NEWS_CANCEL_BTN.style.display = 'none';
                    loadNews();
                } else {
                    showNewsMessage(result.error || 'An error occurred', 'error');
                }
            } catch (error) {
                showNewsMessage('Error: ' + error.message, 'error');
            }
        });
        
        NEWS_CANCEL_BTN.addEventListener('click', () => {
            NEWS_FORM.reset();
            editingNews = null;
            NEWS_FORM_TITLE.textContent = 'Add News Item';
            NEWS_CANCEL_BTN.style.display = 'none';
        });
        
        async function loadNews() {
            console.log('loadNews called');
            try {
                const response = await fetch('/api/news');
                console.log('Response status:', response.status);
                const result = await response.json();
                console.log('News data:', result);
                
                if (result.success && result.news) {
                    const newsItems = Object.entries(result.news).map(([id, data]) => ({
                        id,
                        ...data
                    }));
                    
                    if (newsItems.length === 0) {
                        NEWS_LIST.innerHTML = '<div class="empty-state"><p>No news yet. Add one to get started!</p></div>';
                    } else {
                        NEWS_LIST.innerHTML = newsItems.map(news => `
                            <div class="beer-item">
                                <h3>${news.title}</h3>
                                <p><strong>${formatDate(news.date)}</strong></p>
                                <p>${news.summary || news.content}</p>
                                <p>
                                    ${news.featured ? '<span class="badge badge-featured">Homepage</span>' : ''}
                                </p>
                                <div class="beer-item-actions">
                                    <button class="btn btn-edit" onclick="editNews('${news.id}')">Edit</button>
                                    <button class="btn btn-danger" onclick="deleteNews('${news.id}')">Delete</button>
                                </div>
                            </div>
                        `).join('');
                    }
                }
            } catch (error) {
                console.error('Error loading news:', error);
                NEWS_LIST.innerHTML = '<div class="empty-state"><p>Error loading news: ' + error.message + '</p></div>';
            }
        }
        
        function formatDate(dateStr) {
            const date = new Date(dateStr);
            return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
        }
        
        async function editNews(newsId) {
            try {
                const response = await fetch('/api/news/' + encodeURIComponent(newsId));
                const result = await response.json();
                
                if (result.success && result.newsItem) {
                    const news = result.newsItem;
                    document.getElementById('newsId').value = news.id;
                    document.getElementById('newsTitle').value = news.title;
                    document.getElementById('newsDate').value = news.date;
                    document.getElementById('newsSummary').value = news.summary || '';
                    document.getElementById('newsContent').value = news.content || '';
                    document.getElementById('newsImage').value = news.image || '';
                    document.getElementById('newsFeatured').checked = news.featured;
                    
                    editingNews = newsId;
                    NEWS_FORM_TITLE.textContent = 'Edit News: ' + news.title;
                    NEWS_CANCEL_BTN.style.display = 'block';
                    
                    document.querySelector('#news-tab .panel').scrollIntoView({ behavior: 'smooth' });
                }
            } catch (error) {
                showNewsMessage('Error loading news: ' + error.message, 'error');
            }
        }
        
        async function deleteNews(newsId) {
            if (!confirm(`Are you sure you want to delete this news item?`)) return;
            
            try {
                const response = await fetch('/api/news/delete', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id: newsId })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showNewsMessage('News item deleted successfully!', 'success');
                    loadNews();
                } else {
                    showNewsMessage(result.error || 'Error deleting news', 'error');
                }
            } catch (error) {
                showNewsMessage('Error: ' + error.message, 'error');
            }
        }
        
        function showNewsMessage(text, type) {
            NEWS_MESSAGE.textContent = text;
            NEWS_MESSAGE.className = 'message ' + type;
            setTimeout(() => {
                NEWS_MESSAGE.className = 'message';
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
    
    def handle_get_news(self):
        """Return all news as JSON."""
        try:
            with open(NEWS_FILE, 'r') as f:
                news = json.load(f)
            self.send_json_response({"success": True, "news": news}, 200)
        except FileNotFoundError:
            self.send_json_response({"success": False, "error": "news.json not found"}, 404)
        except json.JSONDecodeError:
            self.send_json_response({"success": False, "error": "Invalid JSON in news.json"}, 500)
    
    def handle_get_news_item(self, news_id):
        """Return a single news item by ID."""
        try:
            with open(NEWS_FILE, 'r') as f:
                news = json.load(f)
            
            if news_id in news:
                item = news[news_id]
                item['id'] = news_id
                self.send_json_response({"success": True, "newsItem": item}, 200)
            else:
                self.send_json_response({"success": False, "error": "News item not found"}, 404)
        except Exception as e:
            self.send_json_response({"success": False, "error": str(e)}, 500)
    
    def handle_file_upload(self, parsed_path):
        """Handle file uploads for beer logos."""
        if parsed_path.path != '/api/upload-logo':
            self.send_json_response({"success": False, "error": "Unknown upload endpoint"}, 404)
            return
        
        try:
            content_type = self.headers.get('Content-Type', '')
            boundary = content_type.split('boundary=')[-1] if 'boundary=' in content_type else None
            
            if not boundary:
                self.send_json_response({"success": False, "error": "No boundary found"}, 400)
                return
            
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            # Parse multipart form data
            parts = body.split(('--' + boundary).encode())
            
            for part in parts:
                if b'Content-Disposition: form-data; name="logo"' in part:
                    # Extract filename and file content
                    header_end = part.find(b'\r\n\r\n')
                    if header_end == -1:
                        continue
                    
                    headers = part[:header_end].decode('utf-8', errors='ignore')
                    file_content = part[header_end + 4:]
                    
                    # Remove trailing \r\n
                    if file_content.endswith(b'\r\n'):
                        file_content = file_content[:-2]
                    
                    # Check file type
                    if not (headers.lower().find('image/png') >= 0 or headers.lower().find('image/jpeg') >= 0):
                        self.send_json_response({"success": False, "error": "Only PNG and JPEG images are allowed"}, 400)
                        return
                    
                    # Generate filename based on timestamp
                    import time
                    timestamp = int(time.time())
                    filename = f"beer-logo-{timestamp}.png"
                    upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images', 'untappd-logos')
                    
                    # Create directory if it doesn't exist
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    # Save file
                    filepath = os.path.join(upload_dir, filename)
                    with open(filepath, 'wb') as f:
                        f.write(file_content)
                    
                    image_path = f"images/untappd-logos/{filename}"
                    self.send_json_response({"success": True, "path": image_path}, 200)
                    return
            
            self.send_json_response({"success": False, "error": "No logo file found"}, 400)
            
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
            
            # Commit to GitHub
            git_success = self.commit_to_github("Add", data['name'])
            
            if git_success:
                self.send_json_response({"success": True, "message": "Beer added and pushed to GitHub"}, 200)
            else:
                self.send_json_response({"success": True, "message": "Beer added (Git push failed - changes saved locally)"}, 200)
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
            
            # Commit to GitHub
            git_success = self.commit_to_github("Update", new_name)
            
            if git_success:
                self.send_json_response({"success": True, "message": "Beer updated and pushed to GitHub"}, 200)
            else:
                self.send_json_response({"success": True, "message": "Beer updated (Git push failed - changes saved locally)"}, 200)
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
            
            beer_name = data['name']
            del beers[data['name']]
            
            with open(BEERS_FILE, 'w') as f:
                json.dump(beers, f, indent=2)
            
            # Commit to GitHub
            git_success = self.commit_to_github("Delete", beer_name)
            
            if git_success:
                self.send_json_response({"success": True, "message": "Beer deleted and pushed to GitHub"}, 200)
            else:
                self.send_json_response({"success": True, "message": "Beer deleted (Git push failed - changes saved locally)"}, 200)
        except Exception as e:
            self.send_json_response({"success": False, "error": str(e)}, 500)
    
    def handle_add_news(self, data):
        """Add a new news item to news.json."""
        try:
            try:
                with open(NEWS_FILE, 'r') as f:
                    news = json.load(f)
            except FileNotFoundError:
                news = {}
            
            required = ['id', 'title', 'date']
            if not all(field in data and data[field] for field in required):
                self.send_json_response({"success": False, "error": "Missing required fields"}, 400)
                return
            
            if data['id'] in news:
                self.send_json_response({"success": False, "error": "News item with this ID already exists"}, 409)
                return
            
            news[data['id']] = {
                'title': data['title'],
                'date': data['date'],
                'summary': data.get('summary', ''),
                'content': data.get('content', ''),
                'image': data.get('image', None),
                'featured': data.get('featured', False)
            }
            
            with open(NEWS_FILE, 'w') as f:
                json.dump(news, f, indent=2)
            
            git_success = self.commit_news_to_github("Add", data['title'])
            
            if git_success:
                self.send_json_response({"success": True, "message": "News item added and pushed to GitHub"}, 200)
            else:
                self.send_json_response({"success": True, "message": "News item added (Git push failed - changes saved locally)"}, 200)
        except Exception as e:
            self.send_json_response({"success": False, "error": str(e)}, 500)
    
    def handle_update_news(self, data):
        """Update an existing news item."""
        try:
            with open(NEWS_FILE, 'r') as f:
                news = json.load(f)
            
            required = ['id', 'oldId', 'title', 'date']
            if not all(field in data and data[field] for field in required):
                self.send_json_response({"success": False, "error": "Missing required fields"}, 400)
                return
            
            if data['oldId'] not in news:
                self.send_json_response({"success": False, "error": "News item not found"}, 404)
                return
            
            old_id = data['oldId']
            new_id = data['id']
            
            news[new_id] = {
                'title': data['title'],
                'date': data['date'],
                'summary': data.get('summary', ''),
                'content': data.get('content', ''),
                'image': data.get('image', None),
                'featured': data.get('featured', False)
            }
            
            if old_id != new_id:
                del news[old_id]
            
            with open(NEWS_FILE, 'w') as f:
                json.dump(news, f, indent=2)
            
            git_success = self.commit_news_to_github("Update", data['title'])
            
            if git_success:
                self.send_json_response({"success": True, "message": "News item updated and pushed to GitHub"}, 200)
            else:
                self.send_json_response({"success": True, "message": "News item updated (Git push failed - changes saved locally)"}, 200)
        except Exception as e:
            self.send_json_response({"success": False, "error": str(e)}, 500)
    
    def handle_delete_news(self, data):
        """Delete a news item from news.json."""
        try:
            with open(NEWS_FILE, 'r') as f:
                news = json.load(f)
            
            if 'id' not in data:
                self.send_json_response({"success": False, "error": "News ID required"}, 400)
                return
            
            if data['id'] not in news:
                self.send_json_response({"success": False, "error": "News item not found"}, 404)
                return
            
            news_title = news[data['id']]['title']
            del news[data['id']]
            
            with open(NEWS_FILE, 'w') as f:
                json.dump(news, f, indent=2)
            
            git_success = self.commit_news_to_github("Delete", news_title)
            
            if git_success:
                self.send_json_response({"success": True, "message": "News item deleted and pushed to GitHub"}, 200)
            else:
                self.send_json_response({"success": True, "message": "News item deleted (Git push failed - changes saved locally)"}, 200)
        except Exception as e:
            self.send_json_response({"success": False, "error": str(e)}, 500)
    
    def send_json_response(self, data, status_code=200):
        """Send a JSON response."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response_text = json.dumps(data)
        self.send_header('Content-Length', str(len(response_text.encode())))
        self.end_headers()
        self.wfile.write(response_text.encode())
    
    def commit_to_github(self, action, beer_name):
        """Commit beers.json changes to GitHub."""
        try:
            # Check if we're in a git repository
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                cwd=STATIC_DIR,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                # Not a git repo, skip commit
                print(f"Git: not a git repo, skipping commit")
                return False
            
            # Stage beers.json
            add_result = subprocess.run(
                ['git', 'add', 'beers.json'],
                cwd=STATIC_DIR,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if add_result.returncode != 0:
                print(f"Git: failed to stage beers.json: {add_result.stderr}")
                return False
            
            # Create commit message
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            commit_msg = f"{action} beer: {beer_name} ({timestamp})"
            
            # Commit changes
            commit_result = subprocess.run(
                ['git', 'commit', '-m', commit_msg],
                cwd=STATIC_DIR,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if commit_result.returncode != 0:
                # Nothing to commit or error
                print(f"Git: nothing to commit or error: {commit_result.stderr}")
                return False
            
            print(f"Git: committed {beer_name}")
            
            # Push to GitHub (requires proper git setup)
            push_result = subprocess.run(
                ['git', 'push'],
                cwd=STATIC_DIR,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if push_result.returncode == 0:
                print(f"Git: pushed successfully")
                return True
            else:
                print(f"Git: push failed: {push_result.stderr}")
                return False
        
        except subprocess.TimeoutExpired:
            # Git operation timed out, but changes were saved locally
            return False
        except Exception as e:
            # Log error but don't fail the beer operation
            print(f"Git commit error: {e}", file=sys.stderr)
            return False
    
    def commit_news_to_github(self, action, news_title):
        """Commit news.json changes to GitHub."""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                cwd=STATIC_DIR,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                print(f"Git: not a git repo, skipping commit")
                return False
            
            add_result = subprocess.run(
                ['git', 'add', 'news.json'],
                cwd=STATIC_DIR,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if add_result.returncode != 0:
                print(f"Git: failed to stage news.json: {add_result.stderr}")
                return False
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            commit_msg = f"{action} news: {news_title} ({timestamp})"
            
            commit_result = subprocess.run(
                ['git', 'commit', '-m', commit_msg],
                cwd=STATIC_DIR,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if commit_result.returncode != 0:
                print(f"Git: nothing to commit or error: {commit_result.stderr}")
                return False
            
            print(f"Git: committed news {news_title}")
            
            push_result = subprocess.run(
                ['git', 'push'],
                cwd=STATIC_DIR,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if push_result.returncode == 0:
                print(f"Git: pushed successfully")
                return True
            else:
                print(f"Git: push failed: {push_result.stderr}")
                return False
        
        except subprocess.TimeoutExpired:
            return False
        except Exception as e:
            print(f"Git commit error: {e}", file=sys.stderr)
            return False
    
    def end_headers(self):
        """Add CORS headers to all responses."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
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
    print(f"  Website: http://localhost:{PORT}")
    print(f"  Admin Panel: http://localhost:{PORT}/admin")
    print(f"")
    print(f"Admin password: {'Set via ADMIN_PASSWORD env var' if 'ADMIN_PASSWORD' in os.environ else '(using default - change in production!)'}")
    print(f"")
    print(f"Press Ctrl+C to stop")
    print(f"=" * 50)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        server.server_close()
