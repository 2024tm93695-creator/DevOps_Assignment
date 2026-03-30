import requests
import json

BASE_URL = 'http://localhost:5000'

def test_api():
    print("Testing ACEest Fitness API...")

    # Test root endpoint
    try:
        response = requests.get(f'{BASE_URL}/')
        print(f"Root endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Root endpoint failed: {e}")

    # Test create member
    member_data = {
        "name": "John Doe",
        "age": 30,
        "height": 175.0,
        "weight": 80.0,
        "program": "Fat Loss (FL) – 3 day",
        "target_weight": 75.0,
        "target_adherence": 80
    }

    try:
        response = requests.post(f'{BASE_URL}/api/members', json=member_data)
        print(f"Create member: {response.status_code}")
        if response.status_code == 201:
            member = response.json()
            print(f"Created member: {member['name']}")
            member_id = member['id']

            # Test get member
            response = requests.get(f'{BASE_URL}/api/members/{member_id}')
            print(f"Get member: {response.status_code}")

            # Test member summary
            response = requests.get(f'{BASE_URL}/api/members/{member["name"]}/summary')
            print(f"Member summary: {response.status_code}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Create member failed: {e}")

    # Test create trainer
    trainer_data = {
        "name": "Jane Smith",
        "specialization": "Strength Training",
        "experience_years": 5,
        "email": "jane@example.com"
    }

    try:
        response = requests.post(f'{BASE_URL}/api/members/trainers', json=trainer_data)
        print(f"Create trainer: {response.status_code}")
        if response.status_code == 201:
            print(f"Created trainer: {response.json()['name']}")
    except Exception as e:
        print(f"Create trainer failed: {e}")

    print("API testing completed!")

if __name__ == '__main__':
    test_api()