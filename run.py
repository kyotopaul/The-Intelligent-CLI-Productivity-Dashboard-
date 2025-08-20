# run.py
#!/usr/bin/env python3
"""
Main entry point for the Productivity Dashboard
"""
import sys
import os

# Add the package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'productivity_dashboard'))

from productivity_dashboard.dashboard import ProductivityDashboard

def main():
    """Main function to run the dashboard"""
    dashboard = ProductivityDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()