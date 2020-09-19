import pytest
import mock
from linguist import breakdown


@mock.patch('linguist.breakdown.GITHUB_TOKEN', None)
def test_run_no_github_token():
    message = 'GITHUB_TOKEN must be present to run linguist-breakdown.'
    with pytest.raises(ValueError) as error:
        breakdown.Linguist.run('', '', False, False)
    assert message == str(error.value)


@mock.patch('linguist.breakdown.Linguist.get_languages',
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


@pytest.mark.skip('Skip as this is more an integration test (requires GUI)')
def test_generate_chart():
    # As such, this function has been excluded from coverage reports
    assert 'test' == 'skipped'
