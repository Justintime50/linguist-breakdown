import urllib.request
import json

username = "justintime50"

with urllib.request.urlopen(f'https://api.github.com/users/{username}/repos') as repos:
    data = json.load(repos)

# TODO: Add try/catch for repos that won't work.

for repo in data:
    name = repo["name"]
    with urllib.request.urlopen(f'https://api.github.com/repos/{username}/{name}/languages') as languages:
        data = json.load(languages)
        print(name, data)
