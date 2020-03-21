import time
import threading
import datetime

class IssueTimer:
    def __init__(self,timer_list):
        self.timer_list = timer_list

    def add_time(self,timer):
        self.timer_list.push(timer)

    def check_time(self):
        t = threading.Timer(1, self.check_time)
        t.start()
        
        current_time = datetime.datetime.now()
        print(current_time)
        
        out_time_list= [time for time in self.timer_list if time["expired_at"] <= current_time]
        self.timer_list = [timer for timer in self.timer_list if not timer in out_time_list]

        print(len(self.timer_list))
        #print("timer_list : {}".format(self.timer_list))

if __name__ == "__main__":
    start_time = datetime.datetime.now()
    expaired_at = start_time + datetime.timedelta(seconds=2)
    expaired_at2 = start_time + datetime.timedelta(seconds=4)
    expaired_at3 = start_time + datetime.timedelta(seconds=6)
    expaired_at4 = start_time + datetime.timedelta(seconds=8)


    test_list = [
      {
        "team": "A",
        "issue": 0,
        "expired_at": expaired_at
      },
      {
        "team": "A",
        "issue": 1,
        "expired_at": expaired_at2
      },
      {
        "team": "A",
        "issue": 2,
        "expired_at": expaired_at3
      },
      {
        "team": "B",
        "issue": 0,
        "expired_at": expaired_at4
      },
    ]

    issue_timer = IssueTimer(test_list)
    t = threading.Thread(target=issue_timer.check_time())
    t.start()
