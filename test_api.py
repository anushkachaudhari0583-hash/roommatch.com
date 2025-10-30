#!/usr/bin/env python3
"""
Test script for Roommatch Backend API
Run this script to test all the API endpoints
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:5000/api"
TEST_EMAIL = "test@roommatch.com"
TEST_PASSWORD = "testpassword123"

def test_endpoint(method, endpoint, data=None, headers=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers)
        
        print(f"\n{method.upper()} {endpoint}")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        return response
        
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Connection Error: Make sure the Flask server is running on {BASE_URL}")
        return None
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

def main():
    """Run all API tests"""
    print("🧪 Testing Roommatch Backend API")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check")
    health_response = test_endpoint("GET", "/health")
    if not health_response or health_response.status_code != 200:
        print("❌ Health check failed. Make sure the server is running.")
        sys.exit(1)
    
    # Test 2: Register User
    print("\n2️⃣ Testing User Registration")
    register_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "first_name": "Test",
        "last_name": "User",
        "phone": "+1234567890"
    }
    register_response = test_endpoint("POST", "/auth/register", register_data)
    
    if not register_response or register_response.status_code not in [200, 201]:
        print("❌ Registration failed")
        return
    
    # Extract access token
    access_token = register_response.json().get("access_token")
    if not access_token:
        print("❌ No access token received")
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Test 3: Login
    print("\n3️⃣ Testing User Login")
    login_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    login_response = test_endpoint("POST", "/auth/login", login_data)
    
    # Test 4: Get Profile (should be empty initially)
    print("\n4️⃣ Testing Get Profile")
    profile_response = test_endpoint("GET", "/profile", headers=headers)
    
    # Test 5: Create Profile
    print("\n5️⃣ Testing Profile Creation")
    profile_data = {
        "age": 25,
        "gender": "Non-binary",
        "occupation": "Software Developer",
        "education": "Bachelor's Degree",
        "budget_min": 800,
        "budget_max": 1200,
        "location_preference": "Downtown",
        "room_type": "shared",
        "cleanliness_level": 4,
        "social_level": 3,
        "noise_tolerance": 3,
        "pet_preference": "yes",
        "smoking_preference": "no",
        "bio": "I'm a friendly software developer looking for a compatible roommate!",
        "lifestyle_preferences": {
            "wake_up_time": "7:00 AM",
            "sleep_time": "11:00 PM",
            "cooking_frequency": "daily",
            "guest_policy": "occasional"
        },
        "interests": ["coding", "hiking", "cooking", "movies"],
        "deal_breakers": ["smoking", "loud parties", "messy roommates"]
    }
    create_profile_response = test_endpoint("POST", "/profile", profile_data, headers)
    
    # Test 6: Get Updated Profile
    print("\n6️⃣ Testing Get Updated Profile")
    updated_profile_response = test_endpoint("GET", "/profile", headers=headers)
    
    # Test 7: Join Waitlist (without authentication)
    print("\n7️⃣ Testing Waitlist Signup")
    waitlist_data = {
        "email": "waitlist@example.com",
        "name": "Waitlist User"
    }
    waitlist_response = test_endpoint("POST", "/waitlist", waitlist_data)
    
    # Test 8: Generate Matches
    print("\n8️⃣ Testing Match Generation")
    matches_response = test_endpoint("POST", "/matches/generate", headers=headers)
    
    # Test 9: Get Matches
    print("\n9️⃣ Testing Get Matches")
    get_matches_response = test_endpoint("GET", "/matches", headers=headers)
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("\n📝 Next Steps:")
    print("1. Create more test users to see matches")
    print("2. Test the frontend integration")
    print("3. Deploy to production")

if __name__ == "__main__":
    main()
