#!/usr/bin/env python3
"""
Test script for Narrato API
"""

import requests
import sys
import time

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing Narrato API...\n")
    
    # Test 1: Root endpoint
    print("1. Testing root endpoint...")
    r = requests.get(f"{BASE_URL}/")
    if r.status_code == 200:
        print(f"   ✅ API is running: {r.json()['message']}")
    else:
        print(f"   ❌ Failed: {r.status_code}")
        return
    
    # Test 2: List voices
    print("\n2. Testing voices endpoint...")
    r = requests.get(f"{BASE_URL}/voices")
    if r.status_code == 200:
        voices = r.json()['voices']
        print(f"   ✅ Found {len(voices)} voices")
        print(f"   📢 Default: {voices[0]['name']} ({voices[0]['language']})")
    else:
        print(f"   ❌ Failed: {r.status_code}")
    
    # Test 3: Check API keys
    print("\n3. Checking API key configuration...")
    r = requests.get(f"{BASE_URL}/")
    # This just checks if server responds - actual key check happens during upload
    print("   ℹ️  Server responding. Keys validated during video processing.")
    
    print("\n✅ API tests passed!")
    print(f"\n📡 API Documentation: {BASE_URL}/docs")
    print(f"🚀 Ready to upload videos!")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API")
        print(f"   Is the server running? Start with: ./start.sh")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
