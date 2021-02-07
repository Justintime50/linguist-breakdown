import mock
import pytest
from linguist_breakdown import breakdown


@mock.patch('linguist_breakdown.breakdown.GITHUB_TOKEN', None)
def test_run_no_github_token():
    message = 'GITHUB_TOKEN must be present to run linguist-breakdown.'
    with pytest.raises(ValueError) as error:
        breakdown.Linguist.run(None, None, False, False)
    assert message == str(error.value)


@mock.patch('linguist_breakdown.breakdown.GITHUB_TOKEN', '123')
@mock.patch('linguist_breakdown.breakdown.Linguist.generate_chart')
@mock.patch('linguist_breakdown.breakdown.Linguist.determine_overall_breakdown')
@mock.patch('linguist_breakdown.breakdown.Linguist.get_repos')
@mock.patch('linguist_breakdown.breakdown.Linguist.iterate_repos')
def test_run(mock_iterate_repos, mock_overall_breakdown, mock_get_repos, mock_generate_chart):
    result = breakdown.Linguist.run(None, None, False, True)
    mock_get_repos.assert_called_once()
    mock_iterate_repos.assert_called_once()
    mock_overall_breakdown.assert_called_once()
    mock_generate_chart.assert_called_once()
    assert result is True


@mock.patch('linguist_breakdown.breakdown.Linguist.calculate_percentages')
def test_iterate_repos_no_forks(mock_percentages):
    mock_repo = mock.Mock()
    mock_repo.fork = False
    mock_repos = [mock_repo]
    breakdown.Linguist.iterate_repos(False, mock_repos)
    mock_percentages.assert_called_once()


@mock.patch('linguist_breakdown.breakdown.Linguist.calculate_percentages')
def test_iterate_repos_with_forks(mock_percentages):
    mock_repo = mock.Mock()
    mock_repo.fork = True
    mock_repos = [mock_repo]
    breakdown.Linguist.iterate_repos(False, mock_repos)


@mock.patch('linguist_breakdown.breakdown.USER.get_repos')
@mock.patch('linguist_breakdown.breakdown.USER')
def test_get_repos(mock_user, mock_get_repos):
    breakdown.Linguist.get_repos('owner')
    mock_get_repos.assert_called_once()


@mock.patch('linguist_breakdown.breakdown.Linguist.get_languages_of_repo',
            return_value={'Shell': 5419, 'Emacs Lisp': 2689})
def test_calulate_percentages(mock_langs):
    mock_repo = mock.Mock()
    mock_repo.name = 'test-repo-name'
    result = breakdown.Linguist.calculate_percentages(mock_repo)
    assert '"Shell": "66.84%"' in result
    assert '"Emacs Lisp": "33.16%"' in result


def test_determine_overall_breakdown():
    result = breakdown.Linguist.determine_overall_breakdown(8)
    assert '"Shell": 66.84' in result[0]
    assert '"Emacs Lisp": 33.16' in result[0]
    assert {'Emacs Lisp': 33.16, 'Shell': 66.84} == result[1]


@mock.patch('github.Repository.Repository.get_languages')
@mock.patch('github.Repository.Repository')
def test_get_languages_or_repo(mock_repo, mock_get_langs):
    breakdown.Linguist.get_languages_of_repo(mock_repo)
    mock_get_langs.assert_called_once()


@mock.patch('matplotlib.pyplot.show')
@mock.patch('linguist_breakdown.breakdown.Linguist.calculate_percentages')
def test_generate_chart(mock_percentages, mock_plotter):
    breakdown.Linguist.generate_chart(mock_percentages)
    mock_plotter.assert_called_once()
