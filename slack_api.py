import os
import slack
from flask import Flask
from slackeventsapi import SlackEventAdapter


class Slack:
    def __init__(self, token, signing_secret, flask, port):
        self.token = token
        self.signing_secret = signing_secret
        self.port = port
        self.flask = flask
        client = slack.WebClient(token=token)
        events_adapter = SlackEventAdapter(
                signing_secret,
                "/slack/events",
                flask)
        self.events_adapter = events_adapter

        client.chat_postMessage(
            channel='#test',
            text="参加!")

        self.subscrive_events()

    def subscrive_events(self):
        # app_mention
        app_mention_deco = self.events_adapter.on("app_mention")
        app_mention_deco(self.app_mention)

    def app_mention(self, e):
        e["event"]
        print("aaa")

    def run(self):
        self.flask.run(port=3000)


if __name__ == "__main__":
    f = Flask(__name__)

    TOKEN = os.getenv("SLACKBOT_API_TOKEN")
    SIGNING_SECRET = os.getenv("SLACKBOT_API_SIGNING_SECRET")

    s = Slack(TOKEN, SIGNING_SECRET, f, 3000)
    s.run()
