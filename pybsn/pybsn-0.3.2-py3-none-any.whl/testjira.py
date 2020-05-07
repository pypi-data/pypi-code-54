from jira import JIRA
import re

# By default, the client will connect to a JIRA instance started from the Atlassian Plugin SDK
# (see https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK for details).
# Override this with the options parameter.
options = {"server": 'https://bigswitch.atlassian.net/'}
jira = JIRA(options, basic_auth=('srv-ticketanalytics@arista.com', 'gKzlhwW8z3L3OyHK28OZCBD8'))
# jira = JIRA(options, auth=('srv-ticketanalytics', 'gKzlhwW8z3L3OyHK28OZCBD8'))

# Get all projects viewable by anonymous users.
# projects = jira.projects()

# Sort available project keys, then return the second, third, and fourth keys.
# keys = sorted([project.key for project in projects])[2:5]

# Get an issue.
issue = jira.issue("BSC-13539")
print(issue)
# # Find all comments made by Atlassians on this issue.
# atl_comments = [
#     comment
#     for comment in issue.fields.comment.comments
#     if re.search(r"@atlassian.com$", comment.author.emailAddress)
# ]