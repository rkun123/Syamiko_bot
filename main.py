import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask

from slack_api import Slack
from github_issue import Issue
from firebase.firebase import FireBase

if __name__ == "__main__":
    # Load dotenv
    load_dotenv(verbose=True)
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    SLACKBOT_API_TOKEN = os.environ.get("SLACKBOT_API_TOKEN")
    SLACKBOT_API_SIGNING_SECRET = os.environ.get("SLACKBOT_API_SIGNING_SECRET")

    GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")

    FIREBASE_CREDENTIAL_PATH = os.environ.get("FIREBASE_CREDENTIAL_PATH")

    # Generate flask instance
    flask = Flask(__name__)

    # Generate github client
    github = Issue(GITHUB_ACCESS_TOKEN)
    firebase = FireBase(join(dirname(__file__), FIREBASE_CREDENTIAL_PATH))

    # Generate slack client and run
    slack = Slack(
        SLACKBOT_API_TOKEN,
        SLACKBOT_API_SIGNING_SECRET,
        flask,
        3000,
        None
    )

    def add_issue(team_id, title, description, limited_time, selected_users):
        """
        Issue追加
        """
        repo = firebase.get_repo(team_id)
        print(repo)
        print(selected_users)
        github_users = [firebase.get_user(team_id, i)["github_user_id"] for i in selected_users]
        print(github_users)
        issue_num = github.create_issue("YuichirouSeitoku/TestRepository", title, description, github_users).number
        firebase.add_issue(team_id, issue_num, title, description, limited_time, selected_users)

        return ('', 204)

    slack.setAddIssueCallback(add_issue)

    def add_channel(team_id, repo):
        """
        Channel追加
        """
        firebase.add_channel(team_id, repo)
        
        return ('', 204)

    slack.setAddChannelCallback(add_channel)

    def assign_user(team_id, assignee, issue_num):
        """
        ユーザーアサイン
        """
        repo = firebase.get_repo(team_id)
        github.get_issue(repo, issue_num).add_to_assignees(assignee)
        firebase.assign_user(team_id, assignee, issue_num)
        return ('', 200)

    slack.setAssignUserCallback(assign_user)

    def connect_github(team_id, slack_user, github_user):
        firebase.add_user(team_id, slack_user, github_user)
        return ('', 200)

    slack.setConnectGithubCallback(connect_github)

    def close_issue(team_id, issue_num):
        """
        Issueクローズ
        """
        repo = firebase.get_repo(team_id)
        github.close_issue(repo, issue_num)
        return "OK", 200
        

    slack.setAssignUserCallback(close_issue)

    slack.run()
