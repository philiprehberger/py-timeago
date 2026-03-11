"""Convert timestamps to relative time phrases like '3 hours ago'."""

from __future__ import annotations

from datetime import datetime, date, timedelta, timezone


__all__ = [
    "timeago",
    "timedelta_human",
]

_THRESHOLDS: list[tuple[float, str, str, float]] = [
    # (max_seconds, singular, plural, divisor)
    (10, "just now", "just now", 1),
    (60, "{n} second ago", "{n} seconds ago", 1),
    (3600, "{n} minute ago", "{n} minutes ago", 60),
    (86400, "{n} hour ago", "{n} hours ago", 3600),
    (172800, "yesterday", "yesterday", 1),
    (604800, "{n} day ago", "{n} days ago", 86400),
    (2592000, "{n} week ago", "{n} weeks ago", 604800),
    (31536000, "{n} month ago", "{n} months ago", 2592000),
    (float("inf"), "{n} year ago", "{n} years ago", 31536000),
]

_FUTURE_THRESHOLDS: list[tuple[float, str, str, float]] = [
    (10, "just now", "just now", 1),
    (60, "in {n} second", "in {n} seconds", 1),
    (3600, "in {n} minute", "in {n} minutes", 60),
    (86400, "in {n} hour", "in {n} hours", 3600),
    (172800, "tomorrow", "tomorrow", 1),
    (604800, "in {n} day", "in {n} days", 86400),
    (2592000, "in {n} week", "in {n} weeks", 604800),
    (31536000, "in {n} month", "in {n} months", 2592000),
    (float("inf"), "in {n} year", "in {n} years", 31536000),
]


def timeago(dt: datetime | date | int | float, *, now: datetime | None = None) -> str:
    """Convert a timestamp to a relative time phrase.

    Args:
        dt: A datetime, date, or Unix timestamp (int/float).
        now: Reference time. Defaults to ``datetime.now(UTC)``.

    Returns:
        Human-readable relative time string.
    """
    if now is None:
        now = datetime.now(timezone.utc)

    if isinstance(dt, (int, float)):
        dt = datetime.fromtimestamp(dt, tz=timezone.utc)
    elif isinstance(dt, date) and not isinstance(dt, datetime):
        dt = datetime(dt.year, dt.month, dt.day, tzinfo=timezone.utc)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)

    diff = (now - dt).total_seconds()
    is_future = diff < 0
    seconds = abs(diff)

    thresholds = _FUTURE_THRESHOLDS if is_future else _THRESHOLDS

    for max_sec, singular, plural, divisor in thresholds:
        if seconds < max_sec:
            if "{n}" not in singular:
                return singular
            n = int(seconds / divisor)
            template = singular if n == 1 else plural
            return template.format(n=n)

    return "a long time ago"


def timedelta_human(td: timedelta) -> str:
    """Format a timedelta as a human-readable duration string.

    Args:
        td: The timedelta to format.

    Returns:
        String like ``"3 hours, 25 minutes"`` or ``"45 seconds"``.
    """
    total = int(abs(td.total_seconds()))

    if total == 0:
        return "0 seconds"

    parts: list[str] = []

    days, remainder = divmod(total, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    return ", ".join(parts)
