import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class FireBase:

    def __init__(self, path, team_name):

        cred = credentials.Certificate(path)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

        self.team_name = team_name

    def get_all_issues(self):
        return self.db.collection(self.team_name).document(u'issues').get().to_dict()

    def get_all_users(self):
        return self.db.collection(self.team_name).document(u'users').get().to_dict()

    def get_issue(self, num):
        return self.get_all_issues()[num]

    def get_user(self, slack_id):
        return self.get_all_users()[slack_id]

path = 'testAccount.json'
team_name = 'Team01'

firebase = FireBase(path, team_name)

print(firebase.get_all_issues())
print(firebase.get_all_users())
print(firebase.get_issue(str(1)))
print(firebase.get_user('U010AV12F8D'))