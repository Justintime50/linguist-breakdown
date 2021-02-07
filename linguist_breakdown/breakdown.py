import argparse
import json
import os
from collections import Counter
from threading import Thread

import matplotlib.pyplot as plotter
from github import Github

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
USER = Github(GITHUB_TOKEN).get_user()
BYTES = Counter()


class CLI():
    def __init__(self):
        """Setup the CLI arguments
        """
        parser = argparse.ArgumentParser(
            description='View the language breakdown of your entire GitHub account.'
        )
        parser.add_argument(
            '-t',
            '--type',
            default='owner',
            type=str,
            required=False,
            help='The repo type to look at (OPTIONS: all, owner, member, private, public).'
        )
        parser.add_argument(
            '-p',
            '--pieces',
            default=8,
            type=int,
            required=False,
            help='Number of chart pieces to generate (will use greatest percentages)'
        )
        parser.add_argument(
            '-f',
            '--forks',
            required=False,
            action='store_true',
            help='Include forked repos in the language breakdown.'
        )
        parser.add_argument(
            '-c',
            '--chart',
            required=False,
            action='store_true',
            help='Generate a chart of the language breakdown.'
        )
        parser.parse_args(namespace=self)

    def run(self):
        linguist = Linguist.run(
            repo_type=self.type,
            chart_pieces=self.pieces,
            forks=self.forks,
            chart=self.chart,
        )
        return linguist


class Linguist():
    @staticmethod
    def run(repo_type, chart_pieces, forks, chart):
        """Run the script to get a breakdown of the language usage of each
        of your repos and the overall language usage on your account
        """
        if not GITHUB_TOKEN:
            message = 'GITHUB_TOKEN must be present to run linguist-breakdown.'
            raise ValueError(message)
        else:
            repos = Linguist.get_repos(repo_type)
            Linguist.iterate_repos(forks, repos)
            overall = Linguist.determine_overall_breakdown(chart_pieces)
            if chart:
                Linguist.generate_chart(overall[1])
        return True

    @staticmethod
    def iterate_repos(forks, repos):
        """Grab all the user's repos and iterate over each to get data
        """
        thread_list = []
        print('Gathering languages for each repo...')
        for repo in repos:
            if forks is False and repo.fork:
                continue  # Disregard forks if arg not passed
            repo_thread = Thread(
                target=Linguist.calculate_percentages, args=(repo,)
            )
            thread_list.append(repo_thread)
            repo_thread.start()
        for thread in thread_list:
            thread.join()

    @staticmethod
    def get_repos(repo_type):
        """Gets all the repos of a user
        """
        repos = USER.get_repos(type=repo_type)
        return repos

    @staticmethod
    def get_languages_of_repo(repo):
        """Get the languages of a repo
        """
        repo_languages = repo.get_languages()
        return repo_languages

    @staticmethod
    def calculate_percentages(repo):
        """Logic to calculate the language usage of each repo
        """
        languages = Linguist.get_languages_of_repo(repo)
        BYTES.update(languages)
        total = sum(languages.values())
        percentages = {}
        for key, value in languages.items():
            percentages[key] = str(
                round((value / total) * 100, 2)) + '%'
        print('\n' + repo.name)
        math_output = json.dumps(percentages, indent=4)
        print(math_output)
        return math_output

    @staticmethod
    def determine_overall_breakdown(chart_pieces):
        """Grab all language percentages from repos, print language percentage overall
        to console
        """
        total = sum(BYTES.values())
        percentages = {}
        for key, value in BYTES.items():
            percentages[key] = round((value / total) * 100, 2)
        print('\nOverall language breakdown:\n')
        sorted_percentages = sorted(
            percentages.items(),
            key=lambda x: x[1],
            reverse=True
        )
        overall_breakdown = json.dumps(dict(sorted_percentages), indent=4)
        chart_pieces = dict(sorted_percentages[:chart_pieces])
        print(overall_breakdown)
        return overall_breakdown, chart_pieces

    @staticmethod
    def generate_chart(percentages):
        """Draw and open a pie chart with the overall language breakdown
        """
        print('\nOpening graph...')
        figure_object, axes_object = plotter.subplots()
        axes_object.pie(
            percentages.values(),
            labels=percentages.keys(),
            autopct='%1.2f%%',
            startangle=90)
        axes_object.axis('equal')
        plotter.tight_layout()
        plotter.legend(loc='upper left')
        plotter.show()


def main():
    CLI().run()


if __name__ == '__main__':
    main()
