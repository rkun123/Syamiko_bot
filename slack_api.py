import os
import slack
from flask import Flask, request
from slackeventsapi import SlackEventAdapter
import json
import slack_ui

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
                blocks=slack_ui.OPEN_MODAL_BUTTONS
            )
        
    def show_add_channel_modal(self, trigger_id):
        self.client.views_open(
            trigger_id=trigger_id,
            view=slack_ui.ADD_CHANNEL_MODAL
        )

    def show_add_issue_modal(self, trigger_id):
        """
        Issue追加する用のModalを表示するメソッド

        Parameters
        ----------
        trigger_id : string
            Modalを送信する際に必要なtrigger_id
        """
        self.client.views_open(
            trigger_id=trigger_id,
            view=slack_ui.ADD_ISSUE_MODAL
        )
    
    def show_assign_user_modal(self, trigger_id):
        self.client.views_open(
            trigger_id=trigger_id,
            view=slack_ui.ASSIGN_USER_MODAL
        )

    def show_close_issue_modal(self, trigger_id):
        self.client.views_open(
            trigger_id=trigger_id,
            view=slack_ui.CLOSE_ISSUE_MODAL
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
        # print(dict(req))
        if req["type"] == "block_actions":
            mode = req["actions"][0]["value"]
            if mode == "Add Issue":
                self.show_add_issue_modal(req["trigger_id"])
            elif mode == "Add Channel":
                self.show_add_channel_modal(req["trigger_id"])
            elif mode == "Assign User":
                self.show_assign_user_modal(req["trigger_id"])
            elif mode == "Close Issue":
                self.show_close_issue_modal(req["trigger_id"])
        elif req["type"] == "view_submission":

            callback_id = req["view"]["callback_id"]
            # print(req)

            if callback_id == "ADD_ISSUE":
                team_id = req["view"]["team_id"]
                values = req["view"]["state"]["values"]
                title = values["title_block"]["title"]["value"]
                description = values["description_block"]["description"]["value"]
                limited_time = values["limited_time_block"]["limited_time"]["selected_option"]["value"]
                selected_users = values["member_block"]["member"]["selected_users"]
                print(team_id, title, description,limited_time, selected_users)
                return self.add_issue_callback(team_id=team_id, title=title, description=description, limited_time=limited_time, selected_users=selected_users)
            elif callback_id == "ADD_CHANNEL":
                team_id = req["view"]["team_id"]
                repo = req["view"]["state"]["values"]["repo_block"]["repo"]["value"]
                print(team_id, repo)
                return self.add_channel_callback(team_id=team_id, repo=repo)
            elif callback_id == "ASSIGN_USER":
                team_id = req["view"]["team_id"]
                issue_num = req["view"]["state"]["values"]["issue_block"]["issue"]["selected_option"]["value"]
                assignee = req["view"]["state"]["values"]["assignee_block"]["assignee"]["selected_users"]
                print(team_id, assignee, issue_num)
                return self.assign_user_callback(team_id=team_id, assignee=assignee, issue_num=issue_num)
            elif callback_id == "CLOSE_ISSUE":
                team_id = req["view"]["team_id"]
                issue_num = req["view"]["state"]["values"]["issue_block"]["issue"]["selected_option"]["value"]
                print(team_id, issue_num)
                return self.close_issue_callback(team_id=team_id, issue_num=issue_num)

            # team_id = req["view"]["team_id"]
            # values = req["view"]["state"]["values"]
            # title = values["title_block"]["title"]["value"]
            # description = values["description_block"]["description"]["value"]
            # limited_time = values["limited_time_block"]["limited_time"]["selected_option"]["value"]
            # selected_users = values["member_block"]["member"]["selected_users"]
            # self.callback(team_id, title, description, limited_time, selected_users)

        else:
            print("Invalid interactive_message")

        return "", 200

    def setAddIssueCallback(self, add_issue):
        self.add_issue_callback = add_issue

    def setAddChannelCallback(self, addChannel):
        self.add_channel_callback = addChannel

    def setAssignUserCallback(self, assignUser):
        self.assign_user_callback = assignUser

    def setCloseIssueCallback(self, closeIssue):
        self.close_issue_callback = closeIssue

    def run(self):
        """
        EventsAPI用のFlaskをListenする際に呼ぶメソッド
        """
        self.flask.run(port=3000)


if __name__ == "__main__":
    flask = Flask(__name__)

    TOKEN = os.getenv("SLACKBOT_API_TOKEN")
    SIGNING_SECRET = os.getenv("SLACKBOT_API_SIGNING_SECRET")

    def callback(team_id, title, description, limited_time,selected_users):
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
        print(limited_time)
        print(selected_users)

    API = Slack(TOKEN, SIGNING_SECRET, flask, 3000, callback)

    API.run()
