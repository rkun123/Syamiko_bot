import os
import slack
from flask import Flask, request
from slackeventsapi import SlackEventAdapter
import json


class Slack:
    def __init__(self, token, signing_secret, flask, port, callback):
        self.token = token
        self.signing_secret = signing_secret
        self.flask = flask
        self.port = port
        self.callback = callback
        client = slack.WebClient(token=token)
        events_adapter = SlackEventAdapter(
                signing_secret,
                "/slack/events",
                flask)
        self.events_adapter = events_adapter

        self.client = client

        self.subscribe_events()

    def subscribe_events(self):
        # app_mention
        app_mention_deco = self.events_adapter.on("app_mention")
        app_mention_deco(self.app_mention)
        
        # interactive message
        self.flask.route("/slack/interactives", methods=["POST"])(
                self.interactive_message)

    def post_issue_button(self, channel_id):
        """
        Issue追加ボタンを投稿するメソッド
        Parameters
        ----------
        channel_id : string
            送信先のチャンネルID
        """
        self.client.chat_postMessage(
                channel=channel_id,
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
        """
        Issue追加する用のModalを表示するメソッド

        Parameters
        ----------
        trigger_id : string
            Modalを送信する際に必要なtrigger_id
        """
        self.client.views_open(
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

    def app_mention(self, event):
        """
        @syamikoされた際に呼ばれるイベントハンドラメソッド

        Parameters
        ----------
        e : object
            イベントオブジェクト
        """

        print("User: " + event["event"]["user"])
        if "modal" in event["event"]["text"]:
            self.post_issue_button(event["event"]["channel"])

    def interactive_message(self):
        """
        Button，Modalが返すblock_actions, view_submissionを受けた際に呼ばれるイベントハンドラ
        """
        req = json.loads(request.form["payload"])
        print(dict(req))
        if req["type"] == "block_actions":
            self.show_issue_modal(req["trigger_id"])
        elif req["type"] == "view_submission":
            team_id = req["view"]["team_id"]
            values = req["view"]["state"]["values"]
            title = values["title_block"]["title"]["value"]
            description = values["description_block"]["description"]["value"]
            selected_users = values["member_block"]["member"]["selected_users"]
            self.callback(team_id, title, description, selected_users)

        else:
            print("Invalid interactive_message")

        return "", 200

    def run(self):
        """
        EventsAPI用のFlaskをListenする際に呼ぶメソッド
        """
        self.flask.run(port=3000)


if __name__ == "__main__":
    flask = Flask(__name__)

    TOKEN = os.getenv("SLACKBOT_API_TOKEN")
    SIGNING_SECRET = os.getenv("SLACKBOT_API_SIGNING_SECRET")

    def callback(team_id, title, description, selected_users):
        """
        Issue追加時の情報を受け取る関数
        Parameters
        ---------
        team_id : string
            チームのID
        title : string
            Issueのタイトル
        description : string
            Issueの説明文
        selected_users : list
            IssueにassignされたユーザーIDの文字列のリスト
        """
        print(team_id)
        print(title)
        print(description)
        print(selected_users)

    API = Slack(TOKEN, SIGNING_SECRET, flask, 3000, callback)

    API.run()
