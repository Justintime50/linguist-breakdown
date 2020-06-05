<div align="center">

# Linguist

View the language breakdown of your entire GitHub account.

[![Build Status](https://travis-ci.com/Justintime50/linguist.svg?branch=master)](https://travis-ci.com/Justintime50/linguist)
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

<img src="assets/showcase.png">

</div>

GitHub displays beautiful language breakdowns on each repo on their website; however, they do not show your entire language breakdown across all your projects.

Linguist can return the language breakdown of your personal repos or all repos you have access to individually via the command line, then Linguist will build a customized pie chart breakdown of your overall language usage across all repos (limited to the top 8 for clarity; all languages are returned via CLI). Configure some settings and quickly find out what languages you use the most!

## Install

```bash
git clone https://github.com/Justintime50/linguist.git

pip3 install -e ."[dev]"
```

## Usage

Pass your GitHub Token to the script.

```bash
TOKEN=123... python3 app.py
```

The repos you'd like to include can be configured by changing the `REPO_TYPE` variable in the `linguist.py` file.

## Development

Install project with dev depencencies:

```bash
pip3 install -e ."[dev]"
```

Lint the project:

```bash
pylint linguist/*.py
```
