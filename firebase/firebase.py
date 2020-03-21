import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import datetime

class FireBase:

    def __init__(self, path, team_name, channel=None, repository=None):

        cred = credentials.Certificate(path)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

        self.team_name = team_name

        # summaryが未定義のとき、collectionが存在しない
        summary = self.db.collection(self.team_name).document(u'summary').get().to_dict()
        if summary == None:
            print('init_collection')
            collection = self.db.collection(self.team_name)
            collection.document(u'summary').set({
                u'channel': channel,
                u'repository': repository,
            })
            collection.document(u'users').set({})
            collection.document(u'issues').set({})

    def get_issues_ref(self):
        return self.db.collection(self.team_name).document(u'issues')

    def get_users_ref(self):
        return self.db.collection(self.team_name).document(u'users')

    def get_issue(self, num):
        return self.get_issues_ref().get().to_dict()[num]

    def get_user(self, slack_id):
        return self.get_users_ref().get().to_dict()[slack_id]

    def add_issue(self, issue_num, title, description, limited_sec, closed_at=None, assignee=[]):
        issues_ref = self.get_issues_ref()
        issues = issues_ref.get().to_dict()
        if len(assignee) == 0:
            assigned_at = None
        else:
            assigned_at = datetime.datetime.now()

        new_issue = {
            u'issue_num': str(issue_num),
            u'title': title,
            u'description': description,
            u'assignee': assignee,
            u'limited_sec': limited_sec,
            u'assigned_at': assigned_at,
            u'closed_at': closed_at,
        }
        issues[str(issue_num)] = new_issue
        issues_ref.set(issues)
    
    def add_user(self, slack_id, github_id):
        users_ref = self.get_users_ref()
        users = users_ref.get().to_dict()
        new_user = {
            u'slack_id': slack_id,
            u'github_id': github_id,
            u'issues': [],
        }
        users[slack_id] = new_user
        users_ref.set(users)
    
    def assign_user(self, slack_id, issue_num):
        issues_ref = self.get_issues_ref()
        users_ref = self.get_users_ref()

        issues = issues_ref.get().to_dict()
        users = users_ref.get().to_dict()

        issues[str(issue_num)][u'assignee'].append(slack_id)
        issues[str(issue_num)][u'assigned_at'] = datetime.datetime.now()
        users[slack_id][u'issues'].append(issue_num)

        issues_ref.set(issues)
        users_ref.set(users)

    def close_issue(self, issue_num):
        issues_ref = self.get_issues_ref()

        issues = issues_ref.get().to_dict()

        issues[str(issue_num)][u'closed_at'] = datetime.datetime.now()

        issues_ref.set(issues)
        