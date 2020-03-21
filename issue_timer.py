import time
import threading
import datetime

class IssueTimer:
    def __init__(self,timer_list):
        self.timer_list = timer_list

    def add_time(self,timer):
        self.timer_list.push(timer)

    def check_time(self):
        while True:
            current_time = datetime.datetime.now()
            for i,time in enumerate(self.timer_list):
                if time["expired_at"] <= current_time:
                    test = self.timer_list.pop(i)
                    print(test)

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

    t = IssueTimer(test_list)
    thread_1 = threading.Thread(target=t.check_time())
    thread_2 = threading.Thread(target=t.check_time())
    thread_1.start()
