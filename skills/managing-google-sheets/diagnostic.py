import requests

URL = "https://script.google.com/macros/s/AKfycbyu7QJDGVfU0uJn-BDvayEEtb2USJkze7oTbWwPYHkKkjVutV8jXRL9ETBYCY6rotfXQA/exec?action=check&pwd=12345"

def check_access():
    try:
        # Don't follow redirects so we can see where it's trying to send us
        response = requests.get(URL, allow_redirects=False)
        print(f"Status: {response.status_code}")
        print(f"Location Header: {response.headers.get('Location')}")
        
        # Now follow them to see final content
        full_res = requests.get(URL)
        if "ServiceLogin" in full_res.text or "accounts.google.com" in full_res.text:
            print("RESULT: LOCKED. The script is still requiring a Google Login.")
        else:
            print("RESULT: OPEN. The script is accessible.")
            print(f"Content Sample: {full_res.text[:100]}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_access()
