import getpass 
import json
import urllib.request
from http.client import HTTPSConnection
from base64 import b64encode

username = "justintime50"

# Build the authentication header
password = getpass.getpass(prompt="Token: ")
conn = HTTPSConnection("api.github.com")
b64userpassword = b64encode(bytes(username + ":" + password, encoding='ascii')).decode("ascii")
headers = {'Authorization': 'Basic %s' %  b64userpassword,
            'User-Agent': 'request'}

# Grab repos
# TODO: allow for multiple pages (over 100 results)
url = "/user/repos?page=1&per_page=100&affiliation=owner"
conn.request('GET', url, headers=headers)
res = conn.getresponse()
print(res.status, res.reason)
res_str = res.read()
repos = json.loads(res_str)

# Grab languages and print
for repo in repos:
    name = repo["name"]
    langs_url = repo['languages_url'].replace('https://api.github.com', '')
    conn.request('GET', langs_url, headers=headers)
    res = conn.getresponse()
    res_str = res.read()
    langs = json.loads(res_str)

    t = sum(langs.values())
    percentages = {}
    for k, v in langs.items():
        percentages[k] = (v / t) * 100
    print(name, langs)
