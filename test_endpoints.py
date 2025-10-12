"""
Test script for OMI Twitter Integration endpoints
Run this to verify your deployment is working correctly
"""
import asyncio
import httpx
import json
from typing import Dict

# Configuration
BASE_URL = "http://localhost:8000"  # Change to your deployed URL
TEST_UID = "test_user_123"
TEST_SESSION_ID = "test_session_456"


async def test_health():
    """Test health check endpoint"""
    print("\n🏥 Testing health endpoint...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("✅ Health check passed!")
                print(f"   Response: {response.json()}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False


async def test_root():
    """Test root endpoint"""
    print("\n🏠 Testing root endpoint...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/")
            if response.status_code == 200:
                print("✅ Root endpoint working!")
                data = response.json()
                print(f"   App: {data.get('app')}")
                print(f"   Version: {data.get('version')}")
                return True
            else:
                print(f"❌ Root endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Root endpoint error: {e}")
            return False


async def test_setup_check():
    """Test setup completed endpoint"""
    print("\n🔍 Testing setup-completed endpoint...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}/setup-completed",
                params={"uid": TEST_UID}
            )
            if response.status_code == 200:
                print("✅ Setup check endpoint working!")
                data = response.json()
                print(f"   Setup completed: {data.get('is_setup_completed')}")
                return True
            else:
                print(f"❌ Setup check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Setup check error: {e}")
            return False


async def test_webhook_unauthenticated():
    """Test webhook without authentication"""
    print("\n📡 Testing webhook (unauthenticated)...")
    async with httpx.AsyncClient() as client:
        try:
            payload = [
                {
                    "text": "Tweet Now, This is a test tweet!",
                    "speaker": "SPEAKER_00",
                    "speakerId": 0,
                    "is_user": True,
                    "start": 0.0,
                    "end": 5.0
                }
            ]
            
            response = await client.post(
                f"{BASE_URL}/webhook",
                params={
                    "session_id": TEST_SESSION_ID,
                    "uid": TEST_UID
                },
                json=payload
            )
            
            if response.status_code == 401:
                print("✅ Webhook correctly requires authentication!")
                print(f"   Response: {response.json()}")
                return True
            else:
                print(f"⚠️  Unexpected status: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Webhook test error: {e}")
            return False


async def test_auth_url():
    """Test auth URL (just verify it responds)"""
    print("\n🔐 Testing auth endpoint...")
    async with httpx.AsyncClient(follow_redirects=False) as client:
        try:
            response = await client.get(
                f"{BASE_URL}/auth",
                params={"uid": TEST_UID}
            )
            
            if response.status_code in [302, 307]:
                print("✅ Auth endpoint working (redirects to Twitter)!")
                print(f"   Redirect location: {response.headers.get('location', 'N/A')[:80]}...")
                return True
            else:
                print(f"⚠️  Unexpected status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Auth endpoint error: {e}")
            return False


async def run_all_tests():
    """Run all endpoint tests"""
    print("🚀 Starting OMI Twitter Integration Tests")
    print(f"📍 Testing endpoint: {BASE_URL}")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Health Check", await test_health()))
    results.append(("Root Endpoint", await test_root()))
    results.append(("Setup Check", await test_setup_check()))
    results.append(("Webhook (Unauth)", await test_webhook_unauthenticated()))
    results.append(("Auth URL", await test_auth_url()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your deployment is ready!")
        print("\n📱 Next steps:")
        print("   1. Complete Twitter OAuth by visiting:")
        print(f"      {BASE_URL}/auth?uid=your_omi_uid")
        print("   2. Configure OMI app with these URLs:")
        print(f"      - Webhook: {BASE_URL}/webhook")
        print(f"      - Auth: {BASE_URL}/auth")
        print(f"      - Setup Check: {BASE_URL}/setup-completed")
        print("   3. Start using by saying 'Tweet Now' to your OMI device!")
    else:
        print("\n⚠️  Some tests failed. Please check your configuration.")
        print("   - Verify .env file has all required variables")
        print("   - Ensure the server is running")
        print("   - Check logs for errors")


def main():
    """Main entry point"""
    print("🐦 OMI Twitter Integration - Endpoint Tester")
    print(f"Testing: {BASE_URL}\n")
    
    # Allow user to change URL
    custom_url = input(f"Press Enter to use {BASE_URL}, or enter custom URL: ").strip()
    if custom_url:
        global BASE_URL
        BASE_URL = custom_url.rstrip('/')
    
    # Run tests
    asyncio.run(run_all_tests())


if __name__ == "__main__":
    main()

