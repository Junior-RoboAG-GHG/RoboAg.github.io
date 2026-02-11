import requests

def check_school(server, name):
    url = f"https://{server}/WebUntis/jsonrpc.do?school={name}"
    payload = {
        "id": "1",
        "method": "getAgencies",
        "params": {},
        "jsonrpc": "2.0"
    }
    try:
        r = requests.post(url, json=payload, timeout=3)
        if r.status_code == 200:
            return True, "Found!"
        return False, f"HTTP {r.status_code}"
    except:
        return False, "Timeout/Error"

clusters = ["cissa", "mese", "titan", "nephila", "hepta", "hektos", "buse", "vula", "poly", "web"]
name = "Georg-herwegh-gym"

for c in clusters:
    server = f"{c}.webuntis.com"
    ok, msg = check_school(server, name)
    if ok:
        print(f"SUCCESS: {server} | {name} -> {msg}")
    else:
        print(f"FAILED: {server} | {name} -> {msg}")
