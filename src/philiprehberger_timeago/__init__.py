"""Convert timestamps to relative time phrases like '3 hours ago'."""

from __future__ import annotations

from datetime import datetime, date, timedelta, timezone


__all__ = [
    "format_age",
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

_NUMERIC_THRESHOLDS: list[tuple[float, str, str, float]] = [
    (60, "{n} second ago", "{n} seconds ago", 1),
    (3600, "{n} minute ago", "{n} minutes ago", 60),
    (86400, "{n} hour ago", "{n} hours ago", 3600),
    (172800, "{n} day ago", "{n} day ago", 86400),
    (604800, "{n} day ago", "{n} days ago", 86400),
    (2592000, "{n} week ago", "{n} weeks ago", 604800),
    (31536000, "{n} month ago", "{n} months ago", 2592000),
    (float("inf"), "{n} year ago", "{n} years ago", 31536000),
]

_NUMERIC_FUTURE_THRESHOLDS: list[tuple[float, str, str, float]] = [
    (60, "in {n} second", "in {n} seconds", 1),
    (3600, "in {n} minute", "in {n} minutes", 60),
    (86400, "in {n} hour", "in {n} hours", 3600),
    (172800, "in {n} day", "in {n} day", 86400),
    (604800, "in {n} day", "in {n} days", 86400),
    (2592000, "in {n} week", "in {n} weeks", 604800),
    (31536000, "in {n} month", "in {n} months", 2592000),
    (float("inf"), "in {n} year", "in {n} years", 31536000),
]


def _to_utc(dt: datetime | date | int | float) -> datetime:
    """Normalize an input timestamp to a UTC-aware datetime."""
    if isinstance(dt, (int, float)):
        return datetime.fromtimestamp(dt, tz=timezone.utc)
    if isinstance(dt, date) and not isinstance(dt, datetime):
        return datetime(dt.year, dt.month, dt.day, tzinfo=timezone.utc)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def timeago(
    dt: datetime | date | int | float,
    *,
    now: datetime | None = None,
    numeric: bool = False,
) -> str:
    """Convert a timestamp to a relative time phrase.

    Args:
        dt: A datetime, date, or Unix timestamp (int/float).
        now: Reference time. Defaults to ``datetime.now(UTC)``.
        numeric: If True, suppress "just now"/"yesterday"/"tomorrow" and always
            render a numeric phrase like "5 seconds ago" or "1 day ago".

    Returns:
        Human-readable relative time string.
    """
    if now is None:
        now = datetime.now(timezone.utc)

    dt = _to_utc(dt)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)

    diff = (now - dt).total_seconds()
    is_future = diff < 0
    seconds = abs(diff)

    if numeric:
        thresholds = _NUMERIC_FUTURE_THRESHOLDS if is_future else _NUMERIC_THRESHOLDS
    else:
        thresholds = _FUTURE_THRESHOLDS if is_future else _THRESHOLDS

    for max_sec, singular, plural, divisor in thresholds:
        if seconds < max_sec:
            if "{n}" not in singular:
                return singular
            n = int(seconds / divisor)
            template = singular if n == 1 else plural
            return template.format(n=n)

    return "a long time ago"


def format_age(dt: datetime | date | int | float, *, now: datetime | None = None) -> str:
    """Format a timestamp as a compact age string like "5s", "3m", "2h", "4d", "1mo", "2y".

    Future timestamps are prefixed with "-" (e.g. "-3h" for 3 hours in the future).
    """
    if now is None:
        now = datetime.now(timezone.utc)

    dt = _to_utc(dt)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)

    diff = (now - dt).total_seconds()
    is_future = diff < 0
    seconds = abs(diff)

    if seconds < 60:
        value = int(seconds)
        suffix = "s"
    elif seconds < 3600:
        value = int(seconds / 60)
        suffix = "m"
    elif seconds < 86400:
        value = int(seconds / 3600)
        suffix = "h"
    elif seconds < 2592000:
        value = int(seconds / 86400)
        suffix = "d"
    elif seconds < 31536000:
        value = int(seconds / 2592000)
        suffix = "mo"
    else:
        value = int(seconds / 31536000)
        suffix = "y"

    prefix = "-" if is_future else ""
    return f"{prefix}{value}{suffix}"


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
