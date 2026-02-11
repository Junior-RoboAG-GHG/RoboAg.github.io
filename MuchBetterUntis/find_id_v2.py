import requests
import json

def find_school(search_term):
    # This is the endpoint used by the mobile app to find schools
    url = f"https://mobile.webuntis.com/ms/schoolquery2?searchString={search_term}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        r = requests.get(url, headers=headers)
        print(f"Status: {r.status_code}")
        # The response is actually a JSON-RPC-like structure wrapped in a function call sometimes, 
        # or just plain JSON if we are lucky.
        # Actually, schoolquery2 often returns a JSON object.
        try:
            data = r.json()
            if "result" in data and "schools" in data["result"]:
                for s in data["result"]["schools"]:
                    print(f"School: {s.get('displayName')} | ID: {s.get('loginName')} | Server: {s.get('serverName')}")
            else:
                print("No schools found or unexpected JSON structure.")
                print(json.dumps(data, indent=2))
        except:
            print("Failed to parse JSON. Raw response:")
            print(r.text[:500])
    except Exception as e:
        print(f"Request failed: {e}")

print("Searching for 'Georg-Herwegh'...")
find_school("Georg-Herwegh")
print("\nSearching for 'Herwegh'...")
find_school("Herwegh")
