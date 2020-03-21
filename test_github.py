from github_issue import Issue

from github import Github
from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")

repo_url = "rkun123/Syamiko_bot"
issue_num = 1

g = Issue(GITHUB_ACCESS_TOKEN)
issue = g.get_issue(repo_url,issue_num)

print('  issue name: #{:<4} {} {}'.format(issue.number, issue.title, issue.assignee))
