"""Module with search interface."""
from typing import Dict, Iterable, Optional

from jira import JIRA, Issue
from jira.client import ResultList

from jirapt.jira_response_iterable import JiraResponseIterable


def search_issues(jira: JIRA, jql: str, **kwargs: Optional[Dict]) -> Iterable[Issue]:
    """
    Lazily search for paginated jira issues.

    :param jira: Jira API instance.
    :param jql: JQL query to search.
    :param kwargs: Additional search_issues arguments.
    :return: Iterable of Jira issues found.
    """

    def get_more_fn(start_idx: int) -> ResultList:
        return jira.search_issues(jql, startAt=start_idx, **kwargs)

    return JiraResponseIterable(get_more_fn(0), get_more_fn)
