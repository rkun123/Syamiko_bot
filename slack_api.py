import os
import slack
from flask import Flask, request
from slackeventsapi import SlackEventAdapter
import json


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

        self.client = client

        self.subscribe_events()

    def subscribe_events(self):
        # app_mention
        app_mention_deco = self.events_adapter.on("app_mention")
        app_mention_deco(self.app_mention)
        
        # interactive message
        self.flask.route("/slack/interactives", methods=["POST"])(self.interactive_message)

    def post_issue_button(self):
        self.client.chat_postMessage(
                channel="#test",
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text":
                            "Issueを追加する"
                            },
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Issue追加",
                                "emoji": True
                            },
                            "value": "click_me_123"
                        }
                    }
                ]
            )

    def show_issue_modal(self, trigger_id):
        self.client.views_open(
                channel="#test",
                trigger_id=trigger_id,
                view={
                    "type": "modal",
                    "title": {
                            "type": "plain_text",
                            "text": "My App",
                            "emoji": True
                    },
                    "submit": {
                            "type": "plain_text",
                            "text": "Submit",
                            "emoji": True
                    },
                    "close": {
                            "type": "plain_text",
                            "text": "Cancel",
                            "emoji": True
                    },
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "*Issueを作成*"
                            }
                        },
                        {
                            "type": "input",
                            "block_id": "title_block",
                            "element": {
                                "action_id": "title",
                                "type": "plain_text_input"
                            },
                            "label": {
                                "type": "plain_text",
                                "text": "タイトル",
                                "emoji": True
                            }
                        },
                        {
                            "type": "input",
                            "block_id": "description_block",
                            "element": {
                                "action_id": "description",
                                "type": "plain_text_input",
                                "multiline": True
                            },
                            "label": {
                                "type": "plain_text",
                                "text": "説明",
                                "emoji": True
                            }
                        },
                        {
                            "type": "input",
                            "block_id": "member_block",
                            "element": {
                                "type": "multi_users_select",
                                "action_id": "member",
                                "placeholder": {
                                    "type": "plain_text",
                                    "text": "Select channels",
                                    "emoji": True
                                }
                            },
                            "label": {
                                "type": "plain_text",
                                "text": "担当者",
                                "emoji": True
                            }
                        }
                    ]
                }
            )

    def app_mention(self, e):
        print(vars(e))
        print("User: " + e["event"]["user"])
        if "modal" in e["event"]["text"]:
            self.show_issue_modal(e["event_id"])

    def interactive_message(self):
        req = json.loads(request.form["payload"])
        print(dict(req))
        if req["type"] == "block_actions":
            self.show_issue_modal(req["trigger_id"])
        elif req["type"] == "view_submission":
            print(dict(req))
            values = req["view"]["state"]["values"]
            print("Title: {}".format(values["title_block"]["title"]["value"]))
            print("Description: {}".format(values["description_block"]["description"]["value"]))
            selected_users = values["member_block"]["member"]["selected_users"]
            for idx, option in enumerate(selected_users):
                print("{}: {}".format(str(idx), option))

        else:
            print("Invalid interactive_message")

        return "", 200

    def run(self):
        self.flask.run(port=3000)


if __name__ == "__main__":
    f = Flask(__name__)

    TOKEN = os.getenv("SLACKBOT_API_TOKEN")
    SIGNING_SECRET = os.getenv("SLACKBOT_API_SIGNING_SECRET")

    s = Slack(TOKEN, SIGNING_SECRET, f, 3000)
    s.post_issue_button()

    s.run()
