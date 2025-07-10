# Utility functions for timestamped log generation.
from datetime import datetime, timedelta, time
import random


def generate_realistic_timestamp_logs(day_index=1, after_hours=False):
    """Return a generator yielding sequential timestamp strings.

    Parameters
    ----------
    day_index : int
        Index of the simulated day (1-based).
    after_hours : bool
        If True, timestamps may extend past business hours.

    Returns
    -------
    callable
        Function that when called returns the next timestamp string in
        ``YYYY-MM-DD HH:MM:SS`` format.
    """
    base_date = datetime.now().date() + timedelta(days=day_index - 1)
    current = datetime.combine(base_date, time(8, 0))
    lunch_start = datetime.combine(base_date, time(12, 0))
    lunch_end = datetime.combine(base_date, time(13, 0))
    end_of_day = datetime.combine(base_date, time(18, 0))
    after_end = datetime.combine(base_date, time(22, 0))

    first = True

    def next_timestamp(force_after_hours=False):
        nonlocal current, first
        if first:
            first = False
            return current.strftime("%Y-%m-%d %H:%M:%S")

        increment = timedelta(minutes=random.randint(15, 45))
        current += increment
        if current >= lunch_start and current < lunch_end:
            current = lunch_end + (current - lunch_start)

        if force_after_hours and current < end_of_day:
            current = end_of_day + timedelta(minutes=random.randint(15, 60))
        if not after_hours and current > end_of_day:
            current = end_of_day
        if after_hours and current > after_end:
            current = after_end
        return current.strftime("%Y-%m-%d %H:%M:%S")

    # expose current datetime for inspection
    def _current():
        return current
    next_timestamp.current = _current
    return next_timestamp
