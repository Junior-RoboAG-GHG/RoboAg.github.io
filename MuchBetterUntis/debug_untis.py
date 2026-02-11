import requests
import json

url = "https://cissa.webuntis.com/WebUntis/jsonrpc.do?school=Georg-herwegh-gym"

payload = {
    "id": "1",
    "method": "authenticate",
    "params": {
        "user": "S4936",
        "password": "teny8.WebUntis",
        "client": "BetterUntis"
    },
    "jsonrpc": "2.0"
}

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    print(f"Response Content: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
