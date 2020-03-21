import github_issue
from github import Github
from dotenv import load_dotenv
import os
from os.path import join, dirname

GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")

repo_url = "YuichirouSeitoku/TestRepository"
issue_num = 1

g = github_issue.Issue(GITHUB_ACCESS_TOKEN)

def get_issue_list():
    result = [
        {
            "text": {
                "type": "plain_text",
                "text": '#' + str(i.number) + ' ' + str(i.title),
                "emoji": True
            },
            "value": str(i.number)
	    } for i in g.get_open_list(repo_url)
    ]
    result.reverse()
    return result

print(get_issue_list())

OPEN_MODAL_BUTTONS = [
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Add Channel",
                    "emoji": True
                },
                "value": "Add Channel"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Add Issue",
                    "emoji": True
                },
                "value": "Add Issue"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Assign User",
                    "emoji": True
                },
                "value": "Assign User"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Close Issue",
                    "emoji": True
                },
                "value": "Close Issue"
            }
        ]
    }
]


ADD_ISSUE_MODAL = {
    "type": "modal",
    "callback_id": "ADD_ISSUE",
    "title": {
        "type": "plain_text",
        "text": "ADD_ISSUE_MODAL",
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
            "block_id": "limited_time_block",
            "element": {
                "action_id": "limited_time",
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select your favorites",
                    "emoji": True
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "10分",
                            "emoji": True
                        },
                        "value": "600"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "20分",
                            "emoji": True
                        },
                        "value": "1200"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "30分",
                            "emoji": True
                        },
                        "value": "1800"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "1時間",
                            "emoji": True
                        },
                        "value": "6000"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "2時間",
                            "emoji": True
                        },
                        "value": "12000"
                    },
                ]
            },
            "label": {
                "type": "plain_text",
                "text": "制限時間",
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

ADD_CHANNEL_MODAL = {
	"type": "modal",
    "callback_id": "ADD_CHANNEL",
	"title": {
		"type": "plain_text",
		"text": "ADD_CHANNEL_MODAL",
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
			"type": "input",
            "block_id": "repo_block",
			"element": {
				"type": "plain_text_input",
                "action_id": "repo"
			},
			"label": {
				"type": "plain_text",
				"text": "リポジトリ名 - /user/repository",
				"emoji": True
			}
		}
	]
}

ASSIGN_USER_MODAL = {
	"type": "modal",
    "callback_id": "ASSIGN_USER",
	"title": {
		"type": "plain_text",
		"text": "ASSIGN_USER",
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
			"type": "input",
            "block_id": "issue_block",
			"element": {
				"type": "static_select",
                "action_id": "issue",
				"placeholder": {
					"type": "plain_text",
					"text": "Select options",
					"emoji": True
				},
				"options": get_issue_list()
			},
			"label": {
				"type": "plain_text",
				"text": "Issue名",
				"emoji": True
			}
		},
		{
			"type": "input",
            "block_id": "assignee_block",
			"element": {
				"type": "multi_users_select",
                "action_id": "assignee",
				"placeholder": {
					"type": "plain_text",
					"text": "Select users",
					"emoji": True
				}
			},
			"label": {
				"type": "plain_text",
				"text": "User",
				"emoji": True
			}
		}
	]
}

CLOSE_ISSUE_MODAL = {
	"type": "modal",
    "callback_id": "CLOSE_ISSUE",
	"title": {
		"type": "plain_text",
		"text": "CLOSE_ISSUE",
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
			"type": "input",
            "block_id": "issue_block",
			"element": {
				"type": "static_select",
                "action_id": "issue",
				"placeholder": {
					"type": "plain_text",
					"text": "Select options",
					"emoji": True
				},
				"options": get_issue_list()
			},
			"label": {
				"type": "plain_text",
				"text": "Issue名",
				"emoji": True
			}
		}
	]
}