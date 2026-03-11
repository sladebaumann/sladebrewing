#!/usr/bin/env python3
"""
Simple web server for Slade Brewing website.
Serves static files and provides an API endpoint to enrich beers.json with Untappd data.

Run with: python3 server.py
Then visit: http://localhost:8000
"""

import json
import os
import subprocess
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Configuration
PORT = 8000
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))


class SladBrewingHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler for Slade Brewing site."""
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        
        # API endpoint to enrich beers
        if parsed_path.path == "/api/enrich-beers":
            self.handle_enrich_beers()
            return
        
        # API endpoint to get beers data
        if parsed_path.path == "/api/beers":
            self.handle_get_beers()
            return
        
        # Serve static files
        super().do_GET()
    
    def handle_enrich_beers(self):
        """Run the enrichment script and return results."""
        # Check if credentials are set
        if not os.getenv("UNTAPPD_CLIENT_ID") or not os.getenv("UNTAPPD_CLIENT_SECRET"):
            self.send_json_response({
                "success": False,
                "error": "UNTAPPD_CLIENT_ID and UNTAPPD_CLIENT_SECRET environment variables not set",
                "message": "See README for setup instructions"
            }, 400)
            return
        
        try:
            # Run the enrichment script
            result = subprocess.run(
                [sys.executable, "enrich_beers.py"],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=STATIC_DIR
            )
            
            if result.returncode == 0:
                self.send_json_response({
                    "success": True,
                    "message": "Successfully enriched beers.json with Untappd data",
                    "output": result.stdout
                }, 200)
            else:
                self.send_json_response({
                    "success": False,
                    "error": result.stderr,
                    "output": result.stdout
                }, 500)
        except subprocess.TimeoutExpired:
            self.send_json_response({
                "success": False,
                "error": "Enrichment script timed out"
            }, 500)
        except Exception as e:
            self.send_json_response({
                "success": False,
                "error": str(e)
            }, 500)
    
    def handle_get_beers(self):
        """Return the current beers.json data."""
        try:
            with open("beers.json", "r") as f:
                beers = json.load(f)
            self.send_json_response({"success": True, "beers": beers}, 200)
        except FileNotFoundError:
            self.send_json_response({
                "success": False,
                "error": "beers.json not found"
            }, 404)
        except json.JSONDecodeError:
            self.send_json_response({
                "success": False,
                "error": "Invalid JSON in beers.json"
            }, 500)
        except Exception as e:
            self.send_json_response({
                "success": False,
                "error": str(e)
            }, 500)
    
    def send_json_response(self, data, status_code=200):
        """Send a JSON response."""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def end_headers(self):
        """Add CORS headers to all responses."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


if __name__ == "__main__":
    os.chdir(STATIC_DIR)
    
    server = HTTPServer(("localhost", PORT), SladBrewingHandler)
    print(f"Slade Brewing Website Server")
    print(f"============================")
    print(f"Starting server at http://localhost:{PORT}")
    print(f"Press Ctrl+C to stop")
    print()
    print(f"Available endpoints:")
    print(f"  GET  http://localhost:{PORT}/ - Main website")
    print(f"  GET  http://localhost:{PORT}/api/beers - Current beers data")
    print(f"  GET  http://localhost:{PORT}/api/enrich-beers - Enrich from Untappd")
    print()
    print(f"Setup for Untappd enrichment:")
    print(f"  1. Create app at https://untappd.com/api")
    print(f"  2. export UNTAPPD_CLIENT_ID='your_client_id'")
    print(f"  3. export UNTAPPD_CLIENT_SECRET='your_client_secret'")
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        server.server_close()
