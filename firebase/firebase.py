import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import datetime

class FireBase:

    def __init__(self, path):
        cred = credentials.Certificate(path)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def add_channel(self, slack_team_id, github_repository):
        # summaryが未定義のとき、collectionが存在しない
        summary = self.db.collection(slack_team_id).document(u'summary').get().to_dict()
        if summary == None:
            print('init_collection')
            collection = self.db.collection(slack_team_id)
            collection.document(u'summary').set({
                u'slack_team_id': slack_team_id,
                u'github_repository': github_repository,
            })
            collection.document(u'users').set({

            })
            collection.document(u'issues').set({

            })

    def get_issues_ref(self, slack_team_id):
        return self.db.collection(slack_team_id).document(u'issues')

    def get_users_ref(self, slack_team_id):
        return self.db.collection(slack_team_id).document(u'users')

    def get_issue(self, slack_team_id, issue_num):
        return self.get_issues_ref(slack_team_id).get().to_dict()[str(issue_num)]

    def get_user(self, slack_team_id, slack_user_id):
        return self.get_users_ref(slack_team_id).get().to_dict()[slack_user_id]

    def add_issue(self, slack_team_id, issue_num, title, description, limited_sec, assignee=[]):
        issues_ref = self.get_issues_ref(slack_team_id)
        issues = issues_ref.get().to_dict()

        if issues == None:
            issues = {}

        new_issue = {
            u'issue_num': issue_num,
            u'title': title,
            u'description': description,
            u'assignee': [],
            u'limited_sec': limited_sec,
            u'assigned_at': None,
            u'closed_at': None,
        }

        issues[str(issue_num)] = new_issue
        issues_ref.set(issues)

        if len(assignee) == 0:
            pass
        else:
            assigned_at = datetime.datetime.now()
            self.assign_user(slack_team_id=slack_team_id, assignee=assignee, issue_num=issue_num )
    
    def add_user(self, slack_team_id, slack_user_id, github_user_id):
        users_ref = self.get_users_ref(slack_team_id)
        users = users_ref.get().to_dict()
        
        if users == None:
            users = {}

        new_user = {
            u'slack_user_id': slack_user_id,
            u'github_user_id': github_user_id,
            u'issues': [],
        }
        users[slack_user_id] = new_user
        users_ref.set(users)
    
    def assign_user(self, slack_team_id, assignee, issue_num):
        issues_ref = self.get_issues_ref(slack_team_id)
        users_ref = self.get_users_ref(slack_team_id)

        issues = issues_ref.get().to_dict()
        users = users_ref.get().to_dict()

        for user in assignee:
            if not user in issues[str(issue_num)][u'assignee']:
                issues[str(issue_num)][u'assignee'].append(user)
            if issues[str(issue_num)][u'assigned_at'] == None:
                issues[str(issue_num)][u'assigned_at'] = datetime.datetime.now()
            if not issue_num in users[user][u'issues']:
                users[user][u'issues'].append(issue_num)

        issues_ref.set(issues)
        users_ref.set(users)

    def close_issue(self, slack_team_id, issue_num):
        issues_ref = self.get_issues_ref(slack_team_id)

        issues = issues_ref.get().to_dict()

        issues[str(issue_num)][u'closed_at'] = datetime.datetime.now()

        issues_ref.set(issues)
        
def main():
    firebase = FireBase(path=u'firebaseCredentials.json')
    
    print(firebase.add_channel(slack_team_id=u'slack_team_id', github_repository=u'github_repository'))
    
    print(firebase.get_issues_ref(slack_team_id=u'slack_team_id'))
    print(firebase.get_users_ref(slack_team_id=u'slack_team_id'))
    
    print(firebase.add_user(slack_team_id=u'slack_team_id', slack_user_id=u'slack_user_id', github_user_id=u'github_user_id'))
    print(firebase.add_issue(slack_team_id=u'slack_team_id', issue_num=1, title=u'title', description=u'description', limited_sec=10000))
    print(firebase.add_issue(slack_team_id=u'slack_team_id', issue_num=2, title=u'title', description=u'description', limited_sec=10000, assignee=[u'slack_user_id']))

    print(firebase.get_issue(slack_team_id=u'slack_team_id', issue_num=1))
    print(firebase.get_user(slack_team_id=u'slack_team_id', slack_user_id='slack_user_id'))

    print(firebase.assign_user(slack_team_id=u'slack_team_id', assignee=[u'slack_user_id'], issue_num=1))
    print(firebase.assign_user(slack_team_id=u'slack_team_id', assignee=[u'slack_user_id'], issue_num=2))
    print(firebase.close_issue(slack_team_id=u'slack_team_id', issue_num=1))
    print(firebase.close_issue(slack_team_id=u'slack_team_id', issue_num=2))

if __name__ == '__main__':
    main()