import requests

def search_school(name):
    url = f"https://mobile.webuntis.com/ms/schoolquery2?searchString={name}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            schools = data.get("result", {}).get("schools", [])
            for s in schools:
                print(f"School: {s.get('displayName')} | ID: {s.get('loginName')} | Server: {s.get('serverName')}")
        else:
            print(f"HTTP {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")

search_school("Georg-Herwegh")
search_school("Herwegh")
search_school("Reinickendorf") # GHG is in Reinickendorf
