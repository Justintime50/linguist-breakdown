"""View the language breakdown of your entire GitHub account."""
from collections import Counter
import os
import time
import json
from threading import Thread
import argparse
from github import Github
import matplotlib.pyplot as plotter

# Setup arguments
parser = argparse.ArgumentParser(
    description='View the language breakdown of your entire GitHub account.')
parser.add_argument('-t', '--type', default='owner', type=str,
                    help='The repo type to look at (OPTIONS: all, owner, member, private, public).')
parser.add_argument('-p', '--pieces', default=8, type=int,
                    help='Number of chart pieces to generate (will use greatest percentages)')
parser.add_argument('-f', '--forks', action='store_true',
                    help='Include forked repos in the language breakdown.')
args = parser.parse_args()
GITHUB = Github(os.getenv('GITHUB_TOKEN'))
USER = GITHUB.get_user()
REPO_TYPE = args.type
CHART_PIECES = args.pieces
BYTES = Counter()


class Breakdown():
    """
    Breakdown the language usage of each of your repos and the overall
    language usage on your account
    """
    @classmethod
    def repos(cls):
        """Grab all the user's repos and their data, print language by repo"""
        print(f"Gathering data about {USER.login}'s repos...")
        repos = GITHUB.get_user().get_repos(type=REPO_TYPE)
        for repo in repos:
            if args.forks is False and repo.fork:
                continue  # Disregard forks if arg not passed
            time.sleep(0.1)
            Thread(target=Breakdown.math, args=(repo,)).start()

        time.sleep(2)
        Breakdown.overall()

    @classmethod
    def math(cls, repo):
        """Logic to calculate the language usage of each repo"""
        BYTES.update(repo.get_languages())
        total = sum(repo.get_languages().values())
        percentages = {}
        for key, value in repo.get_languages().items():
            percentages[key] = str(
                round((value / total) * 100, 2)) + '%'
        print('\n' + repo.name)
        print(json.dumps(percentages, indent=4))

    @classmethod
    def overall(cls):
        """Grab all language percentages from repos, print language percentage overall"""
        total = sum(BYTES.values())
        percentages = {}
        for key, value in BYTES.items():
            percentages[key] = round((value / total) * 100, 2)
        print("\nOverall language breakdown:\n")
        sorted_percentages = sorted(
            percentages.items(), key=lambda x: x[1], reverse=True)
        print(json.dumps(dict(sorted_percentages), indent=4))

        Breakdown.chart(dict(sorted_percentages[:CHART_PIECES]))

    @classmethod
    def chart(cls, percentages):
        """Draw and open the pie chart"""
        print("\nOpening graph...")
        figure_object, axes_object = plotter.subplots()  # pylint: disable=W0612
        axes_object.pie(
            percentages.values(),
            labels=percentages.keys(),
            autopct='%1.2f%%',
            startangle=90)
        axes_object.axis('equal')
        plotter.tight_layout()
        plotter.legend(loc="upper left")
        plotter.show()


def main():
    """Run the Linguist breakdown"""
    Breakdown.repos()


if __name__ == '__main__':
    main()
