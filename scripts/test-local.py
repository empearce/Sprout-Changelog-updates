#!/usr/bin/env python3
"""
Test script for local development - manually add a test entry
"""

import json
from datetime import datetime

def add_test_entry():
    """Add a test changelog entry"""
    
    # Load existing changelog
    with open('changelog-data.json', 'r') as f:
        changelog = json.load(f)
    
    # Create test entry
    now = datetime.now()
    test_entry = {
        "month": now.strftime('%B').lower(),
        "year": str(now.year),
        "date": now.strftime('%B %d, %Y'),
        "tldr": "🧪 TEST ENTRY - This is a test entry created locally for testing purposes.",
        "action": "This is a test action item to verify the automation is working correctly.",
        "slackUrl": "https://shopify.slack.com/archives/C05J9RTC9K6/p0000000000000000"
    }
    
    # Add to beginning of entries
    changelog['entries'].insert(0, test_entry)
    
    # Save
    with open('changelog-data.json', 'w') as f:
        json.dump(changelog, f, indent=2, ensure_ascii=False)
    
    print("✅ Test entry added!")
    print(f"📅 Date: {test_entry['date']}")
    print(f"📝 TL;DR: {test_entry['tldr']}")
    print("\n⚠️  Remember to remove this test entry before deploying!")

if __name__ == '__main__':
    add_test_entry()

