#!/usr/bin/env python3
"""
Fetch new messages from Slack and update changelog-data.json
"""

import os
import json
import re
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Configuration
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_CHANNEL_ID = os.environ.get('SLACK_CHANNEL_ID', 'C05J9RTC9K6')
CHANGELOG_FILE = 'changelog-data.json'

# How far back to look for messages (in hours)
# Check last 8 hours to catch messages between 8am and 4pm runs
LOOKBACK_HOURS = 8

def get_slack_messages():
    """Fetch recent messages from Slack channel"""
    client = WebClient(token=SLACK_BOT_TOKEN)
    
    # Calculate timestamp for lookback period
    oldest_timestamp = (datetime.now() - timedelta(hours=LOOKBACK_HOURS)).timestamp()
    
    try:
        response = client.conversations_history(
            channel=SLACK_CHANNEL_ID,
            oldest=str(oldest_timestamp),
            limit=100
        )
        
        messages = response['messages']
        print(f"✅ Found {len(messages)} messages in the last {LOOKBACK_HOURS} hours")
        return messages, client
        
    except SlackApiError as e:
        print(f"❌ Error fetching messages: {e.response['error']}")
        return [], None

def get_thread_context(client, channel_id, thread_ts):
    """Fetch thread replies to get additional context"""
    try:
        response = client.conversations_replies(
            channel=channel_id,
            ts=thread_ts,
            limit=50
        )
        
        # Exclude the parent message (first message)
        replies = response['messages'][1:] if len(response['messages']) > 1 else []
        
        if replies:
            print(f"   📎 Found {len(replies)} thread replies")
        
        return replies
        
    except SlackApiError as e:
        print(f"   ⚠️  Could not fetch thread: {e.response['error']}")
        return []

def parse_message_to_entry(message, channel_id, thread_replies=None):
    """Parse a Slack message into a changelog entry, including thread context"""
    text = message.get('text', '')
    ts = message.get('ts', '')
    
    # Skip if message doesn't look like a changelog entry
    # Look for common patterns like "TL;DR:" or structured updates
    if 'TL;DR:' not in text and 'TLDR:' not in text:
        return None
    
    # Combine main message with thread context for better filtering and parsing
    full_context = text
    if thread_replies:
        thread_text = '\n'.join([reply.get('text', '') for reply in thread_replies])
        full_context = f"{text}\n\nThread context:\n{thread_text}"
    
    # FILTER 1: Must contain "Sprout" (case-insensitive) - check full context
    if 'sprout' not in full_context.lower():
        print(f"⏭️  Skipping: No 'Sprout' mention")
        return None
    
    # FILTER 2: Ignore messages containing "spam" (case-insensitive)
    if 'spam' in full_context.lower():
        print(f"⏭️  Skipping: Contains 'spam'")
        return None
    
    # FILTER 3: Ignore messages asking for help (common help patterns)
    help_patterns = [
        'help with',
        'help me',
        'can someone help',
        'need help',
        'anyone know',
        'how do i',
        'how to',
        'question:',
        'asking for help'
    ]
    context_lower = full_context.lower()
    if any(pattern in context_lower for pattern in help_patterns):
        print(f"⏭️  Skipping: Help request detected")
        return None
    
    # Extract TL;DR from main message
    tldr_match = re.search(r'(?:TL;DR:|TLDR:)\s*(.+?)(?:\n|$)', text, re.IGNORECASE | re.DOTALL)
    tldr = tldr_match.group(1).strip() if tldr_match else text[:200]
    
    # Check thread for corrections or important updates
    if thread_replies:
        # Look for corrections, clarifications, or updates in thread
        correction_keywords = ['actually', 'correction:', 'update:', 'clarification:', 
                               'incorrect', 'should note', 'checking with', 'waiting for',
                               'not quite', 'to clarify']
        
        for reply in thread_replies:
            reply_text = reply.get('text', '').lower()
            if any(keyword in reply_text for keyword in correction_keywords):
                # Append important thread context to TL;DR
                thread_note = reply.get('text', '')[:200]  # First 200 chars of correction
                tldr += f" [Note from thread: {thread_note}]"
                print(f"   ⚠️  Added thread context with correction/clarification")
                break
    
    # Extract Action (if present) - check both main message and thread
    action_match = re.search(r'(?:Action:|ACTION:)\s*(.+?)(?:\n|$)', text, re.IGNORECASE | re.DOTALL)
    action = action_match.group(1).strip() if action_match else ""
    
    # Also check thread for action items
    if not action and thread_replies:
        for reply in thread_replies:
            action_in_thread = re.search(r'(?:Action:|ACTION:)\s*(.+?)(?:\n|$)', 
                                        reply.get('text', ''), re.IGNORECASE | re.DOTALL)
            if action_in_thread:
                action = action_in_thread.group(1).strip()
                break
    
    # Get timestamp and convert to date
    msg_timestamp = float(ts)
    msg_date = datetime.fromtimestamp(msg_timestamp)
    
    # Generate Slack URL
    ts_for_url = ts.replace('.', '')
    slack_url = f"https://shopify.slack.com/archives/{channel_id}/p{ts_for_url}"
    
    # Determine month
    month = msg_date.strftime('%B').lower()
    year = str(msg_date.year)
    date_str = msg_date.strftime('%B %d, %Y')
    
    entry = {
        "month": month,
        "year": year,
        "date": date_str,
        "tldr": tldr,
        "action": action,
        "slackUrl": slack_url
    }
    
    return entry

def load_changelog():
    """Load existing changelog data"""
    try:
        with open(CHANGELOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  {CHANGELOG_FILE} not found, creating new one")
        return {"entries": []}

def save_changelog(data):
    """Save changelog data"""
    with open(CHANGELOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {CHANGELOG_FILE}")

def entry_exists(entries, slack_url):
    """Check if an entry with this Slack URL already exists"""
    return any(entry.get('slackUrl') == slack_url for entry in entries)

def main():
    print("🤖 Starting Slack changelog update...")
    print(f"📅 Looking back {LOOKBACK_HOURS} hours")
    
    if not SLACK_BOT_TOKEN:
        print("❌ Error: SLACK_BOT_TOKEN environment variable not set")
        return
    
    # Fetch messages
    messages, client = get_slack_messages()
    
    if not messages or not client:
        print("ℹ️  No new messages found")
        return
    
    # Load existing changelog
    changelog = load_changelog()
    existing_entries = changelog.get('entries', [])
    
    # Process messages
    new_entries = []
    for message in messages:
        # Check if message has thread replies
        thread_replies = None
        reply_count = message.get('reply_count', 0)
        
        if reply_count > 0:
            print(f"🧵 Message has {reply_count} replies, fetching thread context...")
            thread_replies = get_thread_context(client, SLACK_CHANNEL_ID, message.get('ts'))
        
        # Parse message with thread context
        entry = parse_message_to_entry(message, SLACK_CHANNEL_ID, thread_replies)
        
        if entry and not entry_exists(existing_entries, entry['slackUrl']):
            new_entries.append(entry)
            print(f"✨ New entry: {entry['date']} - {entry['tldr'][:50]}...")
    
    if new_entries:
        # Add new entries to the beginning of the list (most recent first)
        changelog['entries'] = new_entries + existing_entries
        save_changelog(changelog)
        print(f"✅ Added {len(new_entries)} new entries to changelog")
    else:
        print("ℹ️  No new changelog entries to add")

if __name__ == '__main__':
    main()

