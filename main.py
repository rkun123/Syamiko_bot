import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask

from slack_api import Slack
from github_issue import Issue
from firebase.firebase import Firebase

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
    firebase = Firebase(join(dirname(__file__), '.env'))

    def addIssue(team_id, title, description, selected_users):
        github.create_issue(
            , title, description, assignee=selected_users[0])
        firebase.add_issue(team_id, _, title, description, _, selected_users)

    # Generate slack client and run
    slack = Slack(
        SLACKBOT_API_TOKEN,
        SLACKBOT_API_SIGNING_SECRET,
        flask,
        3000,
        addIssue
    )
    slack.run()
