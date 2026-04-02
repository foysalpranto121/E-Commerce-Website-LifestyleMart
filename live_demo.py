"""
Live Demo Script - Run this to get a public URL for your teacher
"""
import os
import sys
import time
from pyngrok import ngrok

# Start ngrok tunnel
print("=" * 60)
print("LIFESTYLE MART - Live Demo")
print("=" * 60)
print("\nStarting server and creating public URL...")
print("(This will give you a link to show your teacher)\n")

# Kill any existing ngrok processes
os.system("taskkill /f /im ngrok.exe 2>nul")

# Start the tunnel on port 5000
try:
    public_url = ngrok.connect(5000, "http")
    print("✅ SUCCESS! Your public URL is:")
    print("=" * 60)
    print(f"\n{public_url}\n")
    print("=" * 60)
    print("\nShare this URL with your teacher!")
    print("The server is running locally on port 5000")
    print("\nLogin Credentials:")
    print("  Admin: admin@lifestylemart.com / admin123")
    print("  User:  john@example.com / password123")
    print("\nPress CTRL+C to stop the server")
    print("=" * 60 + "\n")
    
    # Import and run the Flask app
    from app import app
    app.run(debug=False, host='0.0.0.0', port=5000)
    
except KeyboardInterrupt:
    print("\n\nShutting down...")
    ngrok.kill()
    sys.exit(0)
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTrying alternative method...")
    # Just run the app locally
    from app import app
    print("\nServer running at: http://localhost:5000")
    app.run(debug=False, host='0.0.0.0', port=5000)
