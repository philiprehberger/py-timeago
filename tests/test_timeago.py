from datetime import datetime, timedelta, timezone
from philiprehberger_timeago import timeago, timedelta_human


def _now():
    return datetime.now(timezone.utc)


def test_just_now():
    result = timeago(_now())
    assert "just now" in result


def test_seconds_ago():
    dt = _now() - timedelta(seconds=30)
    result = timeago(dt)
    assert "second" in result


def test_minutes_ago():
    dt = _now() - timedelta(minutes=5)
    result = timeago(dt)
    assert "minute" in result


def test_hours_ago():
    dt = _now() - timedelta(hours=3)
    result = timeago(dt)
    assert "hour" in result


def test_yesterday():
    dt = _now() - timedelta(days=1, hours=12)
    result = timeago(dt)
    assert "yesterday" in result


def test_days_ago():
    dt = _now() - timedelta(days=5)
    result = timeago(dt)
    assert "day" in result


def test_weeks_ago():
    dt = _now() - timedelta(weeks=2)
    result = timeago(dt)
    assert "week" in result


def test_future():
    dt = _now() + timedelta(hours=5)
    result = timeago(dt)
    assert "in " in result


def test_unix_timestamp():
    ts = _now().timestamp() - 3600
    result = timeago(ts)
    assert "hour" in result


def test_timedelta_human_hours():
    result = timedelta_human(timedelta(hours=3, minutes=25))
    assert "3 hours" in result
    assert "25 minutes" in result


def test_timedelta_human_seconds():
    result = timedelta_human(timedelta(seconds=45))
    assert "45 seconds" in result


def test_timedelta_human_zero():
    result = timedelta_human(timedelta(0))
    assert "0 seconds" in result


def test_singular():
    result = timedelta_human(timedelta(hours=1))
    assert "1 hour" in result
    assert "hours" not in result
