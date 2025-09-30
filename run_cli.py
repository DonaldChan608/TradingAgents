#!/usr/bin/env python3
"""
Entry point script for TradingAgents CLI.
This script ensures proper package imports when running from the project root.
"""

import sys
import os
from pathlib import Path

def main():
    
    try:
        # Import and run the CLI
        from cli.main import app
        print("✓ Successfully imported CLI app")
        
        # Run the CLI with all command line arguments
        app()
        
    except ImportError as e:
        print(f"✗ Failed to import CLI app: {e}")
        print("Make sure all dependencies are installed and the project structure is correct.")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
