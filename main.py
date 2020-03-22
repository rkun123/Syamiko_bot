import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask
import datetime
import threading

from slack_api import Slack
from github_issue import Issue
from issue_timer import IssueTimer
from firebase.firebase import FireBase

if __name__ == "__main__":
    # Load dotenv
    load_dotenv(verbose=True)
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    SLACKBOT_API_TOKEN = os.environ.get("SLACKBOT_API_TOKEN")
    SLACKBOT_API_SIGNING_SECRET = os.environ.get("SLACKBOT_API_SIGNING_SECRET")

    GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET")
    GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")

    FIREBASE_CREDENTIAL_PATH = os.environ.get("FIREBASE_CREDENTIAL_PATH")

    timer_list = []
    issue_timer = IssueTimer(timer_list)

    t = threading.Thread(target=issue_timer.check_time())
    t.start()

    # Generate flask instance
    flask = Flask(__name__)

    # Generate github client
    github = Issue(GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, GITHUB_ACCESS_TOKEN)
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
        issue_num = github.create_issue(repo, title, description, selected_users).number
        firebase.add_issue(team_id, issue_num, title, description, limited_time, selected_users)

        # Issue追加時からタイマースタート
        issue_timer.add_time({
            "team": team_id,
            "issue": issue_num,
            "expired_at": datetime.datetime.now() + datetime.timedelta(seconds=limited_time)
            })

        return ('', 204)

    slack.setAddIssueCallback(add_issue)

    def add_channel(team_id, repo):
        """
        Channel追加
        """
        firebase.add_channel(team_id, repo)
        
        return ('', 204)

    slack.setAddChannelCallback(add_channel)

    def assign_user(team_id, assignee=None, issue_num=None):
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


    def expired(timer):
        """
        時間切れのタイマーが出た際に呼ばれる関数
        """
        print("Expired!!!")
        print("Team: {}, Issue: {}".format(timer["team"], timer["issue"]))

    issue_timer.set_callback(expired)

    slack.run()
