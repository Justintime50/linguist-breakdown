import getpass 
import json
import urllib.request
from http.client import HTTPSConnection
from base64 import b64encode

# Configuration (user changeable)
username = "justintime50"
page = "1"
per_page = "100" # must be <=100 per Github's API limits
affiliation = "owner" # owner, collaborator, organization_member OR use all three separated by commas
visibility = "all" # all, public, private

# Build the authentication header
password = getpass.getpass(prompt="Token: ")
conn = HTTPSConnection("api.github.com")
b64userpassword = b64encode(bytes(username + ":" + password, encoding='ascii')).decode("ascii")
headers = {'Authorization': 'Basic %s' %  b64userpassword,
            'User-Agent': 'request'}

# Grab repos
# TODO: allow for multiple pages (over 100 results) by iterating here
url = (f"/user/repos?page={page}&per_page={per_page}&affiliation={affiliation}&visibility={visibility}")
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

    # Get language percentage
    total = sum(langs.values())
    percentages = {}
    for key, value in langs.items():
        percentages[key] = round((value / total) * 100, 2)
    print(name, percentages) # TODO: Add percentage sign
