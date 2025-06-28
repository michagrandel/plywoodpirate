from plywoodpirate.datetime import get_human_readable_time

def test_get_human_readable_time():
    assert get_human_readable_time(hours=1, minutes=1, seconds=1) == "01:01:01 hours"
    assert get_human_readable_time(minutes=59) == "59:00 minutes"
    assert get_human_readable_time(minutes=60) == "01:00:00 hours"
    assert get_human_readable_time(minutes=135) == "02:15:00 hours"
    assert get_human_readable_time(seconds=135*60) == "02:15:00 hours"
    assert get_human_readable_time(seconds=3600*8) == "08:00:00 hours"

