import time
import threading
import datetime

class IssueTimer:
    def __init__(self,timer_list):
        self.timer_list = timer_list
        self.output_list = []

    def set_callback(self, callback):
        self.callback = callback

    def add_time(self,timer):
        if isinstance(timer, list):
            for t in timer:
                self.timer_list.append(t)
        else:    
            self.timer_list.append(timer)

    def pop_output(self):
        if self.output_list:
            output = self.output_list.copy()
            self.output_list.clear()
        else:
            output = None

        return output
        
    def check_time(self):
        t = threading.Timer(1, self.check_time)
        t.start()
        
        current_time = datetime.datetime.now()

        out_time_list = [time for time in self.timer_list if time["expired_at"] <= current_time]
        if out_time_list:
            self.output_list += out_time_list
             
        self.timer_list = [timer for timer in self.timer_list if not timer in out_time_list]

        for timer in out_time_list:
            self.callback(timer)


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

    def timer_expired(_timer):
        print("Callback: ")
        print(_timer)

    issue_timer = IssueTimer(test_list)
    
    issue_timer.set_callback(timer_expired)

    t = threading.Thread(target=issue_timer.check_time())
    t.start()
    
    print(issue_timer.timer_list)
    issue_timer.add_time({
        "team": "A",
        "issue": 3,
        "expired_at": start_time + datetime.timedelta(seconds=7)
      })
    print(issue_timer.timer_list)

    time.sleep(5)
    print("pop_output")
    print(issue_timer.pop_output())
    print(issue_timer.pop_output())

