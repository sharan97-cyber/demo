#!/usr/bin/env python3
"""
Simple Python application - Data processor
"""

import json
from datetime import datetime

def process_data():
    """Process sample data and return results"""
    data = {
        "timestamp": datetime.now().isoformat(),
        "status": "success",
        "message": "Python application executed successfully",
        "items_processed": 42,
        "output_file": "output.json"
    }
    return data

def write_output(data):
    """Write processed data to file"""
    with open("output.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"✓ Output written to output.json")

def main():
    print("Starting Python application...")
    data = process_data()
    write_output(data)
    print(f"✓ Status: {data['status']}")
    print(f"✓ Timestamp: {data['timestamp']}")
    print(f"✓ Items processed: {data['items_processed']}")

if __name__ == "__main__":
    main()
