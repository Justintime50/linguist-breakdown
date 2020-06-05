"""View the language breakdown of your entire GitHub account."""
from collections import Counter
import os
import time
import json
from threading import Thread
from github import Github
import matplotlib.pyplot as plotter

# Define some variables
GITHUB = Github(os.getenv("TOKEN"))  # Your GitHub token
REPO_TYPE = "owner"  # OPTIONS: all, owner, member, private, public
BYTES = Counter()
USER = GITHUB.get_user()
# Number of chart pieces to generate (will use greatest percentages )
CHART_PIECES = 8


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
            if not repo.fork:  # Disregard forks
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
        print(json.dumps(sorted_percentages))

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
