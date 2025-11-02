"""
Simple test script for Loy Kratong API
Run this after starting the API server with: python test_api.py
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("=" * 50)
    print("Testing Health Check...")
    print("=" * 50)
    try:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        print(f"✓ Health check passed: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_get_all_kratongs():
    """Test getting all kratongs"""
    print("\n" + "=" * 50)
    print("Testing GET /kratong...")
    print("=" * 50)
    try:
        response = requests.get(f"{BASE_URL}/kratong")
        response.raise_for_status()
        data = response.json()
        print(f"✓ Get all kratongs passed")
        print(f"  Found {len(data.get('kratongs', []))} kratongs")
        if data.get('kratongs'):
            print(f"  Sample: {json.dumps(data['kratongs'][0], indent=2, ensure_ascii=False)}")
        return True
    except Exception as e:
        print(f"✗ Get all kratongs failed: {e}")
        return False

def test_create_kratong():
    """Test creating a new kratong"""
    print("\n" + "=" * 50)
    print("Testing POST /kratong...")
    print("=" * 50)
    
    # Create a test kratong with current timestamp
    test_kratong = {
        "id": str(int(datetime.now().timestamp() * 1000)),
        "ownerName": "Test User",
        "wishText": "ขอให้มีความสุข สมหวัง ปลอดภัย 🌕",
        "shapeImg": "/kratong1.png",
        "createdAt": int(datetime.now().timestamp() * 1000)
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/kratong",
            json=test_kratong,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        print(f"✓ Create kratong passed")
        print(f"  Created: {json.dumps(data, indent=2, ensure_ascii=False)}")
        return True, data
    except Exception as e:
        print(f"✗ Create kratong failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"  Response: {e.response.text}")
        return False, None

def main():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("Loy Kratong API Test Suite")
    print("=" * 50)
    print(f"Testing API at: {BASE_URL}")
    print("Make sure the API server is running!")
    print()
    
    results = []
    
    # Test health check
    results.append(("Health Check", test_health_check()))
    
    # Test get all kratongs
    results.append(("Get All Kratongs", test_get_all_kratongs()))
    
    # Test create kratong
    success, created_data = test_create_kratong()
    results.append(("Create Kratong", success))
    
    # Test get all kratongs again to verify the new one is there
    if success:
        print("\n" + "=" * 50)
        print("Verifying created kratong exists...")
        print("=" * 50)
        try:
            response = requests.get(f"{BASE_URL}/kratong")
            response.raise_for_status()
            data = response.json()
            found = any(k.get('id') == created_data.get('id') for k in data.get('kratongs', []))
            if found:
                print("✓ Created kratong found in list")
            else:
                print("✗ Created kratong not found in list")
        except Exception as e:
            print(f"✗ Verification failed: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n" + "=" * 50)
        print("ERROR: Cannot connect to API server")
        print("=" * 50)
        print("Make sure the API is running:")
        print("  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

