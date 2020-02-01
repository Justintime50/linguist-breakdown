# create a counter to accumulate the bytes per language
bytes_per_lang = Counter()
# get a list of our repos
repos = getURL('roehnan', password, '/user/repos')
# iterate over the repos
for repo in repos:
    # the github API returns URLs that are complete; we only need after the domain since our
    # HTTPSConnection object in the getURL function already contains the domain
    repo_url = repo['url'].replace('https://api.github.com', '')
    langs_url = repo['languages_url'].replace('https://api.github.com', '')
    # get the languages data for the repo we're currently on
    langs = getURL('roehnan', password, langs_url)
    # update our count of bytes, adding in any new/missing keys
    bytes_per_lang.update(langs)
    print(repo_url, langs_url, bytes_per_lang)
# total all the bytes in the repos so we can calc the percentage by language
t = sum(bytes_per_lang.values())
# for each language, calculate its percent of the total bytes
percentages = {}
for k, v in bytes_per_lang.items():
    percentages[k] = (v / t) * 100
# show the results
print(percentages)
