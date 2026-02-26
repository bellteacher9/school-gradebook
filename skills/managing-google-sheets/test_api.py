import requests
import json

API_URL = "https://script.google.com/macros/s/AKfycbyu7QJDGVfU0uJn-BDvayEEtb2USJkze7oTbWwPYHkKkjVutV8jXRL9ETBYCY6rotfXQA/exec"

def test_api():
    params = {
        "action": "check",
        "pwd": "12345"
    }
    try:
        print(f"Testing URL: {API_URL}")
        response = requests.get(API_URL, params=params, allow_redirects=True)
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        try:
            data = response.json()
            print("Parsed JSON:", json.dumps(data, indent=2))
        except:
            print("Failed to parse JSON response.")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_api()
