"""
Google OAuth2 Setup Script

This script helps you authenticate with Google APIs and generate the necessary
token.json file for accessing Calendar, Gmail, Tasks, and Photos APIs.

SETUP INSTRUCTIONS:
1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Create a new project (or select existing)
3. Enable these APIs:
   - Google Calendar API
   - Gmail API
   - Google Tasks API
   - Google Photos Library API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Select "Desktop application"
6. Download the JSON file and save as 'credentials.json' in this folder
7. Run this script: python setup_google_auth.py
"""

import os
import json
from pathlib import Path

# Check if google packages are installed
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    print("❌ Required packages not installed. Run:")
    print("   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    exit(1)

# Scopes required for all our APIs
SCOPES = [
    # Calendar - full access to create/read/update/delete events
    'https://www.googleapis.com/auth/calendar',
    
    # Gmail - compose and manage drafts
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/gmail.modify',
    
    # Tasks - full access to manage tasks
    'https://www.googleapis.com/auth/tasks',
    
    # Photos - read access to search and view photos
    'https://www.googleapis.com/auth/photoslibrary.readonly',
]

CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'


def main():
    """Run the OAuth2 flow to generate token.json"""
    
    print("=" * 60)
    print("Google API Authentication Setup")
    print("=" * 60)
    
    # Check if credentials.json exists
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"\n❌ Error: '{CREDENTIALS_FILE}' not found!")
        print("\nPlease follow these steps:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create or select a project")
        print("3. Enable: Calendar API, Gmail API, Tasks API, Photos Library API")
        print("4. Go to Credentials → Create Credentials → OAuth 2.0 Client ID")
        print("5. Select 'Desktop application'")
        print("6. Download JSON and save as 'credentials.json' in this folder")
        print(f"7. Run this script again")
        return
    
    creds = None
    
    # Check if we already have a token
    if os.path.exists(TOKEN_FILE):
        print(f"\n📄 Found existing {TOKEN_FILE}")
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        
        if creds and creds.valid:
            print("✅ Token is still valid!")
            print_token_info(creds)
            return
        
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Token expired, attempting to refresh...")
            try:
                creds.refresh(Request())
                print("✅ Token refreshed successfully!")
            except Exception as e:
                print(f"❌ Failed to refresh: {e}")
                print("Will need to re-authenticate...")
                creds = None
    
    # Run OAuth flow if needed
    if not creds or not creds.valid:
        print("\n🔐 Starting OAuth2 authentication flow...")
        print("   A browser window will open for you to sign in with Google.")
        print("")
        
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)  # Use any available port
        
        # Save the credentials
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        
        print(f"\n✅ Authentication successful!")
        print(f"   Token saved to: {TOKEN_FILE}")
    
    print_token_info(creds)
    
    # Test the APIs
    print("\n" + "=" * 60)
    print("Testing API Access...")
    print("=" * 60)
    test_apis(creds)


def print_token_info(creds):
    """Print information about the token"""
    print("\n📋 Token Information:")
    print(f"   Valid: {creds.valid}")
    print(f"   Expired: {creds.expired if hasattr(creds, 'expired') else 'N/A'}")
    if hasattr(creds, 'expiry') and creds.expiry:
        print(f"   Expiry: {creds.expiry}")
    print(f"   Scopes: {len(SCOPES)} APIs authorized")


def test_apis(creds):
    """Test that we can access each API"""
    from googleapiclient.discovery import build
    
    # Test Calendar API
    print("\n1️⃣  Testing Google Calendar API...")
    try:
        service = build('calendar', 'v3', credentials=creds)
        calendars = service.calendarList().list(maxResults=3).execute()
        print(f"   ✅ Calendar API works! Found {len(calendars.get('items', []))} calendars")
        for cal in calendars.get('items', [])[:2]:
            print(f"      - {cal.get('summary', 'Unnamed')}")
    except Exception as e:
        print(f"   ❌ Calendar API error: {e}")
    
    # Test Gmail API
    print("\n2️⃣  Testing Gmail API...")
    try:
        service = build('gmail', 'v1', credentials=creds)
        profile = service.users().getProfile(userId='me').execute()
        print(f"   ✅ Gmail API works! Email: {profile.get('emailAddress')}")
    except Exception as e:
        print(f"   ❌ Gmail API error: {e}")
    
    # Test Tasks API
    print("\n3️⃣  Testing Google Tasks API...")
    try:
        service = build('tasks', 'v1', credentials=creds)
        tasklists = service.tasklists().list(maxResults=3).execute()
        print(f"   ✅ Tasks API works! Found {len(tasklists.get('items', []))} task lists")
        for tl in tasklists.get('items', [])[:2]:
            print(f"      - {tl.get('title', 'Unnamed')}")
    except Exception as e:
        print(f"   ❌ Tasks API error: {e}")
    
    # Test Photos API
    print("\n4️⃣  Testing Google Photos API...")
    try:
        service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)
        # Just test that we can make a request
        albums = service.albums().list(pageSize=3).execute()
        print(f"   ✅ Photos API works! Found {len(albums.get('albums', []))} albums")
        for album in albums.get('albums', [])[:2]:
            print(f"      - {album.get('title', 'Unnamed')}")
    except Exception as e:
        print(f"   ❌ Photos API error: {e}")
    
    print("\n" + "=" * 60)
    print("Setup complete! You can now use the Life Admin Agent.")
    print("=" * 60)


if __name__ == '__main__':
    main()
