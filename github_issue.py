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

        for _issue in repo.get_issues(state="all"):
            if _issue.number == issue_num:
                issue = _issue

        if issue == None:
            print("該当するIssue番号は存在しません。")
        return issue

    def create_issue(self,repo_url,title,body,assignees=None):
        g = Github(self.token)
        repo = g.get_repo(repo_url)
        new_issue = None

        new_issue = repo.create_issue(title,body)

        if assignees:
            for assignee in assignees:
                new_issue.add_to_assignees(assignee)
        print("new issue number is {}".format(new_issue.number))

        return new_issue
    def get_open_list(self, repo_url):
        g = Github(self.token)
        repo = g.get_repo(repo_url)
        open_issues = repo.get_issues(state='open')

        return open_issues

    def close_issue(self,repo_url,issue_num):
        g = Github(self.token)
        repo = g.get_repo(repo_url)
        open_issues = repo.get_issues(state='open')
        close_issue = self.get_issue(repo_url, issue_num)

        if close_issue and close_issue in open_issues:
            close_issue.edit(state='closed')
            print("close issue number is {}".format(close_issue.number))
        else:
            print("該当するOpenされたIssue番号は存在しません。")
        
        return close_issue

if __name__ == "__main__":

    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)

    GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")

    repo_url = "YuichirouSeitoku/TestRepository"
    issue_num = 1

    g = Issue(GITHUB_ACCESS_TOKEN)
    issue = g.get_issue(repo_url,issue_num)

    title = "test"
    body = "テストの文章です"
    assignees = ["YuichirouSeitoku","rkun123","Futaba-Kosuke"]
    assignees = ["YuichirouSeitoku"]

    g.create_issue(repo_url,title,body,assignees)
    g.close_issue(repo_url,issue_num)
