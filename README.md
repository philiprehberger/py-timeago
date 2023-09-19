# philiprehberger-timeago

[![Tests](https://github.com/philiprehberger/py-timeago/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-timeago/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-timeago.svg)](https://pypi.org/project/philiprehberger-timeago/)
[![License](https://img.shields.io/github/license/philiprehberger/py-timeago)](LICENSE)
[![Sponsor](https://img.shields.io/badge/sponsor-GitHub%20Sponsors-ec6cb9)](https://github.com/sponsors/philiprehberger)

Convert timestamps to relative time phrases like "3 hours ago".

## Installation

```bash
pip install philiprehberger-timeago
```

## Usage

```python
from philiprehberger_timeago import timeago, timedelta_human
from datetime import datetime, timedelta, timezone

now = datetime.now(timezone.utc)

timeago(now - timedelta(seconds=30))  # "30 seconds ago"
timeago(now - timedelta(hours=3))     # "3 hours ago"
timeago(now - timedelta(days=1))      # "yesterday"
timeago(now + timedelta(days=7))      # "in 1 week"

# Unix timestamps
timeago(1709913600)

# Duration formatting
timedelta_human(timedelta(hours=3, minutes=25))  # "3 hours, 25 minutes"
```

## API

- `timeago(dt, now=None)` — Relative time phrase from datetime, date, or Unix timestamp
- `timedelta_human(td)` — Format a timedelta as readable duration


## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## License

MIT
