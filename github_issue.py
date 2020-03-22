from github import Github
from dotenv import load_dotenv
import os
from os.path import join, dirname
import time

class Issue:
    def __init__(self, token):
        self.token = token
        
    def get_issue(self,repo_url,issue_num):
        print('get_issue')
        g = Github(self.token)
        repo = g.get_repo(repo_url)
        issue = None

        for _issue in repo.get_issues(state="all"):
            if int(_issue.number) == int(issue_num):
                issue = _issue

        if issue is None:
            print("該当するIssue番号は存在しません。")
        return issue

    def create_issue(self,repo_url,title,body,assignees=None):
        print('create_issue')
        print(repo_url, title, body, assignees)
        g = Github(self.token)
        repo = g.get_repo(repo_url)
        new_issue = None

        new_issue = repo.create_issue(title,body)

        # time.sleep(10)

        if assignees:
            for assignee in assignees:
                new_issue.add_to_assignees(assignee)
        print("new issue number is {}".format(new_issue.number))

        return new_issue
    def get_open_list(self, repo_url):
        print('get_open_list')
        g = Github(self.token)
        repo = g.get_repo(repo_url)
        open_issues = repo.get_issues(state='open')

        return open_issues

    def close_issue(self,repo_url,issue_num):
        print('close_issue')
        g = Github(self.token)
        repo = g.get_repo(repo_url[1:])
        open_issues = repo.get_issues(state='open')
        close_issue = self.get_issue(repo_url[1:], issue_num)

        if close_issue and close_issue in open_issues:
            close_issue.edit(state='closed')
            print("close issue number is {}".format(close_issue.number))
        else:
            print("該当するOpenされたIssue番号は存在しません。")
        
        return close_issue

    def get_commit_info(self, repo_url, issue_num):
        print('get_commit_info')
        g = Github(self.token)
        repo = g.get_repo(repo_url)
        issue = self.get_issue(repo_url, issue_num)
        commit_info = {}
        event_ids = [id.id for id in issue.get_events()]
        for event_id in event_ids:
            issue_event = repo.get_issues_event(event_id)
            if not issue_event.commit_id:
                continue
            commit_id = issue_event.commit_id
            author = repo.get_commit(commit_id).author.login

            files = repo.get_commit(commit_id).files
            progress = 0
            for file in files:
                progress += file.additions+file.deletions+file.changes

            if author in commit_info:
                commit_info[author] += progress
            else:
                commit_info[author] = progress
        
        return commit_info

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

    print(repo_url, title, body, assignees)

    g.create_issue(repo_url,title,body,assignees)
    g.close_issue(repo_url,issue_num)
    commit_info = g.get_commit_info(repo_url,issue_num)

    print(commit_info)