#!/usr/bin/env python3
"""
Simple Web Interface Launcher for Daily Vocabulary Bot
Single launcher script - no confusion, just run this!
"""

import sys
import os

def main():
    """Launch the web interface."""
    print("🌐 Daily Vocabulary Bot - Web Interface")
    print("=" * 50)
    print("📱 Opening web interface...")
    print("🔧 Configure your bot settings at: http://localhost:5000")
    print("\n⏹️ Press Ctrl+C to stop the web server")
    print("-" * 50)
    
    try:
        # Import and run the web interface
        from web_interface import app
        app.run(debug=False, host='127.0.0.1', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Web interface stopped. Goodbye!")
    except ImportError as e:
        print(f"\n❌ Error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"\n❌ Error starting web interface: {e}")
        print("💡 Check the logs for more details")

if __name__ == "__main__":
    main()



