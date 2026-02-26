import requests
import json

API_URL = "https://script.google.com/macros/s/AKfycbxVwldwWQMt9Gs9-T2l49beZLud5TCOYkAgeORnsFCORu8awMhaE4v9bNzcaBFOWgK9UQ/exec"

def check_term_dates():
    params = {
        "action": "fetch",
        "year": "2026",
        "pwd": "12345"
    }
    try:
        response = requests.get(API_URL, params=params)
        data = response.json()
        if data['success']:
            term_dates = data['data'].get('admin_term_dates', {})
            print(json.dumps(term_dates, indent=2))
        else:
            print(f"API Error: {data.get('error')}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    check_term_dates()
