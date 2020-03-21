from issue_timer import IssueTimer
import threading
import datetime

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
      }
    ]
    t = IssueTimer(test_list)
    thread_1 = threading.Thread(target=t.check_time())
    thread_1.start()


    print('start add test')
    test_list = [
      {
        "team": "A",
        "issue": 0,
        "expired_at": expaired_at
      }
    ]
    t.add_time(test_list)
