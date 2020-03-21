from github import Github
from dotenv import load_dotenv
import os
from os.path import join, dirname

class Issue:
    def __init__(self, token):
        self.token = token
        
    def get_issue(self,repo_url,issue_num):

        g = Github(self.token)
        repo = g.get_repo(repo_url)
        issue = None

        for _issue in repo.get_issues(state='all'):
            if _issue.number == issue_num:
                issue = _issue

        if issue == None:
            print('該当するIssue番号は存在しません。')
        return issue

    def create_issue(self,repo_url,title,body,assignee=None):
        g = Github(self.token)
        repo = g.get_repo(repo_url)
        new_issue = None

        if assignee is None:
            new_issue = repo.create_issue(title,body)
        else:
            new_issue = repo.create_issue(title,body,assignee)
        print('new issue number is {}'.format(new_issue.number))

        return new_issue

if __name__ == '__main__':

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")

    repo_url = "YuichirouSeitoku/TestRepository"
    issue_num = 9

    g = Issue(GITHUB_ACCESS_TOKEN)
    issue = g.get_issue(repo_url,issue_num)

    title = 'test'
    body = 'テストの文章です'
    assignee = 'YuichirouSeitoku'

    g.create_issue(repo_url,title,body,assignee)
