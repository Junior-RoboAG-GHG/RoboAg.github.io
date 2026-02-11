import webuntis

try:
    s = webuntis.Session(
        username='S4936',
        password='teny8.WebUntis',
        server='cissa.webuntis.com',
        school='Georg-herwegh-gym',
        useragent='Mozilla/5.0'
    )
    s.login()
    print("Login successful!")
    s.logout()
except Exception as e:
    print(f"Login failed: {e}")
