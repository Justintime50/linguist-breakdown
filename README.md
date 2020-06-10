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
pip3 install linguist-breakdown
```

## Usage

```
Usage:
    GITHUB_TOKEN=123... linguist --type private --pieces 4 --forks

Options:
    -t, --type TYPE         The repo type to look at (OPTIONS: all, owner, member, private, public. Default: owner).
    -p, --pieces PIECES     Number of pieces of the chart to generate (Default: 8).
    -f, --forks             Include forked repos in the language breakdown.

TYPE expects a string option listed above.
PIECES expects an integer. The lower the number, the more readable your graph will be.
```

## Development

Install project with dev depencencies:

```bash
pip3 install -e ."[dev]"
```

Lint the project:

```bash
pylint linguist/*.py
```
